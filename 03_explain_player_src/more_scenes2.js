/* ===== 🧩 build · 🗣️ talk · 🎚️ slide · 🔍 look closer — explanation activities (nothing graded, no right/wrong) ===== */
function artOf(id,size){const ic=iconOf(id);let a=(ic?artSVG(ic,""):null)||`<svg class="ch" viewBox="0 0 100 100">${ARTS.blob(colorOf(id))}</svg>`;return a.replace("<svg ",`<svg width="${size}" height="${size}" x="${-size/2}" y="${-size/2}" `);}
/* 🧩 build the lesson's picture: each character goes to ITS shadow (a puzzle, not a test); it wakes up and says what it is */
function sceneAssemble(s){const v=V(),lv=s.levels;const cols={};s.concepts.forEach(c=>{(cols[lv[c]]=cols[lv[c]]||[]).push(c);});const L=Object.keys(cols).map(Number).sort((a,b)=>a-b);
  const N=s.concepts.length,per=N<=6?3:4,rowsN=Math.ceil(N/per),trayH=rowsN*92+20;
  const W=v?380:640,H=v?50+(L.length-1)*104+90+trayH+10:400;const trayTop=H-trayH-10;const pos={};
  L.forEach((k,i)=>{const n=cols[k].length;cols[k].forEach((c,j)=>{const al=L.length===1?.5:i/(L.length-1),ac=(j+1)/(n+1);pos[c]=v?[(1-ac)*W,56+i*104]:[W-70-al*(W-70-310),40+ac*(H-60)];});});
  const oneCol=!v&&N<=4,step1=Math.min(95,(H-120)/Math.max(1,N-1));   /* ≤ 4 pieces: one column, so long names («معادلة الخط المستقيم») never touch */
  const tray=s.concepts.map((c,i)=>v?[W-W*((i%per)+0.5)/per,trayTop+48+Math.floor(i/per)*92]:oneCol?[120,56+i*step1]:[80+(i%2)*90,60+Math.floor(i/2)*95]);
  const svg=`<svg class="xstage" id="xs" viewBox="0 0 ${W} ${H}" data-bubble="70" role="img" aria-label="ركّب المشهد">${DEFS}<g id="asArrows"></g>
    ${s.concepts.map(c=>`<g class="shadow" data-id="${c}" transform="translate(${pos[c][0]} ${pos[c][1]})">${artOf(c,74)}</g>`).join("")}
    ${s.concepts.map(c=>{const L=lines(exName(c),11,2);return `<text class="xname astag" data-for="${c}" x="${pos[c][0]}" y="${pos[c][1]+50}" text-anchor="middle">${L.map((t,i)=>`<tspan x="${pos[c][0]}" dy="${i?14:0}">${t}</tspan>`).join("")}</text>`;}).join("")}
    ${!v?`<rect x="20" y="20" width="200" height="${H-40}" rx="16" class="tray"/>`:`<rect x="10" y="${trayTop}" width="${W-20}" height="${trayH}" rx="16" class="tray"/>`}
    ${s.concepts.map((c,i)=>node(c,tray[i][0],tray[i][1],64,"happy","piece").replace('<g class="xbody"','<rect class="ashit" x="-38" y="-38" width="76" height="76" fill="transparent"/><g class="xbody"')).join("")}</svg>`;   /* the whole piece can be grabbed, not only its painted parts */
  return {svg,wire:root=>{const placed=new Set();const R=()=>root.getBoundingClientRect();
      const arrows=()=>{root.querySelector("#asArrows").innerHTML=s.edges.filter(([a,b])=>placed.has(a)&&placed.has(b)).map(([a,b])=>{const [p,q]=edgeEnds(pos[b],pos[a],44);return `<g class="xedge lit">${flow(curve(p,q,10),"")}</g>`;}).join("");};
      root.querySelectorAll(".xnode.piece").forEach(nd=>{const id=nd.dataset.id;const home=nd.getAttribute("transform");
        nd.addEventListener("pointerdown",e=>{if(placed.has(id))return;e.preventDefault();const r=R(),k=W/r.width;nd.classList.add("lifted");
          const mv=ev=>nd.setAttribute("transform",`translate(${(ev.clientX-r.left)*k} ${(ev.clientY-r.top)*k})`);
          const up=ev=>{window.removeEventListener("pointermove",mv);window.removeEventListener("pointerup",up);nd.classList.remove("lifted");const x=(ev.clientX-r.left)*k,y=(ev.clientY-r.top)*k;const [tx,ty]=pos[id];
            if(Math.hypot(x-tx,y-ty)<70){nd.setAttribute("transform",`translate(${tx} ${ty})`);placed.add(id);nd.classList.add("placed");root.querySelector(`.shadow[data-id="${id}"]`).classList.add("filled");const tg=root.querySelector(`.astag[data-for="${id}"]`);if(tg)tg.classList.add("gone");
              mood(root,id,"laugh");say(root,id,"«"+exName(id)+"»: "+(s.says[id]||""));sfx("pop");arrows();cap("✨ «"+exName(id)+"» "+(s.says[id]||""));
              if(placed.size===s.concepts.length){sfx("tada");sparkles();setTimeout(()=>cap("🎉 ركّبت صورة الدرس كاملة! شوف الأسهم: مين بيحتاج مين."),1400);}}
            else{nd.setAttribute("transform",home);   /* batch 29: dropped on ANOTHER shadow (similar pictures) → say whose place it is */
              const near=s.concepts.filter(c=>!placed.has(c)).map(c=>[c,Math.hypot(x-pos[c][0],y-pos[c][1])]).sort((a,b)=>a[1]-b[1])[0];
              if(near&&near[1]<70&&near[0]!==id){sfx("nope");cap("🙂 هاد مكان «"+exName(near[0])+"». دوّر على اسم «"+exName(id)+"»");}
              else cap("🙂 دوّر على اسم «"+exName(id)+"» تحت ظلّه");}};
          window.addEventListener("pointermove",mv);window.addEventListener("pointerup",up);});});}};}
