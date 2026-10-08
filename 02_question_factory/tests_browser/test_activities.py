"""🆕 The 5 new activities (batch 26), played by a «student» robot in a real browser — every stage, computer AND phone (touch).
For each kind and each age stage it opens one real scene and checks:
  · video mode never plays the activity for the student (nothing moves by itself);
  · the student CAN do it: right moves are accepted and explained, wrong moves are explained (reversed arrow, wrong place, wrong answer);
  · it ends (the finish sentence comes), and the reset / help work;
  · the layout: nothing outside the picture, names not on top of each other, no text spilling, no sideways page scroll,
    text ≥ 12px, touch targets ≥ 40px, never one word per line;
  · the words: the age's way of talking (no «بيحتاج» for teen/senior, no dangling «على،», no pictures in the senior's sentences);
  · no JS errors.
    python tests_browser/test_activities.py            (computer + phone)"""
import json
import pathlib
import re
import sys

from playwright.sync_api import sync_playwright

PAGE = pathlib.Path(__file__).resolve().parent.parent / "player" / "explain.html"
data = json.loads(PAGE.read_text(encoding="utf-8").split("const DATA = ")[1].split(";\nconst $")[0])
KINDS = ["recipe", "connect", "compare", "teach", "ladder"]
STAGES = ["kids", "junior", "teen", "senior"]
fails, oks, errs = [], [], []


def ok(cond, what):
    (oks if cond else fails).append(what)
    if not cond:
        print("❌", what)


def find(kind, stage):
    """(book, lesson, concept index, steps to press inside the concept, scene) of the first scene of this kind for this stage."""
    best = None
    for gi, g in enumerate(data["graphs"]):
        for li, l in enumerate(g["lessons"]):
            for ci, c in enumerate(l["concepts"]):
                for si, s in enumerate(c["scenes"]):
                    if s["kind"] == kind:
                        hit = (gi, li, ci, sum(len(x["steps"]) for x in c["scenes"][:si]), s)
                        if g["audience"]["stage"] == stage:
                            return hit
                        best = best or hit
    return best


def open_scene(pg, hit, video):
    gi, li, ci, presses, s = hit
    pg.click(f'#side .les[data-g="{gi}"][data-l="{li}"]'); pg.wait_for_timeout(100)
    pg.click(f'#prog .pstop[data-c="{ci}"]'); pg.wait_for_timeout(100)
    for _ in range(presses):
        pg.click("#next")
    if not video and "وقّف" in pg.inner_text("#play"):
        pg.click("#play")
    if video and "شغّل" in pg.inner_text("#play"):
        pg.click("#play")                                          # 🎬 from the first step
    pg.wait_for_timeout(700)
    return s


def center(pg, sel):
    return pg.evaluate("s=>{const r=document.querySelector(s).getBoundingClientRect();return [r.left+r.width/2,r.top+r.height/2];}", sel)


def tap(pg, sel, touch):
    pg.evaluate("s=>document.querySelector(s).scrollIntoView({block:'center'})", sel); pg.wait_for_timeout(60)   # (the characters bob forever: no «stable» wait)
    x, y = center(pg, sel)
    if touch:
        pg.touchscreen.tap(x, y)
    else:
        pg.mouse.click(x, y)
    pg.wait_for_timeout(160)


def node(id_):
    return f'#xs .xnode[data-id="{id_}"]'


