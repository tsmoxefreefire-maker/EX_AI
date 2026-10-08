/* ===== 🎤 interview · 🎴 flip cards · ⏳ before/after — more ways to explore, so it never feels the same ===== */
function sceneInterview(s){const v=V(),W=v?380:640,H=v?330:320;const T=v?[190,200]:[480,180],M=v?[78,46]:[150,175];
  const svg=`<svg class="xstage" id="xs" viewBox="0 0 ${W} ${H}" role="img" aria-label="مقابلة">${node(s.target,T[0],T[1],v?140:150,"happy","star")}
    <g transform="translate(${M[0]} ${M[1]}) scale(${v?.8:1})"><rect x="-70" y="-28" width="140" height="56" rx="14" fill="#3b2a1a"/><circle cx="-40" cy="0" r="14" fill="#E8574A"/><text x="10" y="6" text-anchor="middle" fill="#fff" font-weight="800" font-size="16">🎤 مقابلة</text></g></svg>
    <div class="chatbox" hidden><div class="chat" id="chat" aria-live="polite"></div></div><div class="qbtns">${s.qa.map((x,i)=>`<button class="qbtn" data-i="${i}">${VOICE(x.q)}</button>`).join("")}</div>`;
  return {svg,wire:root=>{document.querySelectorAll(".qbtn").forEach(b=>b.addEventListener("click",()=>{const x=s.qa[+b.dataset.i];b.classList.add("asked");sfx("pop");
      const c=document.getElementById("chat");c.parentNode.hidden=false;c.insertAdjacentHTML("beforeend",`<div class="msg me">${VOICE(x.q)}</div><div class="msg them">${richText(x.a)}</div>`);c.scrollTop=c.scrollHeight;
      mood(root,s.target,"laugh");say(root,s.target,x.a.replace(/«|»/g,""));setTimeout(()=>mood(root,s.target,"happy"),1400);cap("🎤 "+x.a);}));}};}
function sceneFlip(s){const v=V();const svg=`<svg class="xstage" id="xs" viewBox="0 0 ${v?380:640} ${v?190:200}" role="img" aria-label="بطاقات">${node(s.target,v?190:320,v?88:100,v?120:130,"happy","star")}</svg>
    <div class="cards2 n${s.cards.length}">${s.cards.map((c,i)=>`<div class="card2b" role="button" tabindex="0" data-i="${i}" aria-pressed="false"><span class="face front"><b class="fq">${VOICE(c.front)}</b><small>اقلبني 🔄</small></span><span class="face back" hidden><small class="bq">${VOICE(c.front)}</small><span class="bt">${richText(c.back)}</span></span></div>`).join("")}</div>`;
  return {svg,wire:root=>{document.querySelectorAll(".card2b").forEach(b=>b.addEventListener("keydown",e=>{if(e.key==="Enter"||e.key===" "){e.preventDefault();b.click();}}));
    document.querySelectorAll(".card2b").forEach(b=>b.addEventListener("click",e=>{if(e.target.closest(".kw"))return;if(b.classList.contains("turning"))return;b.classList.add("turning");sfx("flip");
      setTimeout(()=>{const open=b.getAttribute("aria-pressed")!=="true";b.setAttribute("aria-pressed",String(open));b.querySelector(".front").hidden=open;b.querySelector(".back").hidden=!open;b.classList.toggle("flipped",open);b.classList.remove("turning");
        if(open){mood(root,s.target,"laugh");setTimeout(()=>mood(root,s.target,"happy"),900);cap("🎴 "+s.cards[+b.dataset.i].back);}},160);}));}};}
/* ⏳ two honest meanings (the factory decides from the graph's own words):
   · «becomes» (the seed sprouts): قبل / بعد — the old one fades INTO the new one;
   · «needs»  (the stem needs the root): أول / وبعدين — the first one STAYS, the second comes after it, and the «بيحتاج» arrow + the reason appear.
   A line under the slider always says in words what the picture shows (it was not explained before). */
function sceneBeforeAfter(s){const v=V(),W=v?380:640,H=v?250:300,becomes=s.mode==="becomes";const A=exName(s.before),B=exName(s.target);
  const L1=becomes?"قبل":"أول",L2=becomes?"بعد":"وبعدين";const xa=v?W-95:W-150,xb=v?95:150,Z=v?96:120;
  const arrow=becomes?`<path class="xarrow" id="baArrow" d="M${xa-Z*0.7} 150 L${xb+Z*0.7} 150" marker-end="url(#xhead)" opacity=".25"/>`
    :`<g id="baArrow" opacity="0">${flow(`M${xb+Z*0.6} 150 Q${W/2} 120 ${xa-Z*0.6} 150`,"",false,true)}</g>`;   /* «needs»: from the one who needs → to what it needs */
  const svg=`<svg class="xstage" id="xs" viewBox="0 0 ${W} ${H}" role="img" aria-label="${L1} و${L2}">${DEFS}
    <text x="${xa}" y="36" class="xlabel" text-anchor="middle">${L1}</text><text x="${xb}" y="36" class="xlabel" text-anchor="middle">${L2}</text>
    <g id="bef">${node(s.before,xa,150,Z,"happy")}</g>${arrow}
    <g id="aft" opacity=".15">${node(s.target,xb,150,Z,becomes?"sad":"happy")}</g></svg>
    <div class="slider2"><span>${L1}: «${A}»</span><input type="range" id="ba" min="0" max="100" value="0" aria-label="${L1} و${L2}"><span>${L2}: «${B}»</span></div>
    <p class="baexp" id="baexp" aria-live="polite"></p>`;
  const say0=becomes?`👀 هاد «${A}». اسحب الشريط وشوف شو بيصير فيه.`:`1️⃣ أول لازم يكون في «${A}». اسحب الشريط ←`;
  const sayMid=becomes?`⏳ «${A}» عم ${/ة$/.test(A.split(" ")[0])?"بتتغيّر":"بيتغيّر"}…`:`2️⃣ «${A}» لسا موجود، و«${B}» عم ييجي بعده…`;
  const sayEnd=s.steps[1]||"";
  return {svg,wire:root=>{const r=document.getElementById("ba"),ex=document.getElementById("baexp");let told=false,last="";
      const tell=t=>{const msg=t>=0.95?"✅ "+sayEnd:t>0.05?sayMid:say0;if(msg!==last){last=msg;ex.innerHTML=richText(msg);}};tell(0);
      r.addEventListener("input",()=>{const t=+r.value/100;
        if(becomes)root.querySelector("#bef").setAttribute("opacity",(1-0.75*t).toFixed(2));              /* becomes: the old one fades into the new */
        else root.querySelector("#bef").setAttribute("opacity","1");                                       /* needs: the first one STAYS */
        root.querySelector("#aft").setAttribute("opacity",(0.15+0.85*t).toFixed(2));
        root.querySelector("#baArrow").setAttribute("opacity",(becomes?0.25+0.75*t:Math.max(0,(t-0.4)/0.6)).toFixed(2));
        mood(root,s.target,t>0.9?"laugh":t>0.4?"happy":becomes?"sad":"happy");tell(t);
        if(t>0.95&&!told){told=true;sfx("bloom");cap("⏳ "+sayEnd);}if(t<0.5)told=false;});}};}
SCENES.interview=sceneInterview;SNAME.interview="🎤 مقابلة";SCENES.flip=sceneFlip;SNAME.flip="🎴 بطاقات";SCENES.before_after=sceneBeforeAfter;SNAME.before_after="⏳ قبل وبعد";
