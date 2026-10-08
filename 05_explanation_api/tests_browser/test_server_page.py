"""🆕 batch 27 — the page the SERVER gives, in a real browser (Playwright + Chromium):
  1) the API draws the subject characters EXACTLY like the page (every emblem × long and short names);
  2) a NEW subject (the computer book, never seen by the code) sent to the service → its page works: its own sound (chip),
     its own characters (💻 with whole names, a colour each), its own mascot «بِتّو», every scene opens, no JS error;
  3) a subject NOTHING matches → a stable identity of its own (a friendly shape + its own instrument), and its page works too;
  4) the new instruments really sound: loud enough, never clipping, each one different.
Run:  python tests_browser/test_server_page.py          (from 05_explanation_api)"""
import json
import os
import re
import sys
import tempfile

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.environ["EXPLAIN_DATA_DIR"] = tempfile.mkdtemp(prefix="explain_page_test_")
os.environ["EXPLAIN_SEED"] = "0"
sys.path.insert(0, HERE)
from playwright.sync_api import sync_playwright  # noqa: E402

from core import art, service  # noqa: E402

FACTORY = os.path.join(os.path.dirname(HERE), "02_question_factory")
OUT = tempfile.mkdtemp(prefix="explain_pages_")
oks, fails = [], []


def ok(cond, what, extra=""):
    (oks if cond else fails).append(what)
    print(("✅ " if cond else "❌ ") + what + (f"  · {extra}" if extra else ""))


def page_file(book_ids, name):
    p = os.path.join(OUT, name)
    with open(p, "w", encoding="utf-8") as f:
        f.write(service.page_html(book_ids))
    return "file://" + p


def page_data(url):
    """The data inside a page (the page keeps it private, inside its own function)."""
    html = open(url[len("file://"):], encoding="utf-8").read()
    return json.loads(html.split("const DATA = ")[1].split(";\nconst $")[0])


with open(os.path.join(FACTORY, "examples", "new_subject_computer_g7.json"), encoding="utf-8") as f:
    CS = json.load(f)
cs = service.generate(graph=CS)
odd_graph = json.loads(json.dumps(CS).replace("cs_g7", "bugs_g4"))
odd_graph["book"].update({"subject": "عالم الحشرات", "title": "عالم الحشرات · الصف الرابع", "grade": 4})
odd = service.generate(graph=odd_graph)

