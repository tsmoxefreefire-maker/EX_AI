"""Every film (real process) in every book: the cinema plays each part, then the student drives it. No errors."""
import json, sys, pathlib, urllib.parse, urllib.request
from playwright.sync_api import sync_playwright
HERE = pathlib.Path(__file__).resolve().parent
URL = sys.argv[1] if len(sys.argv) > 1 else (HERE.parent / "player" / "explain.html").as_uri()
data = json.loads(open(urllib.request.url2pathname(urllib.parse.urlparse(URL).path), encoding="utf-8").read().split("const DATA = ")[1].split(";\nconst $")[0])
res, errs = [], []
def ok(n, c, x=""): res.append(("✅" if c else "❌") + " " + n + " " + str(x))
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1250, "height": 1000}); pg.route("**/fonts.*/**", lambda r: r.abort())
    pg.on("pageerror", lambda e: errs.append(str(e)[:150]))
    pg.goto(URL); pg.wait_for_timeout(300)
    films = 0
    for gi, g in enumerate(data["graphs"]):
        for li, l in enumerate(g["lessons"]):
            for ci, c in enumerate(l["concepts"]):
                for si, s in enumerate(c["scenes"]):
                    if s["kind"] != "play": continue
                    pg.click(f'#side .les[data-g="{gi}"][data-l="{li}"]'); pg.click(f'#prog .pstop[data-c="{ci}"]', force=True)
                    for prev in c["scenes"][:si]:
                        for _ in range(len(prev["steps"])): pg.click("#next")
                    if "وقّف" in pg.inner_text("#play"): pg.click("#play")
                    for _ in range(len(s["steps"]) - 1): pg.click("#next"); pg.wait_for_timeout(1700)
                    pg.wait_for_timeout(2200); films += 1
                    v = s["verb"]
                    if v == "visit":
                        bx = pg.evaluate("document.querySelector('#xs .actor').getAttribute('transform')")
                        ok(f"🐝 {exn if (exn:=g['names'][s['target']]) else ''}: the bee FLIES to the flower (the flower does not move)", "340" in bx and "300 220" in pg.evaluate("document.querySelector('#xs .tgt').getAttribute('transform')"), bx)
                        ok("🍎 the fruit grows from the flower", pg.evaluate("document.querySelector('#xs #res')?.getAttribute('opacity')") in ("1", None))
                    elif v == "carry": ok("🌬️ the wind carries the seed far", "520" in pg.evaluate("document.querySelector('#xs .item').getAttribute('transform')"))
                    elif v == "combine": ok("➕ 3 + 4 = 7: the groups come together", "= 7" in (pg.text_content("#xs #eq") or ""))
                    elif v == "take_away": ok("➖ 7 − 3 = 4: three blocks go away", "= 4" in (pg.text_content("#xs #eq") or ""))
                    elif v == "groups": ok("✖️ 3 rows × 4 = 12", pg.locator("#xs .rowb").count() == 12)
                    elif v == "share": ok("➗ 12 shared into 3 groups", "= 4" in (pg.text_content("#xs #eq") or ""))
                    elif v == "cut": ok("🍕 the pizza is cut into equal parts", pg.locator("#xs .slices path").count() >= 4)
                    elif v == "equivalent": ok("🟰 1/2 = 2/4", "2/4" in (pg.text_content("#xs #eq") or ""))
                    elif v == "compare": ok("⚖️ 1/2 > 1/4", ">" in (pg.text_content("#xs #eq") or ""))
                    elif v == "build": ok("🔺 the stones become a pyramid", pg.evaluate("[...document.querySelectorAll('#xs .stone')].every(s=>+s.getAttribute('x')<380)"))
                    elif v == "exchange": ok("💰 goods go to the buyer, money to the seller", "430" in pg.evaluate("document.querySelector('#xs #goods').getAttribute('transform')"))
                    ok(f"   then «🖐️ دورك» ({v})", pg.locator("#drive").is_visible())
    # the student drives the bee by hand
    g = data["graphs"][0]
    for li, l in enumerate(g["lessons"]):
        for ci, c in enumerate(l["concepts"]):
            for si, s in enumerate(c["scenes"]):
                if s["kind"] == "play" and s["verb"] == "visit":
                    pg.click(f'#side .les[data-g="0"][data-l="{li}"]'); pg.click(f'#prog .pstop[data-c="{ci}"]', force=True)
                    for prev in c["scenes"][:si]:
                        for _ in range(len(prev["steps"])): pg.click("#next")
                    if "وقّف" in pg.inner_text("#play"): pg.click("#play")
                    pg.wait_for_timeout(500)
                    a = pg.locator("#xs .actor").bounding_box(); t = pg.locator("#xs .tgt").bounding_box()     # grab the bee where it IS
                    pg.mouse.move(a["x"] + a["width"] / 2, a["y"] + a["height"] / 2); pg.mouse.down()
                    pg.mouse.move(t["x"] + t["width"] / 2, t["y"] + t["height"] / 2, steps=12); pg.mouse.up(); pg.wait_for_timeout(1500)
                    ok("🖐️ the student flies the bee to the flower by hand → pollen + fruit", pg.locator("#xs #pollen circle").count() > 0 and "برافو" in pg.inner_text("#cap"))
    ok("films found in the books", films >= 8, films)
    b.close()
print("\n".join(res)); print("JS errors:", errs[:3] or "none")
