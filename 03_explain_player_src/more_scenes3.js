/* ===== 🆕 five new activities (batch 26): 🧪 recipe · ✏️ connect · ⚖️ compare · 🧑‍🏫 teach · 🪜 ladder =====
   Rules from the old mistakes (each one broke something before):
   · every class name starts with «na-» (the questions game also has .face .tail .lifted .card .on .done … on this page);
   · no CSS animation on a <g> that has a transform (only opacity, or an inner group);
   · no <button> inside a <button> (cards are <div role="button">, their words are plain text);
   · every word goes through VOICE / richText (the age's way of talking); « و» stays glued (richText);
   · the STUDENT does every move: video mode only plays the captions, it never plays the activity for him;
   · every move is explained (right → the reason · wrong → why it is wrong), and «💡 ساعدني» / a second try always opens the way;
   · a phone (≈380px) has its own layout; touch works by TAPPING (dragging is a bonus); timers check root.isConnected. */
const naTake=root=>{if(VIDEO)stopVideo(root);};                    /* the student touched it → the scene is his */
const naEsc=t=>String(t).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");
const naQ=id=>"«"+exName(id)+"»";
function naEnds(a,b,ra,rb){const dx=b[0]-a[0],dy=b[1]-a[1],d=Math.hypot(dx,dy)||1;return [[a[0]+dx/d*ra,a[1]+dy/d*ra],[b[0]-dx/d*rb,b[1]-dy/d*rb]];}
function naKeys(el,fn){el.addEventListener("keydown",e=>{if(e.key==="Enter"||e.key===" "){e.preventDefault();fn();}});}

/* 🧪 RECIPE — the things a concept needs, as switches. It starts empty; the ring fills; complete only when ALL are on.
   Turning one off says which one is missing and why (necessity: every one of them, not «some»). */
function sceneRecipe(s){const v=V(),n=s.needs.length;
  const W=v?380:640,H=v?430:Math.max(330,92*n+60),Z=v?104:122,IZ=v?62:64,T=v?[W/2,H-128]:[170,H/2];
  const ins=v&&n>1?Math.min(W/2,Math.max(52,...[0,n-1].map(i=>String(exName(s.needs[i].id)).length*3.6+8))):52;   /* phone: a long name at the edge stays inside («معادلة الخط المستقيم») */
  const pos=s.needs.map((x,i)=>v?[n===1?W/2:W-ins-i*((W-2*ins)/(n-1)),78]:[W-104,n===1?H/2:58+i*((H-116)/(n-1))]);
  const R=Z/2+6,C=2*Math.PI*R;   /* the ring hugs the picture, above the name */
  const svg=`<svg class="xstage" id="xs" viewBox="0 0 ${W} ${H}" data-bubble="78" role="img" aria-label="${naEsc(VOICE("الشروط"))}">${DEFS}
    ${s.needs.map((x,i)=>{const [p,q]=naEnds(T,pos[i],R+4,IZ/2+12);return `<g class="xedge na-p na-poff" data-i="${i}">${flow(curve(p,q,v?0:18),"")}</g>`;}).join("")}
    <circle class="na-ring0" cx="${T[0]}" cy="${T[1]}" r="${R}"/><circle class="na-ring" cx="${T[0]}" cy="${T[1]}" r="${R}" stroke-dasharray="0 ${C.toFixed(1)}" style="opacity:0" transform="rotate(-90 ${T[0]} ${T[1]})"/>
    ${node(s.target,T[0],T[1],Z,"sad","star na-tgt").replace(`class="xname" y="${Z/2+18}"`,`class="xname" y="${Z/2+30}"`)}
    ${s.needs.map((x,i)=>node(x.id,pos[i][0],pos[i][1],IZ,"sad","na-ing na-offn")).join("")}</svg>
    <div class="na-sw" role="group" aria-label="${naEsc(VOICE("شغّل وطفّي"))}">${s.needs.map((x,i)=>`<button class="na-tog" data-i="${i}" aria-pressed="false"><span class="na-led" aria-hidden="true"></span><span class="na-tn">${naEsc(naQ(x.id))}</span><b class="na-ts">${VOICE("مش موجود")}</b></button>`).join("")}</div>
    <p class="na-count" id="naCount" aria-live="polite">0 ${VOICE("من")} ${n}</p>`;
  return {svg,wire:root=>{const on=new Set();let wasAll=false;
      const tgt=root.querySelector(".na-tgt");
      const set=(i,val)=>{naTake(root);if(val)on.add(i);else on.delete(i);const id=s.needs[i].id;
        const b=document.querySelector(`.na-tog[data-i="${i}"]`);b.setAttribute("aria-pressed",String(val));b.querySelector(".na-ts").textContent=VOICE(val?"موجود ✔️":"مش موجود");
        root.querySelector(`.na-ing[data-id="${id}"]`).classList.toggle("na-offn",!val);mood(root,id,val?"laugh":"sad");
        const p=root.querySelector(`.na-p[data-i="${i}"]`);p.classList.toggle("na-poff",!val);p.classList.toggle("lit",val);
        const ring=root.querySelector(".na-ring");ring.setAttribute("stroke-dasharray",`${(C*on.size/n).toFixed(1)} ${C.toFixed(1)}`);ring.style.opacity=on.size?1:0;   /* (0: no dot) */
        document.getElementById("naCount").textContent=`${on.size} ${VOICE("من")} ${n}`;
        const all=on.size===n;tgt.classList.toggle("na-ready",all);
        sfx(val?"on":"off",{n:on.size-(val?1:0)});
        if(all){mood(root,s.target,"laugh");cap(s.ready);if(!wasAll){setTimeout(()=>{if(root.isConnected&&on.size===n)sfx("ready");},220);if(!grown())sparkles();}}
        else{mood(root,s.target,on.size?"happy":"sad");const miss=s.needs.map((_,k)=>k).filter(k=>!on.has(k));
          cap((val?`✔️ شغّلت ${naQ(id)}. `:`⛔ طفّيت ${naQ(id)}. `)+`${VOICE("لسا ناقص")} ${miss.map(k=>naQ(s.needs[k].id)).join(" و")}. `+s.needs[i].why);}
        wasAll=all;};
      document.querySelectorAll(".na-tog").forEach(b=>b.addEventListener("click",()=>{const i=+b.dataset.i;set(i,!on.has(i));}));
      root.querySelectorAll(".na-ing").forEach(nd=>nd.addEventListener("click",()=>{const i=s.needs.findIndex(x=>x.id===nd.dataset.id);if(i>=0)set(i,!on.has(i));}));}};}