/* 🗣️ two characters talk; «كمّل ▶» shows the next line; the one talking bounces */
function sceneDialogue(s){const v=V(),W=v?380:640,H=v?340:330;const A=v?[92,215]:[160,200],B=v?[288,215]:[480,200],Z=v?104:120;
  const svg=`<svg class="xstage" id="xs" viewBox="0 0 ${W} ${H}" role="img" aria-label="حوار">${node(s.with,A[0],A[1],Z,"happy")}${node(s.target,B[0],B[1],Z,"happy")}</svg>
    <div class="talk" id="talk"></div><div class="row center"><button class="btn" id="more">كمّل ▶</button></div>`;
  let k=0;return {svg,wire:root=>{const next=()=>{if(k>=s.lines.length){cap("🗣️ خلص الحوار! اكبس «يلا ←» للي بعده.");document.getElementById("more").disabled=true;return;}
        const L=s.lines[k++];const other=L.who===s.target?s.with:s.target;mood(root,L.who,"laugh");mood(root,other,"happy");say(root,L.who,L.say);
        root.querySelectorAll(".xnode").forEach(n=>n.classList.toggle("talking",n.dataset.id===L.who));sfx("pop");
        document.getElementById("talk").insertAdjacentHTML("beforeend",`<div class="msg ${L.who===s.target?"them":"me"}"><b>${exName(L.who)}:</b> ${richText(L.say)}</div>`);const talk=document.getElementById("talk");talk.scrollTop=talk.scrollHeight;cap("🗣️ "+L.say);};
      document.getElementById("more").addEventListener("click",next);next();}};}
