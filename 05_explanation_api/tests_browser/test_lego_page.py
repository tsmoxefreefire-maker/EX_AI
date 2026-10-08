"""🧱 Lego drawings in a real browser (batch 29):
(1) the page and the API draw the SAME SVG for every part (JS legoSVG == Python art.lego_svg),
(2) a NEW subject (the computer book) shows its built characters: drawn, moving, a note when poked, every step without errors,
(3) the 12 books did not change.        python tests_browser/test_lego_page.py"""
import json
import os
import sys
import tempfile

from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FACTORY = os.path.join(os.path.dirname(HERE), "02_question_factory")
sys.path.insert(0, HERE); sys.path.insert(0, FACTORY); sys.path.insert(0, os.path.join(FACTORY, "player"))
from core import art  # noqa: E402
import build_explain_player as player  # noqa: E402
import explain_main  # noqa: E402
import lego  # noqa: E402

res, errs = [], []
def ok(n, c, x=""): res.append(("✅" if c else "❌") + " " + n + ("" if c else " " + str(x)[:300]))

tmp = tempfile.mkdtemp()
lego.set_store(os.path.join(tmp, "lego_library.json"))               # nothing saved: the drawings come from the words only
cs = os.path.join(FACTORY, "examples", "new_subject_computer_g7.json")
explain_main.run(cs, os.path.join(tmp, "cs"), None)
page = os.path.join(tmp, "cs.html")
open(page, "w", encoding="utf-8").write(player.page_html([player.pack(cs, os.path.join(tmp, "cs"))]))

with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1250, "height": 950}); pg.route("**/fonts.*/**", lambda r: r.abort())
    pg.on("pageerror", lambda e: errs.append(str(e)[:150]))
    pg.goto("file://" + page); pg.wait_for_timeout(600)
    # ---------- (1) the same SVG in the page and in the API ----------
    mains = sorted(lego.MAINS); extras = sorted(lego.EXTRAS)
    keys = [f"lego:{m}:{x}:{c}:{mo}" for c, m in enumerate(mains) for x, mo in (("", "bob"), (extras[c % 12], "sun"), (extras[c % 12] + "+" + extras[(c + 5) % 12], "wobble"))]
    js = pg.evaluate("ks=>ks.map(k=>window.__ART.legoSVG(k))", keys)
    bad = [k for k, j in zip(keys, js) if j != art.lego_svg(k)]
    ok(f"page == API for {len(keys)} built drawings (27 parts × badges × colours)", not bad, bad[:3])
    ok("a wrong key draws nothing (no broken picture)", pg.evaluate("window.__ART.legoSVG('lego:pizza::1:bob')") is None and art.lego_svg("lego:pizza::1:bob") is None)
    # ---------- (2) the computer book ----------
    data = json.loads(open(page, encoding="utf-8").read().split("const DATA = ")[1].split(";\nconst $")[0])
    icons = {k: v for l in data["graphs"][0]["lessons"] for k, v in l["icons"].items()}
    ok("every computer concept got a built drawing (by its words, no AI)", icons and all(v.startswith("lego:") for v in icons.values()), icons)
    pg.click('#prog .pstop[data-c="-1"]', force=True); pg.wait_for_timeout(500)
    nodes = pg.evaluate("[...document.querySelectorAll('#xs .xnode')].map(n=>({id:n.dataset.id,svg:!!n.querySelector('svg.ch'),k:(n.querySelector('[data-k]')||{dataset:{}}).dataset.k||'',a:(n.querySelector('.alive')||{className:''}).className.baseVal||((n.querySelector('.alive')||{}).className||'')}))")
    ok("big picture: every character is drawn", nodes and all(n["svg"] for n in nodes), nodes)
    moves = pg.evaluate("[...document.querySelectorAll('#prog .pstop .alive')].map(e=>e.getAttribute('class')+' '+e.dataset.k)")
    ok("the stops at the top: they move the way their recipe says, and a poke plays the subject's note",
       any("a-buzz" in m for m in moves) and any("a-wobble" in m for m in moves) and all(m.endswith(" subj") for m in moves[1:]), moves)
    css = pg.evaluate("[...document.styleSheets].flatMap(s=>{try{return [...s.cssRules].map(r=>r.cssText)}catch(e){return []}}).join(' ')")
    ok("every Lego motion has its animation in the page", all(f".a-{m}" in css for m in lego.MOTIONS), [m for m in lego.MOTIONS if f".a-{m}" not in css])
    ink = pg.evaluate("(()=>{const s=document.querySelector('#xs .xnode svg.ch');if(!s)return 0;const r=s.getBoundingClientRect();return r.width*r.height})()")
    ok("a character has a real size on the screen", ink > 1500, ink)
    # walk EVERY step of every scene of both lessons
    steps = 0
    for li in range(len(data["graphs"][0]["lessons"])):
        pg.click(f'#side .les[data-g="0"][data-l="{li}"]', force=True); pg.wait_for_timeout(250)
        pg.evaluate("document.getElementById('play') && document.getElementById('play').textContent.includes('وقّف') && document.getElementById('play').click()")
        for _ in range(140):
            nxt = pg.inner_text("#next")
            if "خلصت الدرس" in nxt:
                break
            pg.click("#next", force=True); pg.wait_for_timeout(35); steps += 1
            pg.evaluate("document.getElementById('play') && document.getElementById('play').textContent.includes('وقّف') && document.getElementById('play').click()")
    ok(f"every step of the computer book ({steps}) without a JS error", steps > 40 and not errs, errs[:3])
    blank = pg.evaluate("[...document.querySelectorAll('svg.ch')].filter(s=>!s.innerHTML.trim()).length")
    ok("no empty character anywhere", blank == 0, blank)
    b.close()

# ---------- (3) the 12 books ----------
# the published page is built by build_all_books.py: its data must have no Lego key
pub = open(os.path.join(FACTORY, "player", "explain.html"), encoding="utf-8").read()
d12 = json.loads(pub.split("const DATA = ")[1].split(";\nconst $")[0])
lego_in_12 = [v for g in d12["graphs"] for l in g["lessons"] for v in l.get("icons", {}).values() if v.startswith("lego:")]
ok("the 12 books did not change: none of their concepts needed a built drawing", not lego_in_12, lego_in_12[:5])

print("\n".join(r for r in res if r.startswith("❌")) or "")
print(f"✅ {sum(r.startswith('✅') for r in res)} checks passed · ❌ {sum(r.startswith('❌') for r in res)} failed")
print("JS errors:", errs or "none")
