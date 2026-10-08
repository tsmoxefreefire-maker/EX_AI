"""🤖 The model writes a NEW scene with our template's toolkit (option «ج» — hybrid).

What the model writes:   function buildScene(SDK, data) { … }    (≈ 30–120 lines, only the SDK, see sdk/scene_sdk.js)
What it can NOT do:      the network, the page around it, cookies/storage, eval… (checked here, and blocked again by the sandbox)
The flow:
  1. scene_data(...)   → what the model knows: the concept, its meaning, what it needs / who needs it (+ why), the age stage
  2. build_prompt(...) → system + user messages (toolkit reference, rules for the age, one worked example)
  3. llm(system, user) → the gateway (Gemini → GPT → Claude); any function(system, user) -> text works (tests use a fake one)
  4. check_code(...)   → safety + size + structure + a real JavaScript syntax check (node --check, if Node is installed)
  5. one repair round  → if the checks fail, the model gets the list of problems once and tries again
  6. runner_html(...)  → the sandbox page (CSP: no network) that runs the scene and reports back {ok, drawn, outside, errors}
Nothing reaches a student before a teacher approves it (status «pending_review»), and the factory's own scenes always stay.
Plain Python (standard library)."""
import json
import os
import re
import shutil
import subprocess
import tempfile

import audience as A
import offline_generator as og

HERE = os.path.dirname(os.path.abspath(__file__))
SDK_PATH = os.path.join(HERE, "sdk", "scene_sdk.js")
PROMPT_VERSION = "scene-v1"
MAX_CODE = 9000

# ---------- 1. what the model knows ----------
def scene_data(g, lesson, cid: str, art_svg=None) -> dict:
    """The facts for ONE concept (only from the graph) + the age stage + our drawings of it and its neighbours."""
    name = lambda x: g.concepts[x].text
    ins = [p for p in sorted(g.prereq_in.get(cid, [])) if og.is_entity(g, p)][:2]
    outs = [x for x in sorted(g.prereq_out.get(cid, [])) if og.is_entity(g, x)][:2]
    st = A.stage(g)
    ids = [cid] + ins + outs
    subject = str(g.book.get("subject", ""))
    icons = {x: og.icon_for(name(x), g.concepts[x].description, subject) for x in ids}
    why = {}
    for p in ins:
        w = p and name(p).replace("ال", "", 1).split()[0]
        why[p] = next((f.strip(" .") for f in (og.fragments(g.concepts[cid].description) or []) if w and w in f), "")
    return {"concept": {"id": cid, "name": name(cid), "meaning": g.concepts[cid].description or "",
                        "ins": [{"id": p, "name": name(p), "why": why.get(p, "")} for p in ins],
                        "outs": [{"id": x, "name": name(x)} for x in outs]},
            "concepts": {x: {"name": name(x), "meaning": g.concepts[x].description or ""} for x in ids},
            "lesson": {"id": lesson.id, "title": lesson.title}, "subject": subject, "stage": st,
            "grade": A.grade_of(g.book), "needsWord": "بيحتاج" if st in ("kids", "junior") else "بيعتمد على",
            "icons": icons, "art": {x: (art_svg(icons[x]) if art_svg else None) for x in ids}}


# ---------- 2. the prompt ----------
SDK_REFERENCE = """SDK (the ONLY things you may use). Stage: 640×340 units, (0,0) top-left. Right-to-left Arabic page.
- SDK.character(id, {x, y, size=90, label=true}) → h   draws OUR picture of a concept (ids from data.concepts)
    h.moveTo(x, y, ms) → Promise · h.say(text) (speech bubble, auto-wrapped, stays inside) · h.dim(bool) · h.glow(bool)
    h.onTap(fn) · h.draggable({onMove(h), onDrop(h)}) · h.near(otherHandle, dist=80) → bool · h.x, h.y, h.size
- SDK.arrow(fromH, toH, {label, hidden}) → a   the «needs» arrow FROM the one who needs TO what it needs; a.show(bool), a.redraw()
- SDK.text(x, y, str, {size=16, weight=700, color, ltr=false, anchor="middle"})   (formulas: ltr:true, e.g. "v = a × t")
- SDK.shape("circle"|"rect"|"line"|"path"|"ellipse"|"polygon"|"polyline", attrs)   (simple SVG shapes; colours: "var(--brand)", "var(--good)", "var(--warn)", "var(--ink)", "var(--muted)")
- SDK.slider({label, min, max, step, value}, onChange(value)) → {set(v), value}   ·   SDK.button(label, onClick)
- SDK.caption(text)   the narrator line under the picture (one sentence at a time)
- SDK.tween(ms, fn(t from 0 to 1)) → Promise   ·   SDK.wait(ms) → Promise   ·   SDK.done(note)   call when the student finished the activity"""

