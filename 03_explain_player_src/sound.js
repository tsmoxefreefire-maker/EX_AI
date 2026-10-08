/* ======================= 🎵 THE SOUNDS (batch 26) — made in the browser with Web Audio, no sound files =======================
   · the AGE STAGE decides the character of the sound: kids = little melodies, high and bouncy · junior = soft and friendly ·
     teen = short clean notes · senior = deeper and calmer (one octave lower, a bigger room) — 🆕 batch 29: EVERY stage has a sound
     for every touch and move (Hareth: «لكل مرحلة أصوات خاصة، والكبار أصوات كبيرة»), only the little ones are the loudest;
   · the SUBJECT decides the instrument and the scale, so every subject sounds different:
       science = marimba · maths = plucked string · physics = electric piano · chemistry = glass bells ·
       geography = kalimba · history = wood · language = a soft flute · (anything else = a small bell);
   · never the same sound twice in a row: every event picks a note of the subject's pentatonic scale (always pleasant together),
     not the one it played last time, with a tiny change of pitch and loudness;
   · right moves in a row climb up the scale (a little tune that grows); a wrong move is a soft low note, never a buzzer;
   · a soft room echo + a limiter: never harsh, never too loud;
   · hovering a character (its pitch always comes from its name, so each one has its OWN voice): kids = a giggle · junior = a curious
     «همم؟» · teen = two quick rising notes · senior = one warm low note (🆕 batch 29: it used to be silent).
   Events it does not know (the films' cat, train, water…) go back to the old sounds (part3_core.js) and the stage packs (stage.js).
   🆕 batch 27 — a NEW subject (identity.py) brings its OWN sound in the page data (graph().sound = {instr, root, scale}):
       computer = a soft 8-bit «chip» · music = a harp · art = a vibraphone · economy / sport = a steel drum · religion = a calm harp …
       and anything else gets a stable instrument + key + scale from its name. The 7 subjects we had keep exactly their sounds. */