/* 🎚️ the magic slider (maths): move it — the picture changes at once — discover the rule */
function sceneSlider(s){const m=s.mode;const W=640,H=300;
  const R=(id,lab,min,max,val,step)=>`<label class="sl"><span>${lab}</span><input type="range" id="${id}" min="${min}" max="${max}" value="${val}" step="${step||1}"><b id="${id}v" dir="ltr">${val}</b></label>`;
  const SCI=["line","motion","accel"].includes(m);   /* 📐 the bigger grades: formulas read left-to-right (y = mx + b) */
  const ctl={add:R("a","المجموعة الأولى",0,9,3)+R("b","الثانية",0,9,4),sub:R("a","عنا",1,12,7)+R("b","بناخد",0,12,3),mul:R("a","صفوف",1,6,3)+R("b","بكل صف",1,8,4),
    div:R("a","المكعبات",1,24,12)+R("b","المجموعات",1,6,3),frac:R("a","نقطّع لـ",2,10,4)+R("b","وناخد",0,10,1),
    line:R("a","الميل m",-3,3,1,0.5)+R("b","المقطع b",-4,4,1),motion:R("a","السرعة (م/ث)",1,10,4)+R("b","الزمن (ث)",0,10,5),accel:R("a","التسارع (م/ث²)",0,4,2,0.5)+R("b","الزمن (ث)",0,8,3)}[m];
  const svg=`<svg class="xstage" id="xs" viewBox="0 0 ${W} ${H}" role="img" aria-label="الشريط السحري"><g id="pic"></g><text id="eq" x="${W/2}" y="${H-18}" text-anchor="middle" class="bigeq" ${SCI?'direction="ltr" unicode-bidi="embed"':""}></text></svg><div class="sliders">${ctl}</div>`;
  const blk=(x,y,c,o)=>`<rect x="${x-13}" y="${y-13}" width="26" height="26" rx="6" fill="${c}" stroke="#3b2a1a" stroke-width="2" opacity="${o||1}" class="pop1"/>`;
  return {svg,wire:root=>{const a=document.getElementById("a"),b=document.getElementById("b");let lastEq="";
      const draw=()=>{let A=parseFloat(a.value),B=parseFloat(b.value);if(m==="sub"&&B>A){B=A;b.value=B;}if(m==="frac"&&B>A){B=A;b.value=B;}document.getElementById("av").textContent=A;document.getElementById("bv").textContent=B;let out="",eq="";
        if(m==="add"){for(let i=0;i<A;i++)out+=blk(400+(i%3)*32,60+Math.floor(i/3)*32,"#7CC6F2");for(let i=0;i<B;i++)out+=blk(150+(i%3)*32,60+Math.floor(i/3)*32,"#F28AA8");eq=`${A} + ${B} = ${A+B}`;}
        if(m==="sub"){for(let i=0;i<A;i++)out+=blk(160+(i%6)*34,70+Math.floor(i/6)*34,"#7CC6F2",i>=A-B?0.2:1);eq=`${A} − ${B} = ${A-B}`;}
        if(m==="mul"){for(let r=0;r<A;r++)for(let c=0;c<B;c++)out+=blk(320-(B-1)*17+c*34,40+r*34,["#7CC6F2","#F28AA8","#6CC27A","#F6C177"][r%4]);eq=`${A} × ${B} = ${A*B}`;}
        if(m==="div"){const per=Math.floor(A/B),rest=A-per*B;for(let g=0;g<B;g++){out+=`<rect x="${40+g*(560/B)}" y="40" width="${560/B-10}" height="170" rx="12" fill="none" stroke="var(--line)" stroke-width="3" stroke-dasharray="6 5"/>`;
            for(let i=0;i<per;i++)out+=blk(40+g*(560/B)+(560/B-10)/2+((i%2)?16:-16),70+Math.floor(i/2)*32,"#F6C177");}eq=`${A} ÷ ${B} = ${per}`+(rest?` (والباقي ${rest})`:"");}
        if(m==="frac"){const cx=320,cy=120,r=95;for(let i=0;i<A;i++){const a0=-Math.PI/2+i*2*Math.PI/A,a1=a0+2*Math.PI/A;const P=t=>[cx+r*Math.cos(t),cy+r*Math.sin(t)];const [x0,y0]=P(a0),[x1,y1]=P(a1);
            out+=`<path d="M${cx} ${cy} L${x0} ${y0} A${r} ${r} 0 ${A===1?1:0} 1 ${x1} ${y1}Z" fill="${i<B?"#E8574A":"#F6C177"}" stroke="#3b2a1a" stroke-width="2.4"/>`;}eq=`${B} / ${A}`+(B&&A%B===0&&B!==A?` = 1/${A/B}`:"");}
        const num=x=>(Math.round(x*10)/10).toString().replace("-","−");                     /* −2.5 */
        const lab=(x,y,t,cls,anc)=>`<text x="${x}" y="${y}" class="${cls||"sclab"}" text-anchor="${anc||"middle"}">${t}</text>`;
        const ltr=(x,y,t,cls,anc)=>`<text x="${x}" y="${y}" class="${cls||"sclab"}" text-anchor="${anc||"middle"}" direction="ltr" unicode-bidi="embed">${t}</text>`;
        let say="";
        if(m==="line"){const k=20,cx=320,cy=140,X=x=>cx+x*k,Y=y=>cy-y*k;                 /* 📈 y = mx + b on a grid: 1 square = 1 */
          out+=`<defs><clipPath id="plotc"><rect x="${X(-7)}" y="${Y(5.5)}" width="${14*k}" height="${11*k}"/></clipPath></defs>`;
          for(let i=-7;i<=7;i++)out+=`<path d="M${X(i)} ${Y(5.5)} V${Y(-5.5)}" class="scgrid"/>`;for(let j=-5;j<=5;j++)out+=`<path d="M${X(-7)} ${Y(j)} H${X(7)}" class="scgrid"/>`;
          out+=`<path d="M${X(-7)} ${cy} H${X(7)} M${cx} ${Y(5.5)} V${Y(-5.5)}" class="scaxis"/>`+ltr(X(7)+10,cy+4,"x","sclab","start")+ltr(cx,Y(5.5)-6,"y");
          out+=`<g clip-path="url(#plotc)"><path d="M${X(-7)} ${Y(A*-7+B)} L${X(7)} ${Y(A*7+B)}" class="scline"/>`;
          if(A!==0)out+=`<path d="M${X(1)} ${Y(A+B)} H${X(2)} V${Y(2*A+B)}" class="scrun"/>`+ltr(X(1.5),Y(A+B)+(A>0?14:-6),"1","scsmall")+ltr(X(2)+8,Y(1.5*A+B)+4,"m = "+num(A),"scsmall","start");
          out+=`</g><circle cx="${cx}" cy="${Y(B)}" r="7" class="scpt"/>`+ltr(cx-10,Y(B)-10,"(0, "+num(B)+")","scsmall","end");
          const mt=A===0?"":A===1?"x":A===-1?"−x":num(A)+"x";eq="y = "+(mt?mt+(B?(B>0?" + ":" − ")+num(Math.abs(B)):""):num(B));
          say=A===0?"الميل صفر: الخط أفقي، ما بيطلع ولا بينزل.":A>0?`الميل ${num(A)}: كل خطوة لليمين، الخط بيطلع ${num(A)}.`:`الميل ${num(A)}: كل خطوة لليمين، الخط بينزل ${num(-A)}.`;
          say+=` والخط بيقطع محور y عند ${num(B)}.`;}
        if(m==="motion"){const x0=60,x1=580,sc=(x1-x0)/100,d=A*B;                               /* 🚗 distance = speed × time (constant speed) */
          out+=`<path d="M${x0} 210 H${x1}" class="scaxis"/>`;for(let i=0;i<=100;i+=10)out+=`<path d="M${x0+i*sc} 204 V216" class="scaxis"/>`+ltr(x0+i*sc,234,i,"scsmall");
          out+=ltr(x1+8,236,"m","scsmall","start")+`<path d="M${x0} 210 H${x0+d*sc}" class="scdone"/>`;
          for(let t=1;t<=B;t++)out+=`<circle cx="${x0+A*t*sc}" cy="190" r="4" class="scghost"/>`+(B<=6?ltr(x0+A*t*sc,178,t+"s","sctiny"):"");
          out+=`<g transform="translate(${x0+d*sc} 168)"><rect x="-26" y="-14" width="44" height="22" rx="7" class="sccar"/><circle cx="-16" cy="10" r="6" class="scwheel"/><circle cx="8" cy="10" r="6" class="scwheel"/></g>`;
          eq=`d = v × t = ${A} × ${B} = ${d} m`;say=`كل ثانية بتقطع ${A} متر (النقاط بنفس البعد)، فبعد ${B} ثانية بتكون قطعت ${d} متر.`;}
        if(m==="accel"){const gx=60,gy=240,gw=250,gh=190,vmax=32,v=A*B,X=t=>gx+t*gw/8,Y=vv=>gy-vv*gh/vmax;   /* 📈 v = a × t, from rest */
          out+=`<path d="M${gx} ${gy-gh-6} V${gy} H${gx+gw+8}" class="scaxis"/>`+ltr(gx+gw+12,gy+4,"t (s)","scsmall","start")+ltr(gx,gy-gh-12,"v (m/s)","scsmall");
          for(let t=0;t<=8;t+=2)out+=ltr(X(t),gy+18,t,"sctiny");for(let vv=0;vv<=32;vv+=8)out+=ltr(gx-8,Y(vv)+4,vv,"sctiny","end");
          out+=`<path d="M${X(0)} ${Y(0)} L${X(8)} ${Y(A*8)}" class="scline" opacity=".25"/><path d="M${X(0)} ${Y(0)} L${X(B)} ${Y(v)}" class="scline"/><circle cx="${X(B)}" cy="${Y(v)}" r="6" class="scpt"/>`;
          const ang=-180+180*Math.min(1,v/vmax),nx=470+70*Math.cos(ang*Math.PI/180),ny=200+70*Math.sin(ang*Math.PI/180);
          out+=`<path d="M400 200 A70 70 0 0 1 540 200" class="scdial"/><path d="M470 200 L${nx.toFixed(1)} ${ny.toFixed(1)}" class="scneedle"/><circle cx="470" cy="200" r="6" class="scpt"/>`+ltr(470,230,v+" m/s","sclab");
          eq=`v = a × t = ${A} × ${B} = ${num(v)} m/s`;say=A===0?"التسارع صفر: السرعة ما بتتغير.":`كل ثانية السرعة بتزيد ${A} م/ث، فبعد ${B} ثواني بتصير ${num(v)} م/ث.`;}
        root.querySelector("#pic").innerHTML=out;root.querySelector("#eq").textContent=eq;if(eq!==lastEq){lastEq=eq;sfx("pop");cap(SCI?say:"🎚️ "+eq);}};
      a.addEventListener("input",draw);b.addEventListener("input",draw);draw();}};}
