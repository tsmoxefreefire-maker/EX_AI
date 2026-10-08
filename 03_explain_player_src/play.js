/* ======================= 🎞️ THE FILM ENGINE: real processes, acted out — then the student drives them =======================
   One engine for every subject. Each verb = what REALLY happens:
   visit (a bee flies to the flower) · carry (the wind takes the seed far) · transform (the seed sprouts) ·
   combine / take_away / groups / share (blocks) · cut / equivalent / compare (pizza) · build (stones become a pyramid) ·
   exchange (goods ↔ money) · flow_river (the river waters the fields) · write (pictures on a tablet).
   Each step of the narrator plays one part of the film; then «🖐️ دورك»: the student does it by hand. */
function scenePlay(s){const W=640,H=340;const A=(id,sz,x,y,cls)=>{const ic=iconOf(id);let a=(ic?artSVG(ic,""):null)||`<svg class="ch" viewBox="0 0 100 100">${ARTS.blob(colorOf(id))}</svg>`;
    return `<g class="pa ${cls||""}" data-id="${id}" transform="translate(${x} ${y})"><g class="xbody" data-mood="happy">${a.replace("<svg ",`<svg width="${sz}" height="${sz}" x="${-sz/2}" y="${-sz/2}" `)}</g><text class="xname" y="${/actor/.test(cls||"")?-sz/2-8:sz/2+16}" text-anchor="middle">${exName(id)}</text></g>`;};   /* the one who MOVES has its name on top: it never lands on the flower's petals */
  const block=(x,y,col,cls)=>`<rect class="blk ${cls||""}" x="${x-13}" y="${y-13}" width="26" height="26" rx="6" fill="${col}" stroke="#3b2a1a" stroke-width="2.2"/>`;
  const ex=s.example||{};let body="";const v=s.verb;
  if(v==="visit")body=`${A(s.with,110,300,220,"tgt")}${s.result?`<g id="res" opacity="0">${A(s.result,64,430,250)}</g>`:""}<g id="pollen"></g>${A(s.target,70,560,70,"actor drag")}`;
  else if(v==="carry")body=`<g id="windl"></g>${A(s.target,70,90,70,"actor")}${A(s.with,56,170,230,"item drag")}<path d="M60 300 H600" stroke="#B07A4A" stroke-width="10"/>${s.result?`<g id="res" opacity="0">${A(s.result,58,540,250)}</g>`:""}`;
  else if(v==="transform")body=`${A(s.with,100,320,190,"from")}<g id="to" opacity="0">${A(s.target,110,320,180)}</g>${s.result?`<g id="res" opacity="0">${A(s.result,60,500,200)}</g>`:""}`;
  else if(v==="combine")body=`<g id="ga">${[...Array(ex.a)].map((_,i)=>block(470+(i%2)*30,140+Math.floor(i/2)*30,"#7CC6F2")).join("")}</g><g id="gb">${[...Array(ex.b)].map((_,i)=>block(150+(i%2)*30,140+Math.floor(i/2)*30,"#F28AA8")).join("")}</g><text id="eq" x="320" y="300" text-anchor="middle" class="bigeq">${ex.a} + ${ex.b} = ?</text>`;
  else if(v==="take_away")body=`<g id="all">${[...Array(ex.a)].map((_,i)=>block(230+(i%4)*32,130+Math.floor(i/4)*32,"#7CC6F2",i<ex.b?"go drag":"")).join("")}</g><text id="eq" x="320" y="300" text-anchor="middle" class="bigeq">${ex.a} − ${ex.b} = ?</text>`;
  else if(v==="groups")body=`<g id="rows"></g><text id="eq" x="320" y="310" text-anchor="middle" class="bigeq">${ex.a} × ${ex.b} = ?</text>`;
  else if(v==="share")body=`${[0,1,2].map(i=>`<rect x="${100+i*170}" y="200" width="130" height="70" rx="12" fill="none" stroke="var(--line)" stroke-width="3" stroke-dasharray="6 5"/>`).join("")}<g id="pile">${[...Array(ex.a)].map((_,i)=>block(250+(i%6)*28,90+Math.floor(i/6)*28,"#F6C177","drag")).join("")}</g><text id="eq" x="320" y="320" text-anchor="middle" class="bigeq">${ex.a} ÷ ${ex.b} = ?</text>`;
  else if(v==="cut"||v==="equivalent"||v==="compare"){const pie=(cx,cy,r,parts,shade,id)=>`<g id="${id}"><circle cx="${cx}" cy="${cy}" r="${r}" fill="#F6C177" stroke="#3b2a1a" stroke-width="3"/><g class="slices" data-parts="${parts}" data-shade="${shade}" data-cx="${cx}" data-cy="${cy}" data-r="${r}"></g></g>`;
    body=v==="cut"?`${pie(320,170,110,ex.parts,ex.shade,"p1")}<text id="eq" x="320" y="320" text-anchor="middle" class="bigeq"> </text>`:
      v==="equivalent"?`${pie(190,160,90,2,1,"p1")}${pie(450,160,90,4,2,"p2")}<text id="eq" x="320" y="300" text-anchor="middle" class="bigeq"> </text>`:
      `<rect x="120" y="90" width="400" height="50" rx="8" fill="#fff" stroke="#3b2a1a" stroke-width="2.4"/><rect id="b1" x="120" y="90" width="0" height="50" rx="8" fill="#7CC6F2"/><rect x="120" y="190" width="400" height="50" rx="8" fill="#fff" stroke="#3b2a1a" stroke-width="2.4"/><rect id="b2" x="120" y="190" width="0" height="50" rx="8" fill="#F28AA8"/><text x="560" y="122" class="bigeq">1/2</text><text x="560" y="222" class="bigeq">1/4</text><text id="eq" x="320" y="300" text-anchor="middle" class="bigeq"> </text>`;}
  else if(v==="build")body=`<g id="slots"></g><g id="stones">${[...Array(6)].map((_,i)=>`<rect class="stone drag" data-i="${i}" x="${470+(i%3)*44}" y="${230+Math.floor(i/3)*34}" width="40" height="28" rx="4" fill="#E9C46A" stroke="#B8893B" stroke-width="2.4"/>`).join("")}</g>`;
  else if(v==="exchange")body=`<g transform="translate(150 180)"><g class="xbody" data-mood="happy"><svg width="90" height="90" x="-45" y="-45" class="ch" viewBox="0 0 100 100">${ARTS.blob("#9CCFD8")}</svg></g><text class="xname" y="62" text-anchor="middle">البائع</text></g><g transform="translate(490 180)"><g class="xbody" data-mood="happy"><svg width="90" height="90" x="-45" y="-45" class="ch" viewBox="0 0 100 100">${ARTS.blob("#F6C177")}</svg></g><text class="xname" y="62" text-anchor="middle">الشاري</text></g><g id="goods" class="drag" transform="translate(220 150)"><rect x="-22" y="-18" width="44" height="36" rx="5" fill="#C98A55" stroke="#3b2a1a" stroke-width="2.4"/><path d="M-22 -4 H22" stroke="#3b2a1a" stroke-width="2"/></g><g id="coins" transform="translate(420 150)"><svg width="46" height="46" x="-23" y="-23" class="ch" viewBox="0 0 100 100">${ARTS.coins()}</svg></g>`;
  else if(v==="flow_river")body=`<path id="riv" d="M40 80 C200 40 220 200 330 170 C440 140 470 280 610 260" stroke="#7CC6F2" stroke-width="34" fill="none" stroke-linecap="round"/><g id="drops"></g><g id="fields"></g>`;
  else if(v==="write")body=`<rect x="200" y="50" width="240" height="250" rx="12" fill="#E9C46A" stroke="#3b2a1a" stroke-width="3"/><g id="glyphs"></g>`;
  const svg=`<svg class="xstage play" id="xs" viewBox="0 0 ${W} ${H}" role="img" aria-label="فيلم: ${SNAME.play}">${DEFS}${body}<g id="pfx"></g></svg><div class="drive" id="drive" hidden>🖐️ ${s.drive}</div>`;
  let done=-1,driving=false,root=null;
  const $p=q=>root.querySelector(q);
  const moveTo=(el,to,ms,arc)=>new Promise(res=>{const m=(el.getAttribute("transform")||"").match(/translate\(([-\d.]+)[ ,]+([-\d.]+)/)||[0,0,0];const a=[+m[1],+m[2]];let t=0;
    const go=()=>{if(!el.isConnected)return res();t=Math.min(1,t+(reduce?1:16/ms));const e=t<.5?2*t*t:1-Math.pow(-2*t+2,2)/2;const x=a[0]+(to[0]-a[0])*e,y=a[1]+(to[1]-a[1])*e-Math.sin(Math.PI*e)*(arc||0);
      el.setAttribute("transform",`translate(${x} ${y})`);if(t<1)requestAnimationFrame(go);else res();};go();});
  const fade=(el,op)=>{if(el){el.style.transition="opacity .6s";el.setAttribute("opacity",op);}};
  const grow=el=>{if(!el)return;el.setAttribute("opacity","1");el.classList.add("growin");};
  const blockMove=(el,dx,dy,ms)=>new Promise(res=>{const x0=+el.getAttribute("x"),y0=+el.getAttribute("y");let t=0;const go=()=>{if(!el.isConnected)return res();t=Math.min(1,t+(reduce?1:16/ms));el.setAttribute("x",x0+dx*t);el.setAttribute("y",y0+dy*t);if(t<1)requestAnimationFrame(go);else res();};go();});
  const eq=t=>{const e=$p("#eq");if(e){e.textContent=t;e.classList.remove("pop2");void e.getBBox;e.classList.add("pop2");}};
  const slices=(g,upto)=>{const n=+g.dataset.parts,sh=+g.dataset.shade,cx=+g.dataset.cx,cy=+g.dataset.cy,r=+g.dataset.r;let out="";
    for(let i=0;i<n;i++){const a0=-Math.PI/2+i*2*Math.PI/n,a1=a0+2*Math.PI/n;const p=(a)=>[cx+r*Math.cos(a),cy+r*Math.sin(a)];const [x0,y0]=p(a0),[x1,y1]=p(a1);
      out+=`<path d="M${cx} ${cy} L${x0} ${y0} A${r} ${r} 0 0 1 ${x1} ${y1}Z" fill="${i<Math.min(sh,upto)?"#E8574A":"transparent"}" stroke="#3b2a1a" stroke-width="2.4"/>`;}g.innerHTML=out;};
  /* the film, in parts (one per narrator step); each part is safe to call again */
  const parts={
    visit:[()=>{const b=$p(".actor");say(root,null,"");return moveTo(b,[340,150],1500,60);},
           ()=>{const fx=$p("#pollen");for(let i=0;i<10;i++){const c=document.createElementNS(svgNS,"circle");c.setAttribute("r",3);c.setAttribute("fill","#F2B33D");c.setAttribute("cx",300+Math.cos(i)*40);c.setAttribute("cy",200+Math.sin(i)*30);c.classList.add("sparkle");fx.appendChild(c);}sfx("buzz");return Promise.resolve();},
           ()=>{grow($p("#res"));sfx("bloom");return Promise.resolve();}],
    carry:[()=>{const w=$p("#windl");w.innerHTML=[0,1,2].map(i=>`<path d="M${80+i*30} ${120+i*20} C200 ${100+i*20} 300 ${150+i*20} 420 ${120+i*20}" class="windline"/>`).join("");sfx("wind");return Promise.resolve();},
           ()=>moveTo($p(".item"),[520,240],1800,90),
           ()=>{grow($p("#res"));return Promise.resolve();}],
    transform:[()=>{$p(".from").classList.add("shake");return Promise.resolve();},
               ()=>{fade($p(".from"),0);grow($p("#to"));sfx("bloom");return Promise.resolve();},          /* the old one disappears completely: no name under the new one */
               ()=>{grow($p("#res"));return Promise.resolve();}],
    combine:[()=>Promise.resolve(),()=>{const a=$p("#ga"),b=$p("#gb");return Promise.all([moveTo(a,[-110,0],1200),moveTo(b,[110,0],1200)]).then(()=>{eq(`${ex.a} + ${ex.b} = ${ex.r}`);sfx("pop");});},()=>Promise.resolve()],
    take_away:[()=>Promise.resolve(),()=>Promise.all([...root.querySelectorAll(".blk.go")].map((b,i)=>blockMove(b,260+i*10,-60,900))).then(()=>{root.querySelectorAll(".blk.go").forEach(b=>fade(b,0.15));eq(`${ex.a} − ${ex.b} = ${ex.r}`);}),()=>Promise.resolve()],
    groups:[()=>Promise.resolve(),()=>{const g=$p("#rows");let out="";for(let r=0;r<ex.a;r++)for(let c=0;c<ex.b;c++)out+=block(230+c*34,80+r*40,["#7CC6F2","#F28AA8","#6CC27A"][r%3],"rowb r"+r);g.innerHTML=out;
      root.querySelectorAll(".rowb").forEach(b=>{const r=+b.getAttribute("class").match(/r(\d)/)[1];b.style.animationDelay=(r*0.45)+"s";b.classList.add("growin");});setTimeout(()=>eq(`${ex.a} × ${ex.b} = ${ex.r}`),1400);return Promise.resolve();},()=>Promise.resolve()],
    share:[()=>Promise.resolve(),()=>Promise.all([...root.querySelectorAll("#pile .blk")].map((b,i)=>{const box=i%ex.b,slot=Math.floor(i/ex.b);return blockMove(b,(110+box*170+12+slot*28)-(+b.getAttribute("x")),(215)-(+b.getAttribute("y")),700+i*60);})).then(()=>eq(`${ex.a} ÷ ${ex.b} = ${ex.r}`)),()=>Promise.resolve()],
    cut:[()=>{root.querySelectorAll(".slices").forEach(g=>slices(g,0));sfx("pop");return Promise.resolve();},
         ()=>{root.querySelectorAll(".slices").forEach(g=>slices(g,99));const p=$p(".slices");if(p)eq(s.target&&iconOf(s.target)==="🔼"?`البسط = ${p.dataset.shade}`:iconOf(s.target)==="🔽"?`المقام = ${p.dataset.parts}`:`${p.dataset.shade}/${p.dataset.parts}`);return Promise.resolve();},()=>Promise.resolve()],
    equivalent:[()=>{root.querySelectorAll(".slices").forEach(g=>slices(g,99));return Promise.resolve();},()=>{eq("1/2 = 2/4 ✓");sfx("pop");return Promise.resolve();},()=>Promise.resolve()],
    compare:[()=>{$p("#b1").setAttribute("width","200");$p("#b2").setAttribute("width","100");return Promise.resolve();},()=>{eq("1/2 > 1/4");sfx("pop");return Promise.resolve();},()=>Promise.resolve()],
    build:[()=>Promise.resolve(),()=>{const pos=[[230,240],[274,240],[318,240],[252,212],[296,212],[274,184]];return Promise.all([...root.querySelectorAll(".stone")].map((st,i)=>new Promise(res=>setTimeout(()=>blockMove(st,pos[i][0]-(+st.getAttribute("x")),pos[i][1]-(+st.getAttribute("y")),700).then(res),i*350)))).then(()=>{sfx("tada");eq&&0;});},()=>Promise.resolve()],
    exchange:[()=>Promise.resolve(),()=>Promise.all([moveTo($p("#goods"),[430,150],1300,40),moveTo($p("#coins"),[210,150],1300,40)]).then(()=>sfx("pop")),()=>Promise.resolve()],
    flow_river:[()=>{const d=$p("#drops"),rv=$p("#riv"),L=rv.getTotalLength();let k=0;const t=setInterval(()=>{if(!root.isConnected)return clearInterval(t);const c=document.createElementNS(svgNS,"circle");c.setAttribute("r",5);c.setAttribute("fill","#fff");d.appendChild(c);let u=0;const go=()=>{if(!c.isConnected)return;u+=0.01;const p=rv.getPointAtLength(L*u);c.setAttribute("cx",p.x);c.setAttribute("cy",p.y);if(u<1)requestAnimationFrame(go);else c.remove();};go();if(++k>40)clearInterval(t);},180);return Promise.resolve();},
                ()=>Promise.resolve(),()=>{$p("#fields").innerHTML=[[140,170],[250,250],[440,90],[540,190],[90,250],[380,280]].map(([x,y])=>`<g transform="translate(${x} ${y})"><g class="growin"><svg width="54" height="54" x="-27" y="-27" class="ch" viewBox="0 0 100 100">${ARTS.wheat()}</svg></g></g>`).join("");sfx("bloom");return Promise.resolve();}],
    write:[()=>Promise.resolve(),()=>{const g=$p("#glyphs");const G=["𓂀","𓃒","𓆣","𓇳","𓈖","𓊖"];g.innerHTML=G.map((x,i)=>`<text x="${240+(i%3)*70}" y="${110+Math.floor(i/3)*90}" font-size="44" class="growin" style="animation-delay:${i*0.3}s">${x}</text>`).join("");return Promise.resolve();},()=>Promise.resolve()]};
  const P=parts[v]||[];
  const playUpTo=k=>{const last=k>=s.steps.length-1;for(let i=done+1;i<=(last?P.length-1:Math.min(k,P.length-1));i++){done=i;P[i]();}if(last)setTimeout(startDrive,1600);};   /* last step → the WHOLE film has played (a 2-step film was missing its ending) */
  /* 🖐️ the student does it by hand (same result, his own hand) */
  const startDrive=()=>{if(driving||!root||!root.isConnected)return;driving=true;const d=document.getElementById("drive");if(d)d.hidden=false;};
  return {svg,wire:r=>{root=r;
      /* drag: the actor/item/goods/stones/blocks; drop near where it really goes → that part of the film plays */
      root.querySelectorAll(".drag").forEach(el=>el.addEventListener("pointerdown",e=>{e.preventDefault();const R=root.getBoundingClientRect(),vb=root.viewBox.baseVal;
        const sx=vb.width/R.width,sy=vb.height/R.height;const isRect=el.tagName==="rect";const p0=isRect?[+el.getAttribute("x"),+el.getAttribute("y")]:null;const t0=el.getAttribute("transform");
        const mv=ev=>{const x=vb.x+(ev.clientX-R.left)*sx,y=vb.y+(ev.clientY-R.top)*sy;if(isRect){el.setAttribute("x",x-13);el.setAttribute("y",y-13);}else el.setAttribute("transform",`translate(${x} ${y})`);};
        const up=ev=>{window.removeEventListener("pointermove",mv);window.removeEventListener("pointerup",up);const x=vb.x+(ev.clientX-R.left)*sx,y=vb.y+(ev.clientY-R.top)*sy;let good=false;
          if(v==="visit")good=Math.hypot(x-300,y-220)<110;else if(v==="carry")good=x>420;else if(v==="exchange")good=x>380;
          else if(v==="take_away")good=y<90||x>460;else if(v==="build")good=x<380;else if(v==="share")good=y>190;else good=true;
          if(good){sfx("pop");if(v==="visit"){done=0;P[1]();setTimeout(()=>P[2](),900);cap("🐝 برافو! «"+exName(s.target)+"» صار: "+(s.steps[2]||""));}
            else if(v==="carry"){P[2]();cap("🌬️ برافو! "+(s.steps[2]||""));}
            else if(v==="exchange"){moveTo($p("#coins"),[210,150],900,30);cap("💰 برافو! "+(s.steps[1]||""));}
            else if(v==="take_away"){fade(el,0.15);if([...root.querySelectorAll(".blk.go")].every(b=>b.getAttribute("opacity")==="0.15")){eq(`${ex.a} − ${ex.b} = ${ex.r}`);cap("➖ برافو! "+s.steps[1]);}}
            else if(v==="build"){const placed=[...root.querySelectorAll(".stone")].filter(st=>+st.getAttribute("x")<380).length;if(placed>=6){sfx("tada");cap("🔺 برافو! "+(s.steps[1]||""));}}
            else cap("✅ "+(s.steps[1]||""));}
          else{if(isRect){el.setAttribute("x",p0[0]);el.setAttribute("y",p0[1]);}else el.setAttribute("transform",t0);cap("🙂 مش هون… "+s.drive);}};
        window.addEventListener("pointermove",mv);window.addEventListener("pointerup",up);}));
      /* taps: transform / groups / cut / river / write etc. */
      root.addEventListener("click",e=>{if(!driving)return;if(["transform","groups","cut","equivalent","compare","flow_river","write","combine"].includes(v)){done=-1;P.forEach(f=>f());cap("✅ "+(s.steps[1]||""));}});},
    onStep:(r,k)=>playUpTo(k)};}
SCENES.play=scenePlay;SNAME.play="🎞️ الفيلم";
