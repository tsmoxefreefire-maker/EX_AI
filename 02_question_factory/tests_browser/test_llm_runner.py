"""🤖 The sandbox page of a model-written scene, in a real browser: the toolkit draws, the drag works, the report comes back,
and the network is blocked. Uses the worked example as «the model's answer» (no keys needed)."""
import json, os, pathlib, sys
from playwright.sync_api import sync_playwright
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import scene_writer  # noqa: E402
from graph_reader import Graph  # noqa: E402

ART = HERE.parent.parent / "05_explanation_api" / "art" / "art.json"          # every drawing in ONE file (batch 27)
FILES = json.load(open(ART, encoding="utf-8"))["files"]
art_svg = lambda k: FILES.get(k)
g = Graph.load(str(HERE.parent / "phy_g10_book_graph.json")); lesson = next(l for l in g.lessons() if l.id == "l_speed")
data = scene_writer.scene_data(g, lesson, "accel", art_svg=art_svg)
res = []
def ok(n, c, x=""): res.append(("✅" if c else "❌") + " " + n + " " + str(x))
EVIL = "function buildScene(SDK, data) { SDK.caption('x'); }\n;(function(){var x=new XMLHttpRequest();x.onload=function(){window.__NET='LOADED'};x.onerror=function(){window.__NET='blocked'};x.open('GET','https://example.com');x.send();})();"
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 700, "height": 520}); failed = []
    pg.on("requestfailed", lambda r: failed.append((r.url, r.failure)))
    pg.set_content(scene_writer.runner_html(scene_writer.EXAMPLE, data)); pg.wait_for_timeout(1600)
    rep = pg.evaluate("window.__REPORT")
    ok("the scene draws and reports back", rep and rep["ok"] and rep["drawn"] > 3, rep)
    ok("everything is inside the picture", rep and rep["outside"] == 0, rep and rep["outside"])
    ok("the caption tells the student what to do", "اسحب" in pg.inner_text("#cap"), pg.inner_text("#cap"))
    ok("our characters (from the art library), not blobs", pg.locator(".sdk-char").count() == 2 and pg.locator(".sdk-blob").count() == 0)
    me = pg.locator('.sdk-char[data-id="accel"]').bounding_box(); it = pg.locator('.sdk-char[data-id="velocity"]').bounding_box()
    pg.mouse.move(me["x"] + me["width"] / 2, me["y"] + me["height"] / 2); pg.mouse.down()
    pg.mouse.move(it["x"] + it["width"] / 2 + 40, it["y"] + it["height"] / 2, steps=12); pg.mouse.up(); pg.wait_for_timeout(900)
    rep = pg.evaluate("window.__REPORT")
    ok("dragging works: the arrow + the bubble + done", pg.locator(".sdk-bub").count() == 1 and rep and rep["done"] == "connected", rep)
    ok("the bubble says the relation with the age's word", "بيعتمد على" in pg.text_content("#bubbles"), pg.text_content("#bubbles")[:80])
    ok("senior stage: no faces", pg.evaluate("[...document.querySelectorAll('.sface')].every(e=>getComputedStyle(e).display==='none')"))
    pg.set_content(scene_writer.runner_html(EVIL, data)); pg.wait_for_timeout(1500)
    ok("the network is blocked inside the sandbox (CSP)", pg.evaluate("window.__NET") == "blocked" and any(f[1] == "csp" for f in failed), (pg.evaluate("window.__NET"), failed))
    b.close()
print("\n".join(res))
sys.exit(0 if all(r.startswith("✅") for r in res) else 1)