/* split a sentence into lines of about n characters (max lines; the last one keeps the rest) */
function wrapLines(t,n,max){const w=String(t).split(" ");const out=[""];w.forEach(x=>{const c=out[out.length-1];if((c+" "+x).trim().length>n&&out.length<max)out.push(x);else out[out.length-1]=(c+" "+x).trim();});return out;}
/* 🔍 the magnifying glass: the character is in the fog; where the lens goes, the fog clears and a fact appears */
function sceneLens(s){const v=V(),W=v?380:640,H=v?460:350,c=[W/2,v?220:175];const n=s.facts.length;
  /* the facts sit around the character, AWAY from the edges (a box is 210 wide; on the phone they go top and bottom) */
  const BW=v?(n>2?168:300):210;let spots;
  if(v)spots=s.facts.map((f,i)=>n>2?[i%2?W*0.27:W*0.73,i<2?56:H-60]:[W/2,i?H-58:54]);           /* phone: top and bottom */
  else spots=s.facts.map((f,i)=>{const a=-Math.PI/2+i*2*Math.PI/n;return [c[0]+Math.cos(a)*(W/2-BW/2-24),c[1]+Math.sin(a)*(H/2-52)];});
  const fogs=[[.2,.25,90],[.75,.2,110],[.5,.8,120],[.15,.75,80],[.85,.7,95]];
  const svg=`<svg class="xstage" id="xs" viewBox="0 0 ${W} ${H}" role="img" aria-label="العدسة" style="touch-action:none"><defs><mask id="fogm"><rect width="${W}" height="${H}" fill="white"/><circle id="hole" cx="${c[0]}" cy="${c[1]}" r="72" fill="black"/></mask>
      <radialGradient id="fogg" cx="50%" cy="45%" r="70%"><stop offset="0" style="stop-color:var(--chip)"/><stop offset="1" style="stop-color:var(--line)"/></radialGradient>
      <filter id="fogb" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="18"/></filter></defs>
    ${node(s.target,c[0],c[1],130,"happy","star")}
    <g id="facts">${s.facts.map((f,i)=>{f=VOICE(f);const ls=wrapLines(f,v?(n>2?18:34):22,3);const h=16+ls.length*18;return `<g class="fact" data-i="${i}" transform="translate(${spots[i][0].toFixed(1)} ${spots[i][1].toFixed(1)})"><rect x="${-BW/2}" y="${-h/2}" width="${BW}" height="${h}" rx="12"/>${ls.map((l,j)=>`<text y="${-h/2+21+j*18}" text-anchor="middle">${l}</text>`).join("")}</g>`;}).join("")}</g>
    <g class="fog" mask="url(#fogm)"><rect width="${W}" height="${H}" fill="url(#fogg)"/>${fogs.map(([x,y,r])=>`<ellipse cx="${x*W}" cy="${y*H}" rx="${r}" ry="${r*.6}" style="fill:var(--panel)" opacity=".6" filter="url(#fogb)"/>`).join("")}</g>
    <g id="found"></g>
    <g id="lens" style="pointer-events:none" transform="translate(${c[0]} ${c[1]})"><g class="lenshint"><rect x="-78" y="80" width="156" height="30" rx="15"/><text y="100" text-anchor="middle">👆 حرّك العدسة</text></g><circle r="72" fill="none" stroke="#3b2a1a" stroke-width="6"/><circle r="66" fill="none" stroke="#fff" stroke-width="2" opacity=".6"/><line x1="52" y1="52" x2="96" y2="96" stroke="#7A4D2B" stroke-width="12" stroke-linecap="round"/></g></svg>`;
  return {svg,wire:root=>{const hole=root.querySelector("#hole"),lens=root.querySelector("#lens");const seen=new Set();const R=()=>root.getBoundingClientRect();
      const at=(x,y)=>{x=Math.max(20,Math.min(W-20,x));y=Math.max(20,Math.min(H-20,y));hole.setAttribute("cx",x);hole.setAttribute("cy",y);lens.setAttribute("transform",`translate(${x} ${y})`);
        spots.forEach((p,i)=>{if(!seen.has(i)&&Math.abs(p[0]-x)<BW/2+10&&Math.abs(p[1]-y)<46){seen.add(i);const f=root.querySelector(`.fact[data-i="${i}"]`);
          root.querySelector("#found").appendChild(f);f.classList.add("found");                 /* found → it comes OUT of the fog, whole and clear */
          sfx("pop");mood(root,s.target,"laugh");cap("🔍 «"+exName(s.target)+"»: "+s.facts[i]);
          if(seen.size===n){setTimeout(()=>{root.querySelector(".fog").classList.add("gone2");cap("✨ اكتشفت كل أسرار «"+exName(s.target)+"»!");sfx("tada");},700);}}});};
      /* 🎬 video mode does NOT move the lens: the student discovers by himself. It only shows a «move me» hint until the first touch. */
      root.querySelector("#lens").classList.add("hintme");
      const mv=e=>{const r=R(),k=W/r.width;at((e.clientX-r.left)*k,(e.clientY-r.top)*k);};const first=()=>{root.querySelector("#lens").classList.remove("hintme");};
      root.addEventListener("pointermove",e=>{first();mv(e);});root.addEventListener("pointerdown",e=>{first();mv(e);});at(c[0],c[1]);}};}