/* ✏️ CONNECT — the student draws the «needs» arrows himself: drag from the one who needs to what it needs (or tap them in order).
   Right → the arrow stays + the reason. Reversed → it is explained (the commonest mistake). No link → said so. */
function sceneConnect(s){const v=V(),W=v?380:640,H=v?480:390,c=[W/2,v?H/2:H/2-4],others=s.nodes.slice(1),n=others.length,TZ=v?96:104,OZ=v?64:70;
  const slots=v?[[296,80],[84,400],[296,400],[84,80],[190,54]]:[[544,80],[96,290],[544,290],[96,80],[588,186],[52,186]];   /* the corners first: far from the middle one */
  const pos={};pos[s.target]=c;shuffle(slots.slice(0,n),[...s.target].reduce((a,ch)=>a+ch.charCodeAt(0),7)).forEach((p,i)=>pos[others[i]]=p);   /* mixed: the place never tells who needs whom */
  const size=id=>id===s.target?TZ:OZ;
  const svg=`<svg class="xstage" id="xs" viewBox="0 0 ${W} ${H}" data-bubble="78" role="img" aria-label="${naEsc(VOICE("ارسم الأسهم"))}">${DEFS}<g id="naArrows"></g>
    ${node(s.target,c[0],c[1],TZ,"happy","star na-cn")}${others.map(id=>node(id,pos[id][0],pos[id][1],OZ,"happy","na-cn")).join("")}
    <g id="naTop" pointer-events="none"><line class="na-rubber" x1="0" y1="0" x2="0" y2="0" visibility="hidden"/></g></svg>
    <div class="row center na-crow"><span class="na-count" id="naCount" aria-live="polite"></span><button class="chipbtn na-help" id="naHelp">💡 ${VOICE("ساعدني")}</button></div>`;
  const req=s.links.map((l,k)=>k).filter(k=>s.links[k].required);
  return {svg,wire:root=>{let sel=null,drag=null;const drawn=new Set();const rub=root.querySelector(".na-rubber");
      const count=()=>{document.getElementById("naCount").textContent=`✏️ ${req.filter(k=>drawn.has(k)).length} ${VOICE("من")} ${req.length}`;};count();
      const toSvg=e=>{const pt=root.createSVGPoint();pt.x=e.clientX;pt.y=e.clientY;return pt.matrixTransform(root.getScreenCTM().inverse());};
      const hit=p=>{let best=null,bd=1e9;s.nodes.forEach(id=>{const q=pos[id],d=Math.hypot(p.x-q[0],p.y-q[1]);if(d<size(id)/2+18&&d<bd){bd=d;best=id;}});return best;};
      const select=id=>{sel=id;root.querySelectorAll(".na-cn").forEach(nd=>nd.classList.toggle("na-sel",nd.dataset.id===id));};
      const arrow=(a,b,cls)=>{const [p,q]=naEnds(pos[a],pos[b],size(a)/2+6,size(b)/2+12);const g=document.createElementNS(svgNS,"g");g.setAttribute("class","xedge lit na-arr "+(cls||""));
        g.innerHTML=flow(curve(p,q,16),"");root.querySelector("#naArrows").appendChild(g);return g;};
      const wrong=(a,b)=>{const [p,q]=naEnds(pos[a],pos[b],size(a)/2+6,size(b)/2+12);const l=document.createElementNS(svgNS,"line");
        l.setAttribute("class","na-wrongline");[["x1",p[0]],["y1",p[1]],["x2",q[0]],["y2",q[1]]].forEach(([k,x])=>l.setAttribute(k,x.toFixed(1)));
        root.querySelector("#naTop").appendChild(l);setTimeout(()=>l.remove(),900);};
      const finish=()=>{cap(s.end_say);sfx("ready");if(!grown())sparkles();document.getElementById("naHelp").hidden=true;root.querySelectorAll(".na-ghost").forEach(x=>x.remove());};
      const attempt=(a,b)=>{const k=s.links.findIndex(l=>l.from===a&&l.to===b),r=s.links.findIndex(l=>l.from===b&&l.to===a);
        if(k>=0){if(drawn.has(k)){cap(VOICE("هاد السهم مرسوم ✔️"));return;}drawn.add(k);root.querySelectorAll(".na-ghost").forEach(x=>x.remove());
          arrow(a,b,s.links[k].required?"":"na-bonus");cap(s.links[k].ok_say);sfx("connect",{n:drawn.size});mood(root,a,"laugh");mood(root,b,"laugh");count();
          if(s.links[k].required&&req.every(x=>drawn.has(x)))setTimeout(()=>{if(root.isConnected)finish();},900);}
        else if(r>=0){wrong(a,b);cap(s.links[r].rev_say);sfx("nope");}
        else{wrong(a,b);cap(`🙂 ما في سهم مباشر بين ${naQ(a)} و${naQ(b)}.`);sfx("nope");}};
      const rubber=(a,p)=>{if(!a){rub.setAttribute("visibility","hidden");return;}rub.setAttribute("visibility","visible");rub.setAttribute("x1",a[0]);rub.setAttribute("y1",a[1]);rub.setAttribute("x2",p[0].toFixed(1));rub.setAttribute("y2",p[1].toFixed(1));};
      root.querySelectorAll(".na-cn").forEach(nd=>{nd.style.touchAction="none";});
      root.addEventListener("pointerdown",e=>{const id=hit(toSvg(e));if(!id){if(sel)select(null);return;}naTake(root);e.preventDefault();
        if(sel&&sel!==id){const a=sel;select(null);attempt(a,id);return;}
        select(id);drag={id};try{root.setPointerCapture(e.pointerId);}catch(_){}});
      root.addEventListener("pointermove",e=>{if(drag){const p=toSvg(e);rubber(pos[drag.id],[p.x,p.y]);}});
      root.addEventListener("pointerup",e=>{if(!drag)return;const from=drag.id,id=hit(toSvg(e));drag=null;rubber(null);
        if(id&&id!==from){select(null);attempt(from,id);}
        else if(id===from){sfx("pick");cap(`👉 اخترت ${naQ(from)}. ${VOICE("هلأ اكبس على المفهوم الثاني.")}`);}});
      root.addEventListener("pointercancel",()=>{drag=null;rubber(null);});
      document.getElementById("naHelp").addEventListener("click",()=>{naTake(root);const k=req.find(x=>!drawn.has(x));if(k===undefined)return;const l=s.links[k];
        root.querySelectorAll(".na-ghost").forEach(x=>x.remove());arrow(l.from,l.to,"na-ghost");sfx("pick");cap(`💡 ${VOICE("جرّب")}: ${VOICE("من")} ${naQ(l.from)} ${VOICE("لـ")}${naQ(l.to)}.`);});}};}

