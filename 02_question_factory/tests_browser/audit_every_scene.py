"""Audit EVERY scene of the explanation page: empty cards, text overflowing, labels on top of each other, cut bubbles, JS errors."""
import json
from playwright.sync_api import sync_playwright
import pathlib, sys
HERE=pathlib.Path(__file__).resolve().parent
PAGE=HERE.parent/"player"/"explain.html"
URL=PAGE.as_uri()
html=open(PAGE,encoding="utf-8").read(); data=json.loads(html.split("const DATA = ")[1].split(";\nconst $")[0])
CHECK=r"""()=>{const out=[];const xs=document.getElementById('xs');
  /* 1) text that does not fit its box (cards, chat, captions, buttons) */
  document.querySelectorAll('#q .fb, #q .ff, #q .msg, #q .qbtn, #q .cap, #q .why p, #q .legend, #q .slider2, #q .sl').forEach(e=>{if(e.offsetParent===null&&!e.closest('.fcard2'))return;
     if(e.scrollHeight>e.clientHeight+3||e.scrollWidth>e.clientWidth+3)out.push('overflow:'+e.className+':'+e.textContent.trim().slice(0,30));});
  /* 2) cards: both faces have text, ONE face shown at a time, nothing spills out */
  document.querySelectorAll('#q .fcard2, #q .card2b').forEach(c=>{const b=c.querySelector('.back, .fb'),f=c.querySelector('.front, .ff');
     if(!b||!b.textContent.trim())out.push('empty-back');if(!f||!f.textContent.trim())out.push('empty-front');
     if(c.classList.contains('card2b')){const vis=[...c.querySelectorAll('.face')].filter(x=>getComputedStyle(x).display!=='none');if(vis.length!==1)out.push('two-faces-shown');}
     if(c.scrollHeight>c.clientHeight+3)out.push('card-overflow');});
  /* 3) character names on top of each other inside the picture */
  if(xs){const vis=e=>{for(let x=e;x&&x!==xs;x=x.parentNode){const o=x.getAttribute&&x.getAttribute('opacity');if(o!==null&&o!==undefined&&parseFloat(o)<0.2)return false;if(x.style&&parseFloat(getComputedStyle(x).opacity)<0.2)return false;}return true;};
     const t=[...xs.querySelectorAll('.xname')].filter(vis).map(e=>e.getBoundingClientRect()).filter(r=>r.width>0);
     for(let i=0;i<t.length;i++)for(let j=i+1;j<t.length;j++){const a=t[i],b=t[j];const ox=Math.min(a.right,b.right)-Math.max(a.left,b.left),oy=Math.min(a.bottom,b.bottom)-Math.max(a.top,b.top);if(ox>4&&oy>4)out.push('names-overlap');}
     /* 4) names / bubbles cut by the edge of the picture */
     const R=xs.getBoundingClientRect();xs.querySelectorAll('.xname,.bub rect,.fact rect').forEach(e=>{const r=e.getBoundingClientRect();if(r.width&&(r.left<R.left-2||r.right>R.right+2||r.top<R.top-2))out.push('cut:'+(e.textContent||e.parentNode.textContent||'').trim().slice(0,20));});}
  /* 4b) text spilling out of its speech bubble */
  if(xs)xs.querySelectorAll('.bub').forEach(b=>{const r=b.querySelector('rect').getBoundingClientRect();b.querySelectorAll('text').forEach(t=>{const q=t.getBoundingClientRect();if(q.left<r.left-2||q.right>r.right+2)out.push('bubble-text:'+t.textContent.slice(0,20));});});
  /* 4c) a flip card whose back is broken into one word per line */
  document.querySelectorAll('#q .fcard2.flipped .fbt').forEach(p=>{const tops=new Set([...p.querySelectorAll('.w,.kw')].map(e=>Math.round(e.getBoundingClientRect().top)));const words=p.textContent.trim().split(/\s+/).length;if(words>=4&&tops.size>=words-1)out.push('card-one-word-per-line');});
  /* 5) an empty caption line */
  const cap=document.getElementById('cap');if(cap&&!cap.textContent.trim())out.push('empty-caption');
  return out;}"""
issues={};errs=[]
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={"width":390,"height":844} if "phone" in sys.argv else {"width":1250,"height":1000}); pg.route("**/fonts.*/**",lambda r:r.abort()); pg.on("pageerror",lambda e:errs.append(str(e)[:150]))
    pg.goto(URL); pg.wait_for_timeout(300); n=0
    ONLY=[int(x) for x in sys.argv[1:] if x.isdigit()]        # optional: audit only these books (by order), to run in parallel
    for gi,g in enumerate(data["graphs"]):
        if ONLY and gi not in ONLY: continue
        for li,l in enumerate(g["lessons"]):
            pg.click(f'#side .les[data-g="{gi}"][data-l="{li}"]'); pg.wait_for_timeout(150)
            if "وقّف" in pg.inner_text("#play"): pg.click("#play"); pg.wait_for_timeout(500)
            total=sum(len(s["steps"]) for s in [l["overview"]]+([l["world"]] if l.get("world") else [])+([l["assemble"]] if l.get("assemble") else [])+[s for c in l["concepts"] for s in c["scenes"]])
            seen=set()
            for _ in range(total+2):
                where=pg.inner_text(".where").strip()
                if where not in seen:
                    seen.add(where); n+=1; pg.wait_for_timeout(200)
                    if "وقّف" in pg.inner_text("#play"): pg.click("#play")
                    pg.wait_for_timeout(750)                                   # the camera comes back to the whole picture
                    # flip every card so the backs are measured too
                    for c in pg.locator("#q .fcard2, #q .card2b").all():
                        c.click(force=True)
                    if pg.locator("#q .fcard2, #q .card2b").count(): pg.wait_for_timeout(600)
                    # ask every interview question so the chat is measured
                    for q in pg.locator("#q .qbtn").all(): q.click(force=True)
                    if pg.locator("#q #more").count():
                        for _ in range(6): pg.click("#q #more",force=True)
                    found=pg.evaluate(CHECK)
                    if found:
                        key=f"{g['title'][:8]} · {l['lesson_title']} · {where}"
                        issues[key]=sorted(set(found))
                        pg.screenshot(path=str(HERE/"shots"/f"aud_{n}.png"))
                if "خلصت الدرس" in pg.inner_text("#next"): break
                pg.click("#next"); pg.wait_for_timeout(60)
    b.close()
print("scenes checked:",n); print("scenes with problems:",len(issues))
from collections import Counter
c=Counter(x.split(":")[0] for v in issues.values() for x in v); print("problem kinds:",dict(c))
for k,v in list(issues.items())[:14]: print("-",k,"→",v[:3])
print("JS errors:",errs[:3] or "none")
json.dump(issues,open(str(HERE/"shots")+"/audit_ex.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
