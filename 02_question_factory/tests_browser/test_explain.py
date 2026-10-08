"""Browser test of the explanation page: one clear path, every scene, every interaction, phone (vertical)."""
import json, sys, pathlib, urllib.parse, urllib.request
from playwright.sync_api import sync_playwright
HERE = pathlib.Path(__file__).resolve().parent
URL = sys.argv[1] if len(sys.argv) > 1 else (HERE.parent / "player" / "explain.html").as_uri()
html = open(urllib.request.url2pathname(urllib.parse.urlparse(URL).path), encoding="utf-8").read()
data = json.loads(html.split("const DATA = ")[1].split(";\nconst $")[0])
SHOT = lambda n: str(HERE / "shots" / n)
res, errs = [], []
def ok(n, c, x=""): res.append(("✅" if c else "❌") + " " + n + " " + str(x))
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1250, "height": 1000}); pg.route("**/fonts.*/**", lambda r: r.abort())
    pg.on("pageerror", lambda e: errs.append(str(e)[:120]))
    pg.goto(URL); pg.wait_for_timeout(400)
    ok("clear page: no scene tabs, one progress bar, one place for words", pg.locator("#stabs").count() == 0 and pg.locator("#prog .pbar").count() == 1 and pg.locator("#cap").count() == 1)
    # ---- 🎬 video mode: plays by itself, spotlight + camera on what we talk about ----
    pg.click('#side .les[data-g="0"][data-l="0"]'); pg.click('#prog .pstop[data-c="0"]', force=True); pg.wait_for_timeout(900)
    ok("video: the scene plays by itself (⏸ shown)", "وقّف" in pg.inner_text("#play"))
    pg.wait_for_timeout(1200)
    ok("video: everything dims except what we talk about (spotlight)", pg.locator("#xs #spot .spotdim").count() == 1)
    vb_mid = pg.evaluate("document.getElementById('xs').getAttribute('viewBox')")
    pg.click("#play"); pg.wait_for_timeout(900)
    full = pg.evaluate("document.getElementById('xs').getAttribute('viewBox')")
    ok("video: the camera had moved closer, and comes back after ⏸", vb_mid != full and float(vb_mid.split()[2]) < float(full.split()[2]), (vb_mid, full))
    ok("⏸ stops the video: the light comes back", pg.locator("#xs #spot").count() == 0 and "شغّل" in pg.inner_text("#play"))
    # ---- the camera goes to the NEW character of the step, not the middle between two ----
    best = None
    for li, l in enumerate(data["graphs"][0]["lessons"]):
        for ci, c in enumerate(l["concepts"]):
            m = c["scenes"][0]; idx = [i for i, f in enumerate(m.get("focus", [])) if f.startswith("out:")]
            if idx and (best is None or idx[0] < best[2]): best = (li, ci, idx[0], m["focus"][idx[0]][4:], m["target"])
    if best:
        li, ci, k, out_id, tgt = best
        pg.click(f'#side .les[data-g="0"][data-l="{li}"]'); pg.click(f'#prog .pstop[data-c="{ci}"]', force=True)
        out_name = data["graphs"][0]["names"][out_id]
        for _ in range(80):                                   # wait for the sentence about the NEW character, then for the camera
            if out_name in pg.inner_text("#cap") and "بيحتاج" in pg.inner_text("#cap"): break
            pg.wait_for_timeout(400)
        pg.wait_for_timeout(1400)
        CEN = "(id)=>{const t=document.querySelector('#xs .xnode[data-id=\"'+id+'\"]').getAttribute('transform').match(/translate\\(([-\\d.]+) ([-\\d.]+)/);return [+t[1],+t[2]];}"
        vb = [float(x) for x in pg.evaluate("document.getElementById('xs').getAttribute('viewBox')").split()]
        cx, cy = vb[0] + vb[2] / 2, vb[1] + vb[3] / 2
        o = pg.evaluate(CEN, out_id); t0 = pg.evaluate(CEN, tgt)
        d_out = ((cx - o[0]) ** 2 + (cy - o[1]) ** 2) ** .5; d_mid = ((cx - (o[0] + t0[0]) / 2) ** 2 + (cy - (o[1] + t0[1]) / 2) ** 2) ** .5
        ok("video: the camera goes to the NEW character (not the line between them)", d_out < d_mid and d_out < 90, (round(d_out), round(d_mid)))
        if "وقّف" in pg.inner_text("#play"): pg.click("#play"); pg.wait_for_timeout(500)
    # ---- the narrator (on a fresh scene, video paused like a student) ----
    pg.click('#side .les[data-g="0"][data-l="0"]'); pg.click('#prog .pstop[data-c="0"]', force=True); pg.wait_for_timeout(600)
    if "وقّف" in pg.inner_text("#play"): pg.click("#play"); pg.wait_for_timeout(800)
    pg.click("#next"); pg.wait_for_timeout(700)
    kw = pg.locator("#cap .kw").first
    if kw.count():
        kw.click(force=True); pg.wait_for_timeout(250)
        ok("tapping a name in the sentence lights the character + a short tip", pg.locator("#xs .xnode.dim").count() > 0 or pg.locator(".tip").count() == 1, (pg.locator("#xs .xnode.dim").count(), pg.locator(".tip").count()))
        pg.wait_for_timeout(1400)
    n0 = pg.locator("#xs .xnode").first
    n0.hover(force=True); pg.wait_for_timeout(250)
    ok("coming close: the character giggles (eyes ^ ^)", pg.locator('#xs .xnode .xbody[data-mood="joy"]').count() >= 1)
    pg.mouse.move(5, 5); pg.wait_for_timeout(200)
    ok("going away: it looks normal again", pg.locator('#xs .xnode .xbody[data-mood="joy"]').count() == 0)
    for _ in range(20):
        if "المشهد الجاي" in pg.inner_text("#next") or "خلصت" in pg.inner_text("#next"): break
        pg.click("#next")
    pg.wait_for_timeout(300)
    ok("end of the scene: «💡 ليش؟» opens by itself + «جرّب بنفسك»", pg.locator("#why").is_visible() and pg.locator("#tryit").is_visible())
    pg.screenshot(path=SHOT("ex_over.png"))
    # walk EVERY lesson of every book from start to end with the single «يلا» button
    walked = 0
    for gi, g in enumerate(data["graphs"]):
        for li, l in enumerate(g["lessons"]):
            pg.click(f'#side .les[data-g="{gi}"][data-l="{li}"]')
            total = sum(len(s["steps"]) for s in [l["overview"]] + ([l["world"]] if l.get("world") else []) + ([l["assemble"]] if l.get("assemble") else []) + [s for c in l["concepts"] for s in c["scenes"]])
            for _ in range(total - 1): pg.click("#next")
            walked += 1 + (1 if l.get("world") else 0) + (1 if l.get("assemble") else 0) + sum(len(c["scenes"]) for c in l["concepts"])
            ok(f"walked to the end: {l['lesson_title']}", "خلصت الدرس" in pg.inner_text("#next"))
    ok("every scene reached with one button", walked > 0, walked)
    g = data["graphs"][0]
    def go(kind, minlen=0, mover=None):
        for li, l in enumerate(g["lessons"]):
            for ci, c in enumerate(l["concepts"]):
                for si, s in enumerate(c["scenes"]):
                    if s["kind"] == kind and (kind != "journey" or (len(s["route"]) >= minlen and (mover is None or (s["traveller"] != "spark") == mover))):
                        pg.click(f'#side .les[data-g="0"][data-l="{li}"]'); pg.click(f'#prog .pstop[data-c="{ci}"]', force=True)
                        for prev in c["scenes"][:si]:
                            for _ in range(len(prev["steps"])): pg.click("#next")
                        pg.wait_for_timeout(200)
                        if "وقّف" in pg.inner_text("#play"): pg.click("#play"); pg.wait_for_timeout(700)
                        return s
    pg.click('#side .les[data-g="0"][data-l="0"]'); pg.wait_for_timeout(200)
    ok("big picture: concepts are numbered in learning order", pg.locator("#xs .xnum").count() == len(data["graphs"][0]["lessons"][0]["overview"]["concepts"]))
    pg.locator("#xs .xnode").nth(1).click(force=True); pg.wait_for_timeout(200)
    ok("big picture: tapping lights its links, dims the rest", pg.locator("#xs .xnode.dim").count() > 0 and len(pg.inner_text("#cap")) > 5)
    s = go("meet")
    ok("meet: arrows say «بيحتاج» (no flowing dots) + one legend", pg.locator("#xs .xdot").count() == 0 and pg.locator("#xs .needs").count() == len(s["ins"][:2] + s["outs"][:2]) and pg.locator(".legend .lg").count() == 1)
    ARROW = "(id)=>{const e=document.querySelector('#xs .xedge[data-a=\"'+id+'\"] path, #xs .xedge[data-b=\"'+id+'\"] path');const d=e.getAttribute('d').match(/M([-\\d.]+) ([-\\d.]+).* ([-\\d.]+) ([-\\d.]+)$/);return [[+d[1],+d[2]],[+d[3],+d[4]]];}"
    CEN = "(id)=>{const t=document.querySelector('#xs .xnode[data-id=\"'+id+'\"]').getAttribute('transform').match(/translate\\(([-\\d.]+) ([-\\d.]+)/);return [+t[1],+t[2]];}"
    dist = lambda a, b: ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** .5
    if s["outs"]:
        o = s["outs"][0]; a = pg.evaluate(ARROW, o); po, pt = pg.evaluate(CEN, o), pg.evaluate(CEN, s["target"])
        ok("meet: «X بيحتاج Y» → the arrow goes FROM X TO Y (like the sentence)", dist(a[0], po) < dist(a[0], pt) and dist(a[1], pt) < dist(a[1], po))
    if s["ins"]:
        i0 = s["ins"][0]; a = pg.evaluate(ARROW, i0); pi, pt = pg.evaluate(CEN, i0), pg.evaluate(CEN, s["target"])
        ok("meet: the target needs its «ins» → arrow FROM the target TO them", dist(a[0], pt) < dist(a[0], pi) and dist(a[1], pi) < dist(a[1], pt))
    pg.click("#next"); pg.wait_for_timeout(150)
    ok("meet: a step focuses on one thing (others dimmed)", pg.locator("#xs .xnode.dim").count() > 0 or len(s["ins"] + s["outs"]) == 0)
    nb = pg.locator("#xs .xnode.side").first
    if nb.count(): nb.click(force=True); pg.wait_for_timeout(200); ok("meet: only ONE speech bubble at a time", pg.locator("#xs .bub").count() == 1)
    pg.screenshot(path=SHOT("ex_meet.png"))
    s = go("journey", 4); n = len(s["route"])
    for i in range(1, n): pg.locator(f'#xs .xnode[data-id="{s["route"][i]}"]').click(force=True); pg.wait_for_timeout(1300)
    ok("journey: every station wakes up, one bubble only", pg.locator("#xs .xnode.woke").count() == n and pg.locator("#xs .bub").count() == 1, (pg.locator("#xs .xnode.woke").count(), n))
    ok("journey: the road lights up behind", pg.evaluate("[...document.querySelectorAll('.xglow')].every(g=>parseFloat(g.style.strokeDashoffset)<1)"))
    pg.screenshot(path=SHOT("ex_journey.png"))
    s = go("journey", 3, mover=False)
    ok("stages journey: nothing flies — no traveller, you tap the next stage", pg.locator("#trav").count() == 0)
    pg.locator(f'#xs .xnode[data-id="{s["route"][2]}"]').click(force=True); pg.wait_for_timeout(300)
    ok("stages journey: skipping a stage explains why (step by step)", "خطوة خطوة" in pg.inner_text("#cap") and pg.locator("#xs .xnode.woke").count() == 1)
    s = go("journey", 3, mover=True)
    if s:
        pg.locator(f'#xs .xnode[data-id="{s["route"][1]}"]').click(force=True); pg.wait_for_timeout(1400)
        end = pg.evaluate("(()=>{const g=document.querySelector('.xglow[data-i=\"0\"]');const p=g.getPointAtLength(g.getTotalLength());const t=document.querySelector('#trav').getAttribute('transform').match(/translate\\(([-\\d.]+) ([-\\d.]+)/);return Math.hypot(p.x-parseFloat(t[1]),p.y-parseFloat(t[2]));})()")
        ok("water journey: the drop walks ALONG the road to the next station", end < 3 and pg.locator("#xs .xnode.woke").count() == 2, round(end, 1))
        ok("every move explains what happened", "📍" in pg.inner_text("#cap"))
    # ---- the new activities ----
    s = go("interview")
    if s:
        pg.locator(".qbtn").first.click(); pg.wait_for_timeout(300)
        ok("🎤 interview: tap a question → the character answers (chat)", pg.locator("#chat .msg.them").count() == 1 and pg.locator(".qbtn.asked").count() == 1)
    s = go("flip")
    if s:
        pg.locator(".card2b").first.click(); pg.wait_for_timeout(600)
        ok("🎴 flip cards: tap → the card turns and shows the fact", pg.locator(".card2b.flipped").count() == 1 and pg.locator(".card2b.flipped .bq").count() == 1)
    s = go("before_after")
    if s:
        pg.locator("#ba").fill("100"); pg.wait_for_timeout(200)
        bef = float(pg.get_attribute("#xs #bef", "opacity")); aft = pg.get_attribute("#xs #aft", "opacity")
        if s.get("mode") == "becomes":   # really turns into: the old one fades (stays as a faint ghost, 0.25)
            ok("⏳ before/after (becomes): slide → «before» fades into «after»", aft == "1.00" and bef <= 0.3)
        else:                            # «needs»: the first one STAYS, the second comes after it, the «بيحتاج» arrow + the reason appear
            ok("⏳ first/then (needs): the first STAYS, the second appears, the arrow + the reason are shown",
               aft == "1.00" and bef == 1 and float(pg.get_attribute("#xs #baArrow", "opacity")) > 0.9 and "✅" in pg.inner_text("#baexp"))
    kinds = [[sc["kind"] for sc in c["scenes"][:2]] for c in data["graphs"][0]["lessons"][0]["concepts"]]
    ok("variety: two concepts in a row never start the same way", all(kinds[i] != kinds[i + 1] for i in range(len(kinds) - 1)), kinds)
    s = go("what_if"); pg.click("#sw"); pg.wait_for_timeout(700 + 720 * len(s["affected"]))
    ok("what if: off → domino of tired characters", pg.locator("#xs .xnode.tired").count() == len(s["affected"]) and pg.locator("#xs .xnode.gone").count() == 1)
    pg.screenshot(path=SHOT("ex_whatif.png"))
    pg.click("#sw"); pg.wait_for_timeout(700 + 720 * len(s["affected"])); ok("what if: on → everyone recovers", pg.locator("#xs .xnode.tired").count() == 0)
    m = b.new_page(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True); m.route("**/fonts.*/**", lambda r: r.abort()); m.on("pageerror", lambda e: errs.append(str(e)[:120]))
    m.goto(URL); m.wait_for_timeout(300)
    vb = m.evaluate("document.getElementById('xs').viewBox.baseVal.width")
    ok("phone: scenes turn vertical and fit the screen", vb <= 400 and m.evaluate("document.documentElement.scrollWidth") <= 392, (vb, m.evaluate("document.documentElement.scrollWidth")))
    m.screenshot(path=SHOT("ex_phone.png"), full_page=True)
    b.close()
print("\n".join(res)); print("JS errors:", errs[:3] or "none")