LAYOUT = r"""(stage)=>{const out=[];const xs=document.getElementById('xs'),q=document.getElementById('q');if(!xs)return ['no picture'];
  const R=xs.getBoundingClientRect();const seen=e=>{for(let x=e;x&&x!==xs;x=x.parentNode){if(x.nodeType===1&&parseFloat(getComputedStyle(x).opacity)<0.2)return false;}return true;};
  xs.querySelectorAll('.xnode').forEach(n=>{if(!seen(n))return;const r=n.getBoundingClientRect();if(r.width&&(r.left<R.left-2||r.right>R.right+2||r.top<R.top-2||r.bottom>R.bottom+2))out.push('outside:'+n.dataset.id);});
  const t=[...xs.querySelectorAll('.xname')].filter(seen).map(e=>e.getBoundingClientRect()).filter(r=>r.width);
  for(let i=0;i<t.length;i++)for(let j=i+1;j<t.length;j++){const a=t[i],b=t[j];if(Math.min(a.right,b.right)-Math.max(a.left,b.left)>3&&Math.min(a.bottom,b.bottom)-Math.max(a.top,b.top)>3)out.push('names-overlap');}
  document.querySelectorAll('#q .na-tog,#q .na-card,#q .na-zone,#q .na-opt,#q .na-msg,#q .na-note,#q .na-placed,#q .na-count,#q #cap').forEach(e=>{if(e.offsetParent===null)return;
    if(e.scrollWidth>e.clientWidth+2)out.push('spills:'+e.className);const fs=parseFloat(getComputedStyle(e).fontSize);if(fs<12)out.push('tiny-text:'+e.className+':'+fs);
    const r=e.getBoundingClientRect(),Q=q.getBoundingClientRect();if(r.left<Q.left-2||r.right>Q.right+2)out.push('outside-box:'+e.className);
    const words=e.textContent.trim().split(/\s+/).length;if(words>=4&&!e.matches('#cap')){const rg=document.createRange();rg.selectNodeContents(e);const cs=[...rg.getClientRects()].filter(x=>x.width>6).map(x=>x.top+x.height/2).sort((a,b)=>a-b);let n=0,last=-99;cs.forEach(y=>{if(y-last>8){n++;last=y;}});if(n>=words)out.push('one-word-per-line:'+e.className);}});
  document.querySelectorAll('#q .na-tog,#q .na-card,#q .na-zone,#q .na-opt,#q #naAsk,#q #naHelp').forEach(e=>{if(e.offsetParent===null)return;const h=e.getBoundingClientRect().height;if(h<40)out.push('small-target:'+e.className+':'+Math.round(h));});
  if(document.documentElement.scrollWidth>innerWidth+1)out.push('page-scrolls-sideways');
  const txt=[...document.querySelectorAll('#q #cap,#q .na-msg,#q .na-note,#q .na-placed,#q .na-card,#q .na-opt,#q .na-zh')].map(e=>e.textContent).join(' \n ');
  if(/على\s*[،.؟!:]|على\s+للي|على\s*$/m.test(txt))out.push('dangling-على');
  if((stage==='teen'||stage==='senior')&&/(^|\s)(بيحتاج|بتحتاج|بيحتاجه|بيحتاجوا)(\s|$)/.test(txt))out.push('childish-بيحتاج');
  if(stage==='senior'){const c=(document.getElementById('cap')||{}).textContent||'';if(/[\u{1F300}-\u{1FAFF}\u{2600}-\u{26FF}]/u.test(c.replace(/[✅✔⚠]/g,'')))out.push('picture-in-senior-caption');}
  return out;}"""


def layout(pg, where, stage):
    p = pg.evaluate(LAYOUT, stage)
    ok(not p, f"{where}: layout/words {p[:4] if p else ''}")


def cap(pg):
    return pg.inner_text("#cap")


def play_recipe(pg, s, where, touch):
    n = len(s["needs"])
    for i in range(n):
        tap(pg, f'.na-tog[data-i="{i}"]', touch)
        ok(pg.get_attribute(f'.na-tog[data-i="{i}"]', "aria-pressed") == "true", f"{where}: switch {i} turns on")
    pg.wait_for_timeout(400)
    ok("na-ready" in (pg.get_attribute("#xs .na-tgt", "class") or ""), f"{where}: all on → complete")
    ok(f"{n}" in pg.inner_text("#naCount"), f"{where}: the counter says {n}")
    tap(pg, '.na-tog[data-i="0"]', touch)
    c = cap(pg)
    ok("na-ready" not in (pg.get_attribute("#xs .na-tgt", "class") or "") and "طفّيت" in c, f"{where}: one off → not complete, and it says what is missing")
    ok(re.sub(r"[«»]", "", data_name(s["needs"][0]["id"])) in re.sub(r"[«»]", "", c), f"{where}: the missing one is named")