const SOUND=(()=>{
  const SCALE={major:[0,2,4,7,9],sus:[0,2,5,7,9],minor:[0,3,5,7,10],egypt:[0,2,5,7,10]};
  const SUBJ={science:{instr:"marimba",root:65,scale:"major"},math:{instr:"pluck",root:60,scale:"major"},physics:{instr:"epiano",root:62,scale:"major"},
    chemistry:{instr:"glass",root:69,scale:"major"},geography:{instr:"kalimba",root:67,scale:"sus"},history:{instr:"wood",root:57,scale:"minor"},
    language:{instr:"flute",root:62,scale:"minor"},general:{instr:"bell",root:60,scale:"major"}};
  const STG={kids:{vel:1,oct:12,wet:.14},junior:{vel:.64,oct:0,wet:.2},teen:{vel:.52,oct:0,wet:.14},senior:{vel:.44,oct:-12,wet:.22}};   /* senior: an octave lower + a bigger room = a «big», calm sound */
  let bus=null,TEST=null,FORCE=null,NB=null;const LOG=[];
  const ctx=()=>TEST||ac();
  const hz=m=>440*Math.pow(2,(m-69)/12);
  function impulse(a,sec,decay){const n=Math.floor(a.sampleRate*sec),b=a.createBuffer(2,n,a.sampleRate);
    for(let c=0;c<2;c++){const d=b.getChannelData(c);for(let i=0;i<n;i++)d[i]=(Math.random()*2-1)*Math.pow(1-i/n,decay);}return b;}
  function getBus(){const a=ctx();if(bus&&bus.a===a)return bus;
    const lim=a.createDynamicsCompressor();lim.threshold.value=-14;lim.knee.value=10;lim.ratio.value=4;lim.attack.value=.003;lim.release.value=.25;lim.connect(a.destination);
    const master=a.createGain();master.gain.value=.7;master.connect(lim);
    const rev=a.createConvolver();rev.buffer=impulse(a,1.8,3);const wet=a.createGain();wet.gain.value=1;rev.connect(wet);wet.connect(master);
    bus={a,master,rev};return bus;}
  function env(g,t,peak,att,dec){dec=Math.max(.06,dec);g.gain.setValueAtTime(.0001,t);   /* never a click too short to hear */g.gain.exponentialRampToValueAtTime(Math.max(.0002,peak),t+att);g.gain.exponentialRampToValueAtTime(.0001,t+att+dec);}
  function part(a,d,type,f,t,peak,att,dec,det){const g=a.createGain();g.connect(d);env(g,t,peak,att,dec);const o=a.createOscillator();o.type=type;o.frequency.setValueAtTime(f,t);
    if(det)o.detune.setValueAtTime(det,t);o.connect(g);o.start(t);o.stop(t+att+Math.max(.06,dec)+.05);}
  function hit(a,d,t,peak,dec){if(!NB||NB.sampleRate!==a.sampleRate){NB=a.createBuffer(1,Math.floor(a.sampleRate*.4),a.sampleRate);const c=NB.getChannelData(0);for(let i=0;i<c.length;i++)c[i]=Math.random()*2-1;}
    const s=a.createBufferSource();s.buffer=NB;const g=a.createGain();g.connect(d);env(g,t,peak,.001,dec);s.connect(g);s.start(t);s.stop(t+dec+.05);}
  /* the instruments: f = pitch (Hz), t = when, v = loudness, L = length factor */
  const VOICES={
    marimba:(a,d,f,t,v,L)=>{part(a,d,"sine",f,t,.34*v,.004,.45*L);part(a,d,"sine",f*3.93,t,.09*v,.002,.09*L);part(a,d,"sine",f*9.4,t,.03*v,.001,.03);},
    pluck:(a,d,f,t,v,L)=>{const lp=a.createBiquadFilter();lp.type="lowpass";lp.Q.value=1.5;lp.frequency.setValueAtTime(Math.min(9000,f*10),t);
      lp.frequency.exponentialRampToValueAtTime(Math.max(220,f*1.5),t+.3*L);lp.connect(d);part(a,lp,"triangle",f,t,.36*v,.002,.55*L);part(a,lp,"sawtooth",f,t,.08*v,.002,.35*L,4);},
    epiano:(a,d,f,t,v,L)=>{const g=a.createGain();g.connect(d);env(g,t,.3*v,.003,.7*L);const car=a.createOscillator();car.frequency.setValueAtTime(f,t);   /* FM, like an electric piano */
      const mod=a.createOscillator();mod.frequency.setValueAtTime(f*2,t);const mg=a.createGain();mg.gain.setValueAtTime(f*1.6,t);mg.gain.exponentialRampToValueAtTime(f*.05,t+.4*L);
      mod.connect(mg);mg.connect(car.frequency);car.connect(g);car.start(t);mod.start(t);car.stop(t+.75*L+.06);mod.stop(t+.75*L+.06);},
    glass:(a,d,f,t,v,L)=>{part(a,d,"sine",f,t,.22*v,.002,1*L);part(a,d,"sine",f*2.756,t,.09*v,.002,.45*L,3);part(a,d,"sine",f*5.404,t,.04*v,.001,.22*L,-4);},
    kalimba:(a,d,f,t,v,L)=>{part(a,d,"sine",f,t,.32*v,.003,.55*L);part(a,d,"sine",f*6.26,t,.06*v,.001,.05);part(a,d,"triangle",f*2,t,.05*v,.002,.12*L);},
    wood:(a,d,f,t,v,L)=>{const bp=a.createBiquadFilter();bp.type="bandpass";bp.frequency.value=Math.min(8000,f*2.2);bp.Q.value=9;bp.connect(d);hit(a,bp,t,.7*v,.06);
      part(a,d,"sine",f,t,.36*v,.002,Math.max(.12,.2*L));part(a,d,"triangle",f*2.01,t,.08*v,.002,.08*L);},   /* a hollow wooden «tok», long enough to hear */
    flute:(a,d,f,t,v,L)=>{const g=a.createGain();g.connect(d);g.gain.setValueAtTime(.0001,t);g.gain.exponentialRampToValueAtTime(.24*v,t+.035);g.gain.exponentialRampToValueAtTime(.0001,t+.035+.5*L);
      const o=a.createOscillator();o.frequency.setValueAtTime(f,t);const lfo=a.createOscillator();lfo.frequency.value=5.2;const lg=a.createGain();lg.gain.value=f*.006;lfo.connect(lg);lg.connect(o.frequency);o.connect(g);
      const o2=a.createOscillator();o2.frequency.setValueAtTime(f*2,t);const h=a.createGain();h.gain.value=.12;o2.connect(h);h.connect(g);[o,lfo,o2].forEach(x=>{x.start(t);x.stop(t+.6*L+.08);});
      const hp=a.createBiquadFilter();hp.type="highpass";hp.frequency.value=2500;hp.connect(d);hit(a,hp,t,.05*v,.12);},
    bell:(a,d,f,t,v,L)=>{part(a,d,"sine",f,t,.26*v,.003,.7*L);part(a,d,"sine",f*2,t,.07*v,.002,.3*L);part(a,d,"sine",f*3.01,t,.03*v,.002,.15*L);},
    /* 🆕 for new subjects */
    chip:(a,d,f,t,v,L)=>{const lp=a.createBiquadFilter();lp.type="lowpass";lp.frequency.value=Math.min(5000,f*5);lp.connect(d);   /* a soft 8-bit blip (filtered, never harsh) */
      part(a,lp,"square",f,t,.13*v,.003,.22*L);part(a,lp,"square",f*2,t+.04,.06*v,.002,.12*L);part(a,d,"triangle",f,t,.2*v,.003,.32*L);},
    harp:(a,d,f,t,v,L)=>{const lp=a.createBiquadFilter();lp.type="lowpass";lp.Q.value=.7;lp.frequency.setValueAtTime(Math.min(10000,f*8),t);
      lp.frequency.exponentialRampToValueAtTime(Math.max(400,f*2),t+.6*L);lp.connect(d);part(a,lp,"triangle",f,t,.3*v,.002,.9*L);part(a,lp,"sine",f*2,t,.1*v,.002,.5*L);part(a,lp,"sine",f*3,t,.04*v,.002,.25*L);},
    vibes:(a,d,f,t,v,L)=>{const g=a.createGain();g.connect(d);env(g,t,.3*v,.006,.9*L);const tr=a.createGain();tr.gain.value=.8;tr.connect(g);   /* a vibraphone: a soft bar with a slow tremolo */
      const lfo=a.createOscillator();lfo.frequency.value=5.5;const lg=a.createGain();lg.gain.value=.25;lfo.connect(lg);lg.connect(tr.gain);
      const o=a.createOscillator();o.frequency.setValueAtTime(f,t);o.connect(tr);const o2=a.createOscillator();o2.frequency.setValueAtTime(f*4,t);const h=a.createGain();h.gain.value=.06;o2.connect(h);h.connect(tr);
      [o,o2,lfo].forEach(x=>{x.start(t);x.stop(t+.96*L+.08);});},
    steel:(a,d,f,t,v,L)=>{part(a,d,"sine",f,t,.3*v,.003,.55*L);part(a,d,"sine",f*2.01,t,.12*v,.002,.35*L);part(a,d,"sine",f*3.98,t,.06*v,.002,.18*L);part(a,d,"triangle",f*1.5,t,.04*v,.002,.12*L);}};
  /* the sound of the book on the screen: a NEW subject's own sound (from the data) if it is valid, else its subject's */
  const own=g=>{const x=g&&g.sound;return x&&VOICES[x.instr]&&SCALE[x.scale]&&isFinite(x.root)?{instr:x.instr,root:Math.max(48,Math.min(76,+x.root)),scale:x.scale}:null;};
  function who(){if(FORCE)return {stage:FORCE.stage,subject:FORCE.subject,prof:FORCE.prof||SUBJ[FORCE.subject]||SUBJ.general};
    const g=(typeof graph==="function"&&graph())||{},subject=SUBJ[g.subject]?g.subject:"general";
    return {subject,stage:STAGES[stageNow()]?stageNow():"kids",prof:own(g)||SUBJ[subject]};}
  /* one note: a degree of the subject's scale (0 = the root, 5 = one octave up), always in tune */
  function note(deg,o){const c=who(),S=c.prof,P=STG[c.stage],sc=SCALE[S.scale];o=o||{};const a=ctx(),b=getBus();
    const m=S.root+P.oct+(o.oct||0)+sc[((deg%5)+5)%5]+12*Math.floor(deg/5);LOG.push(m);if(LOG.length>200)LOG.shift();
    const f=hz(m)*Math.pow(2,(Math.random()-.5)*.01),t=a.currentTime+.01+(o.at||0);           /* ±½ of a «cent» step: alive, never out of tune */
    const d=a.createGain();d.connect(b.master);const send=a.createGain();send.gain.value=P.wet*(S.instr==="glass"?1.4:1);d.connect(send);send.connect(b.rev);
    VOICES[o.instr||S.instr](a,d,f,t,(o.vel||1)*P.vel*(.9+Math.random()*.2),o.len||1);}
  const last={};function fresh(key,opts){const pool=opts.length>1?opts.filter(x=>x!==last[key]):opts;const x=pool[Math.floor(Math.random()*pool.length)];last[key]=x;return x;}   /* never the same one twice in a row */
  let streak=0,streakT=0,lastAt={};
  /* the gestures: what each event sounds like at each age. true = handled here. */
  function play(name,o){o=o||{};const st=who().stage,kid=st==="kids",jun=st==="junior",teen=st==="teen",sen=st==="senior";
    const now=performance.now();if(now-(lastAt[name]||0)<60)return true;lastAt[name]=now;                 /* the same event twice in 60ms: once */
    const N=(d,x)=>note(d,x);
    switch(name){
      case "pop":case "pick":N(fresh("pick",kid?[5,6,7,8]:jun?[4,5,6]:[5,6]),{len:kid?.6:jun?.5:teen?.3:.25,vel:sen?.55:teen?.8:1});return true;
      case "flip":if(sen){N(fresh("flip",[4,5]),{len:.3,vel:.6});return true;}if(teen){N(7,{len:.2,vel:.5});return true;}N(fresh("flip",[6,7]),{len:.3,vel:jun?.6:.8});if(kid)N(8,{at:.05,len:.25,vel:.5});return true;
      case "step":N(fresh("step",[0,1,2]),{len:sen?.35:teen?.2:.3,vel:sen?.55:teen?.4:.6});return true;
      case "good":case "place":{streak=now-streakT<6000?Math.min(streak+1,4):0;streakT=now;const b=fresh("good",[2,3,4])+streak;
        if(sen){N(b+2,{len:.6,vel:.8});return true;}N(b,{len:teen?.5:1});N(b+2,{at:teen?.07:.09,len:teen?.5:1,vel:jun?.9:1});if(kid)N(b+4,{at:.18,len:.8,vel:.7});return true;}
      case "bad":case "nope":streak=0;if(sen){N(0,{len:.4,vel:.45,oct:-12});return true;}if(teen){N(1,{len:.4,vel:.5});return true;}
        N(3,{len:.5,vel:jun?.55:.7});N(1,{at:.12,len:.6,vel:jun?.5:.6});return true;
      case "tada":case "ready":case "cheer":{const k=fresh("tada",[0,1,2]),arp=kid?[0,2,4,5,7]:jun?[0,2,4,5]:teen?[2,4,5]:[0,4];
        arp.forEach((d,i)=>N(d+k,{at:i*(sen?.14:.09),len:kid?1.2:1,vel:i===arp.length-1?1:.85}));if(kid||name==="cheer"&&jun)N(9+k,{at:arp.length*.09+.05,len:1.4,vel:.5,instr:"glass"});return true;}
      case "sparkle":(sen?[7,9]:teen?[8,9]:[7,8,9]).forEach((d,i)=>N(d,{at:i*(sen?.12:.07),len:.5,vel:sen||teen?.4:.5,instr:"glass"}));return true;
      case "bloom":(sen?[0,4]:teen?[4,7]:[2,4,7]).forEach((d,i)=>N(d,{at:i*(sen?.12:.08),len:sen?.9:.7,vel:sen?.7:1}));return true;
      case "ding":N(9,{len:.9,vel:sen?.5:.8,instr:"glass"});return true;
      case "on":N(1+2*Math.min(o.n||0,4),{len:kid?.7:.45,vel:sen?.6:1});return true;
      case "off":N(Math.max(0,2*(o.n||0)-1),{len:.35,vel:.5,oct:sen?-12:0});return true;
      case "connect":{const d=fresh("connect",[1,2,3])+Math.min(o.n||0,3);if(sen){N(d+3,{len:.6,vel:.8});return true;}N(d,{len:.4});N(d+3,{at:.07,len:.8});return true;}
      case "rung":N(o.down?7-2*(o.n||0):2+2*(o.n||0),{len:sen?.6:.8,vel:sen?.7:1});return true;
      case "giggle":hover("");return true;}
    return false;}
  /* hovering a character: the little ones' characters each have their OWN voice (pitch from the name) */
  const voiceOf=id=>[...String(id||"x")].reduce((a,c)=>a+c.charCodeAt(0),0)%5;
  const GIGGLES=[[0,1,2,3],[0,2,1,3],[3,2,3,4],[0,0,2,4],[2,1,0,2]];
  function hover(id){const st=who().stage,base=5+voiceOf(id);
    if(st==="kids"){fresh("giggle",[0,1,2,3,4]);GIGGLES[last.giggle].forEach((d,i)=>note(base+d,{at:i*.07,len:.28,vel:.55}));return;}
    if(st==="junior"){note(base,{len:.35,vel:.55});note(base+fresh("curious",[1,2]),{at:.11,len:.45,vel:.5});return;}
    if(st==="teen"){note(base,{len:.22,vel:.45});note(base+2,{at:.08,len:.28,vel:.42});return;}
    note(base,{len:.5,vel:.55});}                                                                   /* senior: one warm, low note */
  /* 🎵 the little demo (the button next to the stage switcher): hover → pick → right → right → wrong → right → done */
  /* 🆕 batch 30: a new tune STOPS the one still playing (two stages one after the other never sound on top of each other) */
  let DEMO_T=[],DEMO_END=0;
  function demo(){DEMO_T.forEach(clearTimeout);DEMO_T=[];if(typeof soundOn!=="undefined"&&!soundOn)return;const seq=[["hover"],["pick"],["place"],["place"],["nope"],["place"],["ready"]];
    DEMO_END=performance.now()+seq.length*520;
    seq.forEach(([e],i)=>DEMO_T.push(setTimeout(()=>{if(e==="hover")hover("demo"+i);else{lastAt[e]=0;play(e);}},i*520)));}
  const demoing=()=>performance.now()<DEMO_END;
  /* 🧪 for the tests: render one event OFFLINE (no speakers) and measure it: loudness, peak, length, brightness */
  async function render(name,stage,subject,o){const sr=22050;TEST=new OfflineAudioContext(1,Math.floor(sr*2.6),sr);bus=null;   /* subject: a name, or a sound {instr, root, scale} */
    FORCE=typeof subject==="object"?{stage,subject:"general",prof:own({sound:subject})||SUBJ.general}:{stage,subject};lastAt={};
    try{if(name==="hover")hover(o&&o.id||"x");else play(name,o);const buf=await TEST.startRendering();const d=buf.getChannelData(0);
      let peak=0,end=0;for(let i=0;i<d.length;i++){const x=Math.abs(d[i]);if(x>peak)peak=x;if(x>.002)end=i;}
      let sum=0,all=0;for(let i=0;i<d.length;i++){all+=d[i]*d[i];if(i<=end)sum+=d[i]*d[i];}   /* all: the energy in the same 2.6 s for everyone (fair loudness) */
      let st0=0;while(st0<d.length&&Math.abs(d[st0])<.001)st0++;const M=2048,mag=[];   /* the first 93 ms after it starts */
      for(let k=1;k<M/4;k++){let re=0,im=0;for(let i=0;i<M;i++){const x=(d[st0+i]||0)*(.5-.5*Math.cos(2*Math.PI*i/M));re+=x*Math.cos(2*Math.PI*k*i/M);im-=x*Math.sin(2*Math.PI*k*i/M);}mag.push(Math.hypot(re,im));}
      let top=0,ws=0,w=0;mag.forEach((m,i)=>{if(m>mag[top])top=i;ws+=m*(i+1);w+=m;});
      return {peak,loud:Math.sqrt(all/d.length),rms:end?Math.sqrt(sum/end):0,secs:end/sr,pitch:(top+1)*sr/M,bright:w?ws/w*sr/M:0};}
    finally{TEST=null;bus=null;FORCE=null;}}
  return {play,hover,demo,demoing,render,voiceOf,log:LOG,instruments:SUBJ,stages:STG,voices:Object.keys(VOICES),scales:Object.keys(SCALE),now:()=>who().prof,_force:x=>{FORCE=x;}};})();
try{window.__SOUND=SOUND;}catch(e){}   /* for the tests only (tests_browser/test_sounds.py measures the sounds offline) */
