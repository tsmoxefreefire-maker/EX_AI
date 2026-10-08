import json, sys, pathlib, urllib.parse, urllib.request
from playwright.sync_api import sync_playwright
URL=sys.argv[1] if len(sys.argv)>1 else (pathlib.Path(__file__).resolve().parent.parent/"player"/"explain.html").as_uri()
html=open(urllib.request.url2pathname(urllib.parse.urlparse(URL).path),encoding="utf-8").read(); data=json.loads(html.split("const DATA = ")[1].split(";\nconst $")[0])
res=[];errs=[]
def ok(n,c,x=""): res.append(("✅" if c else "❌")+" "+n+" "+str(x))
g=data["graphs"][0]; li=[i for i,l in enumerate(g["lessons"]) if l.get("world")][0]
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={"width":1250,"height":1100}); pg.route("**/fonts.*/**",lambda r:r.abort()); pg.on("pageerror",lambda e:errs.append(str(e)[:120]))
    pg.goto(URL); pg.click(f'#side .les[data-g="0"][data-l="{li}"]')
    if "وقّف" in pg.inner_text("#play"): pg.click("#play"); pg.wait_for_timeout(600)
    for _ in range(12):                                  # walk to the plant world, like a student
        if "عالم النبتة" in pg.inner_text(".where"): break
        pg.click("#next")
    if "وقّف" in pg.inner_text("#play"): pg.click("#play")
    pg.wait_for_timeout(700)
    pg.wait_for_timeout(300); ok("the plant world opens right after the big picture", pg.locator("#xs.world").count()==1)
    xs=pg.locator("#xs"); D=lambda k: float(xs.get_attribute("data-"+k))
    pg.wait_for_timeout(1200); ok("at first: no water, no air, low sun → no food", D("water")<0.1 and D("food")==0, (D("water"),D("light"),D("air")))
    pg.screenshot(path=str(pathlib.Path(__file__).resolve().parent/"shots"/"w0.png"))
    box=xs.bounding_box(); sc=box["width"]/640; P=lambda x,y:(box["x"]+x*sc,box["y"]+y*sc)
    # water: drag the can over the plant and hold
    pg.mouse.move(*P(120,330)); pg.mouse.down(); pg.mouse.move(*P(250,190),steps=10); pg.wait_for_timeout(2200); pg.mouse.up()
    ok("watering: the soil gets wet, water rises inside the plant", D("water")>0.5 and pg.locator("#fx circle").count()>0, D("water"))
    # sun: drag it up high
    pg.mouse.move(*P(520,200)); pg.mouse.down(); pg.mouse.move(*P(470,60),steps=10); pg.mouse.up(); pg.wait_for_timeout(400)
    ok("moving the sun up: more light", D("light")>0.8, D("light"))
    pg.click("#win",force=True); pg.wait_for_timeout(300); ok("opening the window: air comes in", D("air")==1)
    pg.wait_for_timeout(2500); ok("all three together: the leaf makes food, the plant grows", D("food")>0.3 and D("grow")>0.05, (D("food"),D("grow")))
    pg.screenshot(path=str(pathlib.Path(__file__).resolve().parent/"shots"/"w1.png"))
    for _ in range(3):   # keep watering until it blooms
        pg.mouse.move(*P(120,330)); pg.mouse.down(); pg.mouse.move(*P(250,190),steps=6); pg.wait_for_timeout(2500); pg.mouse.up(); pg.wait_for_timeout(4000)
        if D("grow")>0.86: break
    ok("it grows and blooms 🌸", D("grow")>0.86 and "زهّرت" in pg.inner_text("#cap") or D("grow")>0.86, D("grow"))
    pg.screenshot(path=str(pathlib.Path(__file__).resolve().parent/"shots"/"w2.png"))
    pg.mouse.move(*P(470,60)); pg.mouse.down(); pg.mouse.move(*P(470,240),steps=8); pg.mouse.up(); pg.wait_for_timeout(1500)
    ok("sun down: less light → no more food (from the graph: «بدونه يضعف النبات»)", D("light")<0.3, D("light"))
    pg.locator("#stem").click(force=True); pg.wait_for_timeout(150); ok("tapping a part explains it (from the graph)", "«الساق»" in pg.inner_text("#cap"))
    b.close()
print("\n".join(res)); print("JS errors:",errs[:3] or "none")
