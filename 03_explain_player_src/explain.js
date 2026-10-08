/* ======================= THE EXPLANATION PLAYER — clear: one path, one place for words, one thing moving at a time ======================= */
let EG=0,EL=0,POS=0,STEP=0;   /* book, lesson, position in the lesson's path of scenes, step inside the scene */
const syncCore=()=>{G=EG;L=EL;};
const exName=id=>graph().names[id]||id;
const iconOf=id=>(lesson().icons||{})[id];
const V=()=>{const q=document.getElementById("q");return !!q&&q.clientWidth<600;};   /* narrow screen → scenes go top-to-bottom */
function pathOf(){const l=lesson();const p=[{c:-1,s:l.overview}];if(l.world)p.push({c:-1,s:l.world});if(l.assemble)p.push({c:-1,s:l.assemble});l.concepts.forEach((c,ci)=>c.scenes.forEach(s=>p.push({c:ci,s})));return p;}
function node(id,x,y,size,mood,extra){const ic=iconOf(id);let art=ic?artSVG(ic,""):null;
  if(!art)art=`<svg class="ch" viewBox="0 0 100 100">${ARTS.blob(colorOf(id))}</svg>`;
  art=art.replace("<svg ",`<svg width="${size}" height="${size}" x="${-size/2}" y="${-size/2}" `);
  return `<g class="xnode ${extra||""}" data-id="${id}" transform="translate(${x} ${y})" tabindex="0" role="button" aria-label="${exName(id)}">
    <g class="xbody" data-mood="${mood||"happy"}">${art}</g><text class="xname" y="${size/2+18}" text-anchor="middle">${exName(id)}</text><g class="xsay"></g></g>`;}
/* split what a character says into short lines (≈22 letters); never cut a word; very long → «…» at a word boundary */
function lines(t,n,max){n=n||22;max=max||4;const w=String(t).split(/\s+/).filter(Boolean);const out=[""];let cut=false;
  for(const x of w){const cur=out[out.length-1];if(!cur||(cur+" "+x).length<=n)out[out.length-1]=(cur+" "+x).trim();else if(out.length<max)out.push(x);else{cut=true;break;}}
  if(cut)out[out.length-1]=out[out.length-1].replace(/\s+\S+$/,"")+" …";return out;}
/* 💬 the speech bubble lives in ITS OWN top layer (#saylayer, always the last thing in the picture):
   · above the video spotlight → never dimmed, never half-dark;
   · above the other characters → never hidden behind one;
   · it always stays INSIDE the current frame (also when the camera is zoomed in), with a tail pointing to who speaks;
   · it keeps the same size on the screen while the camera moves. */
function sayLayer(svg){let g=svg.querySelector(":scope > #saylayer");if(!g){g=document.createElementNS(svgNS,"g");g.id="saylayer";g.setAttribute("pointer-events","none");}
  if(svg.lastElementChild!==g)svg.appendChild(g);return g;}