STAGE_RULES = {
    "kids": "Grade 1–4. A playful friend: simple Jordanian Arabic, characters may talk in the first person, at most one emoji per sentence.",
    "junior": "Grade 5–7. A curious explorer: friendly Jordanian Arabic, few emoji, short sentences.",
    "teen": "Grade 8–9. A confident classmate: clear Jordanian Arabic, NO face emoji, say «بيعتمد على» (not «بيحتاج»), no baby talk.",
    "senior": "Grade 10–12. A calm expert: precise and simple Arabic with the correct scientific terms, NO emoji, third person "
              "(««التسارع» بيعتمد على …»), formulas written left-to-right with SDK.text(..., {ltr:true}).",
}

EXAMPLE = r"""function buildScene(SDK, data) {
  const c = data.concept, need = c.ins[0];
  const me = SDK.character(c.id, { x: 470, y: 170, size: 110 });
  if (!need) { me.say(c.meaning); SDK.caption("«" + c.name + "»: " + c.meaning); SDK.done(); return; }
  const it = SDK.character(need.id, { x: 150, y: 170, size: 90 });
  const arrow = SDK.arrow(me, it, { hidden: true });
  SDK.caption("اسحب «" + c.name + "» لـ«" + need.name + "» وشوف شو العلاقة.");
  me.draggable({
    onMove: () => arrow.redraw(),
    onDrop: () => {
      if (!me.near(it, 140)) { me.moveTo(470, 170, 400).then(() => arrow.redraw()); return; }
      me.moveTo(330, 170, 300).then(() => {
        arrow.redraw(); arrow.show(true);
        me.say("«" + c.name + "» " + data.needsWord + " «" + need.name + "»" + (need.why ? ": " + need.why : "") + ".");
        SDK.caption(need.why ? "لأنه " + need.why + "." : "ما بيصير بدونه.");
        SDK.done("connected");
      });
    }
  });
}"""

SYSTEM = f"""You write ONE interactive explanation scene for an Arabic learning platform, as plain JavaScript.
Output ONLY one ```javascript code block containing exactly: function buildScene(SDK, data) {{ ... }}

Goal: the student UNDERSTANDS the concept by DOING something (drag, slide, tap) and SEEING what changes. No quiz, no right/wrong score.
Use ONLY the facts in `data` (data.concept.meaning, data.concept.ins[].why, names). Never invent facts, numbers or relations.

{SDK_REFERENCE}

Hard rules (the code is checked automatically and rejected otherwise):
- Use only SDK.* and plain JS (const/let, arrays, Math, arrow functions, if, for with a fixed bound). No while loops, no for(;;).
- Never use: window, document, fetch, XMLHttpRequest, import, eval, Function, setInterval, innerHTML, localStorage, parent, top, location, navigator, constructor, prototype.
- Everything stays inside 640×340. At most 4 characters. Under {MAX_CODE} characters, ideally 30–120 lines.
- Every text shown to the student is Arabic (formulas may be Latin), short, and correct.
- Call SDK.caption(...) at the start (what to do) and SDK.done() when the activity is complete.

Worked example (one possible scene; invent a DIFFERENT activity that fits the concept):
```javascript
{EXAMPLE}
```"""


def build_prompt(data: dict, idea: str = None) -> tuple:
    """(system, user): the rules + the facts for this concept + the age stage + an optional idea from the teacher."""
    facts = {k: data[k] for k in ("concept", "concepts", "lesson", "subject", "stage", "grade", "needsWord")}
    user = (f"Age stage: {STAGE_RULES.get(data['stage'], STAGE_RULES['kids'])}\n"
            f"Concept data (JSON):\n{json.dumps(facts, ensure_ascii=False, indent=1)}\n"
            + (f"Teacher's idea for the activity: {idea}\n" if idea else "Choose the activity that best shows this concept and its relations.\n")
            + "Return only the code block.")
    return SYSTEM, user


