/* ======================= 🧰 SCENE SDK v1 — the toolkit a model-written scene may use =======================
   The model writes ONLY:   function buildScene(SDK, data) { ... }
   It runs inside a sandboxed iframe (no network, no cookies, no parent page). Everything it draws goes through this SDK,
   so the scene keeps the platform's look: our characters, our speech bubbles (never cut, wrapped), our arrows, the age stage.
   data = {concept:{id,name,meaning,ins:[{id,name,why}],outs:[{id,name}]}, stage, subject, art:{id: "<svg…>"}, lesson}
   The runner reports back to the page: {type:"llm-scene", ok, drawn, outside, errors, done}. */
(function(){
  const NS="http://www.w3.org/2000/svg",W=640,H=340;
  const stage=document.getElementById("stage"),capEl=document.getElementById("cap"),ui=document.getElementById("ui");
  const errors=[];let drawn=0,doneNote=null;const handles=[];
  const node=(tag,attrs,parent)=>{const e=document.createElementNS(NS,tag);Object.entries(attrs||{}).forEach(([k,v])=>{if(v!==undefined&&v!==null)e.setAttribute(k,String(v));});(parent||stage).appendChild(e);drawn++;return e;};
  const clamp=(v,a,b)=>Math.max(a,Math.min(b,v));
  const layer=node("g",{id:"scene"}),bubbles=node("g",{id:"bubbles","pointer-events":"none"});drawn-=2;
  /* split a sentence into short lines (≈22 letters), never cutting a word; at most 4 lines */
  function lines(t){const w=String(t||"").split(/\s+/).filter(Boolean),out=[""];let cut=false;for(const x of w){const c=out[out.length-1];if(!c||(c+" "+x).length<=22)out[out.length-1]=(c+" "+x).trim();else if(out.length<4)out.push(x);else{cut=true;break;}}if(cut)out[out.length-1]+=" …";return out;}
  function bubbleFor(h,text){bubbles.innerHTML="";if(!text)return;const ls=lines(text),LH=19,bh=14+ls.length*LH;
    const g=node("g",{class:"sdk-bub"},bubbles);const r=node("rect",{rx:12,height:bh},g);const ts=ls.map((l,i)=>node("text",{y:22+i*LH,"text-anchor":"middle"},g));ts.forEach((t,i)=>t.textContent=ls[i]);
    let tw=0;ts.forEach(t=>{try{tw=Math.max(tw,t.getComputedTextLength());}catch(e){}});const bw=Math.max(70,Math.ceil(tw||ls.join("").length*8)+28);r.setAttribute("width",bw);ts.forEach(t=>t.setAttribute("x",bw/2));
    let top=h.y-h.size/2-bh-12;const down=top<6;if(down)top=Math.min(H-bh-6,h.y+h.size/2+26);const left=clamp(h.x-bw/2,6,W-6-bw);const tx=clamp(h.x-left,16,bw-16);
    node("path",{class:"sdk-tail",d:down?`M${tx-8} 2 L${tx} -10 L${tx+8} 2`:`M${tx-8} ${bh-2} L${tx} ${bh+10} L${tx+8} ${bh-2}`},g);g.setAttribute("transform",`translate(${left} ${top})`);drawn-=ls.length+3;}
  function art(id,size){const s=(window.DATA.art||{})[id];if(!s)return `<circle cx="50" cy="50" r="40" class="sdk-blob"/>`;return s.replace(/^[\s\S]*?<svg[^>]*>/,"").replace(/<\/svg>\s*$/,"");}
  const SDK={
    W,H,
    data:null,
    /* a character from our art library: SDK.character("root", {x, y, size, label}) */
    character(id,o){o=o||{};const size=o.size||90,c=(window.DATA.concepts||{})[id]||{name:o.name||id};
      const g=node("g",{class:"sdk-char",transform:`translate(${o.x||W/2} ${o.y||H/2})`,"data-id":id},layer);
      const body=node("g",{class:"sdk-body"},g);body.innerHTML=`<svg x="${-size/2}" y="${-size/2}" width="${size}" height="${size}" viewBox="0 0 100 100" overflow="visible">${art(id,size)}</svg>`;
      if(o.label!==false){const t=node("text",{y:size/2+18,"text-anchor":"middle",class:"sdk-name"},g);t.textContent=o.name||c.name;}
      const h={id,g,size,x:o.x||W/2,y:o.y||H/2,
        moveTo(x,y,ms){const fx=h.x,fy=h.y;x=clamp(x,size/2,W-size/2);y=clamp(y,size/2,H-size/2-18);return SDK.tween(ms||600,t=>{h.x=fx+(x-fx)*t;h.y=fy+(y-fy)*t;g.setAttribute("transform",`translate(${h.x} ${h.y})`);});},
        say(text){bubbleFor(h,text);return h;},
        dim(on){g.style.opacity=on?.3:1;return h;},glow(on){g.classList.toggle("sdk-glow",!!on);return h;},
        onTap(fn){g.style.cursor="pointer";g.addEventListener("click",e=>{try{fn(h,e);}catch(err){errors.push(String(err));}});return h;},
        draggable(opts){opts=opts||{};g.style.cursor="grab";g.style.touchAction="none";
          g.addEventListener("pointerdown",ev=>{ev.preventDefault();const R=stage.getBoundingClientRect(),k=W/R.width;g.setPointerCapture&&g.setPointerCapture(ev.pointerId);
            const mv=e=>{h.x=clamp((e.clientX-R.left)*k,size/2,W-size/2);h.y=clamp((e.clientY-R.top)*k,size/2,H-size/2-18);g.setAttribute("transform",`translate(${h.x} ${h.y})`);try{opts.onMove&&opts.onMove(h);}catch(err){errors.push(String(err));}};
            const up=()=>{window.removeEventListener("pointermove",mv);window.removeEventListener("pointerup",up);try{opts.onDrop&&opts.onDrop(h);}catch(err){errors.push(String(err));}};
            window.addEventListener("pointermove",mv);window.addEventListener("pointerup",up);});return h;},
        near(other,dist){return Math.hypot(h.x-other.x,h.y-other.y)<(dist||80);}};
      handles.push(h);return h;},
    /* the platform's «needs» arrow: from the one who needs → to what it needs, with the age's word on it */
    arrow(from,to,o){o=o||{};const g=node("g",{class:"sdk-arrow",opacity:o.hidden?0:1},layer);
      const draw=()=>{const dx=to.x-from.x,dy=to.y-from.y,d=Math.hypot(dx,dy)||1,r1=from.size/2+6,r2=to.size/2+10;
        const a=[from.x+dx/d*r1,from.y+dy/d*r1],b=[to.x-dx/d*r2,to.y-dy/d*r2],m=[(a[0]+b[0])/2,(a[1]+b[1])/2-18];
        g.innerHTML=`<path d="M${a[0]} ${a[1]} Q${m[0]} ${m[1]} ${b[0]} ${b[1]}" class="sdk-line" marker-end="url(#sdkhead)"/>`+(o.label===false?"":`<g transform="translate(${(a[0]+2*m[0]+b[0])/4} ${(a[1]+2*m[1]+b[1])/4})"><rect class="sdk-tag" x="-34" y="-11" width="68" height="20" rx="10"/><text y="4" text-anchor="middle" class="sdk-tagt">${o.label||window.DATA.needsWord}</text></g>`);};
      draw();return {g,redraw:draw,show(on){g.setAttribute("opacity",on?1:0);}};},
    text(x,y,str,o){o=o||{};const t=node("text",{x,y,"text-anchor":o.anchor||"middle",class:"sdk-text","font-size":o.size||16,"font-weight":o.weight||700,fill:o.color,direction:o.ltr?"ltr":null,"unicode-bidi":o.ltr?"embed":null},layer);t.textContent=String(str);return t;},
    shape(kind,attrs){if(!["circle","rect","line","path","ellipse","polygon","polyline"].includes(kind))throw new Error("shape: "+kind);return node(kind,Object.assign({class:"sdk-shape"},attrs||{}),layer);},
    slider(o,onChange){o=o||{};const lab=document.createElement("label");lab.className="sdk-sl";const sp=document.createElement("span");sp.textContent=o.label||"";
      const r=document.createElement("input");r.type="range";r.min=o.min??0;r.max=o.max??10;r.step=o.step??1;r.value=o.value??o.min??0;const b=document.createElement("b");b.textContent=r.value;
      lab.append(sp,r,b);ui.appendChild(lab);const fire=()=>{b.textContent=r.value;try{onChange&&onChange(parseFloat(r.value));}catch(err){errors.push(String(err));}};r.addEventListener("input",fire);setTimeout(fire,0);
      return {set(v){r.value=v;fire();},get value(){return parseFloat(r.value);}};},
    button(label,onClick){const bt=document.createElement("button");bt.className="sdk-btn";bt.textContent=label;bt.addEventListener("click",()=>{try{onClick&&onClick();}catch(err){errors.push(String(err));}});ui.appendChild(bt);return bt;},
    caption(t){capEl.textContent=String(t||"");parent.postMessage({type:"llm-caption",text:String(t||"")},"*");},
    tween(ms,fn){return new Promise(res=>{const t0=performance.now();const go=()=>{const t=Math.min(1,(performance.now()-t0)/(ms||1));try{fn(t<.5?2*t*t:1-Math.pow(-2*t+2,2)/2);}catch(err){errors.push(String(err));}if(t<1)requestAnimationFrame(go);else res();};go();});},
    wait(ms){return new Promise(r=>setTimeout(r,Math.min(ms||0,10000)));},
    done(note){doneNote=String(note||"تم");report();}};
  /* the report the page/teacher screen receives: did it draw, is everything inside the picture, any errors? */
  function report(){const R=stage.getBoundingClientRect(),k=W/(R.width||W);let outside=0;
    stage.querySelectorAll(".sdk-char,.sdk-text,.sdk-bub rect").forEach(e=>{const r=e.getBoundingClientRect();if(!r.width)return;const x0=(r.left-R.left)*k,x1=(r.right-R.left)*k,y0=(r.top-R.top)*k,y1=(r.bottom-R.top)*k;if(x0<-2||y0<-2||x1>W+2||y1>H+2)outside++;});
    const msg={type:"llm-scene",ok:!errors.length&&drawn>0,drawn,outside,errors:errors.slice(0,5),done:doneNote};window.__REPORT=msg;try{parent.postMessage(msg,"*");}catch(e){}}
  window.addEventListener("error",e=>{errors.push(String(e.message||e));});
  const size=()=>{try{parent.postMessage({type:"llm-size",h:document.documentElement.scrollHeight},"*");}catch(e){}};   /* the page sizes the iframe to fit */
  window.addEventListener("resize",size);setTimeout(size,50);setTimeout(size,600);
  window.__bootScene=function(){SDK.data=window.DATA;
    if(typeof window.buildScene!=="function"){errors.push("buildScene is missing");report();return;}
    try{const r=window.buildScene(SDK,window.DATA);if(r&&r.then)r.catch(err=>errors.push(String(err)));}catch(err){errors.push(String(err&&err.message||err));}
    setTimeout(report,1200);};
})();
