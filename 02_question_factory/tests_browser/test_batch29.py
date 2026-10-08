"""🆕 batch 29 (Hareth) in a real browser:
(1) choosing an age stage TAKES you to that stage's books, and the books list is grouped by stage;
(2) every stage makes a sound when the mouse is on a character (the secondary used to be silent), each in its own way.
python tests_browser/test_batch29.py"""
import json, pathlib, urllib.parse, urllib.request
from playwright.sync_api import sync_playwright
HERE = pathlib.Path(__file__).resolve().parent
URL = (HERE.parent / "player" / "explain.html").as_uri()
html = open(urllib.request.url2pathname(urllib.parse.urlparse(URL).path), encoding="utf-8").read()
data = json.loads(html.split("const DATA = ")[1].split(";\nconst $")[0])
res, errs = [], []
def ok(n, c, x=""): res.append(("✅" if c else "❌") + " " + n + ("" if c else " " + str(x)[:300]))
STAGES = ["kids", "junior", "teen", "senior"]
first = {st: next((i for i, g in enumerate(data["graphs"]) if g["audience"]["stage"] == st), None) for st in STAGES}
with sync_playwright() as p:
    b = p.chromium.launch(args=["--autoplay-policy=no-user-gesture-required"])
    for vp in ({"width": 1250, "height": 950}, {"width": 390, "height": 844}):
        tag = "📱" if vp["width"] < 500 else "🖥️"
        pg = b.new_page(viewport=vp); pg.route("**/fonts.*/**", lambda r: r.abort()); pg.on("pageerror", lambda e: errs.append(str(e)[:150]))
        pg.goto(URL); pg.wait_for_timeout(500)
        heads = pg.evaluate("[...document.querySelectorAll('#side .stghead')].map(h=>h.id)")
        ok(f"{tag} the books list has one heading per stage, in order", heads == [f"stg-{st}" for st in STAGES], heads)
        for st in ["senior", "kids", "teen", "junior", "senior"]:
            pg.select_option("#stageSel", st); pg.wait_for_timeout(450)
            cur = pg.evaluate("(()=>{const b=document.querySelector('#side .les[aria-current=\"true\"]');return b?+b.dataset.g:-1})()")
            body = pg.evaluate("document.body.dataset.stage")
            sel = pg.evaluate("document.getElementById('stageSel').value")
            ok(f"{tag} choose «{st}» → its first book ({data['graphs'][first[st]]['title']}), its own look", cur == first[st] and body == st and sel == "", (cur, body, sel))
            if vp["width"] < 500:
                vis = pg.evaluate(f"(()=>{{const s=document.getElementById('side'),h=document.getElementById('stg-{st}');const a=s.getBoundingClientRect(),r=h.getBoundingClientRect();return r.top>=a.top-2&&r.top<a.bottom}})()")
                ok(f"{tag} the list scrolled to the «{st}» heading", vis)
        # choosing the stage of the book we are already in: we stay in the same lesson
        pg.click(f'#side .les[data-g="{first["teen"]}"][data-l="1"]', force=True) if len(data["graphs"][first["teen"]]["lessons"]) > 1 else None
        pg.wait_for_timeout(300)
        before = pg.evaluate("document.querySelector('#side .les[aria-current=\"true\"]').dataset.l")
        pg.select_option("#stageSel", "teen"); pg.wait_for_timeout(400)
        after = pg.evaluate("document.querySelector('#side .les[aria-current=\"true\"]').dataset.l")
        ok(f"{tag} the stage of the book you are in → you stay in your lesson", before == after, (before, after))
        pg.close()
    # ---------- (2) hover sounds in every stage ----------
    pg = b.new_page(viewport={"width": 1250, "height": 950}); pg.route("**/fonts.*/**", lambda r: r.abort()); pg.on("pageerror", lambda e: errs.append(str(e)[:150]))
    pg.goto(URL); pg.wait_for_timeout(500)
    for st in STAGES:
        pg.select_option("#stageSel", st); pg.wait_for_timeout(400)
        pg.click('#prog .pstop[data-c="0"]', force=True); pg.wait_for_timeout(400)
        pg.evaluate("document.getElementById('play') && document.getElementById('play').textContent.includes('وقّف') && document.getElementById('play').click()")
        pg.wait_for_timeout(600)
        pg.wait_for_function("!window.__SOUND.demoing()", timeout=6000)   # 🆕 batch 30: arriving at a stage plays its tune → wait for it to end, then measure the hover alone
        n0 = pg.evaluate("window.__SOUND.log.length")
        node = pg.locator("#xs .xnode").first
        box = node.bounding_box()
        pg.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2); pg.wait_for_timeout(500)
        n1 = pg.evaluate("window.__SOUND.log.length")
        ok(f"{st}: the mouse on a character → a sound", n1 > n0, (n0, n1))
        pg.mouse.move(5, 5); pg.wait_for_timeout(600)
    pg.close()
    # ---------- (3) the puzzle: every shadow shows its NAME (similar pictures, e.g. Arabic) · a wrong shadow says whose place it is ----------
    ga = next(i for i, x in enumerate(data["graphs"]) if "العربية" in x["title"])
    li = next(i for i, l in enumerate(data["graphs"][ga]["lessons"]) if l.get("assemble"))
    for vp in ({"width": 1250, "height": 950}, {"width": 390, "height": 844}):
        tag = "📱" if vp["width"] < 500 else "🖥️"
        pg = b.new_page(viewport=vp); pg.route("**/fonts.*/**", lambda r: r.abort()); pg.on("pageerror", lambda e: errs.append(str(e)[:150]))
        pg.goto(URL); pg.wait_for_timeout(500)
        pg.click(f'#side .les[data-g="{ga}"][data-l="{li}"]', force=True); pg.wait_for_timeout(300)
        pg.click('#prog .pstop[data-c="-1"]', force=True); pg.wait_for_timeout(300)
        pg.evaluate("document.getElementById('play').textContent.includes('وقّف')&&document.getElementById('play').click()")
        for _ in range(8):
            if pg.evaluate("(document.getElementById('xs')||{}).getAttribute&&document.getElementById('xs').getAttribute('aria-label')") == "ركّب المشهد":
                break
            pg.click("#next", force=True); pg.wait_for_timeout(150)
        ids = pg.evaluate("[...document.querySelectorAll('#xs .xnode.piece')].map(n=>n.dataset.id)")
        tags = pg.evaluate("[...document.querySelectorAll('#xs .astag')].map(t=>[t.dataset.for,t.textContent.trim()])")
        ok(f"{tag} puzzle: every shadow shows its name ({len(ids)})", sorted(t[0] for t in tags) == sorted(ids) and all(t[1] for t in tags), tags)
        a, c = ids[0], ids[1]
        pc = pg.locator(f'#xs .xnode.piece[data-id="{a}"]').bounding_box(); sh = pg.locator(f'#xs .shadow[data-id="{c}"]').bounding_box()
        pg.mouse.move(pc["x"] + pc["width"] / 2, pc["y"] + 20); pg.mouse.down(); pg.mouse.move(sh["x"] + sh["width"] / 2, sh["y"] + sh["height"] / 2, steps=6); pg.mouse.up(); pg.wait_for_timeout(300)
        ok(f"{tag} puzzle: on the WRONG shadow → it goes back and says whose place it is", "هاد مكان" in pg.inner_text("#cap") and pg.locator("#xs .xnode.placed").count() == 0, pg.inner_text("#cap"))
        for cid in ids:
            pc = pg.locator(f'#xs .xnode.piece[data-id="{cid}"]').bounding_box(); sh = pg.locator(f'#xs .shadow[data-id="{cid}"]').bounding_box()
            pg.mouse.move(pc["x"] + pc["width"] / 2, pc["y"] + 20); pg.mouse.down(); pg.mouse.move(sh["x"] + sh["width"] / 2, sh["y"] + sh["height"] / 2, steps=6); pg.mouse.up(); pg.wait_for_timeout(250)
        ok(f"{tag} puzzle: every piece grabbed and placed (even the wide ones)", pg.locator("#xs .xnode.placed").count() == len(ids), pg.locator("#xs .xnode.placed").count())
        ok(f"{tag} puzzle: a placed piece hides the shadow's name (no name twice)", pg.locator("#xs .astag.gone").count() == len(ids))
        sel = pg.evaluate("String(window.getSelection())")
        ok(f"{tag} puzzle: dragging never selects (highlights) the names", sel.strip() == "", sel)
        pg.wait_for_timeout(1600)
        short = pg.evaluate(r"""[...document.querySelectorAll('#xs .xarrow')].map(p=>{const m=p.getAttribute('d').match(/M([-\d.]+) ([-\d.]+) Q[-\d.]+ [-\d.]+ ([-\d.]+) ([-\d.]+)/);
            const L=m?Math.hypot(m[3]-m[1],m[4]-m[2]):999;const pill=p.nextElementSibling&&p.nextElementSibling.classList.contains('needs');return [Math.round(L),pill];})""")
        ok(f"{tag} arrows: a word sits ON an arrow only when there is room for it", all((not pill) or L >= 85 for L, pill in short), short)
        mk = pg.evaluate("document.querySelector('#xs marker#xhead').getAttribute('markerUnits')")
        ok(f"{tag} arrow heads: one fixed size (not «bent» blobs on the thick, lit arrows)", mk == "userSpaceOnUse", mk)
        pg.close()
    b.close()
print("\n".join(r for r in res if r.startswith("❌")) or "")
print(f"✅ {sum(r.startswith('✅') for r in res)} checks passed · ❌ {sum(r.startswith('❌') for r in res)} failed")
print("JS errors:", errs or "none")