NAMES = {}


def data_name(i):
    if not NAMES:
        for g in data["graphs"]:
            NAMES.update(g["names"])
    return NAMES.get(i, i)


def drag(pg, a, b):
    pg.evaluate("s=>document.querySelector(s).scrollIntoView({block:'center'})", node(a)); pg.wait_for_timeout(60)
    x1, y1 = center(pg, node(a) + " .xbody"); x2, y2 = center(pg, node(b) + " .xbody")
    pg.mouse.move(x1, y1); pg.mouse.down(); pg.mouse.move((x1 + x2) / 2, (y1 + y2) / 2, steps=4); pg.mouse.move(x2, y2, steps=4); pg.mouse.up(); pg.wait_for_timeout(200)


def tap2(pg, a, b, touch):
    tap(pg, node(a) + " .xbody", touch); tap(pg, node(b) + " .xbody", touch)


def play_connect(pg, s, where, touch):
    req = [l for l in s["links"] if l["required"]]
    l0 = req[0]
    tap2(pg, l0["to"], l0["from"], touch)                          # reversed on purpose
    ok("بالعكس" in cap(pg), f"{where}: a reversed arrow is explained")
    ok(pg.locator("#xs .na-arr:not(.na-ghost)").count() == 0, f"{where}: a reversed arrow is not drawn")
    if s.get("calm"):
        tap2(pg, s["target"], s["calm"][0], touch)
        ok("ما في سهم مباشر" in cap(pg), f"{where}: no link → it says so")
    tap(pg, "#naHelp", touch)
    ok(pg.locator("#xs .na-ghost").count() == 1, f"{where}: «help» shows the next arrow")
    for k, l in enumerate(req):
        if k == 0 and not touch:
            drag(pg, l["from"], l["to"])                          # dragging (computer)
        else:
            tap2(pg, l["from"], l["to"], touch)                   # tapping in order (phone / touch)
        ok(pg.locator("#xs .na-arr:not(.na-ghost)").count() >= k + 1, f"{where}: arrow {k + 1} is drawn")
    pg.wait_for_timeout(1300)
    ok("رسمت كل الأسهم" in cap(pg), f"{where}: the end sentence")


def play_compare(pg, s, where, touch):
    facts = s["facts"]
    for n_, f in enumerate(facts):
        i = facts.index(f)
        wrong = next(x for x in ("a", "both", "b") if x != f["side"])
        tap(pg, f'.na-card[data-i="{i}"]', touch)
        if n_ == 0:
            tap(pg, f'.na-zone[data-side="{wrong}"]', touch)
            ok("مش هون" in cap(pg), f"{where}: a wrong place is said kindly")
            tap(pg, f'.na-zone[data-side="{f["side"]}"]', touch)
        elif n_ == 1:
            tap(pg, f'.na-zone[data-side="{wrong}"]', touch); tap(pg, f'.na-zone[data-side="{wrong}"]', touch)
            ok(pg.locator(f'.na-card[data-i="{i}"]').count() == 0, f"{where}: two wrong tries → it goes to its place, with the reason")
        else:
            tap(pg, f'.na-zone[data-side="{f["side"]}"]', touch)
        ok(pg.locator(f'.na-zone[data-side="{f["side"]}"] .na-placed').count() >= 1, f"{where}: card {n_ + 1} is in its place")
    pg.wait_for_timeout(1200)
    ok(pg.locator(".na-card").count() == 0 and "رتّبت كل البطاقات" in cap(pg), f"{where}: all placed → the end sentence")