/* ⚖️ COMPARE — two close concepts. Each fact card goes to «X», to «Y», or to «الاثنين» (tap the card, then its place).
   Right → it is explained. Wrong → «try another place»; a second wrong try puts it in its place, with the reason. */
function sceneCompare(s){const v=V(),W=v?380:640,H=v?196:216,Z=v?76:90,A=s.target,B=s.other;
  const pa=[W*0.77,H/2-10],pb=[W*0.23,H/2-10];
  const svg=`<svg class="xstage" id="xs" viewBox="0 0 ${W} ${H}" role="img" aria-label="${naEsc(VOICE("قارن"))}">
    <ellipse class="na-venn na-va" cx="${W*0.62}" cy="${H/2}" rx="${W*0.25}" ry="${H*0.45}"/><ellipse class="na-venn na-vb" cx="${W*0.38}" cy="${H/2}" rx="${W*0.25}" ry="${H*0.45}"/>
    <text class="na-vlab" x="${W/2}" y="${H/2+5}" text-anchor="middle">${VOICE("الاثنين")}</text>
    ${node(A,pa[0],pa[1],Z,"happy","na-ca")}${node(B,pb[0],pb[1],Z,"happy","na-cb")}</svg>
    <div class="na-tray" id="naTray">${s.facts.map((f,i)=>`<div class="na-card" role="button" tabindex="0" data-i="${i}" aria-pressed="false">${naEsc(VOICE(f.fact))}</div>`).join("")}</div>
    <div class="na-zones">${[["a",naQ(A)],["both",VOICE("الاثنين")],["b",naQ(B)]].map(([k,t])=>`<div class="na-zone na-z-${k}" role="button" tabindex="0" data-side="${k}"><b class="na-zh">${naEsc(t)}</b><div class="na-zl"></div></div>`).join("")}</div>`;
  return {svg,wire:root=>{let pick=null;const tries={};
      const choose=i=>{naTake(root);pick=pick===i?null:i;document.querySelectorAll(".na-card").forEach(c=>{const on=+c.dataset.i===pick;c.classList.toggle("na-picked",on);c.setAttribute("aria-pressed",String(on));});if(pick!==null)sfx("pick");};
      const place=(i,side,auto)=>{const f=s.facts[i],card=document.querySelector(`.na-card[data-i="${i}"]`);if(!card)return;
        const z=document.querySelector(`.na-zone[data-side="${side}"] .na-zl`);const d=document.createElement("div");d.className="na-placed";d.textContent="✔️ "+VOICE(f.fact);z.appendChild(d);card.remove();pick=null;
        cap((auto?"💡 ":"")+f.why);sfx(auto?"pick":"place");(side==="both"?[A,B]:[side==="a"?A:B]).forEach(id=>mood(root,id,"laugh"));
        if(!document.querySelector(".na-card"))setTimeout(()=>{if(!root.isConnected)return;cap(s.end_say);sfx("ready");if(!grown())sparkles();},900);};
      const drop=side=>{naTake(root);if(pick===null){cap(VOICE("👆 اختار بطاقة أول، وبعدين مكانها."));return;}const i=pick,f=s.facts[i];
        if(f.side===side){place(i,side,false);return;}
        tries[i]=(tries[i]||0)+1;const z=document.querySelector(`.na-zone[data-side="${side}"]`);z.classList.remove("na-nope");void z.offsetWidth;z.classList.add("na-nope");sfx("nope");
        if(tries[i]>=2)place(i,f.side,true);else cap(VOICE("🙂 مش هون. فكّر فيها كمان، وجرّب مكان ثاني."));};
      document.querySelectorAll(".na-card").forEach(c=>{c.addEventListener("click",()=>choose(+c.dataset.i));naKeys(c,()=>choose(+c.dataset.i));});
      document.querySelectorAll(".na-zone").forEach(z=>{z.addEventListener("click",()=>drop(z.dataset.side));naKeys(z,()=>drop(z.dataset.side));});}};}