function nodeSpot(svg,nd){   /* the speaker's centre and radius in picture units (works inside moved groups, too) */
  const sz=parseFloat((nd.querySelector("svg")||{getAttribute:()=>70}).getAttribute("width"))||70;
  const m=(nd.getAttribute("transform")||"").match(/translate\(([-\d.]+)[ ,]+([-\d.]+)/)||[0,0,0];
  let x=+m[1],y=+m[2];const P=nd.parentNode&&nd.parentNode.getScreenCTM?nd.parentNode.getScreenCTM():null,S=svg.getScreenCTM();
  if(P&&S){const pt=svg.createSVGPoint();pt.x=x;pt.y=y;const q=pt.matrixTransform(S.inverse().multiply(P));x=q.x;y=q.y;}
  return {x,y,r:sz/2};}
function placeBubble(svg){const g=svg.querySelector(":scope > #saylayer .bub");if(!g||!svg.__lastSay)return;
  const nd=svg.querySelector(`.xnode[data-id="${svg.__lastSay[0]}"]`);if(!nd){g.remove();return;}
  const vb=svg.viewBox.baseVal,F=FULL||[vb.x,vb.y,vb.width,vb.height],shown=svg.getBoundingClientRect().width||F[2];
  const k0=Math.min(2.2,Math.max(1,13/(13.5*shown/F[2]))),k=k0*Math.min(1,vb.width/F[2]);   /* small screen → bigger bubble (text ≥13px); zoomed in → smaller (looks the same) */
  const w=+g.dataset.w,h=+g.dataset.h,M=8*k,T=9;
  const n=nodeSpot(svg,nd),bw=w*k,bh=(h+T)*k;
  let top=n.y-n.r-2*k-bh,down=false;                                               /* first choice: above the speaker */
  if(top<vb.y+M){const below=n.y+n.r+24;if(below+bh<=vb.y+vb.height-M){top=below;down=true;}else top=vb.y+M;}   /* no room → below the name */
  const left=Math.max(vb.x+M,Math.min(vb.x+vb.width-M-bw,n.x-bw/2));
  const tx=Math.max(16,Math.min(w-16,(n.x-left)/k));                              /* the tail points at the speaker */
  const tail=down?`M${tx-8} ${T+2} L${tx} 0 L${tx+8} ${T+2}`:`M${tx-8} ${h-2} L${tx} ${h+T} L${tx+8} ${h-2}`;
  g.querySelector(".btail").setAttribute("d",tail);g.querySelector(".bin").setAttribute("transform",`translate(0 ${down?T:0})`);
  g.setAttribute("transform",`translate(${left.toFixed(1)} ${top.toFixed(1)}) scale(${k.toFixed(3)})`);}
function say(svg,id,text){text=VOICE(text);const layer=sayLayer(svg);layer.innerHTML="";svg.querySelectorAll(".xsay").forEach(x=>x.innerHTML="");   /* 👥 said the way this age talks */
  if(!text||!id){svg.__lastSay=null;return;}const nd=svg.querySelector(`.xnode[data-id="${id}"]`);if(!nd)return;svg.__lastSay=[id,text];
  const ls=lines(text),LH=19,h=14+ls.length*LH;
  layer.innerHTML=`<g class="bub" data-for="${id}"><g class="bin"><rect x="0" y="0" height="${h}" rx="13"/>${ls.map((l,i)=>`<text y="${22+i*LH}" text-anchor="middle">${l}</text>`).join("")}</g><path class="btail"/></g>`;
  const g=layer.querySelector(".bub");let tw=0;g.querySelectorAll("text").forEach(t=>{try{tw=Math.max(tw,t.getComputedTextLength());}catch(e){}});
  if(!tw)tw=Math.max(...ls.map(l=>l.length))*8.6;                                    /* (not drawn yet: measure generously) */
  const w=Math.max(70,Math.ceil(tw)+30);g.querySelector("rect").setAttribute("width",w);g.querySelectorAll("text").forEach(t=>t.setAttribute("x",w/2));
  g.dataset.w=w;g.dataset.h=h;placeBubble(svg);}
function mood(svg,id,m){const b=svg.querySelector(`.xnode[data-id="${id}"] .xbody`);if(b)b.dataset.mood=m;}
function focus(svg,ids){const keep=new Set(ids||[]);svg.querySelectorAll(".xnode").forEach(n=>n.classList.toggle("dim",!!ids&&!keep.has(n.dataset.id)));}
const curve=(a,b,bend)=>{const L=Math.hypot(b[0]-a[0],b[1]-a[1]),mx=(a[0]+b[0])/2,my=(a[1]+b[1])/2-(bend||0)*Math.min(1,L/220);return `M${a[0]} ${a[1]} Q${mx} ${my} ${b[0]} ${b[1]}`;};   /* batch 29: a short arrow is (almost) straight, never «bent» */
/* a «needs» arrow: it reads like the sentence «الساق بيحتاج الجذر» — from the one who needs to what it needs; nothing flows on it */
function flow(d,cls,dots,label){const m=d.match(/M([-\d.]+) ([-\d.]+) Q([-\d.]+) ([-\d.]+) ([-\d.]+) ([-\d.]+)/);let t="";
  if(m&&label!==false){const x=(+m[1]+2*+m[3]+ +m[5])/4,y=(+m[2]+2*+m[4]+ +m[6])/4;const nw=ARROW_WORD(),hw=Math.max(24,nw.length*3.6+10);
    if(Math.hypot(m[5]-m[1],m[6]-m[2])<2*hw+24)return `<path class="xarrow ${cls||""}" d="${d}" marker-end="url(#xhead)"/>`;   /* batch 29: no room → no word ON the arrow (the legend says what it means) */
    t=`<g class="needs" transform="translate(${x} ${y})"><rect x="${-hw}" y="-11" width="${2*hw}" height="20" rx="10"/><text y="4" text-anchor="middle">${nw}</text></g>`;}   /* «بيعتمد على» for the bigger grades */
  return `<path class="xarrow ${cls||""}" d="${d}" marker-end="url(#xhead)"/>${t}`;}
const DEFS=`<defs><marker id="xhead" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="14" markerHeight="14" markerUnits="userSpaceOnUse" orient="auto-start-reverse"><path d="M1 1 L9 5 L1 9" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></marker></defs>`;
const edgeEnds=(a,b,r)=>{const dx=b[0]-a[0],dy=b[1]-a[1],d=Math.hypot(dx,dy)||1;return [[a[0]+dx/d*r,a[1]+dy/d*r],[b[0]-dx/d*r,b[1]-dy/d*r]];};

/* 🗺️ the big picture: in learning order, numbered, columns sorted to avoid crossings */
function sceneOverview(s){const v=V(),lv=s.levels;const cols={};s.concepts.forEach(c=>{(cols[lv[c]]=cols[lv[c]]||[]).push(c);});
  const L=Object.keys(cols).map(Number).sort((a,b)=>a-b);
  const W=v?380:Math.max(600,L.length*190),H=v?Math.max(420,L.length*150+80):Math.max(320,Math.max(...L.map(k=>cols[k].length))*140+60);const pos={};
  L.forEach((k,i)=>{if(i){const m=x=>{const ps=s.edges.filter(e=>e[1]===x&&pos[e[0]]).map(e=>v?W-pos[e[0]][0]:pos[e[0]][1]);return ps.length?ps.reduce((a,b)=>a+b,0)/ps.length:(v?W/2:H/2);};cols[k].sort((a,b)=>m(a)-m(b));}
    const n=cols[k].length;cols[k].forEach((c,j)=>{const along=L.length===1?0.5:i/(L.length-1),across=(j+1)/(n+1);pos[c]=v?[(1-across)*W,70+along*(H-150)]:[W-90-along*(W-180),across*H];});});
  let num=0;const order=[];L.forEach(k=>cols[k].forEach(c=>order.push(c)));
  const svg=`<svg class="xstage" id="xs" viewBox="0 0 ${W} ${H}" data-bubble="78" role="img" aria-label="الصورة الكبيرة للدرس">${DEFS}
    ${s.edges.map(([a,b])=>{const [p,q]=edgeEnds(pos[b],pos[a],46);return `<g class="xedge" data-a="${a}" data-b="${b}">${flow(curve(p,q,v?0:16),"",0,false)}</g>`;}).join("")}
    ${order.map(c=>node(c,pos[c][0],pos[c][1],72)+`<g class="xnum" transform="translate(${pos[c][0]+30} ${pos[c][1]-34})"><circle r="12"/><text y="5" text-anchor="middle">${++num}</text></g>`).join("")}</svg>`;
  return {svg,wire:root=>{root.querySelectorAll(".xnode").forEach(n=>n.addEventListener("click",()=>{const id=n.dataset.id;sfx("pop");
      const linked=new Set([id]);root.querySelectorAll(".xedge").forEach(e=>{const on=e.dataset.a===id||e.dataset.b===id;e.classList.toggle("dim",!on);e.classList.toggle("lit",on);if(on){linked.add(e.dataset.a);linked.add(e.dataset.b);}});
      focus(root,[...linked]);const ins=s.edges.filter(e=>e[1]===id).map(e=>"«"+exName(e[0])+"»"),outs=s.edges.filter(e=>e[0]===id).map(e=>"«"+exName(e[1])+"»");
      cap((ins.length?"«"+exName(id)+"» بيحتاج "+ins.join(" و")+". ":"«"+exName(id)+"» من البداية، ما بيحتاج إشي قبله. ")+(outs.length?"وبيحتاجه "+outs.join(" و")+".":""));}));},
    onStep:(root,k)=>{focus(root,null);root.querySelectorAll(".xedge").forEach(e=>{e.classList.remove("dim");e.classList.toggle("lit",k===1);});}};}

/* 👋 meet: blue = what comes IN, green = what goes OUT */
function sceneMeet(s){const v=V(),ins=s.ins.slice(0,2),outs=s.outs.slice(0,2);
  const W=v?380:660,H=v?560:360,c=v?[190,285]:[330,190];const spread=(n,i,a,b)=>n===1?(a+b)/2:a+i*((b-a)/(n-1));
  const inP=ins.map((x,i)=>v?[spread(ins.length,i,290,90),78]:[W-92,spread(ins.length,i,90,290)]);
  const outP=outs.map((x,i)=>v?[spread(outs.length,i,290,90),H-78]:[92,spread(outs.length,i,90,290)]);
  const svg=`<svg class="xstage" id="xs" viewBox="0 0 ${W} ${H}" data-bubble="${v?92:96}" role="img" aria-label="تعرّف على ${exName(s.target)}">${DEFS}
    ${ins.map((x,i)=>{const [p,q]=edgeEnds(c,inP[i],v?58:70);return `<g class="xedge in" data-a="${x}">${flow(curve(p,q,0),"in")}</g>`;}).join("")}
    ${outs.map((x,i)=>{const [p,q]=edgeEnds(outP[i],c,v?58:70);return `<g class="xedge out" data-b="${x}">${flow(curve(p,q,0),"out")}</g>`;}).join("")}
    ${node(s.target,c[0],c[1],v?110:128,"happy","star")}
    ${ins.map((x,i)=>node(x,inP[i][0],inP[i][1],70,"happy","side in")).join("")}${outs.map((x,i)=>node(x,outP[i][0],outP[i][1],70,"happy","side out")).join("")}</svg>
    <div class="legend"><span class="lg">${ARROW_LEGEND()}</span></div>`;
  return {svg,wire:root=>{root.querySelectorAll(".xnode.side").forEach(n=>n.addEventListener("click",()=>{const id=n.dataset.id;sfx("pop");mood(root,id,"laugh");setTimeout(()=>mood(root,id,"happy"),1200);
      say(root,id,ins.includes(id)?"«"+exName(s.target)+"» بيحتاج «"+exName(id)+"»":"«"+exName(id)+"» بيحتاج «"+exName(s.target)+"»");
      focus(root,[id,s.target]);root.querySelectorAll(".xedge").forEach(e=>{const on=e.dataset.a===id||e.dataset.b===id;e.classList.toggle("lit",on);e.classList.toggle("dim",!on);});
      cap((s.roles||{})[id]?"📌 "+s.roles[id]:"");}));},
    onStep:(root,k)=>{const f=(s.focus||[])[k]||"target";root.querySelectorAll(".xedge").forEach(e=>e.classList.remove("lit","dim"));say(root,null,"");
      if(k===0){focus(root,null);say(root,s.target,"أهلاً! 👋");mood(root,s.target,"laugh");}
      else if(f==="ins"){focus(root,[s.target].concat(ins));root.querySelectorAll(".xedge.out").forEach(e=>e.classList.add("dim"));root.querySelectorAll(".xedge.in").forEach(e=>e.classList.add("lit"));}
      else if(f.startsWith("out:")){const x=f.slice(4);focus(root,[s.target,x]);root.querySelectorAll(".xedge").forEach(e=>{const on=e.dataset.b===x;e.classList.toggle("lit",on);e.classList.toggle("dim",!on);});mood(root,x,"laugh");}
      else{focus(root,[s.target]);mood(root,s.target,"happy");}}};}

/* 🚶 journey — natural:
   · a thing that REALLY travels (water, air, light) moves ALONG the road itself, station by station;
   · stages (flower → pollination → fruit) do not travel: tap the next stage, the road lights up from the one it needs, and it wakes up. */
function sceneJourney(s){const v=V(),n=s.route.length;
  const W=v?380:Math.max(640,n*160),H=v?Math.max(460,n*135+60):320;
  const pos=s.route.map((x,i)=>v?[i%2?120:260,90+i*((H-160)/(n-1))]:[W-90-i*((W-180)/(n-1)),200+(i%2?-24:24)]);
  const segs=pos.slice(1).map((p,i)=>{const [a,b]=edgeEnds(pos[i],p,46);return curve(a,b,v?0:26);});
  const mover=s.traveller!=="spark";const ti=mover?iconOf(s.traveller):null;
  const tart=mover?((ti?artSVG(ti,""):null)||`<svg class="ch" viewBox="0 0 100 100">${ARTS.blob(colorOf(s.traveller))}</svg>`):"";
  const svg=`<svg class="xstage" id="xs" viewBox="0 0 ${W} ${H}" data-bubble="84" role="img" aria-label="رحلة">${DEFS}
    ${segs.map((d,i)=>`<path class="xroad" data-i="${i}" d="${d}"/><path class="xglow" data-i="${i}" d="${d}"/>`).join("")}
    ${s.route.map((x,i)=>node(x,pos[i][0],pos[i][1],76,i===0?"happy":"sad",i===0?"woke":"sleep")).join("")}
    ${mover?`<g id="trav"><g class="xbody" data-mood="laugh">${tart.replace("<svg ",'<svg width="40" height="40" x="-20" y="-20" ')}</g></g>`:""}</svg>`;
  let at=0,busy=false;
  return {svg,wire:root=>{const trav=root.querySelector("#trav");
      root.querySelectorAll(".xglow").forEach(g=>{const L=g.getTotalLength();g.style.strokeDasharray=L;g.style.strokeDashoffset=L;});
      const road=i=>root.querySelector(`.xglow[data-i="${i}"]`);
      if(trav){const p0=road(0).getPointAtLength(0);trav.setAttribute("transform",`translate(${p0.x} ${p0.y})`);}
      const arrive=i=>{at=i;busy=false;root.querySelector(`.xroad[data-i="${i-1}"]`).classList.add("lit");
        const nd=root.querySelector(`.xnode[data-id="${s.route[i]}"]`);nd.classList.remove("sleep");nd.classList.add("woke");mood(root,s.route[i],"laugh");sfx("pop");
        say(root,s.route[i],mover?"وصلتني! 😄":"صار دوري! 😄");cap("📍 "+s.stops[i].say);
        if(i===n-1){sfx("tada");sparkles();setTimeout(()=>cap("🏁 "+(mover?"«"+exName(s.traveller)+"» وصل لآخر محطة: ":"صارت كل المراحل: ")+s.route.map(exName).join(" ← ")),1600);}};
      const go=i=>{if(busy||i!==at+1||i>=n){if(!busy&&i>at+1)cap("خطوة خطوة 🙂 الجاي «"+exName(s.route[at+1])+"»، لأنه "+(s.stops[at+1].say||""));return;}
        busy=true;sfx("step");const g=road(i-1),L=g.getTotalLength();let t=0;const t0=performance.now();
        const step=()=>{if(!g.isConnected)return;t=Math.min(1,(performance.now()-t0)/850);   /* by the clock: same on a slow phone */g.style.strokeDashoffset=String(L*(1-t));
          if(trav){const pt=g.getPointAtLength(L*t);trav.setAttribute("transform",`translate(${pt.x} ${pt.y})`);}
          if(t<1&&!reduce)requestAnimationFrame(step);else{g.style.strokeDashoffset="0";arrive(i);}};step();};
      root.querySelectorAll(".xnode").forEach((nd,i)=>nd.addEventListener("click",()=>go(i)));
      if(trav)trav.addEventListener("pointerdown",e=>{if(busy||at>=n-1)return;e.preventDefault();go(at+1);});
      say(root,s.route[0],mover?"اكبس المحطة الجاية، وأنا بمشي بالطريق 👣":"اكبس المرحلة الجاية 👆");
      cap(mover?"«"+exName(s.traveller)+"» رح يمشي بالطريق من «"+exName(s.route[0])+"» لـ«"+exName(s.route[n-1])+"».":"كل مرحلة بتصحى لما يكون اللي بتحتاجه موجود.");}};}

/* 🔮 what if: one switch; the domino follows the arrows */
function sceneWhatIf(s){const v=V(),all=[s.target].concat(s.affected),n=all.length;
  const W=v?380:Math.max(640,(n+1)*150),H=v?Math.max(460,n*130+80):330;const pos={};
  all.forEach((x,i)=>pos[x]=v?[i%2?130:250,80+i*((H-200)/Math.max(1,n-1))]:[W-90-i*((W-250)/Math.max(1,n-1)),190]);
  (s.calm||[]).forEach(x=>pos[x]=v?[W/2,H-60]:[70,90]);
  const svg=`<svg class="xstage" id="xs" viewBox="0 0 ${W} ${H}" data-bubble="78" role="img" aria-label="شو بيصير لو">${DEFS}
    ${s.edges.map(([a,b])=>{const [p,q]=edgeEnds(pos[b],pos[a],48);return `<g class="xedge" data-b="${b}">${flow(curve(p,q,v?0:22),"")}</g>`;}).join("")}
    ${all.map((x,i)=>node(x,pos[x][0],pos[x][1],i===0?96:74,"happy",i===0?"star":"")).join("")}${(s.calm||[]).map(x=>node(x,pos[x][0],pos[x][1],58,"happy","calm")).join("")}</svg>
    <div class="xswitch"><button class="switch on" id="sw" role="switch" aria-checked="true"><span class="knob"></span></button><b id="swl">«${exName(s.target)}» شغّال ✅</b></div>`;
  let on=true,busy=false;
  return {svg,wire:root=>{const sw=document.getElementById("sw");
      sw.addEventListener("click",()=>{if(busy)return;busy=true;on=!on;sw.classList.toggle("on",on);sw.setAttribute("aria-checked",String(on));
        document.getElementById("swl").textContent=on?"«"+exName(s.target)+"» شغّال ✅":"«"+exName(s.target)+"» مطفي ⛔";
        root.querySelector(`.xnode[data-id="${s.target}"]`).classList.toggle("gone",!on);sfx(on?"bloom":"whoosh");say(root,null,"");
        s.affected.forEach((x,i)=>setTimeout(()=>{if(!root.isConnected)return;root.querySelector(`.xnode[data-id="${x}"]`).classList.toggle("tired",!on);mood(root,x,on?"laugh":"sad");
            const e=root.querySelector(`.xedge[data-b="${x}"]`);if(e)e.classList.toggle("dim",!on);say(root,x,on?"رجعت! 😄":(i===0?"وين راح؟ 😢":"وأنا كمان! 😢"));sfx(on?"pop":"bad");
            if(i===s.affected.length-1){busy=false;cap(on?"رجع «"+exName(s.target)+"»، فرجعوا كلهم مبسوطين 😄":"شايف؟ كل واحد بيحتاج اللي قبله، فتعبوا ورا بعض."+((s.calm||[]).length?" بس «"+exName(s.calm[0])+"» ما بيحتاجه، فضل مبسوط 😎":""));}},500+i*700));});}};}

const SCENES={overview:sceneOverview,meet:sceneMeet,journey:sceneJourney,what_if:sceneWhatIf};
const SNAME={overview:"🗺️ الصورة الكبيرة",meet:"👋 تعرّف عليّ",journey:"🚶 الرحلة",what_if:"🔮 شو بيصير لو"};
let current=null;
function renderSide2(){let lastSt=null;   /* 🆕 batch 29: the books are grouped by age stage, each group under its own heading */
  document.getElementById("side").innerHTML=DATA.graphs.map((g,gi)=>{const st=(g.audience||{}).stage,S=STAGES[st];
    const head=S&&st!==lastSt?`<h2 class="stghead" id="stg-${st}">${S.icon} ${S.label} <small>(${S.grades})</small></h2>`:"";lastSt=st;return head+`<h3>📘 ${g.title}</h3>`+g.lessons.map((l,li)=>`<button class="les" data-g="${gi}" data-l="${li}" ${gi===EG&&li===EL?'aria-current="true"':""}><span>${l.lesson_title}</span><small>${l.concepts.length} مفاهيم</small></button>`).join("");}).join("");
  document.querySelectorAll("#side .les").forEach(b=>b.addEventListener("click",()=>{EG=+b.dataset.g;EL=+b.dataset.l;POS=0;STEP=0;renderAll2();window.scrollTo({top:0});}));}
function renderTop(){const l=lesson();document.body.classList.toggle("skin-garden",l.theme==="garden");
  document.getElementById("welcome").innerHTML=stageWelcome(l)+stageSwitch();   /* 👥 the welcome grows up with the student (stage.js) */
  const p=pathOf(),here=p[POS];const stops=[{t:sceneName("overview").replace(/^\S+\s/,""),i:"🗺️",c:-1}].concat(l.concepts.map((c,ci)=>({t:c.title,i:iconOf(c.concept_id)||"🔹",c:ci})));
  document.getElementById("prog").innerHTML=`<div class="pbar"><i style="width:${Math.round(POS/(p.length-1||1)*100)}%"></i></div>
    <div class="pstops">${stops.map(x=>`<button class="pstop ${x.c===here.c?"on":""} ${x.c<here.c?"done":""}" data-c="${x.c}" title="${x.t}">${alive(x.i)}<small>${x.t}</small></button>`).join("")}</div>
    <div class="where">${sceneName(here.s.kind)}${here.c>=0?" · «"+l.concepts[here.c].title+"»":""}</div>`;
  document.querySelectorAll("#prog .pstop").forEach(b=>b.addEventListener("click",()=>{const c=+b.dataset.c;POS=pathOf().findIndex(x=>x.c===c);STEP=0;renderAll2();}));}
function renderScene(){const p=pathOf(),s=p[POS].s;const box=document.getElementById("q");stopVideo(null);TOUCHED=false;lastV=V();
  current=SCENES[s.kind](s);
  box.innerHTML=`<div class="xwrap">${current.svg}</div>
    <div class="narr"><div class="nline" id="cap" aria-live="polite"></div>
      <div class="nctl"><button class="chipbtn" id="play" aria-pressed="true">⏸ وقّف</button><button class="chipbtn" id="whyb">${ui("why")}</button></div></div>
    ${s.paragraph?`<div class="why" id="why" hidden><b>💡 ليش؟</b><p>${richText(s.paragraph)}</p></div>`:""}
    <div class="tryit" id="tryit" hidden>${ui("tryit")}</div>
    <div class="stepper"><button class="btn ghost" id="prev">→ رجوع</button><span class="dots">${s.steps.map((_,i)=>`<i class="${i===STEP?"on":""}"></i>`).join("")}</span><button class="btn" id="next">${ui("next")}</button></div>`;
  const root=document.getElementById("xs");const vb=root.viewBox.baseVal;FULL=[vb.x,vb.y,vb.width,vb.height];
  current.wire(root);giggles(root);
  document.querySelectorAll("#why .kw").forEach(k=>k.addEventListener("click",()=>{const nd=root.querySelector(`.xnode[data-id="${k.dataset.id}"]`);if(nd){focus(root,[k.dataset.id]);say(root,k.dataset.id,"أنا هون! 👋");}showTip(k);}));
  const show=()=>{cap(s.steps[STEP]||"");document.querySelectorAll(".dots i").forEach((d,i)=>d.classList.toggle("on",i===STEP));
    document.getElementById("prev").disabled=POS===0&&STEP===0;const last=STEP>=s.steps.length-1,end=POS>=p.length-1;
    document.getElementById("next").textContent=!last?ui("next"):end?"✓ خلصت الدرس":"المشهد الجاي ←";if(current.onStep)current.onStep(root,STEP);
    if(VIDEO){videoStep(root,s,STEP);clearTimeout(vTimer);const words=(s.steps[STEP]||"").split(/\s+/).length;
      vTimer=setTimeout(()=>{if(!VIDEO)return;if(STEP<s.steps.length-1){STEP++;show();}else endOfScene(root);},Math.max(3200,words*420,current.stepMs||0));}   /* a scene can ask for more time (the lens tour) */
    else if(last)endOfScene(root);};
  const manual=()=>{if(VIDEO)stopVideo(root);};
  document.getElementById("prev").addEventListener("click",()=>{manual();if(STEP>0){STEP--;sfx("flip");show();}else if(POS>0){POS--;STEP=0;renderAll2();}});
  document.getElementById("next").addEventListener("click",()=>{manual();if(STEP<s.steps.length-1){STEP++;sfx("flip");show();}else if(POS<p.length-1){POS++;STEP=0;renderAll2();}else{sfx("tada");sparkles();cap("🎉 فهمت درس «"+lesson().lesson_title+"»! اختار درس ثاني من القائمة.");}});
  document.getElementById("play").addEventListener("click",()=>{if(VIDEO){stopVideo(root);}else{VIDEO=true;const pb=document.getElementById("play");pb.textContent="⏸ وقّف";pb.setAttribute("aria-pressed","true");
      document.getElementById("why")&&(document.getElementById("why").hidden=true);document.getElementById("tryit").hidden=true;STEP=0;show();}});
  document.getElementById("whyb").addEventListener("click",()=>{const w=document.getElementById("why");if(w){w.hidden=!w.hidden;sfx("flip");}});
  root.addEventListener("pointerdown",()=>{if(!VIDEO)return;VIDEO=false;clearTimeout(vTimer);spotlight(root,null);   /* the student touches the picture → it becomes a playground */
      const pb=document.getElementById("play");if(pb){pb.textContent="▶️ شغّل";pb.setAttribute("aria-pressed","false");}
      setTimeout(()=>camera(root,null),420);},true);                          /* the camera waits until the tap is finished, so the tap never misses */
  VIDEO=!reduce;if(!VIDEO){const pb=document.getElementById("play");pb.textContent="▶️ شغّل";pb.setAttribute("aria-pressed","false");}
  show();}
function renderAll2(){syncCore();renderSide2();renderTop();applyStage();renderScene();}
let lastV=null,rzT=0,TOUCHED=false;   /* TOUCHED: the student already did something in this scene (dragged, switched, drew, chose...) */
document.getElementById("q").addEventListener("pointerdown",e=>{if(!e.target.closest("#play,#prev,#next,#whyb"))TOUCHED=true;},true);
document.getElementById("q").addEventListener("keydown",e=>{if(!e.target.closest("#play,#prev,#next,#whyb"))TOUCHED=true;},true);
window.addEventListener("resize",()=>{clearTimeout(rzT);rzT=setTimeout(()=>{const v=V(),xw=document.querySelector("#q .xwrap");
  if(v===lastV){if(xw)xw.classList.remove("laykeep");return;}
  if(!TOUCHED){renderScene();return;}                                    /* nothing done yet: draw it again in the new layout */
  if(xw)xw.classList.toggle("laykeep",lastV&&!v);},250);});             /* the phone turned AFTER the student did something: keep the work (old layout, good size) */
document.getElementById("soundBtn").addEventListener("click",()=>{soundOn=!soundOn;document.getElementById("soundBtn").textContent=soundOn?"🔊 الصوت":"🔇 الصوت";});
renderAll2();lastV=V();
