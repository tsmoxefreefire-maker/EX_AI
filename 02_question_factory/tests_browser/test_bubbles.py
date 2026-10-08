"""🗨️ Speech bubbles + 🎴 cards — the problems Hareth saw with his own eyes, now checked automatically.

For one scene of EVERY kind in every book, in VIDEO mode (the camera moves, the spotlight dims), at every step:
  1. the bubble is fully INSIDE the frame you see (not cut at the edge of the picture);
  2. the bubble is ABOVE the dark spotlight layer and above every character (never half-dark, never hidden);
  3. the words fit inside the bubble (nothing spills out);
  4. the words are big enough to read on the screen (≥ 11px, also on a phone);
  5. the tail points at the one who speaks.
Then after playing with the scene:
  6. 🎴 every card's text stays inside the card, never one word per line, and the back still shows its question;
  7. 🔍 every lens fact is inside the picture.
Run:  python tests_browser/test_bubbles.py            (desktop)
      python tests_browser/test_bubbles.py phone      (phone size)"""
import json, sys, pathlib
from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent
PAGE = HERE.parent / "player" / "explain.html"
PHONE = "phone" in sys.argv[1:]
data = json.loads(PAGE.read_text(encoding="utf-8").split("const DATA = ")[1].split(";\nconst $")[0])

BUBBLE = r"""()=>{const xs=document.getElementById('xs');if(!xs)return {none:1};const out=[];
  const lay=xs.querySelector(':scope > #saylayer');const bub=lay&&lay.querySelector('.bub');if(!bub)return {none:1};
  if(xs.lastElementChild!==lay)out.push('bubble-not-on-top');
  const spot=xs.querySelector(':scope > #spot');if(spot&&!(spot.compareDocumentPosition(lay)&Node.DOCUMENT_POSITION_FOLLOWING))out.push('bubble-under-spotlight');
  const R=xs.getBoundingClientRect(),r=bub.querySelector('rect').getBoundingClientRect();
  if(r.left<R.left-1||r.right>R.right+1||r.top<R.top-1||r.bottom>R.bottom+1)out.push('bubble-cut-by-frame');
  bub.querySelectorAll('text').forEach(t=>{const q=t.getBoundingClientRect();if(q.left<r.left-1||q.right>r.right+1||q.top<r.top-1||q.bottom>r.bottom+1)out.push('text-outside-bubble');
     if(q.height<11)out.push('text-too-small:'+q.height.toFixed(1));});
  const who=xs.querySelector(`.xnode[data-id="${bub.dataset.for}"] .xbody`);
  if(who){const w=who.getBoundingClientRect(),tl=bub.querySelector('.btail').getBoundingClientRect();const tip=tl.left+tl.width/2;
     if(w.width&&(tip<w.left-12||tip>w.right+12)&&w.right>R.left&&w.left<R.right)out.push('tail-misses-speaker');}
  return {out};}"""
CARDS = r"""()=>{const out=[];document.querySelectorAll('#q .card2b').forEach(c=>{const C=c.getBoundingClientRect();
    c.querySelectorAll('.face:not([hidden])').forEach(f=>{const r=f.getBoundingClientRect();if(r.bottom>C.bottom+1||r.top<C.top-1||r.right>C.right+1||r.left<C.left-1)out.push('card-text-outside');});
    const bt=c.querySelector('.back:not([hidden]) .bt');if(bt){const words=bt.textContent.trim().split(/\s+/).length;
      const range=document.createRange();range.selectNodeContents(bt);const cs=[...range.getClientRects()].filter(x=>x.width>6).map(x=>x.top+x.height/2).sort((a,b)=>a-b);let lines=new Set();let last=-99;cs.forEach(y=>{if(y-last>8){lines.add(y);last=y;}});   /* one line = centres within 8px (a «name» button is taller than plain words) */
      if(words>=4&&lines.size>=words)out.push('card-one-word-per-line');
      if(!c.querySelector('.back:not([hidden]) .bq'))out.push('card-back-lost-its-question');}});
  const xs=document.getElementById('xs');if(xs){const R=xs.getBoundingClientRect();xs.querySelectorAll('.fact rect').forEach(e=>{const r=e.getBoundingClientRect();
    if(r.left<R.left-1||r.right>R.right+1||r.top<R.top-1||r.bottom>R.bottom+1)out.push('lens-fact-cut');});}
  return out;}"""


def path_of(l):
    p = [l["overview"]] + ([l["world"]] if l.get("world") else []) + ([l["assemble"]] if l.get("assemble") else [])
    for c in l["concepts"]:
        p += c["scenes"]
    return p


problems, checked, errs = {}, 0, []
with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_page(viewport={"width": 390, "height": 900} if PHONE else {"width": 1250, "height": 1000})
    pg.route("**/fonts.*/**", lambda r: r.abort()); pg.on("pageerror", lambda e: errs.append(str(e)[:150]))
    pg.goto(PAGE.as_uri()); pg.wait_for_timeout(300)
    for gi, g in enumerate(data["graphs"]):
        done = set()
        for li, l in enumerate(g["lessons"]):
            P = path_of(l)
            for pos, s in enumerate(P):
                k = s["kind"]
                if k in done:
                    continue
                done.add(k)
                pg.click(f'#side .les[data-g="{gi}"][data-l="{li}"]'); pg.wait_for_timeout(120)
                for _ in range(sum(len(x["steps"]) for x in P[:pos])):
                    pg.click("#next")
                if "وقّف" in pg.inner_text("#play"):
                    pg.click("#play")
                pg.click("#play"); pg.locator("#q").scroll_into_view_if_needed()          # 🎬 video from the first step
                where = f"{g['title'][:8]} · {l['lesson_title']} · {k}"
                for st in range(len(s["steps"])):
                    pg.wait_for_timeout(1300)                                              # the camera has arrived
                    r = pg.evaluate(BUBBLE); checked += 1
                    if r.get("out"):
                        problems.setdefault(where, set()).update(f"step{st}:{x}" for x in r["out"])
                    pg.wait_for_timeout(max(3200, len(s["steps"][st].split()) * 420) - 1200)
                pg.wait_for_timeout(800)
                # play with it, then check the cards / lens / the last bubble
                for c in pg.locator("#q .card2b").all():
                    c.click(force=True)
                for q in pg.locator("#q .qbtn").all():
                    q.click(force=True); pg.wait_for_timeout(150)
                    r = pg.evaluate(BUBBLE)
                    if r.get("out"):
                        problems.setdefault(where, set()).update(f"interview:{x}" for x in r["out"])
                if pg.locator("#q #more").count():
                    for _ in range(6):
                        if pg.locator("#q #more").is_enabled():
                            pg.click("#q #more"); pg.wait_for_timeout(150)
                            r = pg.evaluate(BUBBLE)
                            if r.get("out"):
                                problems.setdefault(where, set()).update(f"dialogue:{x}" for x in r["out"])
                pg.wait_for_timeout(500)
                out = pg.evaluate(CARDS)
                if out:
                    problems.setdefault(where, set()).update(out)
    b.close()

print(("📱 phone" if PHONE else "🖥️ desktop"), "· bubble moments checked:", checked)
for w, p in problems.items():
    print("❌", w, sorted(p))
print("✅ no problems" if not problems else f"❌ scenes with problems: {len(problems)}")
print("JS errors:", errs or "none")
sys.exit(1 if problems or errs else 0)