/* 🧑‍🏫 TEACH — a classmate does not get it. He asks; the student picks the answer; the classmate repeats it in his words.
   A wrong pick is answered with WHY (that definition belongs to «Y» · the arrow is the other way). At the end: the explanation he built. */
function sceneTeach(s){const v=V(),W=v?380:640,H=v?226:236,st=stageNow(),Z=v?90:104;
  const mate=st==="kids"?skin().name:st==="junior"?"صاحبك":"زميلك";
  const M=v?[92,104]:[180,108],T=v?[W-96,104]:[W-180,108];                      /* the classmate on the left: his messages are on the left */
  const person=`<svg class="ch" viewBox="0 0 100 100"><circle cx="50" cy="34" r="19" style="fill:var(--chip);stroke:var(--brand)" stroke-width="3"/><path d="M16 94 Q18 60 50 58 Q82 60 84 94 Z" style="fill:var(--chip);stroke:var(--brand)" stroke-width="3"/></svg>`;
  const mart=((st==="kids"||st==="junior")&&artSVG(skin().mascot,""))||person;   /* teen / senior: a plain person (no cartoon face) */
  const svg=`<svg class="xstage" id="xs" viewBox="0 0 ${W} ${H}" data-bubble="70" role="img" aria-label="${naEsc(VOICE("اشرح لزميلك"))}">
    <g class="xnode na-mate" data-id="__mate" transform="translate(${M[0]} ${M[1]})"><g class="xbody" data-mood="o">${mart.replace("<svg ",`<svg width="${Z}" height="${Z}" x="${-Z/2}" y="${-Z/2}" `)}</g><text class="xname" y="${Z/2+18}" text-anchor="middle">${naEsc(mate)}</text><g class="xsay"></g></g>
    ${node(s.target,T[0],T[1],Z,"happy","star")}</svg>
    <div class="na-chat" id="naChat" aria-live="polite"></div><div class="na-opts" id="naOpts"></div><div class="na-note" id="naNote" hidden></div>`;
  return {svg,wire:root=>{let r=0;const chat=document.getElementById("naChat"),opts=document.getElementById("naOpts");
      const msg=(who,html)=>{chat.insertAdjacentHTML("beforeend",`<div class="na-msg na-${who}">${who==="them"?`<b>${naEsc(mate)}:</b> `:""}${html}</div>`);};
      const ask=()=>{const R=s.rounds[r];msg("them",naEsc(VOICE(R.ask)));say(root,"__mate",R.ask);mood(root,"__mate","o");
        opts.innerHTML=R.options.map((o,k)=>`<button class="na-opt" data-k="${k}">${naEsc(VOICE(o.opt))}</button>`).join("");
        opts.querySelectorAll(".na-opt").forEach(b=>b.addEventListener("click",()=>choose(+b.dataset.k,b)));};
      const end=()=>{const note=document.getElementById("naNote");note.hidden=false;note.innerHTML=richText(s.learnt);cap(s.learnt);sfx("ready");if(!grown())sparkles();
        say(root,"__mate",VOICE(st==="kids"?"هلأ فهمت! شكراً 😄":"هلأ وضحت. شكراً."));mood(root,"__mate","laugh");};
      const choose=(k,b)=>{naTake(root);const R=s.rounds[r],o=R.options[k];msg("me",naEsc(VOICE(o.opt)));
        if(o.ok){opts.innerHTML="";msg("them",richText(o.reply));say(root,"__mate",o.reply.replace(/[«»]/g,""));cap(o.reply);sfx("place");mood(root,"__mate","laugh");mood(root,s.target,"laugh");r++;
          setTimeout(()=>{if(!root.isConnected)return;if(r<s.rounds.length)ask();else end();},1300);}
        else{b.disabled=true;b.classList.add("na-wrong");msg("them",richText(o.reply));say(root,"__mate",o.reply.replace(/[«»]/g,""));cap(o.reply);sfx("nope");mood(root,"__mate","sad");}};
      ask();}};}

