/* ===== 🌱 THE PLANT WORLD: one real plant; water it, move the sun, open the window — and WATCH it live ===== */
function sceneWorld(s){const W=640,H=440,GY=262,PX=330;const has=p=>s.needs.includes(p);const nm=p=>s.parts[p]?exName(s.parts[p]):"";
  const svg=`<svg class="xstage world" id="xs" viewBox="0 0 ${W} ${H}" role="img" aria-label="عالم النبتة" data-water="0" data-light="0" data-air="0" data-food="0" data-grow="0">
    <rect width="${W}" height="${GY}" fill="#CFEFFC"/><rect id="dark" width="${W}" height="${GY}" fill="#1b2a44" opacity=".35"/>
    <g id="sun" class="wpart" data-part="sun" style="cursor:grab" transform="translate(520 200)"><svg width="86" height="86" x="-43" y="-43" class="ch" viewBox="0 0 100 100">${ARTS.sun()}</svg><text y="58" text-anchor="middle" class="xtag">${has("sun")?"اسحبني ☀️":""}</text></g>
    ${has("air")?`<g id="win" class="wpart" data-part="air" style="cursor:pointer" transform="translate(70 70)"><rect x="-44" y="-40" width="88" height="80" rx="6" fill="#9B6B43" stroke="#3b2a1a" stroke-width="2.6"/><rect id="paneL" x="-38" y="-34" width="36" height="68" fill="#E6F4FB" stroke="#3b2a1a" stroke-width="2"/><rect id="paneR" x="2" y="-34" width="36" height="68" fill="#E6F4FB" stroke="#3b2a1a" stroke-width="2"/><text y="60" text-anchor="middle" class="xtag">افتحني 💨</text></g>`:""}
    <rect y="${GY}" width="${W}" height="${H-GY}" fill="#B07A4A"/><rect id="wet" y="${GY}" width="${W}" height="${H-GY}" fill="#5a3a1f" opacity="0"/>
    ${Array.from({length:26},(_,i)=>`<circle cx="${(i*97)%W}" cy="${GY+18+(i*53)%(H-GY-26)}" r="${2+(i%3)}" fill="#7A5232" opacity=".6"/>`).join("")}
    <g class="wpart" data-part="soil"><rect y="${GY}" width="${W}" height="${H-GY}" fill="transparent"/></g>
    <g id="roots" class="wpart" data-part="root" stroke="#E6CFA8" stroke-width="5" fill="none" stroke-linecap="round"><path d="M${PX} ${GY} C${PX-4} ${GY+40} ${PX-30} ${GY+60} ${PX-60} ${GY+96}"/><path d="M${PX} ${GY} C${PX+6} ${GY+46} ${PX+34} ${GY+70} ${PX+66} ${GY+104}"/><path d="M${PX} ${GY} L${PX+2} ${GY+120}"/><path d="M${PX-30} ${GY+60} L${PX-44} ${GY+130} M${PX+34} ${GY+70} L${PX+40} ${GY+140}" stroke-width="3"/></g>
    <g id="plant" transform="translate(${PX} ${GY})"><g id="sway">
      <path id="stem" class="wpart" data-part="stem" d="M0 0 L0 -90" stroke="#4E9E5A" stroke-width="9" stroke-linecap="round" fill="none"/>
      <g id="leaves"></g><g id="top"></g></g></g>
    <g id="fx"></g>
    <g id="can" class="wpart" data-part="water" style="cursor:grab" transform="translate(120 330)"><g id="canbody"><path d="M-26 -16 H18 V22 H-26Z" fill="#7CC6F2" stroke="#3b2a1a" stroke-width="2.6"/><path d="M18 -6 L44 -22 L48 -16 L22 4" fill="#7CC6F2" stroke="#3b2a1a" stroke-width="2.4"/><path d="M-26 -10 C-44 -10 -44 18 -26 16" fill="none" stroke="#3b2a1a" stroke-width="3"/></g><text y="44" text-anchor="middle" class="xtag">${has("water")?"اسحبني للتربة 🚿":""}</text></g>
    <g id="meters" transform="translate(${W-150} 22)">${["water","sun","air"].filter(has).map((p,i)=>`<g transform="translate(0 ${i*22})"><text x="-6" y="11" text-anchor="end" class="xtag">${{water:"💧",sun:"☀️",air:"💨"}[p]}</text><rect width="120" height="12" rx="6" fill="#ffffffaa" stroke="#3b2a1a"/><rect id="m_${p}" width="0" height="12" rx="6" fill="${{water:"#4FA3E0",sun:"#F2B33D",air:"#8EC9E8"}[p]}"/></g>`).join("")}<g transform="translate(0 ${s.needs.length*22})"><text x="-6" y="11" text-anchor="end" class="xtag">✨</text><rect width="120" height="12" rx="6" fill="#ffffffaa" stroke="#3b2a1a"/><rect id="m_food" width="0" height="12" rx="6" fill="#7BC67E"/></g></g>
  </svg>`;
  return {svg,wire:root=>{const st={water:has("water")?0:1,light:has("sun")?0.2:1,air:has("air")?0:1,food:0,grow:0,t:0,pour:false};
      const $$=id=>root.querySelector("#"+id);const sun=$$("sun"),can=$$("can"),win=$$("win");const box=()=>root.getBoundingClientRect();const sc=()=>W/box().width;
      const toSvg=ev=>{const b=box();return [(ev.clientX-b.left)*sc(),(ev.clientY-b.top)*sc()];};
      const drag=(el,onMove,onUp)=>el.addEventListener("pointerdown",e=>{e.preventDefault();e.stopPropagation();const mv=ev=>onMove(toSvg(ev));const up=ev=>{window.removeEventListener("pointermove",mv);window.removeEventListener("pointerup",up);if(onUp)onUp(toSvg(ev));};window.addEventListener("pointermove",mv);window.addEventListener("pointerup",up);});
      let sunXY=[520,200];const placeSun=([x,y])=>{sunXY=[Math.max(50,Math.min(W-50,x)),Math.max(46,Math.min(GY-30,y))];sun.setAttribute("transform",`translate(${sunXY[0]} ${sunXY[1]})`);};
      if(has("sun"))drag(sun,placeSun,()=>{sfx("pop");const l=Math.max(0,Math.min(1,1-(sunXY[1]-46)/(GY-76)));
        cap(l>0.5?"☀️ الشمس عالية: الأوراق بتاخد ضوء كفاية "+(s.info.sun?"(«"+nm("sun")+"» "+s.info.sun+")":""):"🌥️ الشمس واطية: الضوء قليل، فالنبتة بتضعف وبتصفرّ.");});
      let canXY=[120,330];const placeCan=([x,y])=>{canXY=[Math.max(40,Math.min(W-40,x)),Math.max(40,Math.min(H-30,y))];const over=canXY[1]<GY+10&&Math.abs(canXY[0]-PX)<200;st.pour=over;
        can.setAttribute("transform",`translate(${canXY[0]} ${canXY[1]})`);$$("canbody").setAttribute("transform",over?"rotate(28)":"");};
      if(has("water"))drag(can,placeCan,()=>{const was=st.pour;st.pour=false;$$("canbody").setAttribute("transform","");
        if(was)cap("💧 سقيت! «"+nm("water")+"» "+(s.info.water||"")+"، شوف النقاط الزرقا كيف بتطلع من "+(nm("root")?"«"+nm("root")+"»":"الجذور")+" لـ"+(nm("stem")?"«"+nm("stem")+"»":"الساق")+" للأوراق.");
        else cap("🚿 قرّب الإبريق من فوق النبتة عشان تسقيها.");});
      if(win)win.addEventListener("click",()=>{st.air=st.air>0.5?0:1;$$("paneL").setAttribute("transform",st.air?"translate(-34 0) scale(.15 1)":"");$$("paneR").setAttribute("transform",st.air?"translate(34 0) scale(.15 1)":"");sfx(st.air?"wind":"pop");cap(st.air?"💨 «"+nm("air")+"» دخل! "+(s.info.air||""):"سكّرنا الشباك.");});
      root.querySelectorAll(".wpart").forEach(el=>el.addEventListener("click",()=>{const p=el.dataset.part;if(p==="air")return;const key={sun:"sun",water:"water",root:"root",stem:"stem",soil:"soil"}[p];
        if(key&&s.info[key])cap("📌 «"+nm(key)+"»: "+s.info[key]);}));
      const fx=$$("fx");const dot=(x,y,r,fill)=>{const c=document.createElementNS(svgNS,"circle");c.setAttribute("cx",x);c.setAttribute("cy",y);c.setAttribute("r",r);c.setAttribute("fill",fill);fx.appendChild(c);return c;};
      const drops=[],flows=[];const mix=(a,b,t)=>a.map((v,i)=>Math.round(v+(b[i]-v)*t));
      let lastLeaves=-1;
      const tick=()=>{if(!root.isConnected)return;st.t++;
        st.light=has("sun")?Math.max(0,Math.min(1,1-(sunXY[1]-46)/(GY-76))):1;
        if(st.pour){st.water=Math.min(1,st.water+0.012);if(st.t%3===0)drops.push({c:dot(canXY[0]+46,canXY[1]-10,3,"#4FA3E0"),y:canXY[1]-10,x:canXY[0]+46});}
        else if(has("water"))st.water=Math.max(0,st.water-0.0012);
        const making=st.water>0.2&&st.light>0.5&&st.air>0.5;
        if(making&&!st.wasMaking)cap("✨ هلأ الورقة عم تصنع غذاء، لأنه عندها "+s.needs.map(p=>({water:"مي",sun:"شمس",air:"هوا"})[p]).join(" و")+"! والغذاء بينزل بالساق لكل النبتة.");
        if(!making&&st.wasMaking&&st.t>60){const miss=[];if(has("water")&&st.water<=0.2)miss.push("المي");if(has("sun")&&st.light<=0.5)miss.push("الشمس");if(has("air")&&st.air<=0.5)miss.push("الهوا");cap("😟 وقف الغذاء! ناقص "+miss.join(" و")+".");}
        st.wasMaking=making;
        if(making){st.food=Math.min(1,st.food+0.01);st.grow=Math.min(1,st.grow+0.0025);}else st.food=Math.max(0,st.food-0.004);
        /* drops fall into the soil */
        for(let i=drops.length-1;i>=0;i--){const d=drops[i];d.y+=6;d.c.setAttribute("cy",d.y);if(d.y>GY+6){d.c.remove();drops.splice(i,1);}}
        /* the plant: grows with food; leaves green with light+water; wilts without water */
        const h=90+st.grow*90,health=Math.min(1,st.water/0.3)*Math.min(1,st.light/0.6);
        $$("stem").setAttribute("d",`M0 0 L0 ${-h}`);
        const nLeaves=st.grow>0.5?3:2;const leafCol=`rgb(${mix([214,190,70],[76,175,80],health).join(",")})`;
        if(nLeaves!==lastLeaves){lastLeaves=nLeaves;$$("leaves").innerHTML=[0.45,0.72,0.9].slice(0,nLeaves).map((f,i)=>`<g class="wpart leaf" data-part="leaf" transform="translate(0 ${-h*f}) rotate(${i%2?-35:35})"><path d="M0 0 C${i%2?-20:20} -10 ${i%2?-46:46} -6 ${i%2?-58:58} 0 C${i%2?-46:46} 10 ${i%2?-20:20} 12 0 0Z" stroke="#3b2a1a" stroke-width="2.4"/><path d="M0 0 L${i%2?-52:52} 0" stroke="#3E8E4C" stroke-width="1.6"/></g>`).join("");
          $$("leaves").querySelectorAll(".leaf").forEach(l=>l.addEventListener("click",()=>cap("📌 «"+(nm("leaf")||"الورقة")+"»: "+(s.info.leaf||""))));}
        $$("leaves").querySelectorAll(".leaf").forEach((l,i)=>{const f=[0.45,0.72,0.9][i];l.setAttribute("transform",`translate(0 ${-h*f}) rotate(${(i%2?-35:35)+(st.water<0.15?(i%2?-30:30):0)})`);l.querySelector("path").setAttribute("fill",leafCol);});
        $$("sway").setAttribute("transform",`rotate(${st.water<0.15?12:Math.sin(st.t/30)*2})`);
        const bloom=st.grow>0.85;const mood=bloom?"laugh":health>0.6?"happy":"sad";
        if(($$("top").dataset.k||"")!==(bloom?"b":"s")+mood){$$("top").dataset.k=(bloom?"b":"s")+mood;
          $$("top").innerHTML=`<g transform="translate(0 ${-h-6})" data-mood="${mood}"><g class="ch">${bloom?[0,72,144,216,288].map(a=>`<ellipse transform="rotate(${a})" cx="0" cy="-22" rx="11" ry="16" fill="#F59BB8" stroke="#3b2a1a" stroke-width="2.4"/>`).join(""):""}<circle r="${bloom?18:16}" fill="${bloom?"#FFD25A":"#8BD08F"}" stroke="#3b2a1a" stroke-width="2.6"/>${faceSVG(0,2,.62)}</g></g>`;
          if(bloom){sfx("bloom");cap("🌸 «بذور» زهّرت! لأنه كان عندها كل اللي بتحتاجه.");sparkles();}}
        $$("top").firstChild&&$$("top").firstChild.setAttribute("transform",`translate(0 ${-h-6})`);
        /* water rises inside roots → stem → leaves; air flows in; food sparkles flow down */
        const pathUp=[[PX,GY+110],[PX,GY],[PX,GY-h*0.7],[PX+(st.t%2?40:-40),GY-h*0.72]];
        if(st.water>0.15&&st.t%10===0)flows.push({c:dot(PX,GY+110,4.5,"#4FA3E0"),pts:pathUp,k:0});
        if(st.air>0.5&&has("air")&&st.t%14===0)flows.push({c:dot(110,70,4,"#8EC9E8"),pts:[[110,70],[230,110],[PX-30,GY-h*0.6]],k:0});
        if(making&&st.t%12===0){const f=document.createElementNS(svgNS,"text");f.textContent="✦";f.setAttribute("fill","#F2B33D");f.setAttribute("font-size","14");fx.appendChild(f);flows.push({c:f,pts:[[PX+30,GY-h*0.7],[PX,GY-h*0.6],[PX,GY-10]],k:0,txt:true});}
        for(let i=flows.length-1;i>=0;i--){const fl=flows[i];fl.k+=0.012;const n=fl.pts.length-1;const seg=Math.min(n-1,Math.floor(fl.k*n)),t=fl.k*n-seg;const a=fl.pts[seg],b=fl.pts[seg+1]||a;const x=a[0]+(b[0]-a[0])*t,y=a[1]+(b[1]-a[1])*t;
          if(fl.txt){fl.c.setAttribute("x",x);fl.c.setAttribute("y",y);}else{fl.c.setAttribute("cx",x);fl.c.setAttribute("cy",y);}if(fl.k>=1){fl.c.remove();flows.splice(i,1);}}
        $$("wet").setAttribute("opacity",(st.water*0.45).toFixed(2));$$("dark").setAttribute("opacity",((1-st.light)*0.45).toFixed(2));
        ["water","sun","air"].filter(has).forEach(p=>$$("m_"+p).setAttribute("width",(120*({water:st.water,sun:st.light,air:st.air}[p])).toFixed(0)));$$("m_food").setAttribute("width",(120*st.food).toFixed(0));
        if(st.t%10===0)Object.assign(root.dataset,{water:st.water.toFixed(2),light:st.light.toFixed(2),air:String(st.air),food:st.food.toFixed(2),grow:st.grow.toFixed(2)});
        if(st.t%90===0&&!making&&st.t>90){const miss=[];if(has("water")&&st.water<=0.2)miss.push("💧 مي");if(has("sun")&&st.light<=0.5)miss.push("☀️ شمس");if(has("air")&&st.air<=0.5)miss.push("💨 هوا");if(miss.length)cap("«بذور» بدها: "+miss.join(" و")+" عشان تصنع غذاها.");}
        requestAnimationFrame(tick);};
      placeSun(sunXY);tick();}};}
SCENES.world=sceneWorld;SNAME.world="🌱 عالم النبتة";
