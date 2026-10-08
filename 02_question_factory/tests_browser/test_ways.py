"""The 4 explanation activities (no right/wrong): 🧩 assemble · 🗣️ dialogue · 🎚️ slider · 🔍 lens."""
import json, sys, pathlib, urllib.parse, urllib.request
from playwright.sync_api import sync_playwright
HERE = pathlib.Path(__file__).resolve().parent
URL = sys.argv[1] if len(sys.argv) > 1 else (HERE.parent / "player" / "explain.html").as_uri()
data = json.loads(open(urllib.request.url2pathname(urllib.parse.urlparse(URL).path), encoding="utf-8").read().split("const DATA = ")[1].split(";\nconst $")[0])
res, errs = [], []
def ok(n, c, x=""): res.append(("✅" if c else "❌") + " " + n + " " + str(x))
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1250, "height": 1100}); pg.route("**/fonts.*/**", lambda r: r.abort()); pg.on("pageerror", lambda e: errs.append(str(e)[:150]))
    pg.goto(URL); pg.wait_for_timeout(300)
    def go(kind, gi=0):
        g = data["graphs"][gi]
        for li, l in enumerate(g["lessons"]):
            for ci, c in enumerate(l["concepts"]):
                for si, s in enumerate(c["scenes"]):
                    if s["kind"] == kind:
                        pg.click(f'#side .les[data-g="{gi}"][data-l="{li}"]'); pg.click(f'#prog .pstop[data-c="{ci}"]', force=True)
                        for prev in c["scenes"][:si]:
                            for _ in range(len(prev["steps"])): pg.click("#next")
                        pg.wait_for_timeout(250)
                        if "وقّف" in pg.inner_text("#play"): pg.click("#play"); pg.wait_for_timeout(700)
                        return s
    # 🧩 assemble: a lesson-level scene right after the big picture
    g = data["graphs"][0]; li = 0
    pg.click(f'#side .les[data-g="0"][data-l="{li}"]'); pg.wait_for_timeout(200)
    if "وقّف" in pg.inner_text("#play"): pg.click("#play"); pg.wait_for_timeout(600)
    for _ in range(14):
        if "ركّب" in pg.inner_text(".where"): break
        pg.click("#next")
    pg.wait_for_timeout(700)
    s = g["lessons"][li]["assemble"]; ok("🧩 the build scene is in the lesson path", "ركّب" in pg.inner_text(".where"))
    for cid in s["concepts"]:
        a = pg.locator(f'#xs .xnode.piece[data-id="{cid}"]').bounding_box(); t = pg.locator(f'#xs .shadow[data-id="{cid}"]').bounding_box()
        pg.mouse.move(a["x"] + a["width"] / 2, a["y"] + a["height"] / 2); pg.mouse.down(); pg.mouse.move(t["x"] + t["width"] / 2, t["y"] + t["height"] / 2, steps=10); pg.mouse.up(); pg.wait_for_timeout(250)
    ok("🧩 every character goes to its shadow and wakes up; the arrows appear", pg.locator("#xs .xnode.placed").count() == len(s["concepts"]) and pg.locator("#asArrows .xedge").count() == len(s["edges"]), (pg.locator("#xs .xnode.placed").count(), len(s["concepts"])))
    pg.screenshot(path=str(HERE / "shots" / "w_assemble.png"))
    s = go("dialogue"); n = len(s["lines"])
    for _ in range(n): pg.click("#more"); pg.wait_for_timeout(150)
    ok("🗣️ the dialogue goes line by line (both characters talk)", pg.locator("#talk .msg").count() == n and pg.locator("#talk .msg.me").count() > 0 and pg.locator("#talk .msg.them").count() > 0)
    pg.screenshot(path=str(HERE / "shots" / "w_dialogue.png"))
    s = go("slider", 1)
    pg.locator("#a").fill("5"); pg.locator("#b").fill("2"); pg.wait_for_timeout(200); eq = pg.text_content("#xs #eq")
    ok(f"🎚️ the slider changes the picture at once ({s['mode']})", any(x in eq for x in ["5 + 2 = 7", "5 − 2 = 3", "5 × 2 = 10", "5 ÷ 2 = 2", "2 / 5"]), eq)
    pg.screenshot(path=str(HERE / "shots" / "w_slider.png"))
    s = go("lens"); box = pg.locator("#xs").bounding_box(); k = box["width"] / 640
    import math
    n = len(s["facts"])
    for i in range(n):
        a = -math.pi / 2 + i * 2 * math.pi / n; x, y = 320 + math.cos(a) * 200, 170 + math.sin(a) * 120
        pg.mouse.move(box["x"] + x * k, box["y"] + y * k, steps=6); pg.wait_for_timeout(150)
    pg.wait_for_timeout(900)
    ok("🔍 the lens clears the fog; every fact is found", pg.locator("#xs .fact.found").count() == n and pg.locator("#xs .fog.gone2").count() == 1, (pg.locator("#xs .fact.found").count(), n))
    pg.screenshot(path=str(HERE / "shots" / "w_lens.png"))
    b.close()
print("\n".join(res)); print("JS errors:", errs[:3] or "none")
