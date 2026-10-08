"""One screenshot per scene kind (after interacting with it), for a human look."""
import json
from playwright.sync_api import sync_playwright
import pathlib, sys
HERE=pathlib.Path(__file__).resolve().parent
PAGE=HERE.parent/"player"/"explain.html"
URL=PAGE.as_uri()
data=json.loads(open(PAGE,encoding="utf-8").read().split("const DATA = ")[1].split(";\nconst $")[0])
want=["flip","interview","dialogue"]
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={"width":1250,"height":1150}); pg.route("**/fonts.*/**",lambda r:r.abort())
    pg.goto(URL); pg.wait_for_timeout(300); g=data["graphs"][0]; done=set()
    for li,l in enumerate(g["lessons"]):
        for ci,c in enumerate(l["concepts"]):
            for si,s in enumerate(c["scenes"]):
                k=s["kind"]
                if k not in want or k in done: continue
                pg.click(f'#side .les[data-g="0"][data-l="{li}"]'); pg.click(f'#prog .pstop[data-c="{ci}"]',force=True)
                for prev in c["scenes"][:si]:
                    for _ in range(len(prev["steps"])): pg.click("#next")
                pg.wait_for_timeout(200)
                if "وقّف" in pg.inner_text("#play"): pg.click("#play")
                pg.wait_for_timeout(800)
                if k=="flip":
                    for x in pg.locator("#q .card2b, #q .fcard2").all()[:4]: x.click(force=True)
                    pg.wait_for_timeout(700)
                if k=="before_after": pg.locator("#ba").fill("60"); pg.wait_for_timeout(200)
                if k=="interview":
                    for x in pg.locator("#q .qbtn").all()[:2]: x.click(force=True)
                if k=="dialogue":
                    for _ in range(3): pg.click("#more")
                pg.locator("#q").screenshot(path=str(HERE/"shots"/f"k_{k}.png")); done.add(k)
    b.close()
print("shot:",sorted(done))
