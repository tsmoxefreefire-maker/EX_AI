"""🆕 batch 30 (Hareth) in a real browser: ARRIVING at an age stage plays its tune by itself (the same tune as «🎵 اسمع»).
Checks: no sound before the first touch · the first touch plays the stage you are in · the same stage again = no tune ·
choosing a stage / opening a book of another stage = that stage's tune · two stages quickly = only the last one ·
mute = silence · «🎵 اسمع» still works · on the phone too (taps).        python tests_browser/test_batch30.py"""
import json, pathlib, urllib.parse, urllib.request
from playwright.sync_api import sync_playwright
HERE = pathlib.Path(__file__).resolve().parent
URL = (HERE.parent / "player" / "explain.html").as_uri()
html = open(urllib.request.url2pathname(urllib.parse.urlparse(URL).path), encoding="utf-8").read()
data = json.loads(html.split("const DATA = ")[1].split(";\nconst $")[0])
res, errs = [], []
def ok(n, c, x=""): res.append(("✅" if c else "❌") + " " + n + ("" if c else " " + str(x)[:300]))
stage_of = [g["audience"]["stage"] for g in data["graphs"]]
# a spy: every tune that really starts, with the stage on the screen at that moment
SPY = """(()=>{const S=window.__SOUND,d=S.demo;window.__TUNES=[];S.demo=function(){window.__TUNES.push(document.body.dataset.stage);return d.apply(this,arguments);};})()"""
tunes = lambda pg: pg.evaluate("window.__TUNES.slice()")
with sync_playwright() as p:
    b = p.chromium.launch()
    for vp in ({"width": 1250, "height": 950}, {"width": 390, "height": 844, "touch": True}):
        tag = "📱" if vp["width"] < 500 else "🖥️"
        ctx = b.new_context(viewport={"width": vp["width"], "height": vp["height"]}, has_touch=bool(vp.get("touch")), is_mobile=bool(vp.get("touch")))
        pg = ctx.new_page(); pg.route("**/fonts.*/**", lambda r: r.abort()); pg.on("pageerror", lambda e: errs.append(str(e)[:150]))
        pg.goto(URL); pg.wait_for_timeout(500); pg.evaluate(SPY)
        press = (lambda sel: pg.tap(sel)) if vp.get("touch") else (lambda sel: pg.click(sel))
        pg.wait_for_timeout(800)
        ok(f"{tag} opening the page: no sound before the first touch (the browser forbids it)", tunes(pg) == [] and pg.evaluate("window.__SOUND.log.length") == 0, tunes(pg))
        first_stage = pg.evaluate("document.body.dataset.stage")
        press("#next"); pg.wait_for_timeout(500)
        ok(f"{tag} the first touch → the tune of the stage you are in ({first_stage})", tunes(pg) == [first_stage], tunes(pg))
        pg.wait_for_timeout(3800)
        n = len(tunes(pg))
        # another lesson / book of the SAME stage → no tune
        same = next(i for i, s in enumerate(stage_of) if s == first_stage and i != 0) if stage_of.count(first_stage) > 1 else 0
        pg.click(f'#side .les[data-g="{same}"][data-l="0"]', force=True); pg.wait_for_timeout(600)
        ok(f"{tag} another book of the same stage → no tune", len(tunes(pg)) == n, tunes(pg))
        # choose a stage from the switcher → its tune
        for st in ["senior", "teen", "kids"]:
            pg.select_option("#stageSel", st); pg.wait_for_timeout(600)
            ok(f"{tag} choose «{st}» → the «{st}» tune, once", tunes(pg)[n:] == [st], tunes(pg)[n:])
            n = len(tunes(pg))
            notes0 = pg.evaluate("window.__SOUND.log.length"); pg.wait_for_timeout(3700)
            ok(f"{tag} «{st}»: the whole tune is heard (7 sounds)", pg.evaluate("window.__SOUND.log.length") - notes0 >= 6, pg.evaluate("window.__SOUND.log.length") - notes0)
        # open a book of ANOTHER stage from the list → that stage's tune
        other = next(i for i, s in enumerate(stage_of) if s == "junior")
        pg.click(f'#side .les[data-g="{other}"][data-l="0"]', force=True); pg.wait_for_timeout(600)
        ok(f"{tag} open a book of another stage (junior) → its tune", tunes(pg)[n:] == ["junior"], tunes(pg)[n:])
        n = len(tunes(pg)); pg.wait_for_timeout(3700)
        # two stages quickly → only the last one plays (never two tunes on top of each other)
        pg.select_option("#stageSel", "senior"); pg.wait_for_timeout(60); pg.select_option("#stageSel", "teen"); pg.wait_for_timeout(700)
        ok(f"{tag} two stages quickly → only the last one's tune", tunes(pg)[n:] == ["teen"], tunes(pg)[n:])
        n = len(tunes(pg)); pg.wait_for_timeout(3700)
        # mute → no sound at all when arriving
        press("#soundBtn"); pg.wait_for_timeout(200)
        notes0 = pg.evaluate("window.__SOUND.log.length")
        pg.select_option("#stageSel", "kids"); pg.wait_for_timeout(1500)
        ok(f"{tag} 🔇 mute → arriving makes no sound", pg.evaluate("window.__SOUND.log.length") == notes0, pg.evaluate("window.__SOUND.log.length") - notes0)
        press("#soundBtn"); pg.wait_for_timeout(200)
        # «🎵 اسمع» still plays it again by hand
        n = len(tunes(pg)); notes0 = pg.evaluate("window.__SOUND.log.length")
        press("#sndDemo"); pg.wait_for_timeout(1200)
        ok(f"{tag} «🎵 اسمع» still plays the tune again", len(tunes(pg)) == n + 1 and pg.evaluate("window.__SOUND.log.length") > notes0)
        ctx.close()
    # the FIRST touch is opening a book of another stage → only THAT stage's tune (not the one the page opened on)
    pg = b.new_page(viewport={"width": 1250, "height": 950}); pg.route("**/fonts.*/**", lambda r: r.abort()); pg.on("pageerror", lambda e: errs.append(str(e)[:150]))
    pg.goto(URL); pg.wait_for_timeout(500); pg.evaluate(SPY)
    other = next(i for i, s in enumerate(stage_of) if s != stage_of[0])
    pg.click(f'#side .les[data-g="{other}"][data-l="0"]'); pg.wait_for_timeout(700)
    ok(f"🖥️ first touch = a book of another stage ({stage_of[other]}) → only its tune", tunes(pg) == [stage_of[other]], tunes(pg))
    pg.close()
    b.close()
print("\n".join(r for r in res if r.startswith("❌")) or "")
print(f"✅ {sum(r.startswith('✅') for r in res)} checks passed · ❌ {sum(r.startswith('❌') for r in res)} failed")
print("JS errors:", errs or "none")