with sync_playwright() as p:
    b = p.chromium.launch()

    # ---------- 1) the API's drawings == the page's drawings ----------
    pg = b.new_page()
    pg.goto(page_file(["cs_g7"], "cs.html")); pg.wait_for_timeout(600)
    emblems = pg.evaluate("Object.keys(window.__ART.SUBJ_ART)")
    labels = ["حاسوب", "وحدة المعالجة المركزية", "الخطأ البرمجي", "الكهرومغناطيسية", "الوحدة الثالثة: الوراثة", "", "ذاكرة"]
    js = pg.evaluate("""([es,ls])=>{const o={};es.forEach(e=>ls.forEach(l=>{o[e+'|'+l]=window.__ART.artSVG('subj:'+e+':'+l,'');}));return o;}""", [emblems, labels])
    bad = []
    for key, svg in js.items():
        e, l = key.split("|", 1)
        body_js = re.sub(r"^<svg[^>]*>|</svg>$", "", svg)
        body_py = re.sub(r"^<svg[^>]*>|</svg>$", "", art.art_svg(f"subj:{e}:{l}") or "")
        if body_js != body_py:
            bad.append(key)
    ok(not bad and len(js) == len(emblems) * len(labels), f"الـ API بيرسم نفس شخصيات الصفحة بالزبط ({len(emblems)} شكل × {len(labels)} اسم)", ", ".join(bad[:4]))
    pg.close()

    # ---------- 2) the NEW subject's page ----------
    for name, ids, want_instr in (("الحاسوب (مادة جديدة)", ["cs_g7"], "chip"), ("عالم الحشرات (ما في كلمة بتعرفها)", ["bugs_g4"], odd["identity"]["sound"]["instr"])):
        pg = b.new_page(viewport={"width": 1280, "height": 900}); errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)[:200]))
        url = page_file(ids, ids[0] + ".html")
        pg.goto(url); pg.wait_for_timeout(900)
        prof = pg.evaluate("window.__SOUND.now()")
        ok(prof["instr"] == want_instr, f"{name}: صوتها الخاص", json.dumps(prof))
        data = page_data(url)["graphs"][0]
        idn = data.get("identity") or {}
        icons = [i for l in data["lessons"] for i in (l.get("icons") or {}).values()]
        ok(icons and all(i.startswith(("lego:", "subj:" + idn["emblem"] + ":")) for i in icons),
           f"{name}: كل شخصياتها إلها: 🧱 رسمة مركّبة (ليغو، الدفعة ٢٩) أو بشكل مادتها ({idn.get('emblem')})", icons[:4])
        if ids[0] == "cs_g7":
            whole = pg.evaluate("window.__ART.artSVG('subj:💻:وحدة المعالجة المركزية','')")
            ok(">وحدة المعالجة<" in whole and ">المركزية<" in whole, f"{name}: مفهوم بلا رسمة ولا قطعة ← الاسم كامل على سطرين (ما في «وحدة المعا»)")
        fills = set(pg.evaluate("[...document.querySelectorAll('#stagebox svg.ch, .stage svg.ch, svg.ch')].map(s=>(s.querySelector('[fill]')||{}).getAttribute&&s.querySelector('[fill]').getAttribute('fill')).filter(Boolean)"))
        ok(len(fills) >= 3, f"{name}: لون مختلف لكل مفهوم", f"{len(fills)} لون")
        # the mascot: switch the page to the little ones' look → «أهلاً! أنا «<mascot>»»
        pg.evaluate("""()=>{const s=document.querySelector('#stageSel,select[id*=stage],select[aria-label*="المرحلة"]');if(s){s.value='kids';s.dispatchEvent(new Event('change',{bubbles:true}));}}""")
        pg.wait_for_timeout(500)
        ok(idn.get("mascot_name") and idn["mascot_name"] in pg.inner_text("body"), f"{name}: شخصيتها «{idn.get('mascot_name')}» بتسلّم على الصغار")
        # poke one of its characters → a note of ITS instrument
        n0 = pg.evaluate("window.__SOUND.log.length")
        el = pg.query_selector('.alive[data-k="subj"], .char[data-k="subj"]')
        if el:
            el.dispatch_event("pointerdown")
        pg.wait_for_timeout(150)
        ok(el is not None and pg.evaluate("window.__SOUND.log.length") > n0, f"{name}: بتكبس على الشخصية ← بتطلع نغمة من آلتها")
        # every step of every lesson opens with no error
        steps = 0
        for li in range(len(data["lessons"])):
            pg.click(f'#side .les[data-g="0"][data-l="{li}"]'); pg.wait_for_timeout(120)
            for _ in range(60):
                nx = pg.query_selector("#next")
                if not nx or nx.is_disabled() or "خلص" in (nx.inner_text() or ""):
                    break
                nx.click(); steps += 1; pg.wait_for_timeout(40)
        ok(steps > 20 and not errs, f"{name}: كل الخطوات بتفتح بلا أخطاء", f"{steps} خطوة · {errs[:2]}")
        pg.close()

    # ---------- 4) the new instruments really sound ----------
    pg = b.new_page()
    pg.goto(page_file(["cs_g7"], "cs2.html")); pg.wait_for_timeout(500)
    res = {}
    for instr in ("chip", "harp", "vibes", "steel"):
        res[instr] = pg.evaluate("async i=>await window.__SOUND.render('good','kids',{instr:i,root:62,scale:'major'})", instr)
    for instr, r in res.items():
        ok(0.02 < r["peak"] < 0.98 and r["secs"] > 0.15, f"الآلة الجديدة «{instr}»: مسموعة وما بتشوّش", f"peak {r['peak']:.2f} · {r['secs']:.2f}s")
    sig = {(round(r["bright"] / 150), round(r["secs"], 1)) for r in res.values()}
    ok(len(sig) == 4, "كل آلة جديدة صوتها مختلف عن الثانية", json.dumps({k: [round(v["bright"]), round(v["secs"], 2)] for k, v in res.items()}))
    pg.close()
    b.close()

print(f"\n{len(oks)} ✅ · {len(fails)} ❌")
if fails:
    print("❌", fails)
    sys.exit(1)