# ---------- 4. the checks ----------
FORBIDDEN = [(r"\bwindow\b", "window"), (r"\bdocument\b", "document"), (r"\bfetch\s*\(", "fetch"), (r"XMLHttpRequest|WebSocket|EventSource", "network"),
             (r"\bimport\b", "import"), (r"\beval\s*\(", "eval"), (r"\bFunction\s*\(", "Function()"), (r"\bsetInterval\b", "setInterval"),
             (r"innerHTML|outerHTML|insertAdjacentHTML", "innerHTML"), (r"localStorage|sessionStorage|indexedDB|cookie", "storage"),
             (r"\bparent\b|\btop\b\s*\.|\bopener\b|postMessage", "parent page"), (r"\blocation\b|\bnavigator\b", "location/navigator"),
             (r"constructor|prototype|__proto__|globalThis|\bself\b", "escape tricks"), (r"<\s*/?\s*script|</", "html tags"),
             (r"\bwhile\b", "while loop"), (r"for\s*\(\s*;\s*;", "endless for")]


def extract_code(text: str) -> str:
    """The code inside the first ```javascript block (or the whole text if there is no block)."""
    m = re.search(r"```(?:javascript|js)?\s*\n([\s\S]*?)```", text or "")
    return (m.group(1) if m else (text or "")).strip()


def _strip_strings(code: str) -> str:
    """The code without strings and comments (so «while» inside an Arabic sentence is not a while loop).
    Inside `template ${strings}` the ${…} parts ARE code, so they are kept."""
    code = re.sub(r"/\*[\s\S]*?\*/|//[^\n]*", " ", code)
    code = re.sub(r"`(?:\\.|[^`\\])*`", lambda m: " ".join(re.findall(r"\$\{([^}]*)\}", m.group())) or "''", code)
    return re.sub(r"'(?:\\.|[^'\\\n])*'|\"(?:\\.|[^\"\\\n])*\"", "''", code)


def check_code(code: str, node_check: bool = True) -> list:
    """Every problem found (empty list = OK): structure, size, forbidden things, brackets, and JavaScript syntax (node --check)."""
    problems = []
    if not code:
        return ["empty: no code"]
    if len(code) > MAX_CODE:
        problems.append(f"too long: {len(code)} > {MAX_CODE} characters")
    if not re.search(r"function\s+buildScene\s*\(\s*SDK\s*,\s*data\s*\)", code):
        problems.append("missing: function buildScene(SDK, data)")
    bare = _strip_strings(code)
    for pat, label in FORBIDDEN:                           # loops: only real code counts · everything else: also inside strings
        if re.search(pat, bare) or (label not in ("while loop", "endless for") and re.search(pat, code)):
            problems.append(f"forbidden: {label}")
    for o, c in ("()", "[]", "{}"):
        if bare.count(o) != bare.count(c):
            problems.append(f"unbalanced: {o}{c}")
    if node_check and shutil.which("node") and not any(p.startswith("forbidden") for p in problems):
        with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as f:
            f.write(code + "\n")
            path = f.name
        try:
            r = subprocess.run(["node", "--check", path], capture_output=True, text=True, timeout=10)
            if r.returncode != 0:
                err = [ln for ln in (r.stderr or "").splitlines() if "Error" in ln]
                problems.append("syntax: " + (err[0] if err else "invalid JavaScript")[:200])
        except Exception:                                    # no node / timeout → the browser check (runner) still runs
            pass
        finally:
            os.unlink(path)
    return problems


# ---------- 3 + 5. ask the model (with one repair round) ----------
def write_scene(data: dict, llm, idea: str = None, repair: bool = True) -> dict:
    """Ask the model for a scene and check it. Returns {code, problems, ok, attempts}. Never raises for a bad answer."""
    system, user = build_prompt(data, idea)
    attempts, code, problems = 0, "", ["not asked"]
    for round_ in range(2 if repair else 1):
        attempts += 1
        msg = user if round_ == 0 else (user + "\n\nYour previous code was REJECTED for these problems:\n- " + "\n- ".join(problems)
                                         + "\nFix them and return the whole function again.\nPrevious code:\n```javascript\n" + code[:MAX_CODE] + "\n```")
        try:
            text = llm(system, msg)
        except Exception as e:                               # no key / no credit / busy → reported, nothing breaks
            return {"code": code, "problems": [f"model: {e}"], "ok": False, "attempts": attempts}
        code = extract_code(text)
        problems = check_code(code)
        if not problems:
            break
    return {"code": code, "problems": problems, "ok": not problems, "attempts": attempts}