/* 🪜 LADDER — «ليش؟» again and again: each answer is the reason one rung deeper, down to the base
   (or «وبعدين؟»: what comes after, rung by rung). The arrows keep the «needs» direction (from the one who needs). */
function sceneLadder(s){const v=V(),n=s.rungs.length,W=v?380:640,G=v?128:140,TZ=v?94:100,Z=v?68:72;const H=72+G*n+82;   /* room between rungs: the «needs» label never sits on a name */
  const ids=[s.target].concat(s.rungs.map(r=>r.id));const dx=v?72:112;
  const pos=ids.map((id,k)=>[W/2+(k%2?-dx:dx),66+k*G]);const rail=v?160:200;   /* zigzag: every rung is beside the one before it */
  const svg=`<svg class="xstage" id="xs" viewBox="0 0 ${W} ${H}" data-bubble="74" role="img" aria-label="${naEsc(VOICE("السلّم"))}">${DEFS}
    <path class="na-rail" d="M${W/2-rail} 26 V${H-30} M${W/2+rail} 26 V${H-30}"/>${ids.slice(1).map((_,k)=>`<path class="na-rungline" d="M${W/2-rail} ${66+(k+1)*G} H${W/2+rail}"/>`).join("")}
    ${ids.slice(1).map((id,k)=>`<g class="na-slot" data-k="${k+1}"><circle cx="${pos[k+1][0]}" cy="${pos[k+1][1]}" r="${Z/2-4}"/><text x="${pos[k+1][0]}" y="${pos[k+1][1]+9}" text-anchor="middle">؟</text></g>`).join("")}
    <g id="naArrows"></g>${ids.map((id,k)=>node(id,pos[k][0],pos[k][1],k?Z:TZ,"happy",k?"na-hid":"star")).join("")}</svg>
    <div class="row center na-lrow"><button class="btn na-ask" id="naAsk">${s.mode==="why"?"❓ "+VOICE("ليش؟"):"⏭️ "+VOICE("وبعدين؟")}</button><button class="btn ghost" id="naReset" hidden>↺ ${VOICE("من الأول")}</button></div>`;
  return {svg,wire:root=>{let k=0;const ask=document.getElementById("naAsk"),reset=document.getElementById("naReset");
      const up=(a,b)=>s.mode==="why"?[a,b]:[b,a];                                 /* [the one who needs, what it needs] */
      ask.addEventListener("click",()=>{naTake(root);if(k>=n)return;const r=s.rungs[k];
        const [a,b]=up(ids[k],ids[k+1]),ia=ids.indexOf(a),ib=ids.indexOf(b);
        root.querySelector(`.xnode[data-id="${ids[k+1]}"]`).classList.remove("na-hid");root.querySelector(`.na-slot[data-k="${k+1}"]`).classList.add("na-found");
        const sg=pos[ib][0]>pos[ia][0]?1:-1,p=[pos[ia][0]+sg*((ia?Z:TZ)/2+6),pos[ia][1]],q=[pos[ib][0]-sg*((ib?Z:TZ)/2+12),pos[ib][1]];   /* from side to side: the arrow never crosses a name */
        const g=document.createElementNS(svgNS,"g");g.setAttribute("class","xedge lit na-arr");g.innerHTML=flow(curve(p,q,14),"");root.querySelector("#naArrows").appendChild(g);
        say(root,a,r.short);cap(r.because);mood(root,ids[k+1],"laugh");sfx("rung",{n:k,down:s.mode==="why"});k++;
        if(k>=n){ask.hidden=true;setTimeout(()=>{if(!root.isConnected)return;cap(s.end_say);sfx("ready");if(!grown())sparkles();reset.hidden=false;},1900);}});
      reset.addEventListener("click",()=>{k=0;root.querySelector("#naArrows").innerHTML="";root.querySelectorAll(".na-slot").forEach(x=>x.classList.remove("na-found"));ids.slice(1).forEach(id=>root.querySelector(`.xnode[data-id="${id}"]`).classList.add("na-hid"));
        say(root,null,"");ask.hidden=false;reset.hidden=true;cap(s.steps[0]);sfx("flip");});}};}

SCENES.recipe=sceneRecipe;SNAME.recipe="🧪 الوصفة";SCENES.connect=sceneConnect;SNAME.connect="✏️ ارسم الأسهم";SCENES.compare=sceneCompare;SNAME.compare="⚖️ قارن";
SCENES.teach=sceneTeach;SNAME.teach="🧑‍🏫 علّم صاحبك";SCENES.ladder=sceneLadder;SNAME.ladder="🪜 السلّم";