SCENES.assemble=sceneAssemble;SNAME.assemble="🧩 ركّب المشهد";SCENES.dialogue=sceneDialogue;SNAME.dialogue="🗣️ حوار";SCENES.slider=sceneSlider;SNAME.slider="🎚️ الشريط السحري";SCENES.lens=sceneLens;SNAME.lens="🔍 العدسة";
/* 🤖 a scene written by the model (or the labeled example): it runs ONLY inside a sandboxed iframe (no network, no access to this page).
   It talks to us by messages: llm-caption (the narrator line), llm-size (its height), llm-scene (the check: drew? inside? errors?). */
let customFrame=null;
window.addEventListener("message",e=>{if(!customFrame||e.source!==customFrame.contentWindow||!e.data||typeof e.data!=="object")return;const m=e.data;
  if(m.type==="llm-caption"&&typeof m.text==="string")cap(m.text.slice(0,300));
  if(m.type==="llm-size"&&+m.h>0)customFrame.style.height=Math.min(900,Math.max(240,+m.h))+"px";
  if(m.type==="llm-scene"){const b=document.getElementById("cbadge");if(b)b.textContent=m.ok?`✅ اشتغل جوا الصندوق المعزول (رسم ${+m.drawn||0} عنصر${+m.outside?" · ⚠️ "+(+m.outside)+" برا الصورة":""})`:"⚠️ ما اشتغل: "+String((m.errors||[])[0]||"").slice(0,120);}});
function sceneCustom(s){
  const svg=`<svg class="xstage xmini" id="xs" viewBox="0 0 640 1" aria-hidden="true"></svg>
    <p class="cnote">${s.label||"🤖 مشهد كتبه الموديل بأدوات القالب، وانقبل من المعلم."}</p>
    <iframe class="cframe" sandbox="allow-scripts" title="مشهد تفاعلي (صندوق معزول)" referrerpolicy="no-referrer"></iframe><p class="cbadge" id="cbadge">⏳ بيشتغل…</p>`;
  return {svg,wire:root=>{customFrame=document.querySelector(".cframe");customFrame.srcdoc=s.runner_html||"";}};}
SCENES.custom=sceneCustom;SNAME.custom="🤖 مشهد من الموديل";