def play_teach(pg, s, where, touch):
    for r in s["rounds"]:
        k_ok = next(k for k, o in enumerate(r["options"]) if o["ok"])
        k_no = next(k for k, o in enumerate(r["options"]) if not o["ok"])
        tap(pg, f'.na-opt[data-k="{k_no}"]', touch)
        ok("لأ" in cap(pg) and pg.locator(f'.na-opt[data-k="{k_no}"]').is_disabled(), f"{where}: a wrong answer is explained")
        tap(pg, f'.na-opt[data-k="{k_ok}"]', touch)
        pg.wait_for_timeout(1500)
    ok(pg.locator("#naNote").is_visible() and "هيك شرحتها" in pg.inner_text("#naNote"), f"{where}: the explanation he built is shown")


def play_ladder(pg, s, where, touch):
    n = len(s["rungs"])
    for k in range(n):
        tap(pg, "#naAsk", touch); pg.wait_for_timeout(350)
    ok(pg.locator("#xs .xnode:not(.na-hid)").count() == n + 1 and pg.locator("#xs .na-arr").count() == n, f"{where}: every «ليش؟» opens one rung")
    pg.wait_for_timeout(2200)
    ok(pg.locator("#naReset").is_visible() and any(w in cap(pg) for w in ("وصلنا", "آخر وحدة")), f"{where}: it reaches the end")
    layout(pg, where + " (opened)", "x")
    tap(pg, "#naReset", touch)
    ok(pg.locator("#xs .xnode.na-hid").count() == n, f"{where}: «من الأول» closes the ladder again")


PLAY = {"recipe": play_recipe, "connect": play_connect, "compare": play_compare, "teach": play_teach, "ladder": play_ladder}
QUIET = {"recipe": "() => document.querySelectorAll('.na-tog[aria-pressed=true]').length",
         "connect": "() => document.querySelectorAll('#xs .na-arr').length",
         "compare": "() => document.querySelectorAll('.na-placed').length",
         "teach": "() => document.querySelectorAll('.na-msg.na-me').length",
         "ladder": "() => document.querySelectorAll('#xs .xnode:not(.na-hid)').length - 1"}

with sync_playwright() as p:
    b = p.chromium.launch()
    for phone in (False, True):
        ctx = b.new_context(viewport={"width": 390, "height": 860} if phone else {"width": 1250, "height": 950}, has_touch=phone, is_mobile=phone)
        pg = ctx.new_page(); pg.route("**/fonts.*/**", lambda r: r.abort()); pg.on("pageerror", lambda e: errs.append(str(e)[:200]))
        pg.goto(PAGE.as_uri()); pg.wait_for_timeout(400)
        for kind in KINDS:
            for st in STAGES:
                hit = find(kind, st)
                if not hit:
                    ok(False, f"{kind}/{st}: no scene"); continue
                g = data["graphs"][hit[0]]
                where = f"{'📱' if phone else '🖥️'} {kind} · {st} · {g['title'][:12]}"
                pg.select_option("#stageSel", st if g["audience"]["stage"] != st else "")    # the right stage (switcher if this book is another age)
                pg.wait_for_timeout(200)
                s = open_scene(pg, hit, video=True)
                pg.wait_for_timeout(3300)                                                    # 🎬 video plays… the activity must stay untouched
                ok(pg.evaluate(QUIET[kind]) == 0, f"{where}: video mode does not play it for the student")
                s = open_scene(pg, hit, video=False)
                layout(pg, where + " (start)", st)
                PLAY[kind](pg, s, where, phone)
                layout(pg, where + " (end)", st)
                if "--shots" in sys.argv:                                                     # pictures of the end state (to look at by eye)
                    (PAGE.parent.parent / "tests_browser" / "shots").mkdir(exist_ok=True)
                    pg.locator("#q").screenshot(path=str(PAGE.parent.parent / "tests_browser" / "shots" / f"na_{kind}_{st}_{'ph' if phone else 'dt'}.png"))
        pg.select_option("#stageSel", "")
        ctx.close()
    b.close()

print(f"✅ {len(oks)} checks passed · ❌ {len(fails)} failed")
print("JS errors:", errs or "none")
sys.exit(1 if fails or errs else 0)