# ---------- 6. the sandbox page ----------
STAGE_CSS = """:root{--bg:#fff;--panel:#fff;--ink:#17222D;--muted:#5C6A77;--line:#D6DEE6;--chip:#EDF1F5;--brand:#1F6F78;--good:#2E8B57;--warn:#B9770E}
@media (prefers-color-scheme:dark){:root{--bg:#151F28;--panel:#151F28;--ink:#E4ECF2;--muted:#9AAAB8;--line:#283643;--chip:#1C2834;--brand:#4FB3BD;--good:#4CB36E;--warn:#E3B44F}}
body[data-stage=teen]{--brand:#2F6FA8}body[data-stage=senior]{--brand:#0F766E}
html,body{margin:0;background:var(--bg);color:var(--ink);font-family:"IBM Plex Sans Arabic",Tahoma,system-ui,sans-serif}
#stage{display:block;width:100%;height:auto;touch-action:none}#cap{min-height:1.8em;padding:6px 12px;font-weight:700;text-align:center}
#ui{display:flex;flex-wrap:wrap;gap:10px;justify-content:center;padding:4px 10px 10px}
.sdk-sl{display:flex;gap:8px;align-items:center;font-weight:700}.sdk-sl b{min-width:2.2em;text-align:center}
.sdk-btn{font:inherit;font-weight:700;border:0;border-radius:10px;padding:7px 14px;background:var(--brand);color:#fff;cursor:pointer}
.sdk-name{font-weight:800;font-size:14px;fill:var(--ink)}.sdk-text{fill:var(--ink)}.sdk-shape:not([fill]){fill:var(--chip)}.sdk-shape:not([stroke]){stroke:var(--ink);stroke-width:1.5}
.sdk-line{fill:none;stroke:var(--muted);stroke-width:3}.sdk-tag{fill:var(--panel);stroke:var(--line)}.sdk-tagt{font-size:11px;font-weight:800;fill:var(--muted)}
.sdk-bub rect{fill:var(--panel);stroke:var(--brand);stroke-width:2}.sdk-tail{fill:var(--panel);stroke:var(--brand);stroke-width:2}.sdk-bub text{font-size:13.5px;font-weight:800;fill:var(--ink)}
.sdk-glow .sdk-body{filter:drop-shadow(0 0 6px var(--brand))}.sdk-blob{fill:var(--brand);opacity:.5}
body[data-stage=senior] .sface{display:none}body[data-stage=teen] .sface .scheek,body[data-stage=teen] .sface .brows,body[data-stage=teen] .sface .m{display:none}
.sface .m{display:none}.sface .m-happy{display:inline}"""


def runner_html(code: str, data: dict, sdk_js: str = None) -> str:
    """The sandbox page for one scene. Put it in <iframe sandbox="allow-scripts">: the CSP blocks every network request."""
    sdk_js = sdk_js if sdk_js is not None else open(SDK_PATH, encoding="utf-8").read()
    safe = lambda s: s.replace("</", "<\\/")
    return ("<!doctype html><html lang=\"ar\" dir=\"rtl\"><head><meta charset=\"utf-8\">"
            "<meta http-equiv=\"Content-Security-Policy\" content=\"default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; img-src data:\">"
            f"<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\"><style>{STAGE_CSS}</style></head>"
            f"<body data-stage=\"{data.get('stage', 'kids')}\"><svg id=\"stage\" viewBox=\"0 0 640 340\" role=\"img\" aria-label=\"{data['concept']['name']}\">"
            "<defs><marker id=\"sdkhead\" viewBox=\"0 0 10 10\" refX=\"8\" refY=\"5\" markerWidth=\"7\" markerHeight=\"7\" orient=\"auto-start-reverse\">"
            "<path d=\"M1 1 L9 5 L1 9\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"1.8\"/></marker></defs></svg>"
            "<div id=\"cap\" aria-live=\"polite\"></div><div id=\"ui\"></div>"
            f"<script>window.DATA={safe(json.dumps(data, ensure_ascii=False))};</script>"
            f"<script>{safe(sdk_js)}</script><script>{safe(code)}\n;window.buildScene=typeof buildScene==='function'?buildScene:undefined;</script>"
            "<script>window.__bootScene();</script></body></html>")
