(function(){
"use strict";
const DATA = /*DATA*/null;
const $=s=>document.querySelector(s);
const svgNS="http://www.w3.org/2000/svg";
const reduce=window.matchMedia("(prefers-reduced-motion: reduce)").matches;
const DIFF={easy:"سهل",mid:"متوسط",hard:"صعب"};
const TNAME={meaning:"🤥 مين الصادق؟",match:"🔗 وصّل",memory:"🃏 الذاكرة",spell:"🔤 ركّب الاسم",true_false:"👉👈 صح ولا غلط",
  sequence:"🌉 ابنِ الجسر",fix_chain:"🚂 صلّح القطار",prereq:"🚪 افتح الباب",unlocks:"🗺️ ضوّي الطرق",sort:"🛗 المصعد",
  odd_one_out:"🧩 الدخيل",who_am_i:"🕵️ مين أنا؟",predict:"🔮 شو بيصير لو؟",adjust:"🎚️ اضبط"};
function shuffle(a,seed){a=a.slice();let s=seed||1;for(let i=a.length-1;i>0;i--){s=(s*9301+49297)%233280;const j=Math.floor(s/233280*(i+1));[a[i],a[j]]=[a[j],a[i]];}return a;}
const pickOne=(arr)=>arr[Math.floor(Math.random()*arr.length)];
let G=0,L=0,C=0,Qi=0; const done=new Set(); const evidence=[]; let tab="file"; let t0=performance.now();
const graph=()=>DATA.graphs[G]; const lesson=()=>graph().lessons[L]; const concept=()=>lesson().concepts[C];
const name=id=>graph().names[id]||id; const key=(c,i)=>G+":"+L+":"+c+":"+i;
const theme=()=>lesson().theme||"default"; const garden=()=>theme()==="garden";
let timers=[]; const later=(fn,ms)=>{const t=setTimeout(fn,reduce?Math.min(ms,30):ms);timers.push(t);return t;};
function clearTimers(){timers.forEach(clearTimeout);timers=[];}
let cleanups=[]; const onCleanup=f=>cleanups.push(f); function runCleanups(){cleanups.forEach(f=>{try{f();}catch(e){}});cleanups=[];}

function record(cid,outcome){const q=concept().questions[Qi];evidence.push({concept_id:cid,lesson_id:lesson().lesson_id,activity:q.template,correctness:outcome,question_difficulty:q.difficulty,response_time_ms:Math.round(performance.now()-t0),modality:"interaction",interaction_yields_evidence:true,timestamp:new Date().toISOString()});t0=performance.now();if(tab==="ev")renderBelow();}

/* ---------- header + side ---------- */
const total=DATA.graphs.reduce((a,g)=>a+g.lessons.reduce((b,l)=>b+l.question_count,0),0);
const nl=DATA.graphs.reduce((a,g)=>a+g.lessons.length,0);
const nc=DATA.graphs.reduce((a,g)=>a+g.lessons.reduce((b,l)=>b+l.concepts.length,0),0);
$("#sub").textContent=`المصنع قرأ الكتاب بالستركشر الجديد، مرّ على ${nl} دروس، ولكل مفهوم (${nc} مفهوم) ولّد تحدياته: ${total} تحدي تفاعلي من 13 نوع، فحصهم وحفظهم مع الدرس.`;
let kid=true; const unlocked=new Set(); let openAll=false;   /* 🔓 demo switch: opens every lesson, station and challenge */
function lessonDone(gi,li){const l=DATA.graphs[gi].lessons[li];return l.concepts.every((c,ci)=>c.questions.every((_,qi)=>done.has(gi+":"+li+":"+ci+":"+qi)));}
function lessonLocked(gi,li){if(!kid||openAll)return false;const g=DATA.graphs[gi],l=g.lessons[li];if(unlocked.has(gi+":"+li))return false;
  return (l.requires||[]).some(rid=>{const ri=g.lessons.findIndex(x=>x.lesson_id===rid);return ri>=0&&!lessonDone(gi,ri);});}
const PLACE=["🏡","🌳","🌻","🪴","⛲","🏞️"];
function renderSide(){
  if(kid){$("#side").innerHTML=DATA.graphs.map((g,gi)=>`<h3>🗺️ ${g.title}</h3><div class="kmap">`+g.lessons.map((l,li)=>{const lock=lessonLocked(gi,li),dn=lessonDone(gi,li);
      const need=(l.requires||[]).map(rid=>(g.lessons.find(x=>x.lesson_id===rid)||{}).lesson_title).filter(Boolean);
      return `<div><button class="kplace${lock?" locked":""}${dn?" done":""}" data-g="${gi}" data-l="${li}" ${gi===G&&li===L?'aria-current="true"':""}><span class="ke">${alive(placeOf(gi,li))}</span><span><b dir="auto">${l.lesson_title}</b><small>${lock?"🔒 بينفتح بعد «"+need.join("» و«")+"»":l.concepts.length+" محطات"}</small></span><span class="klock">${lock?"🔒":""}</span></button>${lock?`<button class="unlockbtn" data-u="${gi}:${li}">🔓 افتحه هلأ</button>`:""}</div>`;}).join("")+`</div>`).join("");
    $("#side").querySelectorAll(".kplace").forEach(b=>b.addEventListener("click",()=>{const gi=+b.dataset.g,li=+b.dataset.l;if(lessonLocked(gi,li)){b.classList.add("shake");later(()=>b.classList.remove("shake"),450);return;}G=gi;L=li;C=0;Qi=0;renderAll();}));
    $("#side").querySelectorAll(".unlockbtn").forEach(b=>b.addEventListener("click",()=>{unlocked.add(b.dataset.u);const [gi,li]=b.dataset.u.split(":").map(Number);G=gi;L=li;C=0;Qi=0;renderAll();}));
    return;}
  $("#side").innerHTML=DATA.graphs.map((g,gi)=>{let last=null,unitShown=false;return `<h3>📘 ${g.title}</h3>`+g.lessons.map((l,li)=>{let head="";
    if(!unitShown&&l.unit_id){head+=`<div class="tree u">${g.names[l.unit_id]||l.unit_id}</div>`;unitShown=true;}
    if(l.topic_id&&l.topic_id!==last){head+=`<div class="tree t">${g.names[l.topic_id]||l.topic_id}</div>`;last=l.topic_id;}
    return head+`<button class="les" data-g="${gi}" data-l="${li}" ${gi===G&&li===L?'aria-current="true"':""}><span dir="auto">${l.lesson_title}</span><small>${l.concepts.length} مفاهيم</small></button>`;}).join("");}).join("");
  $("#side").querySelectorAll(".les").forEach(b=>b.addEventListener("click",()=>{G=+b.dataset.g;L=+b.dataset.l;C=0;Qi=0;renderAll();}));}

/* ---------- stars (note 3: no discouraging "0 of 1") ---------- */
const scores={};
const starStr=r=>{const n=r>=0.99?3:r>=0.5?2:1;return "★".repeat(n)+"☆".repeat(3-n);};
const starWord=r=>r>=0.99?"من أول مرة! 🤩":r>=0.5?"قرّبت كثير! 💪":"وصلت بالآخر، برافو! 💪";
function conceptDone(ci){return lesson().concepts[ci].questions.every((_,i)=>done.has(key(ci,i)));}
/* student mode: one step at a time — a station opens when the one before it is finished, a challenge when the one before it is done */
const stationOpen=ci=>!kid||openAll||ci===0||conceptDone(ci-1)||conceptDone(ci);
const challengeOpen=(ci,i)=>!kid||openAll||i===0||done.has(key(ci,i-1))||done.has(key(ci,i));
function nudge(el,msg){el.classList.add("shake");setTimeout(()=>el.classList.remove("shake"),450);fb(msg,"bad");}
function stars(ci){const qs=lesson().concepts[ci].questions;if(!conceptDone(ci))return "☆☆☆";return starStr(qs.reduce((a,_,i)=>a+(scores[key(ci,i)]||0),0)/qs.length);}
function firstOpenChallenge(ci){const qs=lesson().concepts[ci].questions;const i=qs.findIndex((_,k)=>!done.has(key(ci,k)));return i<0?0:i;}
function renderWelcome(){const l=lesson();$("#welcome").innerHTML=`<span class="big">${alive(skin().mascot)}</span><div><h1>أهلاً! 👋 أنا «${skin().name}»</h1><p>اليوم رح نكتشف <b>${l.lesson_title}</b> مع بعض. كل محطة فيها تحديات، واجمع النجوم ⭐!</p></div>`;}
function renderLesson(){const l=lesson(),c=concept();document.body.classList.toggle("skin-garden",garden());const icons=l.icons||{};
  if(kid){const total=l.concepts.length,fin=l.concepts.filter((_,i)=>conceptDone(i)).length;const plant=skin().grow[Math.min(4,Math.round(fin/Math.max(1,total)*4))];
    const stickers=l.concepts.map((k,i)=>conceptDone(i)?`<span class="stk">🏅 ${alive(icons[k.concept_id]||"")} ${k.title}</span>`:"").join("");
    $("#lesson").innerHTML=`<div class="lhead"><h2 dir="auto">${garden()?"🌿":"📘"} ${l.lesson_title}</h2></div>
      <h3 class="sec">طريق الدرس: كل حجر محطة 🪨</h3>
      <div class="kpath">${l.concepts.map((k,i)=>`${i?'<span class="kdots"></span>':""}<button class="kstone${i===C?" on":""}${stationOpen(i)?"":" locked"}" data-c="${i}">${stationOpen(i)?"":'<span class="klk">🔒</span>'}<span class="si">${alive(icons[k.concept_id]||"🔹")}</span>${k.title}${i===C?'<span class="walkerk">🚶</span>':""}${conceptDone(i)?`<span class="bloom">${skin().done}</span>`:""}<span class="st">${stars(i)}</span></button>`).join("")}</div>
      <div class="kbar"><span class="potplant"><span class="pp">${alive(plant)}</span> ${skin().growLabel}: ${fin} من ${total}</span><span class="album">${stickers||'<small class="small">الملصقات 🏅 بتطلع لما تخلص محطة</small>'}</span></div>
      <h3 class="sec">تحديات «${alive(icons[c.concept_id]||"")} ${c.title}»</h3>
      <div class="kcards" role="tablist">${c.questions.map((q,i)=>`<button class="kcard${done.has(key(C,i))?" done":""}${challengeOpen(C,i)?"":" locked"}" role="tab" aria-selected="${i===Qi}" data-i="${i}">${challengeOpen(C,i)?"":'<span class="klk">🔒</span>'}<span class="kci">${alive((TNAME[q.template]||"").split(" ")[0])}</span>${(TNAME[q.template]||q.template).split(" ").slice(1).join(" ")}</button>`).join("")}</div>`;
    $("#lesson").querySelectorAll(".kstone").forEach(b=>b.addEventListener("click",()=>{const ci=+b.dataset.c;if(!stationOpen(ci))return nudge(b,"🔒 خلّص المحطة اللي قبلها أول");C=ci;Qi=firstOpenChallenge(ci);renderAll();}));
    $("#lesson").querySelectorAll(".kcard").forEach(b=>b.addEventListener("click",()=>{const i=+b.dataset.i;if(!challengeOpen(C,i))return nudge(b,"🔒 خلّص التحدي اللي قبله أول");Qi=i;renderAll();}));return;}
  $("#lesson").innerHTML=`<div class="lhead"><h2 dir="auto">${l.lesson_title}</h2><span><span class="cov${l.coverage.missing.length?" miss":""}">جاهز: ${l.coverage.ready} من ${l.coverage.concepts} مفاهيم</span> <span class="status">بانتظار مراجعة المعلم</span></span></div>
   <div class="small">${l.unit_id?name(l.unit_id)+" ← "+name(l.topic_id)+" ← ":""}<b>${l.lesson_title}</b>${l.lesson_minutes?" · ⏱️ "+l.lesson_minutes+" دقيقة":""} · ${garden()?"🌿 جو الجنينة":"جو عام"}</div>
   <h3 class="sec">رحلة الدرس: كل محطة مفهوم، واجمع النجوم ⭐</h3>
   <div class="stations">${l.concepts.map((k,i)=>`${i?'<span class="link"></span>':""}<button class="station${i===C?" on":""}" data-c="${i}"><b dir="auto">${k.title}</b><span class="st">${stars(i)}</span><small>${k.questions.length} تحديات</small></button>`).join("")}</div>
   <h3 class="sec">تحديات «${c.title}»</h3>
   <div class="qtabs" role="tablist">${c.questions.map((q,i)=>`<button class="qtab${done.has(key(C,i))?" done":""}" role="tab" aria-selected="${i===Qi}" data-i="${i}">${i+1}. ${TNAME[q.template]||q.template}</button>`).join("")}</div>`;
  $("#lesson").querySelectorAll(".station").forEach(b=>b.addEventListener("click",()=>{C=+b.dataset.c;Qi=0;renderAll();}));
  $("#lesson").querySelectorAll(".qtab").forEach(b=>b.addEventListener("click",()=>{Qi=+b.dataset.i;renderAll();}));}

/* ---------- question frame ---------- */
function frame(q,body){return `<div class="mascot" id="mascot" aria-hidden="true"><span class="m-body" data-mood="happy">${artSVG(skin().mascot,"mascotart")}</span><span class="m-say" id="msay"></span></div>
  <div class="qhead"><span class="diff ${q.difficulty}">${DIFF[q.difficulty]}</span></div><p class="qtext" dir="auto">${q.question}</p><p class="how">${q.how}</p>${body}
  <div class="feedback" id="fb"></div><div class="tests">🎯 بيفحص: ${(q.concepts||[]).map(name).join("، ")}</div>`;}
let soundOn=true,actx=null;
/* little sound effects, made in the browser (no files): water, train, door, cat, lift… */
function ac(){actx=actx||new (window.AudioContext||window.webkitAudioContext)();if(actx.state==="suspended")actx.resume();return actx;}
function tone(f1,f2,dur,type,vol,delay){const a=ac(),o=a.createOscillator(),g=a.createGain(),t=a.currentTime+(delay||0);o.type=type||"sine";o.frequency.setValueAtTime(f1,t);o.frequency.exponentialRampToValueAtTime(Math.max(30,f2),t+dur);
  g.gain.setValueAtTime(0.0001,t);g.gain.exponentialRampToValueAtTime(vol||.12,t+.015);g.gain.exponentialRampToValueAtTime(.0001,t+dur);o.connect(g);g.connect(a.destination);o.start(t);o.stop(t+dur+.02);}
function noise(dur,f1,f2,vol,delay,q){const a=ac(),n=a.sampleRate*dur,buf=a.createBuffer(1,n,a.sampleRate),d=buf.getChannelData(0);for(let i=0;i<n;i++)d[i]=Math.random()*2-1;
  const src=a.createBufferSource(),fl=a.createBiquadFilter(),g=a.createGain(),t=a.currentTime+(delay||0);src.buffer=buf;fl.type="bandpass";fl.Q.value=q||1.2;fl.frequency.setValueAtTime(f1,t);fl.frequency.exponentialRampToValueAtTime(f2,t+dur);
  g.gain.setValueAtTime(vol||.2,t);g.gain.exponentialRampToValueAtTime(.0001,t+dur);src.connect(fl);fl.connect(g);g.connect(a.destination);src.start(t);src.stop(t+dur);}
const SFX={
  good:()=>{tone(660,990,.18);},bad:()=>{tone(300,140,.25,"triangle");},
  ding:()=>{tone(1320,1300,.5,"sine",.14);tone(1760,1750,.4,"sine",.06,.05);},
  pop:()=>{tone(500,1500,.08,"sine",.12);},click:()=>{noise(.04,3000,2000,.25);},
  splash:()=>{noise(.5,1800,300,.35);noise(.3,900,200,.2,.08);},
  bubbles:()=>{for(let i=0;i<6;i++)tone(500+Math.random()*500,1200+Math.random()*600,.07,"sine",.06,i*.12);},
  whistle:()=>{[0,.32].forEach(d=>{tone(880,870,.28,"sine",.09,d);tone(1108,1100,.28,"sine",.07,d);tone(1318,1310,.28,"sine",.05,d);});for(let i=0;i<6;i++)noise(.07,700,300,.14,.7+i*.14,2);},
  chug:()=>{for(let i=0;i<4;i++)noise(.09,700,300,.18,i*.18,2);},
  honk:()=>{tone(392,392,.25,"sawtooth",.05);tone(330,330,.3,"sawtooth",.05,.22);},
  creak:()=>{tone(180,90,.9,"sawtooth",.04);},
  meow:()=>{tone(500,900,.18,"triangle",.1);tone(900,420,.35,"triangle",.1,.17);},
  hiss:()=>{noise(.5,4000,6000,.12,0,.6);},
  whoosh:()=>{noise(.35,400,2500,.18,0,.8);},
  hoot:()=>{tone(420,400,.25,"sine",.12);tone(420,380,.35,"sine",.12,.32);},
  laugh:()=>{for(let i=0;i<4;i++)tone(520-i*20,460-i*20,.09,"square",.04,i*.11);},
  crumble:()=>{noise(.5,600,120,.3,0,.7);},
  step:()=>{noise(.05,900,500,.15);noise(.05,900,500,.15,.22);},
  water:()=>{for(let i=0;i<5;i++)tone(700+i*90,900+i*90,.06,"sine",.05,i*.07);},
  bloom:()=>{tone(784,1568,.25,"sine",.08);},
  thud:()=>{tone(120,60,.15,"sine",.18);noise(.08,400,200,.15);},
  flip:()=>{noise(.08,2500,1200,.15);},
  buzz:()=>{tone(220,240,.4,"sawtooth",.03);},
  tada:()=>{[523,659,784,1046].forEach((f,i)=>tone(f,f,.22,"triangle",.08,i*.1));},
  drip:()=>{tone(1200,500,.12,"sine",.14);tone(900,1300,.06,"sine",.05,.1);},
  wind:()=>{noise(.8,300,900,.12,0,.5);},
  rustle:()=>{for(let i=0;i<5;i++)noise(.05,3500,2500,.08,i*.05,2);},
  yip:()=>{tone(700,1100,.08,"square",.05);tone(800,1200,.08,"square",.05,.12);},
  sneeze:()=>{noise(.1,1500,3000,.12);noise(.25,3000,800,.25,.12,.7);},
  creakup:()=>{tone(140,200,.35,"sawtooth",.05);},
  crack:()=>{noise(.12,2500,800,.35,0,3);noise(.1,1800,600,.25,.08,3);},
  chew:()=>{for(let i=0;i<3;i++)noise(.06,600,300,.18,i*.15,2);},
  burp:()=>{tone(110,70,.35,"sawtooth",.09);},
  spit:()=>{noise(.18,1200,3500,.22,0,1.2);},
  cheer:()=>{for(let i=0;i<6;i++)noise(.25,900+i*120,1400,.06,i*.05,.8);[523,659,784,1046,1318].forEach((f,i)=>tone(f,f,.18,"triangle",.07,.1+i*.08));},
  giggle:()=>{[0,.09,.18,.27].forEach((d,i)=>tone(700+i*60,900+i*60,.07,"sine",.06,d));},
  sparkle:()=>{[1568,1976,2349].forEach((f,i)=>tone(f,f,.1,"sine",.05,i*.07));}};
function sfx(name,o){if(!soundOn)return;try{if(typeof SOUND!=="undefined"&&SOUND.play(name,o))return;   /* 🎵 the new sounds (sound.js): by age + by subject */
  const p=(typeof stagePack==="function")?stagePack():null;let f;      /* each age stage has its own sounds (stage.js) */
  if(p&&(name in p))f=p[name];else if(p&&p.__default!==undefined)f=p.__default;else f=SFX[name]||SFX.good;if(f)f();}catch(e){}}
function beep(ok){sfx(ok?"good":"bad");}
const fb=(t,c)=>{const f=$("#fb");if(!f)return;f.textContent=t;f.className="feedback"+(c?" "+c:"");if(c==="good")beep(true);else if(c==="bad")beep(false);};
/* the mascot «بذور» reacts to every move; the joke is on it, never on the student */
const LINES={pat:["ولا يهمك ✨","جرّب كمان، بتقدر!"],happy:["يا سلام! 🎉","برافو عليك!","هيك الشغل! 💪","وااو! ✨"],oops:["أوبس! 😅","قرّبت!","جرّب كمان!","ولا يهمك 😄"],dive:["بنقذ الكرة! 🤿","سباحة! 🏊"]};
function mascot(mood,text){const m=$("#mascot");if(!m)return;m.className="mascot "+mood+" talk";const b=m.querySelector(".m-body");if(b)b.dataset.mood=mood==="happy"?"laugh":mood==="oops"?"o":"happy";
  $("#msay").textContent=text||pickOne(LINES[mood]||LINES.happy);later(()=>{if(m){m.className="mascot";if(b)b.dataset.mood="happy";}},1700);}
function confetti(){if(reduce)return;const box=$("#q");const cols=["#F2B33D","#2E8B57","#1F6F78","#E2543C","#7A45B8","#F28AA8"];
  for(let i=0;i<28;i++){const p=document.createElement("span");p.className="conf";p.style.left=(4+Math.random()*92)+"%";p.style.background=cols[i%cols.length];p.style.animationDelay=(Math.random()*.25)+"s";box.appendChild(p);setTimeout(()=>p.remove(),1800);}}
function sparkles(){if(reduce)return;const box=$("#q");for(let i=0;i<10;i++){const p=document.createElement("span");p.className="spark";p.textContent="✦";p.style.left=(15+Math.random()*70)+"%";p.style.top=(20+Math.random()*50)+"%";p.style.animationDelay=(Math.random()*.3)+"s";box.appendChild(p);setTimeout(()=>p.remove(),1300);}}
function celebrate(ratio){if(ratio>=0.99){confetti();sfx("cheer");mascot("happy","يييييه! 🎉 بطل!");}
  else if(ratio>=0.5){sparkles();sfx("sparkle");mascot("happy","برافو، قرّبت كثير! 💪");}
  else{mascot("pat","ولا يهمك، كل مرة بتتعلم أكثر ✨");}}
function finish(q,ratio,lines){done.add(key(C,Qi));if(!(key(C,Qi) in scores))scores[key(C,Qi)]=ratio;celebrate(ratio);renderLesson();
  if($("#sol"))return;const d=document.createElement("div");d.className="solution";d.id="sol";
  d.innerHTML=`<h3>الحل خطوة خطوة · <span class="stars">${starStr(ratio)}</span> <span class="small">${starWord(ratio)}</span></h3><ol>${(lines||q.solution).map(s=>`<li>${s}</li>`).join("")}</ol>`;$("#q").appendChild(d);
  const c=concept();let label=null,go=null;
  if(Qi<c.questions.length-1){label="التحدي الجاي";go=()=>{Qi++;renderAll();};}
  else if(C<lesson().concepts.length-1){label="المحطة الجاية: "+lesson().concepts[C+1].title;go=()=>{C++;Qi=0;renderAll();};}
  else if(kid){label="🏁 خلصت الدرس! ارجع للخريطة";go=()=>{renderAll();window.scrollTo({top:0,behavior:reduce?"auto":"smooth"});};}
  const low=ratio<0.5;
  if(low){const rr=document.createElement("div");rr.className="row";rr.innerHTML=`<button class="btn" id="again">🔁 جرّب مرة ثانية</button>`;$("#q").appendChild(rr);$("#again").addEventListener("click",()=>{done.delete(key(C,Qi));renderAll();});}
  if(label){const r=document.createElement("div");r.className="row";r.innerHTML=`<button class="btn${low?" ghost":""}" id="nx">${label}</button>`+(kid&&!low?`<button class="btn ghost" id="wait">✋ استنى</button><span class="small" id="auto"></span>`:"");$("#q").appendChild(r);$("#nx").addEventListener("click",go);
    if(kid&&!low){let n=6;const tick=()=>{const a=$("#auto");if(!a)return;if(--n<=0){go();return;}a.textContent="➡️ بننتقل لحالنا بعد "+n+"…";autoT=later(tick,1000);};let autoT=later(tick,10);
      $("#wait").addEventListener("click",()=>{clearTimeout(autoT);$("#auto").textContent="خذ وقتك 🙂";$("#wait").remove();});}}}

/* ---------- drag with mouse or finger; a tap (click) always works too ---------- */
function dragify(el,onDrop,opts){opts=opts||{};el.classList.add("drag");
  let edgeY=null,edgeLoop=0;
  const edgeScroll=()=>{edgeLoop=0;if(edgeY===null)return;const H=window.innerHeight,zone=70;let d=0;
    if(edgeY>H-zone)d=Math.ceil((edgeY-(H-zone))/5);else if(edgeY<zone)d=-Math.ceil((zone-edgeY)/5);
    if(d){window.scrollBy(0,d);edgeLoop=requestAnimationFrame(edgeScroll);}};
  el.addEventListener("pointerdown",e=>{if(el.disabled||el.classList.contains("used")||el.classList.contains("ok"))return;const sx=e.clientX,sy=e.clientY;let ghost=null,over=null,lx=sx,ly=sy,lt=performance.now(),vx=0,vy=0;
    const move=ev=>{const now=performance.now(),dt=Math.max(8,now-lt);vx=(ev.clientX-lx)/dt*16;vy=(ev.clientY-ly)/dt*16;lx=ev.clientX;ly=ev.clientY;lt=now;if(!ghost&&Math.hypot(ev.clientX-sx,ev.clientY-sy)>6){ghost=el.cloneNode(true);ghost.classList.add("drag-ghost");ghost.classList.remove("lifted");ghost.style.width=el.getBoundingClientRect().width+"px";document.body.appendChild(ghost);
        if(opts.keep)ghost.style.opacity="0";else el.classList.add("lifted");   /* keep: you draw FROM it (a stem from a seed), you do not pick it up */
        if(opts.start)opts.start();}
      if(!ghost)return;ev.preventDefault();ghost.style.left=ev.clientX+"px";ghost.style.top=ev.clientY+"px";if(opts.move)opts.move(ev);
      edgeY=ev.clientY;if(!edgeLoop)edgeLoop=requestAnimationFrame(edgeScroll);
      const t=(document.elementFromPoint(ev.clientX,ev.clientY)||{closest:()=>null}).closest("[data-drop]");if(over&&over!==t)over.classList.remove("over");if(t){t.classList.add("over");over=t;}else over=null;};
    const up=ev=>{window.removeEventListener("pointermove",move);window.removeEventListener("pointerup",up);edgeY=null;if(over)over.classList.remove("over");
      if(ghost){el.dataset.dragged="1";setTimeout(()=>delete el.dataset.dragged,60);const t=(document.elementFromPoint(ev.clientX,ev.clientY)||{closest:()=>null}).closest("[data-drop]");if(opts.end)opts.end();
        el.classList.remove("lifted");
        if(t){if(opts.keep)ghost.remove();else snap(ghost,t);onDrop(t);}else if(opts.fly!==false&&!reduce){fly(ghost,el,vx,vy);}else ghost.remove();}};
    window.addEventListener("pointermove",move,{passive:false});window.addEventListener("pointerup",up);});}
const tapped=el=>!el.dataset.dragged;
/* dropped on its place: it flies the last few pixels into it and settles (instead of vanishing) */
function snap(ghost,target){const r=target.getBoundingClientRect();ghost.style.transition="left .16s ease-out,top .16s ease-out,transform .16s ease-out,opacity .16s";
  ghost.style.left=(r.left+r.width/2)+"px";ghost.style.top=(r.top+r.height*0.6)+"px";ghost.style.transform="translate(-50%,-60%) scale(.85)";ghost.style.opacity=".2";setTimeout(()=>ghost.remove(),170);}
/* let go in the air: the card flies, tumbles and bounces around the page, then floats back home */
function fly(ghost,home,vx,vy){home.style.visibility="hidden";
  const kind=home.dataset.throw||(Math.random()<0.5?"ground":"space");
  return kind==="ground"?dropToGround(ghost,home,vx,vy):floatInSpace(ghost,home,vx,vy);}
/* light things: no gravity — they drift, spin slowly and bounce softly off the edges, like in space; catch them in the air */
function floatInSpace(ghost,home,vx,vy){sfx("whoosh");let x=parseFloat(ghost.style.left),y=parseFloat(ghost.style.top),rot=0,t=0,caught=false;
  const sp=Math.hypot(vx||0,vy||0);if(sp<3){const a=Math.random()*Math.PI*2;vx=Math.cos(a)*4;vy=Math.sin(a)*4;}
  const spin=(Math.random()<.5?-1:1)*(2+Math.random()*2);const W=window.innerWidth,H=window.innerHeight;
  ghost.style.transition="none";ghost.classList.add("floating");ghost.style.pointerEvents="auto";ghost.title="امسكني!";
  ghost.addEventListener("pointerdown",e=>{if(caught)return;caught=true;e.preventDefault();ghost.remove();home.style.visibility="";sfx("pop");
    home.dispatchEvent(new PointerEvent("pointerdown",{clientX:e.clientX,clientY:e.clientY,pointerId:e.pointerId,bubbles:true}));},{once:true});
  const step=()=>{if(caught||!ghost.isConnected)return;t++;vx*=0.996;vy*=0.996;x+=vx;y+=vy+Math.sin(t/25)*0.4;rot+=spin;
    if(x<40||x>W-40){vx=-vx;x=Math.max(40,Math.min(W-40,x));}if(y<40||y>H-40){vy=-vy;y=Math.max(40,Math.min(H-40,y));}
    ghost.style.left=x+"px";ghost.style.top=y+"px";ghost.style.transform=`translate(-50%,-60%) rotate(${rot}deg)`;
    if(t<330)requestAnimationFrame(step);else{ghost.classList.remove("floating");ghost.style.pointerEvents="none";goHome(ghost,home);}};
  step();}
function goHome(ghost,home,shadow){if(!ghost.isConnected){if(shadow)shadow.remove();return;}const r=home.getBoundingClientRect();ghost.style.transition="left .6s ease,top .6s ease,transform .6s ease";ghost.style.left=(r.left+r.width/2)+"px";ghost.style.top=(r.top+r.height*0.6)+"px";ghost.style.transform="translate(-50%,-60%) rotate(0deg)";
  if(shadow)shadow.remove();setTimeout(()=>{ghost.remove();home.style.visibility="";},620);}
/* heavy things: they fall to the ground with their shadow; pick them up again, or they go home by themselves after 10 seconds */
function dropToGround(ghost,home,vx){let x=parseFloat(ghost.style.left),y=parseFloat(ghost.style.top),vy=0,bounces=0;vx=(vx||0)*0.5;const H=window.innerHeight,W=window.innerWidth,floor=H-34;
  ghost.style.transition="none";const shadow=document.createElement("div");shadow.className="ground-shadow";document.body.appendChild(shadow);
  const step=()=>{if(!ghost.isConnected){shadow.remove();return;}vy+=0.9;x+=vx;y+=vy;if(x<30||x>W-30){vx=-vx;x=Math.max(30,Math.min(W-30,x));}
    if(y>=floor){y=floor;if(Math.abs(vy)>4&&bounces<2){vy=-vy*0.38;bounces++;sfx("thud");}else{vy=0;}}
    const h=Math.max(0,floor-y);shadow.style.left=x+"px";shadow.style.top=(floor+18)+"px";shadow.style.transform=`translate(-50%,0) scale(${Math.max(.4,1-h/300)})`;shadow.style.opacity=Math.max(.15,.55-h/600);
    ghost.style.left=x+"px";ghost.style.top=y+"px";ghost.style.transform="translate(-50%,-60%) rotate("+(vx*3)+"deg)";
    if(vy!==0||y<floor)requestAnimationFrame(step);else rest();};
  const rest=()=>{ghost.classList.add("resting");ghost.style.pointerEvents="auto";ghost.title="التقطني!";
    const home7=setTimeout(()=>{ghost.classList.remove("resting");ghost.style.pointerEvents="none";goHome(ghost,home,shadow);},10000);   /* 10 seconds on the ground */
    ghost.addEventListener("pointerdown",e=>{clearTimeout(home7);e.preventDefault();ghost.remove();shadow.remove();home.style.visibility="";sfx("pop");
      home.dispatchEvent(new PointerEvent("pointerdown",{clientX:e.clientX,clientY:e.clientY,pointerId:e.pointerId,bubbles:true}));},{once:true});};
  step();}
/* ===== drawn art (SVG) instead of emoji: the same on every phone and computer ===== */
const OL='stroke="#3b2a1a" stroke-width="2.6" stroke-linejoin="round" stroke-linecap="round"';
/* one face for everybody: eyes that blink and follow you, cheeks, brows and a mouth for each mood */
function faceSVG(x,y,s){return `<g class="sface" transform="translate(${x} ${y}) scale(${s})">
 <g class="brows"><path class="brow bl" d="M-17 -18 L-5 -16" ${OL} fill="none"/><path class="brow br" d="M17 -18 L5 -16" ${OL} fill="none"/></g>
 <g transform="translate(-10 -6)"><g class="seye"><ellipse rx="6.6" ry="7.6" fill="#fff" ${OL}/><g class="spupil"><circle r="3.5" fill="#2a1d12"/><circle cx="1.3" cy="-1.5" r="1.25" fill="#fff"/></g></g></g>
 <g transform="translate(10 -6)"><g class="seye"><ellipse rx="6.6" ry="7.6" fill="#fff" ${OL}/><g class="spupil"><circle r="3.5" fill="#2a1d12"/><circle cx="1.3" cy="-1.5" r="1.25" fill="#fff"/></g></g></g>
 <g class="scheek"><ellipse cx="-16" cy="6" rx="4.4" ry="2.6" fill="#F28AA8" opacity=".6"/><ellipse cx="16" cy="6" rx="4.4" ry="2.6" fill="#F28AA8" opacity=".6"/></g>
 <path class="m m-happy" d="M-6.5 6 Q0 13.5 6.5 6" ${OL} fill="none"/>
 <path class="m m-laugh" d="M-7.5 5 Q0 17 7.5 5 Z" ${OL} fill="#C9474E"/>
 <path class="m m-sad" d="M-6 11 Q0 4.5 6 11" ${OL} fill="none"/>
 <path class="m m-angry" d="M-5.5 9 L5.5 9" ${OL} fill="none"/>
 <ellipse class="m m-o" cx="0" cy="9" rx="3.4" ry="4" ${OL} fill="#C9474E"/>
 <path class="ejoy" d="M-16 -5 Q-10 -13 -4 -5 M4 -5 Q10 -13 16 -5" stroke="#3b2a1a" stroke-width="2.8" fill="none" stroke-linecap="round"/>
 <rect class="snose" x="-2" y="-1" width="9" height="6" rx="3" fill="#F2A07B" ${OL}/>
</g>`;}
const ARTS={
 water:()=>`<path d="M50 8 C50 8 22 44 22 64 C22 81 35 93 50 93 C65 93 78 81 78 64 C78 44 50 8 50 8Z" fill="#7CC6F2" ${OL}/><path d="M35 48 C31 57 31 64 34 70" stroke="#fff" stroke-width="4" fill="none" stroke-linecap="round" opacity=".75"/>${faceSVG(50,66,.95)}`,
 sun:()=>`<g class="rays">${[0,45,90,135,180,225,270,315].map(a=>`<path transform="rotate(${a} 50 50)" d="M50 4 L56 18 L44 18Z" fill="#F6B73C" ${OL}/>`).join("")}</g><circle cx="50" cy="50" r="27" fill="#FFD25A" ${OL}/>${faceSVG(50,52,.95)}`,
 leaf:()=>`<path d="M50 6 C20 22 14 66 50 94 C86 66 80 22 50 6Z" fill="#6CC27A" ${OL}/><path d="M50 14 L50 88 M50 34 L36 24 M50 34 L64 24 M50 52 L34 42 M50 52 L66 42" stroke="#3E8E4C" stroke-width="2.4" fill="none" stroke-linecap="round"/>${faceSVG(50,64,.82)}`,
 root:()=>`<path d="M30 74 C26 84 20 90 12 94 M42 78 C41 88 38 94 34 98 M58 78 C59 88 62 94 66 98 M70 74 C74 84 80 90 88 94" stroke="#B07A4A" stroke-width="5" fill="none" stroke-linecap="round"/><path d="M18 30 C18 10 82 10 82 30 L76 74 C62 84 38 84 24 74Z" fill="#C98A55" ${OL}/><path d="M34 24 L38 36 M66 22 L62 34" stroke="#9C6538" stroke-width="2.4" fill="none" stroke-linecap="round"/>${faceSVG(50,50,.95)}`,
 stem:()=>`<path d="M40 96 L40 24 C40 14 60 14 60 24 L60 96Z" fill="#5DB36B" ${OL}/><path d="M60 40 C76 30 88 36 90 46 C78 52 68 48 60 44Z" fill="#7DD08A" ${OL}/><path d="M40 62 C24 52 12 58 10 68 C22 74 32 70 40 66Z" fill="#7DD08A" ${OL}/>${faceSVG(50,46,.72)}`,
 flower:()=>`${[0,72,144,216,288].map(a=>`<ellipse transform="rotate(${a} 50 50)" cx="50" cy="22" rx="15" ry="20" fill="#F59BB8" ${OL}/>`).join("")}<circle cx="50" cy="50" r="22" fill="#FFD25A" ${OL}/>${faceSVG(50,52,.78)}`,
 bud:(c)=>`<path d="M50 96 L50 66" stroke="#3E8E4C" stroke-width="4" stroke-linecap="round"/><path d="M50 70 C26 70 22 40 30 22 C38 34 44 30 50 12 C56 30 62 34 70 22 C78 40 74 70 50 70Z" fill="${c||"#F59BB8"}" ${OL}/>${faceSVG(50,48,.72)}`,
 fruit:()=>`<path d="M50 24 C40 14 14 18 14 48 C14 76 34 94 50 88 C66 94 86 76 86 48 C86 18 60 14 50 24Z" fill="#E8574A" ${OL}/><path d="M50 24 C50 16 52 10 56 6" stroke="#6B4423" stroke-width="3.2" fill="none" stroke-linecap="round"/><path d="M56 12 C66 4 78 8 80 14 C70 20 62 18 56 12Z" fill="#6CC27A" ${OL}/><path d="M28 40 C26 48 27 54 30 58" stroke="#fff" stroke-width="4" fill="none" stroke-linecap="round" opacity=".6"/>${faceSVG(50,56,.92)}`,
 seed:()=>`<path d="M50 10 C78 14 88 46 80 70 C72 90 28 90 20 70 C12 46 22 14 50 10Z" fill="#B9834F" ${OL}/><path d="M50 16 C44 30 44 44 50 54" stroke="#8A5A2E" stroke-width="2.4" fill="none" stroke-linecap="round"/>${faceSVG(50,62,.9)}`,
 soil:()=>`<path d="M6 86 C10 50 34 34 50 34 C66 34 90 50 94 86Z" fill="#9B6B43" ${OL}/><circle cx="26" cy="74" r="3" fill="#7A5232"/><circle cx="74" cy="76" r="3.5" fill="#7A5232"/><circle cx="62" cy="46" r="2.4" fill="#7A5232"/><path d="M50 34 L50 20 M50 26 C44 18 38 20 36 24 C42 28 48 26 50 26 M50 22 C56 14 62 16 64 20 C58 24 52 22 50 22" stroke="#4E9E5A" stroke-width="2.6" fill="#6CC27A" stroke-linecap="round"/>${faceSVG(50,64,.9)}`,
 air:()=>`<path d="M22 70 C8 70 6 50 20 46 C18 30 38 22 48 32 C54 20 76 22 78 38 C94 38 96 62 80 66 C78 74 68 76 62 72 C56 80 40 80 34 72 C30 74 24 74 22 70Z" fill="#E6F4FB" ${OL}/><path d="M8 84 L36 84 M52 88 L90 88 M2 92 L22 92" stroke="#8EC9E8" stroke-width="3" fill="none" stroke-linecap="round"/>${faceSVG(50,54,.9)}`,
 sprout:()=>`<path d="M50 56 L50 26" stroke="#3E8E4C" stroke-width="4" stroke-linecap="round"/><path d="M50 34 C36 18 20 22 18 32 C30 40 44 38 50 34Z" fill="#7DD08A" ${OL}/><path d="M50 30 C62 14 80 16 82 26 C70 34 56 34 50 30Z" fill="#7DD08A" ${OL}/><path d="M50 50 C74 52 84 70 76 84 C68 96 32 96 24 84 C16 70 26 52 50 50Z" fill="#B9834F" ${OL}/>${faceSVG(50,74,.75)}`,
 bee:()=>`<ellipse cx="34" cy="30" rx="16" ry="12" fill="#E6F4FB" ${OL} opacity=".95"/><ellipse cx="66" cy="30" rx="16" ry="12" fill="#E6F4FB" ${OL} opacity=".95"/><ellipse cx="50" cy="60" rx="34" ry="28" fill="#FFD25A" ${OL}/><path d="M28 44 C26 54 26 66 28 76 M50 34 L50 34 M72 44 C74 54 74 66 72 76" stroke="#3b2a1a" stroke-width="6" fill="none" stroke-linecap="round"/><path d="M42 30 C38 20 34 16 30 16 M58 30 C62 20 66 16 70 16" stroke="#3b2a1a" stroke-width="2.4" fill="none" stroke-linecap="round"/>${faceSVG(50,62,.82)}`,
 dandelion:()=>`<path d="M50 96 L50 58" stroke="#5DB36B" stroke-width="4" stroke-linecap="round"/>${Array.from({length:12},(_,i)=>`<path transform="rotate(${i*30} 50 42)" d="M50 42 L50 8" stroke="#C9D6DE" stroke-width="2" stroke-linecap="round"/><circle transform="rotate(${i*30} 50 42)" cx="50" cy="8" r="3.4" fill="#fff" stroke="#C9D6DE"/>`).join("")}<circle cx="50" cy="42" r="22" fill="#F4F7F9" ${OL}/>${faceSVG(50,44,.75)}`,
 sunflower:()=>`<path d="M50 96 L50 64" stroke="#3E8E4C" stroke-width="4" stroke-linecap="round"/>${Array.from({length:10},(_,i)=>`<ellipse transform="rotate(${i*36} 50 40)" cx="50" cy="16" rx="8" ry="14" fill="#F6B73C" ${OL}/>`).join("")}<circle cx="50" cy="40" r="18" fill="#8A5A2E" ${OL}/>${faceSVG(50,42,.62)}`,
 pot:()=>`<path d="M50 54 L50 26" stroke="#3E8E4C" stroke-width="4" stroke-linecap="round"/><path d="M50 36 C36 22 22 26 20 34 C32 42 44 40 50 36Z M50 32 C62 18 78 20 80 28 C68 36 56 36 50 32Z" fill="#7DD08A" ${OL}/><path d="M20 54 L80 54 L72 94 L28 94Z" fill="#D9774B" ${OL}/><path d="M16 50 L84 50 L84 60 L16 60Z" fill="#E88A5E" ${OL}/>${faceSVG(50,76,.75)}`,
 tree:()=>`<path d="M44 96 L44 64 L56 64 L56 96Z" fill="#9B6B43" ${OL}/><circle cx="50" cy="40" r="30" fill="#5DB36B" ${OL}/><circle cx="30" cy="54" r="14" fill="#6CC27A" ${OL}/><circle cx="70" cy="54" r="14" fill="#6CC27A" ${OL}/>${faceSVG(50,44,.8)}`,
 house:()=>`<path d="M14 48 L50 16 L86 48Z" fill="#E8574A" ${OL}/><path d="M22 46 L78 46 L78 92 L22 92Z" fill="#F6E3C6" ${OL}/><path d="M44 92 L44 70 L56 70 L56 92Z" fill="#9B6B43" ${OL}/>${faceSVG(50,60,.7)}`,
 fox:()=>`<path d="M18 18 L34 44 L22 50Z M82 18 L66 44 L78 50Z" fill="#E8853C" ${OL}/><path d="M50 92 C22 92 14 60 22 44 C30 30 70 30 78 44 C86 60 78 92 50 92Z" fill="#E8853C" ${OL}/><path d="M50 92 C38 92 32 80 34 70 L66 70 C68 80 62 92 50 92Z" fill="#fff" ${OL}/><circle cx="50" cy="74" r="4" fill="#3b2a1a"/>${faceSVG(50,58,.85)}`,
 owl:()=>`<path d="M20 30 L30 14 L40 28 M80 30 L70 14 L60 28" fill="#9B6B43" ${OL}/><path d="M50 96 C20 96 16 66 20 46 C24 26 76 26 80 46 C84 66 80 96 50 96Z" fill="#9B6B43" ${OL}/><ellipse cx="50" cy="74" rx="18" ry="16" fill="#E6CFA8" ${OL}/><path d="M46 56 L50 64 L54 56Z" fill="#F6B73C" ${OL}/>${faceSVG(50,48,.95)}`,
 train:()=>`<path d="M12 84 L12 44 L52 44 L52 26 L78 26 L78 84Z" fill="#E8574A" ${OL}/><path d="M60 26 L60 14 L72 14 L72 26" fill="#3b2a1a"/><circle cx="28" cy="88" r="9" fill="#3b2a1a"/><circle cx="64" cy="88" r="9" fill="#3b2a1a"/>${faceSVG(32,62,.72)}`,
 sign:()=>`<path d="M46 96 L46 30 L54 30 L54 96Z" fill="#9B6B43" ${OL}/><path d="M14 18 L76 18 L90 32 L76 46 L14 46Z" fill="#E6CFA8" ${OL}/>${faceSVG(46,34,.55)}`,
 mystery:()=>`<path d="M50 10 C78 10 90 32 88 54 C86 80 70 92 50 92 C30 92 14 80 12 54 C10 32 22 10 50 10Z" fill="#B9A2F0" ${OL}/><path d="M14 40 C30 32 70 32 86 40 L84 56 C70 50 30 50 16 56Z" fill="#3b2a1a"/>${faceSVG(50,52,1)}<text x="50" y="30" text-anchor="middle" font-size="22" font-weight="700" fill="#3b2a1a">?</text>`,
 blob:(c)=>`<path d="M50 10 C78 10 90 32 88 54 C86 80 70 92 50 92 C30 92 14 80 12 54 C10 32 22 10 50 10Z" fill="${c||"#9CCFD8"}" ${OL}/>${faceSVG(50,52,1)}`
};
const ART_OF={"💧":["water"],"☀️":["sun"],"🍃":["leaf"],"🫚":["root"],"🌿":["stem"],"🌸":["flower"],"🍎":["fruit"],"🌰":["seed"],"🟫":["soil"],"💨":["air"],"🌱":["sprout"],
  "🐝":["bee"],"🌬️":["dandelion"],"🌻":["sunflower"],"🌷":["bud","#F59BB8"],"🪷":["bud","#F7B2C9"],"🌼":["bud","#FFD25A"],"🪻":["bud","#B9A2F0"],"🪴":["pot"],"🌳":["tree"],"🏡":["house"],
  "🦊":["fox"],"🦉":["owl"],"🚂":["train"],"🪧":["sign"],"🙂":["blob"],"😄":["blob","#FFD25A"],"🎭":["mystery"]};
/* ===== subject art: the same style and face for maths, physics, chemistry, geography, history, language ===== */
Object.assign(ARTS,{
 plus:()=>`<path d="M38 10 H62 V38 H90 V62 H62 V90 H38 V62 H10 V38 H38Z" fill="#6CC27A" ${OL}/>${faceSVG(50,52,.75)}`,
 minus:()=>`<rect x="8" y="34" width="84" height="34" rx="12" fill="#F28AA8" ${OL}/>${faceSVG(50,52,.75)}`,
 times:()=>`<path d="M26 10 L50 34 L74 10 L90 26 L66 50 L90 74 L74 90 L50 66 L26 90 L10 74 L34 50 L10 26Z" fill="#7CC6F2" ${OL}/>${faceSVG(50,52,.62)}`,
 divide:()=>`<circle cx="50" cy="14" r="9" fill="#B9A2F0" ${OL}/><circle cx="50" cy="88" r="9" fill="#B9A2F0" ${OL}/><rect x="8" y="36" width="84" height="30" rx="12" fill="#B9A2F0" ${OL}/>${faceSVG(50,52,.7)}`,
 numbers:()=>`<rect x="10" y="16" width="80" height="70" rx="16" fill="#FFD25A" ${OL}/><text x="50" y="40" text-anchor="middle" font-size="20" font-weight="800" fill="#3b2a1a">123</text>${faceSVG(50,64,.75)}`,
 pie:()=>`<circle cx="50" cy="52" r="40" fill="#F6C177" ${OL}/><path d="M50 52 L50 12 A40 40 0 0 1 90 52Z" fill="#fff" ${OL} opacity=".9"/><path d="M50 52 L10 52 M50 52 L50 92" stroke="#3b2a1a" stroke-width="2.4"/><circle cx="30" cy="34" r="3.5" fill="#E8574A"/><circle cx="28" cy="72" r="3.5" fill="#E8574A"/><circle cx="66" cy="74" r="3.5" fill="#E8574A"/>${faceSVG(40,58,.62)}`,
 fracTop:()=>`<rect x="18" y="6" width="64" height="38" rx="10" fill="#FFD25A" ${OL}/><rect x="10" y="49" width="80" height="6" rx="3" fill="#3b2a1a"/><rect x="18" y="60" width="64" height="34" rx="10" fill="#E6CFA8" ${OL} opacity=".55"/><text x="50" y="86" text-anchor="middle" font-size="20" font-weight="800" fill="#3b2a1a" opacity=".5">8</text>${faceSVG(50,27,.62)}`,
 fracBottom:()=>`<rect x="18" y="6" width="64" height="34" rx="10" fill="#E6CFA8" ${OL} opacity=".55"/><text x="50" y="31" text-anchor="middle" font-size="20" font-weight="800" fill="#3b2a1a" opacity=".5">3</text><rect x="10" y="45" width="80" height="6" rx="3" fill="#3b2a1a"/><rect x="18" y="56" width="64" height="38" rx="10" fill="#7CC6F2" ${OL}/>${faceSVG(50,77,.62)}`,
 equals:()=>`<rect x="8" y="18" width="84" height="26" rx="12" fill="#6CC27A" ${OL}/><rect x="8" y="58" width="84" height="26" rx="12" fill="#6CC27A" ${OL}/>${faceSVG(50,31,.6)}`,
 scale:()=>`<path d="M50 18 L50 82 M30 92 L70 92" stroke="#9B6B43" stroke-width="6" stroke-linecap="round"/><path d="M14 30 L86 22" stroke="#3b2a1a" stroke-width="4" stroke-linecap="round"/><path d="M4 52 Q14 64 26 52Z M74 44 Q84 56 96 44Z" fill="#FFD25A" ${OL}/><path d="M14 30 L4 52 M14 30 L26 52 M86 22 L74 44 M86 22 L96 44" stroke="#3b2a1a" stroke-width="1.6"/><circle cx="50" cy="56" r="18" fill="#F6C177" ${OL}/>${faceSVG(50,58,.55)}`,
 triangle:()=>`<path d="M50 8 L94 88 L6 88Z" fill="#F28AA8" ${OL}/>${faceSVG(50,64,.75)}`,
 square:()=>`<rect x="12" y="12" width="76" height="76" rx="8" fill="#7CC6F2" ${OL}/>${faceSVG(50,52,.85)}`,
 circle:()=>`<circle cx="50" cy="50" r="40" fill="#FFD25A" ${OL}/>${faceSVG(50,52,.95)}`,
 ruler:()=>`<rect x="6" y="30" width="88" height="40" rx="6" fill="#FFD25A" ${OL}/>${[16,26,36,46,56,66,76,86].map((x,i)=>`<path d="M${x} 30 V${i%2?40:46}" stroke="#3b2a1a" stroke-width="2"/>`).join("")}${faceSVG(50,58,.55)}`,
 magnet:()=>`<path d="M14 14 H38 V58 C38 66 44 72 50 72 C56 72 62 66 62 58 V14 H86 V58 C86 80 70 94 50 94 C30 94 14 80 14 58Z" fill="#E8574A" ${OL}/><path d="M14 14 H38 V30 H14Z M62 14 H86 V30 H62Z" fill="#E6F4FB" ${OL}/>${faceSVG(50,82,.42)}`,
 bolt:()=>`<path d="M58 4 L18 56 H46 L38 96 L84 38 H54Z" fill="#FFD25A" ${OL}/>${faceSVG(48,50,.6)}`,
 arrow:()=>`<path d="M6 36 H56 V14 L96 50 L56 86 V64 H6Z" fill="#7CC6F2" ${OL}/>${faceSVG(38,50,.62)}`,
 atom:()=>`<ellipse cx="50" cy="50" rx="44" ry="16" fill="none" stroke="#7CC6F2" stroke-width="3"/><ellipse cx="50" cy="50" rx="44" ry="16" fill="none" stroke="#7CC6F2" stroke-width="3" transform="rotate(60 50 50)"/><ellipse cx="50" cy="50" rx="44" ry="16" fill="none" stroke="#7CC6F2" stroke-width="3" transform="rotate(-60 50 50)"/><circle cx="50" cy="50" r="22" fill="#F28AA8" ${OL}/>${faceSVG(50,52,.62)}`,
 tube:()=>`<path d="M34 6 H66 M38 6 V70 C38 84 44 94 50 94 C56 94 62 84 62 70 V6" fill="#E6F4FB" ${OL}/><path d="M38 48 H62 V70 C62 84 56 92 50 92 C44 92 38 84 38 70Z" fill="#6CC27A" ${OL}/><circle cx="46" cy="60" r="3" fill="#fff"/><circle cx="54" cy="74" r="2.4" fill="#fff"/>${faceSVG(50,30,.5)}`,
 earth:()=>`<circle cx="50" cy="50" r="42" fill="#7CC6F2" ${OL}/><path d="M24 28 C34 22 42 30 38 40 C34 48 22 46 18 40Z M56 18 C70 18 78 30 72 38 C66 44 56 36 56 28Z M60 62 C72 58 82 66 76 78 C70 86 58 80 60 62Z" fill="#6CC27A" ${OL}/>${faceSVG(46,56,.8)}`,
 map:()=>`<path d="M8 18 L36 8 L64 18 L92 8 V82 L64 92 L36 82 L8 92Z" fill="#F6E3C6" ${OL}/><path d="M36 8 V82 M64 18 V92" stroke="#3b2a1a" stroke-width="2" opacity=".5"/><path d="M18 30 C30 40 46 30 58 44" stroke="#E8574A" stroke-width="3" stroke-dasharray="4 4" fill="none"/>${faceSVG(50,58,.7)}`,
 mountain:()=>`<path d="M4 90 L38 26 L54 52 L66 36 L96 90Z" fill="#9B6B43" ${OL}/><path d="M30 42 L38 26 L46 42 L40 38 L36 44Z" fill="#fff" ${OL}/>${faceSVG(46,70,.7)}`,
 scroll:()=>`<rect x="18" y="16" width="64" height="68" rx="6" fill="#F6E3C6" ${OL}/><rect x="10" y="8" width="80" height="14" rx="7" fill="#E6CFA8" ${OL}/><rect x="10" y="78" width="80" height="14" rx="7" fill="#E6CFA8" ${OL}/><path d="M28 32 H72 M28 40 H64" stroke="#9B6B43" stroke-width="2.4" stroke-linecap="round"/>${faceSVG(50,60,.62)}`,
 columns:()=>`<path d="M8 30 L50 8 L92 30Z" fill="#E6CFA8" ${OL}/><rect x="10" y="84" width="80" height="10" fill="#E6CFA8" ${OL}/>${[18,38,58,78].map(x=>`<rect x="${x-5}" y="32" width="10" height="52" fill="#F6E3C6" ${OL}/>`).join("")}${faceSVG(50,22,.45)}`,
 letters:()=>`<rect x="10" y="14" width="80" height="72" rx="14" fill="#B9A2F0" ${OL}/><text x="50" y="44" text-anchor="middle" font-size="22" font-weight="800" fill="#3b2a1a">أ ب</text>${faceSVG(50,64,.7)}`,
 book:()=>`<path d="M50 20 C38 12 22 12 8 16 V84 C22 80 38 80 50 88 C62 80 78 80 92 84 V16 C78 12 62 12 50 20Z" fill="#7CC6F2" ${OL}/><path d="M50 20 V88" stroke="#3b2a1a" stroke-width="2.4"/>${faceSVG(50,48,.62)}`,
 clock:()=>`<circle cx="50" cy="54" r="40" fill="#F6E3C6" ${OL}/><path d="M30 12 L20 22 M70 12 L80 22" stroke="#3b2a1a" stroke-width="5" stroke-linecap="round"/><path d="M50 30 V38 M74 54 H66 M50 78 V70 M26 54 H34" stroke="#3b2a1a" stroke-width="2.4"/>${faceSVG(50,58,.7)}`,
 coins:()=>`<ellipse cx="38" cy="74" rx="28" ry="12" fill="#F6B73C" ${OL}/><ellipse cx="38" cy="64" rx="28" ry="12" fill="#F6B73C" ${OL}/><circle cx="62" cy="44" r="30" fill="#FFD25A" ${OL}/>${faceSVG(62,46,.7)}`
});
Object.assign(ART_OF,{"➕":["plus"],"➖":["minus"],"✖️":["times"],"➗":["divide"],"🔢":["numbers"],"🍕":["pie"],"🔼":["fracTop"],"🔽":["fracBottom"],"🟰":["equals"],"⚖️":["scale"],
  "🔺":["triangle"],"⏹️":["square"],"⚪":["circle"],"📏":["ruler"],"🧲":["magnet"],"⚡":["bolt"],"➡️":["arrow"],"⚛️":["atom"],"🧪":["tube"],"🌍":["earth"],"🗺️":["map"],"⛰️":["mountain"],
  "📜":["scroll"],"🏛️":["columns"],"🔤":["letters"],"📖":["book"],"⏰":["clock"],"💰":["coins"]});

/* ===== more subject art (the factory may ask for these) + each subject's own character with the concept's name ===== */
Object.assign(ARTS,{
 angle:()=>`<path d="M14 88 L86 88 M14 88 L72 22" stroke="#3b2a1a" stroke-width="7" stroke-linecap="round"/><path d="M40 88 A26 26 0 0 0 32 68" fill="none" stroke="#E8574A" stroke-width="4"/><circle cx="62" cy="62" r="20" fill="#F6C177" ${OL}/>${faceSVG(62,64,.55)}`,
 percent:()=>`<circle cx="26" cy="26" r="14" fill="#7CC6F2" ${OL}/><circle cx="74" cy="74" r="14" fill="#7CC6F2" ${OL}/><path d="M78 14 L22 86" stroke="#3b2a1a" stroke-width="8" stroke-linecap="round"/>${faceSVG(74,76,.45)}`,
 dice:()=>`<rect x="12" y="12" width="76" height="76" rx="16" fill="#fff" ${OL}/><circle cx="30" cy="30" r="6" fill="#3b2a1a"/><circle cx="70" cy="30" r="6" fill="#3b2a1a"/><circle cx="30" cy="74" r="6" fill="#3b2a1a"/><circle cx="70" cy="74" r="6" fill="#3b2a1a"/>${faceSVG(50,56,.6)}`,
 bars:()=>`<path d="M8 92 H92" stroke="#3b2a1a" stroke-width="3"/><rect x="14" y="52" width="18" height="40" fill="#7CC6F2" ${OL}/><rect x="41" y="22" width="18" height="70" fill="#6CC27A" ${OL}/><rect x="68" y="40" width="18" height="52" fill="#F28AA8" ${OL}/>${faceSVG(50,50,.45)}`,
 ring:()=>`<circle cx="50" cy="50" r="38" fill="none" stroke="#E8574A" stroke-width="10"/><circle cx="50" cy="50" r="24" fill="#FFD25A" ${OL}/>${faceSVG(50,52,.55)}`,
 cube:()=>`<path d="M50 8 L90 28 L90 72 L50 92 L10 72 L10 28Z" fill="#7CC6F2" ${OL}/><path d="M10 28 L50 48 L90 28 M50 48 L50 92" stroke="#3b2a1a" stroke-width="2.6" fill="none"/><path d="M50 48 L90 28 L90 72 L50 92Z" fill="#5FAFDD" opacity=".6"/>${faceSVG(30,62,.5)}`,
 cycle:()=>`<path d="M50 14 A36 36 0 1 1 18 66" fill="none" stroke="#6CC27A" stroke-width="10" stroke-linecap="round"/><path d="M8 58 L18 74 L30 60Z" fill="#6CC27A" ${OL}/><circle cx="50" cy="50" r="20" fill="#FFD25A" ${OL}/>${faceSVG(50,52,.5)}`,
 butterfly:()=>`<path d="M50 50 C30 10 4 18 10 42 C14 58 36 56 50 50 C64 56 86 58 90 42 C96 18 70 10 50 50Z" fill="#F59BB8" ${OL}/><path d="M50 52 C34 62 22 82 34 88 C44 92 48 72 50 60 C52 72 56 92 66 88 C78 82 66 62 50 52Z" fill="#B9A2F0" ${OL}/><ellipse cx="50" cy="58" rx="7" ry="22" fill="#3b2a1a"/>${faceSVG(50,44,.42)}`,
 cell:()=>`<path d="M50 8 C76 8 92 26 92 48 C92 74 74 92 50 92 C24 92 8 74 8 50 C8 24 24 8 50 8Z" fill="#A3D9A5" ${OL}/><circle cx="66" cy="34" r="12" fill="#B9A2F0" ${OL}/><circle cx="28" cy="70" r="4" fill="#6CC27A"/><circle cx="74" cy="70" r="5" fill="#6CC27A"/>${faceSVG(46,58,.75)}`,
 heart:()=>`<path d="M50 90 C20 70 6 52 8 34 C10 16 32 8 50 26 C68 8 90 16 92 34 C94 52 80 70 50 90Z" fill="#E8574A" ${OL}/>${faceSVG(50,50,.8)}`,
 paw:()=>`<ellipse cx="50" cy="66" rx="26" ry="22" fill="#C98A55" ${OL}/><circle cx="22" cy="36" r="10" fill="#C98A55" ${OL}/><circle cx="40" cy="20" r="10" fill="#C98A55" ${OL}/><circle cx="60" cy="20" r="10" fill="#C98A55" ${OL}/><circle cx="78" cy="36" r="10" fill="#C98A55" ${OL}/>${faceSVG(50,68,.62)}`,
 speaker:()=>`<path d="M12 38 H32 L56 16 V84 L32 62 H12Z" fill="#7CC6F2" ${OL}/><path d="M66 34 C74 42 74 58 66 66 M76 24 C90 38 90 62 76 76" stroke="#3b2a1a" stroke-width="4" fill="none" stroke-linecap="round"/>${faceSVG(36,50,.45)}`,
 thermo:()=>`<path d="M40 14 C40 6 60 6 60 14 V62 C70 68 72 84 62 92 C54 98 40 96 36 86 C32 76 34 68 40 62Z" fill="#fff" ${OL}/><path d="M44 40 H56 V66 C64 70 66 82 58 88 C52 92 44 90 42 84 C40 76 42 70 44 66Z" fill="#E8574A"/>${faceSVG(50,78,.45)}`,
 rock:()=>`<path d="M10 78 C6 56 22 30 46 28 C62 26 86 38 92 60 C96 76 84 90 60 90 H26 C16 90 12 86 10 78Z" fill="#A8A29E" ${OL}/><path d="M30 50 L38 56 M62 44 L70 50" stroke="#78716C" stroke-width="3" stroke-linecap="round"/>${faceSVG(52,64,.8)}`,
 rain:()=>`<path d="M22 54 C8 54 6 36 20 32 C18 18 36 10 46 20 C52 8 74 10 76 26 C92 26 94 50 78 54Z" fill="#9CB4C8" ${OL}/><path d="M28 64 L22 80 M50 64 L44 80 M72 64 L66 80" stroke="#7CC6F2" stroke-width="5" stroke-linecap="round"/>${faceSVG(50,38,.7)}`,
 planet:()=>`<ellipse cx="50" cy="56" rx="46" ry="12" fill="none" stroke="#B9A2F0" stroke-width="5"/><circle cx="50" cy="50" r="30" fill="#F6C177" ${OL}/>${faceSVG(50,50,.75)}`,
 moon:()=>`<path d="M62 8 C36 12 20 34 22 56 C24 78 44 94 68 92 C50 82 42 66 42 50 C42 32 50 18 62 8Z" fill="#FFD25A" ${OL}/>${faceSVG(34,54,.55)}`,
 star:()=>`<path d="M50 6 L62 36 L94 38 L68 58 L78 90 L50 72 L22 90 L32 58 L6 38 L38 36Z" fill="#FFD25A" ${OL}/>${faceSVG(50,52,.65)}`,
 /* a subject's own character, with the concept's name written on it (when no picture fits) */
 subject:(emblem,label)=>{const S={"🧮":["#F6C177","#E8853C"],"🔬":["#A3D9A5","#4E9E5A"],"🔭":["#9CCFD8","#3E7FA8"],"⚗️":["#C4A7E7","#7A45B8"],"🧭":["#7CC6F2","#2F6FA8"],"📜":["#F6E3C6","#9B6B43"],"📖":["#B9A2F0","#5B3FA0"],"🔹":["#9CCFD8","#3E7FA8"]}[emblem]||["#9CCFD8","#3E7FA8"];
   const t=String(label||"").replace(/[<&>"]/g,"");const fs=t.length>7?11:t.length>5?13:15;
   return `<path d="M50 6 C80 6 94 28 92 54 C90 80 72 94 50 94 C28 94 10 80 8 54 C6 28 20 6 50 6Z" fill="${S[0]}" ${OL}/><rect x="16" y="14" width="68" height="22" rx="11" fill="#fff" stroke="${S[1]}" stroke-width="2.4"/><text x="50" y="30" text-anchor="middle" font-size="${fs}" font-weight="800" fill="${S[1]}" font-family="sans-serif">${t}</text>${faceSVG(50,62,.85)}`;}
});
Object.assign(ART_OF,{"📐":["angle"],"💯":["percent"],"🎲":["dice"],"📊":["bars"],"⭕":["ring"],"🧊":["cube"],"🔁":["cycle"],"🦋":["butterfly"],"🦠":["cell"],"❤️":["heart"],
  "🐾":["paw"],"🔊":["speaker"],"🌡️":["thermo"],"🪨":["rock"],"🌧️":["rain"],"🪐":["planet"],"🌙":["moon"],"⭐":["star"]});

/* every subject has its own skin: the whole page becomes that subject (mascot, progress, map, finished mark) */
ARTS.tower=(n)=>{n=Math.max(1,Math.min(5,n||1));const cols=["#F28AA8","#7CC6F2","#FFD25A","#6CC27A","#B9A2F0"];let out="";
  for(let i=0;i<n;i++){const y=88-(i+1)*16;out+=`<rect x="${26+(i%2)*4}" y="${y}" width="44" height="16" rx="3" fill="${cols[i]}" ${OL}/>`;}
  const top=88-n*16;return out+`<g transform="translate(50 ${top-12})">${faceSVG(0,0,.5)}</g>`;};
["🧱1","🧱2","🧱3","🧱4","🧱5"].forEach((k,i)=>{ART_OF[k]=["tower",i+1];});
const SKINS={
  science:{mascot:"🌱",name:"بذور",grow:["🌰","🌱","🌿","🪴","🌻"],growLabel:"نبتتك",done:"🌸",driver:"seed",places:["🏡","🌳","🌻","🪴"]},
  math:{mascot:"🔢",name:"رقّوم",grow:["🧱1","🧱2","🧱3","🧱4","🧱5"],growLabel:"برجك",done:"⭐",driver:"numbers"},
  physics:{mascot:"🧲",name:"مغنوط",grow:["🧱1","🧱2","🧱3","🧱4","🧱5"],growLabel:"برجك",done:"⭐",driver:"magnet"},
  chemistry:{mascot:"⚛️",name:"ذرّوش",grow:["🧱1","🧱2","🧱3","🧱4","🧱5"],growLabel:"برجك",done:"⭐",driver:"atom"},
  geography:{mascot:"🌍",name:"كرّوية",grow:["🧱1","🧱2","🧱3","🧱4","🧱5"],growLabel:"برجك",done:"⭐",driver:"earth"},
  history:{mascot:"📜",name:"ورّوق",grow:["🧱1","🧱2","🧱3","🧱4","🧱5"],growLabel:"برجك",done:"⭐",driver:"scroll"},
  language:{mascot:"🔤",name:"حرّوف",grow:["🧱1","🧱2","🧱3","🧱4","🧱5"],growLabel:"برجك",done:"⭐",driver:"letters"},
  general:{mascot:"🙂",name:"صاحبي",grow:["🧱1","🧱2","🧱3","🧱4","🧱5"],growLabel:"برجك",done:"⭐",driver:"blob"}};
/* a NEW subject (identity.py) has its own mascot: its emblem as a character, with its own name («بِتّو» for the computer…) */
function skinOf(g){const id=g&&g.identity;return id&&id.mascot?Object.assign({},SKINS.general,{mascot:id.mascot,name:id.mascot_name||SKINS.general.name}):(SKINS[g&&g.subject]||SKINS.general);}
function skin(){const g=(typeof graph==="function"&&graph())||{};return g.identity?skinOf(g):(SKINS[g.subject]||(garden()?SKINS.science:SKINS.general));}
/* a lesson's place on the map: the picture of its first concept (works for any subject); science keeps its garden places */
function placeOf(gi,li){const g=DATA.graphs[gi],l=g.lessons[li];const sk=skinOf(g);
  if(sk.places)return sk.places[li%sk.places.length];const c=l.concepts[0];return c?((l.icons||{})[c.concept_id]||sk.mascot):sk.mascot;}

/* ===== history: each idea its own drawing ===== */
Object.assign(ARTS,{
 pyramid:()=>`<path d="M50 8 L94 88 L6 88Z" fill="#E9C46A" ${OL}/><path d="M28 48 H72 M18 66 H82 M39 30 H61" stroke="#B8893B" stroke-width="2.4"/><path d="M50 8 L50 88" stroke="#B8893B" stroke-width="1.6" opacity=".6"/>${faceSVG(50,62,.62)}`,
 pharaoh:()=>`<path d="M22 40 C22 14 78 14 78 40 L86 84 C70 92 30 92 14 84Z" fill="#3E7FA8" ${OL}/><path d="M30 28 H70 M26 40 H74 M22 54 H78 M18 70 H82" stroke="#FFD25A" stroke-width="5"/><path d="M50 4 C58 4 62 12 56 18 L50 22 L44 18 C38 12 42 4 50 4Z" fill="#FFD25A" ${OL}/><ellipse cx="50" cy="56" rx="22" ry="24" fill="#E0A87A" ${OL}/>${faceSVG(50,58,.62)}`,
 glyphs:()=>`<rect x="14" y="8" width="72" height="84" rx="8" fill="#E9C46A" ${OL}/><path d="M24 22 h8 v8 h-8z M40 20 c6 0 6 10 0 10 M56 22 l6 8 l6 -8 M24 40 c4 -6 8 6 12 0" stroke="#7A4D2B" stroke-width="2.4" fill="none"/>${faceSVG(50,66,.62)}`,
 river:()=>`<path d="M30 4 C10 30 50 40 30 60 C14 76 36 92 50 96 L70 96 C56 90 40 76 56 62 C76 42 36 30 52 4Z" fill="#7CC6F2" ${OL}/><path d="M36 24 C30 30 34 36 40 38 M44 70 C40 74 44 80 50 82" stroke="#fff" stroke-width="3" fill="none" stroke-linecap="round"/><path d="M8 40 C16 34 20 44 14 50 M88 60 C80 54 78 66 84 70" stroke="#6CC27A" stroke-width="5" fill="none" stroke-linecap="round"/>${faceSVG(46,50,.55)}`,
 wheat:()=>`<path d="M50 96 L50 30" stroke="#B8893B" stroke-width="4"/>${[0,1,2,3].map(i=>`<ellipse cx="${42}" cy="${30+i*12}" rx="7" ry="11" fill="#E9C46A" ${OL} transform="rotate(-30 42 ${30+i*12})"/><ellipse cx="${58}" cy="${30+i*12}" rx="7" ry="11" fill="#E9C46A" ${OL} transform="rotate(30 58 ${30+i*12})"/>`).join("")}<ellipse cx="50" cy="18" rx="7" ry="12" fill="#E9C46A" ${OL}/><circle cx="50" cy="80" r="16" fill="#F6E3C6" ${OL}/>${faceSVG(50,81,.42)}`,
 boat:()=>`<path d="M50 10 L50 62 M50 14 L80 56 L50 56Z" stroke="#7A4D2B" stroke-width="3" fill="#F6E3C6"/><path d="M8 62 H92 L80 86 H20Z" fill="#9B6B43" ${OL}/><path d="M4 92 C16 86 26 98 38 92 C50 86 60 98 72 92 C84 86 92 96 98 92" stroke="#7CC6F2" stroke-width="4" fill="none"/>${faceSVG(50,73,.5)}`,
 shield:()=>`<path d="M50 6 L88 20 C88 60 72 82 50 94 C28 82 12 60 12 20Z" fill="#C9474E" ${OL}/><path d="M50 18 L76 28 C76 56 64 72 50 80 C36 72 24 56 24 28Z" fill="#E9C46A" opacity=".85"/>${faceSVG(50,50,.7)}`
});
Object.assign(ART_OF,{"hist:pyramid":["pyramid"],"hist:pharaoh":["pharaoh"],"hist:glyphs":["glyphs"],"hist:river":["river"],"hist:wheat":["wheat"],"hist:boat":["boat"],"hist:shield":["shield"]});
/* ===== 🎭 the SUBJECT characters (batch 27): any subject — known or brand new — gets characters of its own =====
   · the subject's EMBLEM decides the shape (💻 computer · 🎵 music · 🎨 art · 💹 economy · 📗 religion · ⚽ sport · 🩺 health ·
     🏛️ civics · 💡 thinking · 🌾 farming · 🪐 space — or one of 6 friendly shapes for anything else); the emblem comes from identity.py;
   · every CONCEPT of a new subject gets its own colour (from its name), so they are never all the same;
   · the WHOLE name is written on 1 or 2 lines (smaller letters when it is long) — never cut like the old «وحدات إدخا»;
   · the face follows the age stage like every character (the religion book has no face, out of respect).
   The API draws the SAME pictures (core/art.py fills ARTS.subjectTemplate), and a test checks both give the same SVG. */
const SUBJ_COLORS=[["#7CC6F2","#2F6FA8"],["#F6C177","#9A6416"],["#A3D9A5","#2E7D3A"],["#C4A7E7","#6A45A8"],["#F5A97F","#B5532A"],["#9CCFD8","#2E7A86"],["#EBBCBA","#A8505A"],["#F2D479","#8A6D0B"]];
const r1=v=>Math.round(v*10)/10;
function subjColor(label){const s=String(label||"");let n=0;for(let i=0;i<s.length;i++)n+=s.charCodeAt(i);const c=SUBJ_COLORS[n%SUBJ_COLORS.length];return {f:c[0],k:c[1]};}
function subjLabel(label){const t=String(label||"").replace(/[<&>"]/g,"").replace(/\s+/g," ").trim();if(!t)return {lines:[],fs:0};
  let lines=[t];const w=t.split(" ");
  if(t.length>9&&w.length>1){let best=null;for(let i=1;i<w.length;i++){const a=w.slice(0,i).join(" "),b=w.slice(i).join(" "),m=Math.max(a.length,b.length);if(!best||m<best.m)best={m:m,l:[a,b]};}lines=best.l;}
  const n=Math.max(...lines.map(x=>x.length));return {lines:lines,fs:Math.max(7,Math.min(lines.length>1?12:15,Math.floor(128/n)))};}   /* an Arabic letter ≈ half the font size wide (measured); 2 lines: at most 12, so the face stays free */
function nameBlock(x,y,ink,L){if(!L.lines.length)return "";const lh=r1(L.fs*1.2),h=r1(L.lines.length*lh+6),top=r1(y-4-h/2);
  return `<rect x="${x-36}" y="${top}" width="72" height="${h}" rx="${Math.min(10,r1(h/2))}" fill="#fff" stroke="${ink}" stroke-width="2"/>`+
    L.lines.map((t,i)=>{const fit=t.length*L.fs*.5>66?` textLength="66" lengthAdjust="spacingAndGlyphs"`:"";   /* still too long: squeezed to fit, never cut */
      return `<text x="${x}" y="${r1(top+3+lh*(i+.8))}" text-anchor="middle" font-size="${L.fs}" font-weight="800" fill="${ink}" font-family="sans-serif"${fit}>${t}</text>`;}).join("");}
/* every emblem: C = the concept's colours {f fill, k ink} · N(x, y, ink) = the name block */
const SUBJ_ART={
  /* the subjects we already had (same look as before; only the name block is new) */
  "📜":(C,N)=>`<rect x="18" y="14" width="64" height="72" rx="6" fill="#F6E3C6" ${OL}/><rect x="10" y="6" width="80" height="14" rx="7" fill="#E6CFA8" ${OL}/><rect x="10" y="80" width="80" height="14" rx="7" fill="#E6CFA8" ${OL}/>${N(50,40,"#7A4D2B")}${faceSVG(50,64,.55)}`,
  "🧮":(C,N)=>`<rect x="14" y="6" width="72" height="88" rx="12" fill="#F6C177" ${OL}/><rect x="22" y="14" width="56" height="26" rx="6" fill="#E6F4FB" ${OL}/>${N(50,31,"#2F6FA8")}${faceSVG(50,66,.7)}`,
  "🔬":(C,N)=>`<path d="M38 6 H62 M42 6 V36 L16 84 C12 92 18 96 26 96 H74 C82 96 88 92 84 84 L58 36 V6" fill="#A3D9A5" ${OL}/>${N(50,30,"#2E7D3A")}${faceSVG(50,74,.6)}`,
  "📖":(C,N)=>`<path d="M50 20 C38 12 22 12 8 16 V84 C22 80 38 80 50 88 C62 80 78 80 92 84 V16 C78 12 62 12 50 20Z" fill="#B9A2F0" ${OL}/>${N(50,38,"#5B3FA0")}${faceSVG(50,64,.6)}`,
  "🧭":(C,N)=>`<circle cx="50" cy="54" r="40" fill="#7CC6F2" ${OL}/><path d="M50 18 L56 50 L50 56 L44 50Z" fill="#E8574A"/>${N(50,26,"#2F6FA8")}${faceSVG(50,64,.65)}`,
  "🔭":(C,N)=>`<rect x="14" y="30" width="72" height="40" rx="20" fill="#9CCFD8" ${OL}/>${N(50,24,"#3E7FA8")}${faceSVG(50,52,.6)}`,
  "⚗️":(C,N)=>`<path d="M40 6 H60 M44 6 V30 C24 40 16 60 22 76 C28 92 72 92 78 76 C84 60 76 40 56 30 V6" fill="#C4A7E7" ${OL}/>${N(50,26,"#7A45B8")}${faceSVG(50,68,.6)}`,
  "🔹":(C,N)=>`<rect x="10" y="12" width="80" height="78" rx="16" fill="#9CCFD8" ${OL}/>${N(50,36,"#3E7FA8")}${faceSVG(50,64,.7)}`,
  /* 🆕 new subjects (identity.py → FAMILIES) */
  "💻":(C,N)=>`<rect x="12" y="8" width="76" height="60" rx="8" fill="${C.f}" ${OL}/><rect x="18" y="14" width="64" height="48" rx="4" fill="#EAF6FB" ${OL}/><path d="M6 74 H94 L86 90 H14Z" fill="#D8DEE4" ${OL}/><rect x="40" y="79" width="20" height="5" rx="2.5" fill="#9AA6B2"/>${N(50,28,C.k)}${faceSVG(50,54,.44)}`,
  "🎵":(C,N)=>`<path d="M30 8 L46 36 M70 8 L54 36" stroke="#7A4D2B" stroke-width="5" stroke-linecap="round"/><circle cx="30" cy="8" r="4" fill="#E9C46A" ${OL}/><circle cx="70" cy="8" r="4" fill="#E9C46A" ${OL}/><rect x="12" y="38" width="76" height="52" rx="6" fill="${C.f}" ${OL}/><ellipse cx="50" cy="38" rx="38" ry="10" fill="#FBF3E4" ${OL}/><path d="M14 52 L28 86 L42 52 L56 86 L70 52 L86 86" stroke="#fff" stroke-width="2.4" fill="none" opacity=".75"/>${N(50,54,C.k)}${faceSVG(50,78,.42)}`,
  "🎨":(C,N)=>`<path d="M50 8 C24 8 6 26 6 50 C6 74 24 92 48 92 C58 92 60 84 56 78 C52 72 56 66 64 66 H76 C88 66 94 58 94 46 C94 24 74 8 50 8Z" fill="${C.f}" ${OL}/><circle cx="26" cy="62" r="6" fill="#E8574A" ${OL}/><circle cx="76" cy="52" r="5" fill="#7CC6F2" ${OL}/><circle cx="78" cy="30" r="5" fill="#A3D9A5" ${OL}/><circle cx="22" cy="40" r="5" fill="#F2D479" ${OL}/>${N(50,34,C.k)}${faceSVG(46,64,.5)}`,
  "💹":(C,N)=>`<circle cx="50" cy="52" r="42" fill="${C.f}" ${OL}/><circle cx="50" cy="52" r="34" fill="none" stroke="#fff" stroke-width="2.4" opacity=".7"/><path d="M78 16 L84 10 M86 22 L94 20" stroke="#F2D479" stroke-width="3" stroke-linecap="round"/>${N(50,40,C.k)}${faceSVG(50,68,.5)}`,
  "📗":(C,N)=>`<rect x="16" y="8" width="70" height="86" rx="6" fill="${C.f}" ${OL}/><rect x="16" y="8" width="10" height="86" rx="4" fill="#fff" opacity=".35"/><path d="M58 60 L62 70 L72 70 L64 76 L67 86 L58 80 L49 86 L52 76 L44 70 L54 70Z" fill="#E9C46A" ${OL}/>${N(54,40,C.k)}`,
  "⚽":(C,N)=>`<circle cx="50" cy="52" r="42" fill="#FFFFFF" ${OL}/><path d="M50 28 L62 37 L57 51 L43 51 L38 37Z" fill="${C.f}" ${OL}/><path d="M14 46 L24 42 L30 52 L22 62 L12 58" fill="${C.f}" ${OL}/><path d="M86 46 L76 42 L70 52 L78 62 L88 58" fill="${C.f}" ${OL}/><path d="M38 86 L42 76 L58 76 L62 86" fill="${C.f}" ${OL}/>${N(50,26,C.k)}${faceSVG(50,64,.5)}`,
  "🩺":(C,N)=>`<path d="M36 22 V14 C36 10 40 8 44 8 H56 C60 8 64 10 64 14 V22" fill="none" ${OL}/><rect x="8" y="22" width="84" height="70" rx="12" fill="${C.f}" ${OL}/><path d="M74 66 H82 M78 62 V70" stroke="#fff" stroke-width="4" stroke-linecap="round"/>${N(50,42,C.k)}${faceSVG(44,72,.46)}`,
  "🏛️":(C,N)=>`<path d="M6 32 L50 6 L94 32Z" fill="${C.f}" ${OL}/><rect x="10" y="32" width="80" height="8" fill="#F1E6D6" ${OL}/>${[18,36,56,74].map(x=>`<rect x="${x}" y="40" width="8" height="42" fill="#FBF3E4" ${OL}/>`).join("")}<rect x="6" y="82" width="88" height="10" rx="2" fill="#E6D3B8" ${OL}/>${N(50,62,C.k)}${faceSVG(50,24,.36)}`,
  "💡":(C,N)=>`<circle cx="50" cy="40" r="32" fill="${C.f}" ${OL}/><rect x="36" y="70" width="28" height="8" rx="3" fill="#B8C2CC" ${OL}/><rect x="38" y="78" width="24" height="8" rx="3" fill="#9AA6B2" ${OL}/><path d="M44 90 H56" stroke="#3b2a1a" stroke-width="3" stroke-linecap="round"/><path d="M10 14 L4 8 M90 14 L96 8 M50 2 V-2" stroke="#F2D479" stroke-width="3" stroke-linecap="round"/>${N(50,34,C.k)}${faceSVG(50,57,.44)}`,
  "🌾":(C,N)=>`<path d="M50 30 L50 4 M50 12 L42 6 M50 18 L42 12 M50 12 L58 6 M50 18 L58 12" stroke="#B8893B" stroke-width="3" stroke-linecap="round"/><path d="M28 30 H72 L66 38 C84 46 90 66 84 82 C80 92 20 92 16 82 C10 66 16 46 34 38Z" fill="${C.f}" ${OL}/><path d="M30 36 H70" stroke="#7A4D2B" stroke-width="3"/>${N(50,56,C.k)}${faceSVG(50,78,.42)}`,
  "🪐":(C,N)=>`<ellipse cx="50" cy="54" rx="46" ry="12" fill="none" stroke="#E9C46A" stroke-width="5" transform="rotate(-14 50 54)"/><circle cx="50" cy="52" r="32" fill="${C.f}" ${OL}/><path d="M6 64 C30 76 74 64 94 42" stroke="#E9C46A" stroke-width="5" fill="none" stroke-linecap="round"/><circle cx="84" cy="12" r="3" fill="#F2D479"/><circle cx="12" cy="20" r="2" fill="#F2D479"/>${N(50,44,C.k)}${faceSVG(50,68,.4)}`,
  /* anything else: a friendly shape (the same subject always gets the same one) */
  "✦hex":(C,N)=>`<path d="M50 4 L90 27 V73 L50 96 L10 73 V27Z" fill="${C.f}" ${OL}/>${N(50,40,C.k)}${faceSVG(50,68,.55)}`,
  "✦star":(C,N)=>`<path d="M50 4 L62 32 L94 34 L70 54 L78 86 L50 70 L22 86 L30 54 L6 34 L38 32Z" fill="${C.f}" ${OL}/>${N(50,46,C.k)}${faceSVG(50,68,.38)}`,
  "✦cloud":(C,N)=>`<path d="M24 82 C8 82 4 62 18 56 C14 38 34 28 46 38 C52 20 80 22 82 42 C98 44 98 70 84 82Z" fill="${C.f}" ${OL}/>${N(50,50,C.k)}${faceSVG(50,72,.42)}`,
  "✦shield":(C,N)=>`<path d="M50 6 L88 18 C88 58 72 82 50 94 C28 82 12 58 12 18Z" fill="${C.f}" ${OL}/>${N(50,40,C.k)}${faceSVG(50,68,.5)}`,
  "✦drop":(C,N)=>`<path d="M50 4 C66 28 86 46 86 64 C86 84 70 96 50 96 C30 96 14 84 14 64 C14 46 34 28 50 4Z" fill="${C.f}" ${OL}/>${N(50,56,C.k)}${faceSVG(50,78,.42)}`,
  "✦gem":(C,N)=>`<path d="M26 10 H74 L94 36 L50 94 L6 36Z" fill="${C.f}" ${OL}/><path d="M6 36 H94 M26 10 L38 36 L50 10 L62 36 L74 10" stroke="#fff" stroke-width="2" fill="none" opacity=".7"/>${N(50,48,C.k)}${faceSVG(50,70,.36)}`};
/* how each new subject's characters move (the others keep their own way) */
const SUBJ_ANIM={"💻":"wobble","🎵":"sway","🎨":"wiggle","💹":"bounce","⚽":"bounce","🌾":"sway","✦star":"wiggle","✦cloud":"sway","✦drop":"bounce"};
ARTS.subject=(emblem,label)=>{const L=subjLabel(label),C=subjColor(label);return (SUBJ_ART[emblem]||SUBJ_ART["🔹"])(C,(x,y,ink)=>nameBlock(x,y,ink,L));};
/* for the API: the same drawing with holes for the colours and the name ({{FILL}} {{INK}} {{NB|x|y|ink}}), filled by core/art.py */
ARTS.subjectTemplate=emblem=>(SUBJ_ART[emblem]||SUBJ_ART["🔹"])({f:"{{FILL}}",k:"{{INK}}"},(x,y,ink)=>`{{NB|${x}|${y}|${ink}}}`);

/* geography: an ocean */
Object.assign(ARTS,{ocean:()=>`<rect x="6" y="20" width="88" height="72" rx="14" fill="#4FA3E0" ${OL}/><path d="M10 40 C22 32 30 48 42 40 C54 32 62 48 74 40 C82 35 88 40 90 42 M10 62 C22 54 30 70 42 62 C54 54 62 70 74 62 C82 57 88 62 90 64" stroke="#fff" stroke-width="3.4" fill="none" stroke-linecap="round"/>${faceSVG(50,78,.55)}`});
Object.assign(ART_OF,{"🌊":["ocean"]});
/* a drawing made by the LLM for this book ("art:<concept id>"): its body + OUR face, so it moves and feels like the others */
function bookArt(e){if(typeof e!=="string"||!e.startsWith("art:"))return null;const a=((typeof lesson==="function"&&lesson().art)||{})[e.slice(4)];return a||null;}
function subjParts(e){if(typeof e!=="string"||!e.startsWith("subj:"))return null;const i=e.indexOf(":",5);return i<0?[e.slice(5),""]:[e.slice(5,i),e.slice(i+1)];}
function artSVG(e,cls){if(typeof e==="string"&&e.startsWith("lego:")){const lg=legoSVG(e);return lg?`<svg class="ch ${cls||""}" viewBox="0 0 100 100" aria-hidden="true">${lg}</svg>`:null;}   /* 🧱 a Lego drawing (lego.js) */
  const sp=subjParts(e);if(sp)return `<svg class="ch ${cls||""}" viewBox="0 0 100 100" aria-hidden="true">${ARTS.subject(sp[0],sp[1])}</svg>`;const b=bookArt(e);if(b)return `<svg class="ch ${cls||""}" viewBox="0 0 100 100" aria-hidden="true">${b.body}${faceSVG(b.face.x,b.face.y,b.face.s)}</svg>`;
  const a=ART_OF[e];if(!a)return null;return `<svg class="ch ${cls||""}" viewBox="0 0 100 100" aria-hidden="true">${ARTS[a[0]](a[1])}</svg>`;}

/* every picture is alive: each kind of thing moves in its own way (a leaf flutters, the sun spins, water drips…) */
const ALIVE={"🍃":"leaf","🌿":"sway","🌱":"grow","🌸":"sway","🌷":"sway","🌻":"sway","🌼":"sway","🪻":"sway","🪷":"sway","🌺":"sway",
  "💨":"wind","🌬️":"wind","☀️":"sun","💧":"drip","🌰":"wobble","🍎":"bounce","🐝":"buzz","🦋":"buzz","🫚":"wiggle","🟫":"wiggle",
  "🪴":"sway","🌳":"sway","🏡":"bob","🔌":"wobble","💡":"sun","🚂":"chug","🦊":"wobble","🦉":"bob","🐱":"wiggle"};
let aliveN=0;
const animOf=e=>{const lp=legoParts(e);if(lp)return lp.mo;const ba=bookArt(e);if(ba)return ba.anim||"bob";const sp=subjParts(e);return sp?(SUBJ_ANIM[sp[0]]||"bob"):(ALIVE[e]||"bob");};
const kindOf=e=>(subjParts(e)||legoParts(e))?"subj":(ART_OF[e]||[""])[0];   /* «subj»: a subject character (poke it → a note of its subject) */
function alive(e){if(!e)return "";const k=animOf(e);aliveN=(aliveN+1)%7;const a=artSVG(e);
  return `<span class="alive a-${k}${a?" art":""}" data-k="${a?kindOf(e):""}" style="animation-delay:-${aliveN*0.37}s">${a||e}</span>`;}
/* poke any picture: it jumps (works with the mouse and the finger) */
const SOUND_OF={water:"drip",bee:"buzz",air:"wind",dandelion:"wind",train:"whistle",fox:"yip",owl:"hoot",leaf:"rustle",stem:"rustle",tree:"rustle",subj:"pick"};
document.addEventListener("pointerdown",e=>{const a=e.target.closest&&e.target.closest(".alive,.char");if(!a)return;
  if(a.classList.contains("alive")){a.classList.remove("poke");void a.offsetWidth;a.classList.add("poke");setTimeout(()=>a.classList.remove("poke"),500);}
  const k=a.dataset.k;if(k&&SOUND_OF[k])sfx(SOUND_OF[k]);});   /* only things that really make a sound (the sun, a seed… stay quiet) */
/* eyes that follow a point (all faces the same way: no hints) */
function lookAt(root,x,y){root.querySelectorAll(".eye").forEach(e=>{const r=e.getBoundingClientRect();const a=Math.atan2(y-(r.top+r.height/2),x-(r.left+r.width/2));const p=e.querySelector(".pupil");if(p)p.style.transform=`translate(${Math.cos(a)*3.5}px,${Math.sin(a)*3.5}px)`;});
  root.querySelectorAll(".seye").forEach(e=>{const r=e.getBoundingClientRect();const a=Math.atan2(y-(r.top+r.height/2),x-(r.left+r.width/2));const p=e.querySelector(".spupil");if(p)p.setAttribute("transform",`translate(${(Math.cos(a)*2.4).toFixed(2)} ${(Math.sin(a)*2.4).toFixed(2)})`);});}
/* every drawn character looks at your finger or mouse, anywhere on the page */
let lookPending=false;document.addEventListener("pointermove",e=>{if(lookPending)return;lookPending=true;requestAnimationFrame(()=>{lookPending=false;const r={querySelectorAll:s=>s===".seye"?document.querySelectorAll(".seye"):[]};lookAt(r,e.clientX,e.clientY);});});
const faceHTML=(color)=>`<span class="face" style="background:${color}"><span class="eye l"><span class="pupil"></span></span><span class="eye r"><span class="pupil"></span></span><span class="nose"></span><span class="mouth"></span></span>`;
const FACE_COLORS=["#F6C177","#9CCFD8","#C4A7E7","#EBBCBA","#A3D9A5","#F5A97F"];
const colorOf=id=>FACE_COLORS[[...String(id)].reduce((a,c)=>a+c.charCodeAt(0),0)%FACE_COLORS.length];
function charHTML(id,icon,mood){const body=artSVG(icon,"big")||`<svg class="ch big" viewBox="0 0 100 100" aria-hidden="true">${ARTS.blob(colorOf(id))}</svg>`;
  return `<span class="char a-${animOf(icon)}" data-k="${kindOf(icon)||"blob"}" data-mood="${mood||"happy"}" style="animation-delay:-${(aliveN=(aliveN+1)%7)*0.37}s">${body}</span>`;}   /* the whole character moves in its own way */
const setMood=(root,m)=>{const c=root.querySelector(".char");if(c)c.dataset.mood=m;};
/* faces react to you: surprised when you come close, a squeeze when you press */
document.addEventListener("pointerover",e=>{const c=e.target.closest&&e.target.closest(".char");if(!c||c.classList.contains("wow"))return;c.classList.add("wow");setTimeout(()=>c.classList.remove("wow"),700);});
