/* ======================= 👥 THE AGE STAGES (grade 1 → 12) =======================
   The same scenes for every grade, but the WORLD around them grows up with the student:
   · 🌈 kids   (1–4):  a playful friend — full faces, giggles, hops, emoji, playful sounds (as before);
   · 🧭 junior (5–7):  a curious explorer — faces without cheeks, no giggles, fewer emoji, soft sounds;
   · 🔬 teen   (8–9):  a confident classmate — eyes only, no hopping, «بيعتمد على» instead of «بيحتاج», clean clicks, a lab-notebook look;
   · 📐 senior (10–12): a calm expert — NO faces (textbook diagrams, thin lines), no emoji in the words, «نقاش» instead of «حوار», almost silent.
   The stage comes from the lesson (lesson.audience.stage, set by the factory from the book's grade). A small switcher lets you try any stage. */
const STAGES={
  kids:  {label:"الصغار",grades:"١–٤",icon:"🌈",persona:"رفيق مرح",giggle:true},
  junior:{label:"ابتدائي عليا",grades:"٥–٧",icon:"🧭",persona:"مستكشف فضولي",giggle:false},
  teen:  {label:"إعدادي",grades:"٨–٩",icon:"🔬",persona:"زميل واثق",giggle:false},
  senior:{label:"ثانوي",grades:"١٠–١٢",icon:"📐",persona:"خبير هادي",giggle:false}};
const STAGE_ORDER=["kids","junior","teen","senior"];
let STAGE_OVERRIDE=null;
function stageAuto(){const l=lesson()||{},g=graph()||{};const a=l.audience||g.audience||{};return STAGES[a.stage]?a.stage:"kids";}
function stageNow(){return STAGE_OVERRIDE&&STAGES[STAGE_OVERRIDE]?STAGE_OVERRIDE:stageAuto();}
const grown=()=>stageNow()==="teen"||stageNow()==="senior";

/* ---- 🗣️ the VOICE: the same sentence, said the way that age talks (the factory does the same in Python: audience.py) ---- */
const VOICE_WORDS=[["من اللي بيحتاج، للي بيحتاجه","من اللي بيعتمد، للي بيعتمد عليه"],["شو بتحتاجي؟","على شو بتعتمدي؟"],["شو بتحتاج؟","على شو بتعتمد؟"],["شو بيحتاج","على شو بيعتمد"],["بيحتاجك","بيعتمد عليك"],["بتحتاجي","بتعتمدي على"],
  ["خلص الحوار!","خلص النقاش."],["«يلا ←»","«التالي ←»"],["الشريط السحري","جرّب المتغيّرات"],["بيحتاجوه","بيعتمدوا عليه"],["بيحتاجوها","بيعتمدوا عليها"],["بيحتاجوا","بيعتمدوا على"],["بيحتاجه","بيعتمد عليه"],["بيحتاجها","بيعتمد عليها"],
  ["بتحتاجه","بتعتمد عليه"],["بتحتاجها","بتعتمد عليها"],["بتحتاجيني","بتعتمدي عليّ"],["بتحتاجني","بتعتمد عليّ"],["بيحتاجني","بيعتمد عليّ"],["بحتاجك","بعتمد عليك"],
  ["بيحتاج","بيعتمد على"],["بتحتاج","بتعتمد على"],["بيتعبوا","بيتأثروا"],["بيتعب","بيتأثر"],["بتتعب","بتتأثر"],["بيضل مبسوط","ما بيتأثر"],["بترجع مبسوطة","بترجع طبيعية"],
  ["بتصحى","بتتفعّل"],["بيصحى","بيتفعّل"],["صحيت","تفعّلت"],["برافو!","ممتاز."],["يلا نشوف","خلينا نشوف"]];
const VOICE_LINES={   /* whole childish lines → what a bigger student hears (teen | senior) */
  "أهلاً! 👋":["هاد أنا.","—"],"أنا هون! 👋":["هون.","هون."],"وصلتني! 😄":["وصلت.","اكتملت هالمرحلة."],"صار دوري! 😄":["دوري هلأ.","هلأ هالمرحلة."],
  "رجعت! 😄":["رجعت.","رجع يشتغل."],"وين راح؟ 😢":["غيابه أثّر عليّ.","تأثّر بغيابه."],"وأنا كمان! 😢":["وأنا كمان تأثّرت.","تأثّر كمان."],
  "اكبس المحطة الجاية، وأنا بمشي بالطريق 👣":["اكبس المحطة الجاية.","اكبس المرحلة التالية."],"اكبس المرحلة الجاية 👆":["اكبس المرحلة الجاية.","اكبس المرحلة التالية."],
  "أنا تمام 😎":["أنا ما تأثرت.","لا يتأثر."]};
const EMOJI_FACES=/[😀-🙏🤗-🤯🥰-🥺😎👋👣👆🙂]/gu;
function VOICE(t){if(t===null||t===undefined)return t;let s=String(t);const st=stageNow();if(st==="kids")return s;
  if(st==="junior")return s.replace(/\s*[😄😢😟😎]+/gu,"").replace(/\s{2,}/g," ").trim();               /* a few emoji less, the same friendly words */
  const line=VOICE_LINES[s.trim()];if(line){const v=line[st==="senior"?1:0];return v==="—"?"":v;}
  s=s.replace(/^أهلاً! أنا «([^»]+)»\.?$/,(m,n)=>st==="senior"?`تعريف «${n}».`:`هاد «${n}».`).replace(/^📌\s*/,"• ");   /* the first line of «تعرّف عليّ» */
  VOICE_WORDS.forEach(([a,b])=>{s=s.split(a).join(b);});
  s=s.replace(EMOJI_FACES,"");
  if(st==="senior")s=s.replace(/\p{Extended_Pictographic}️?/gu,m=>"✅✔️⚠️".includes(m)?m:"").replace(/(^|[^✅✔⚠])[\u200d\ufe0f]+/gu,"$1");   /* the expert: no pictures inside the words (and no leftover glue of 🧑‍🏫) */
  return s.replace(/\s+([.،!؟:])/g,"$1").replace(/\s{2,}/g," ").trim();}

/* ---- ➜ the WORD ON THE ARROWS, by subject (batch 28): maths «مبني على», history «بسبب»; the other subjects as each age says it ---- */
const ARROW_WORDS={math:"مبني على",history:"بسبب"};
function ARROW_WORD(){const k=(graph()||{}).subject;return ARROW_WORDS[k]||VOICE("بيحتاج");}
function ARROW_LEGEND(){const k=(graph()||{}).subject;
  if(k==="math")return "➜ السهم يعني «مبني على»: من الدرس الجديد، للي مبني عليه";
  if(k==="history")return "➜ السهم يعني «بسبب»: من اللي صار، للي كان السبب";
  return VOICE("➜ السهم يعني «بيحتاج»: من اللي بيحتاج، للي بيحتاجه");}

/* ---- 🔊 the SOUNDS of each stage (all made in the browser; kids = the original playful set) ---- */
const tick=(f,v)=>()=>noise(.03,f||3200,(f||3200)*.8,v||.06,0,2);
const chime=(notes,v,gap)=>()=>notes.forEach((f,i)=>tone(f,f,.22,"sine",v||.05,i*(gap||.09)));
const SILENT=null;
const SOUND_PACKS={
  kids:null,
  junior:{__default:undefined,giggle:SILENT,laugh:SILENT,meow:SILENT,burp:SILENT,sneeze:SILENT,yip:SILENT,honk:SILENT,spit:SILENT,chew:SILENT,
          pop:()=>tone(620,980,.07,"sine",.07),tada:chime([523,659,784],.06),cheer:chime([523,659,784,1046],.05),good:chime([660,880],.06,.07)},
  teen:  {__default:tick(2600,.05),giggle:SILENT,laugh:SILENT,sparkle:chime([1320,1760],.035,.07),cheer:chime([587,880],.05),tada:chime([587,880],.05),good:chime([660,990],.045,.06),
          bad:()=>tone(330,260,.12,"sine",.05),pop:tick(3200,.07),flip:()=>noise(.05,2600,1800,.06),step:tick(1800,.05),bloom:()=>tone(660,880,.18,"sine",.045),
          wind:()=>noise(.5,300,700,.05,0,.5),water:()=>noise(.3,1200,500,.06,0,.8),buzz:()=>tone(200,210,.25,"sine",.02),ding:chime([1320],.05)},
  senior:{__default:tick(2200,.04),giggle:SILENT,laugh:SILENT,sparkle:chime([880,1320],.03,.12),bloom:()=>tone(330,440,.3,"sine",.04),
          buzz:()=>tone(150,156,.3,"sine",.02),step:tick(1400,.04),wind:()=>noise(.6,220,500,.04,0,.5),water:()=>noise(.35,900,400,.045,0,.8),   /* 🆕 batch 29: no more silence, a deeper, calmer set */
          cheer:chime([880],.035),tada:chime([880],.035),good:chime([880],.03),bad:()=>tone(300,280,.1,"sine",.03),pop:tick(3400,.04),flip:tick(2400,.035),ding:chime([1320],.03)}};
function stagePack(){const p=SOUND_PACKS[stageNow()];return p||null;}

/* ---- the names of the activities, for each age ---- */
const SNAME_STAGE={junior:{recipe:"🧪 شو بيلزم؟"},
                   senior:{overview:"🗺️ خريطة المفاهيم",meet:"📄 التعريف",recipe:"🧪 الشروط اللازمة",connect:"✏️ ارسم العلاقات",compare:"⚖️ مقارنة",teach:"🧑‍🏫 اشرح لزميلك",slider:"🎚️ جرّب المتغيّرات",dialogue:"💬 نقاش",interview:"❓ أسئلة وأجوبة",flip:"🎴 بطاقات مراجعة",play:"🎞️ محاكاة",assemble:"🧩 ركّب المخطط",journey:"🔗 السلسلة",what_if:"🔮 شو بيصير لو"},
                   teen:{overview:"🗺️ خريطة الدرس",meet:"🪪 بطاقة تعريف",recipe:"🧪 الشروط",teach:"🧑‍🏫 اشرح لزميلك",slider:"🎚️ جرّب المتغيّرات",play:"🎞️ محاكاة",assemble:"🧩 ركّب المخطط"}};
function sceneName(kind){return ((SNAME_STAGE[stageNow()]||{})[kind])||SNAME[kind]||kind;}
const UI_STAGE={next:{kids:"يلا ←",junior:"يلا ←",teen:"التالي ←",senior:"التالي ←"},why:{kids:"📖 ليش؟",junior:"📖 ليش؟",teen:"📖 ليش؟",senior:"📖 الشرح"},
  tryit:{kids:"🖐️ هلأ دورك: جرّب بنفسك! اكبس، اسحب، وشوف شو بيصير.",junior:"🖐️ هلأ دورك: جرّب بنفسك! اكبس واسحب وشوف.",teen:"🖐️ دورك: جرّب، وشوف شو بيتغيّر.",senior:"جرّب بنفسك: حرّك واكبس، ولاحظ العلاقة."}};
const ui=key=>(UI_STAGE[key]||{})[stageNow()]||"";

/* ---- the welcome at the top: a mascot for the little ones, a lab file for teens, the lesson's objectives for seniors ---- */
function stageWelcome(l){const st=stageNow(),names=l.concepts.map(c=>c.title);
  if(st==="kids")return `<span class="big">${alive(skin().mascot)}</span><div><h1>أهلاً! 👋 أنا «${skin().name}»</h1><p>تعال نفهم <b>${l.lesson_title}</b> مع بعض: شوف، حرّك، وجرّب براحتك.</p></div>`;
  if(st==="junior")return `<span class="big">${alive(skin().mascot)}</span><div><h1>يلا نستكشف: ${l.lesson_title}</h1><p>${names.length} مفاهيم مربوطة ببعض. شوف كيف كل واحد بيعتمد على الثاني، وجرّب بإيدك.</p></div>`;
  if(st==="teen")return `<span class="stg-ic" aria-hidden="true">🔬</span><div><h1>ملف الدرس: ${l.lesson_title}</h1><p>لاحظ، جرّب، واستنتج: ${names.slice(0,4).map(n=>"«"+n+"»").join(" · ")}</p></div>`;
  return `<span class="stg-ic" aria-hidden="true">📐</span><div><h1>${l.lesson_title}</h1><p><b>الأهداف:</b> ${names.map(n=>"«"+n+"»").join("، ")}، والعلاقات بينها.</p></div>`;}
/* ---- the switcher: «auto» = from the lesson's grade; or try any stage ---- */
function stageSwitch(){const a=stageAuto(),g=(lesson()||{}).audience||graph().audience||{};
  return `<label class="stgsw"><span>👥 المرحلة:</span><select id="stageSel" aria-label="المرحلة العمرية">
    <option value="">تلقائي: ${STAGES[a].icon} ${STAGES[a].label}${g.grade?" (صف "+g.grade+")":""}</option>
    ${STAGE_ORDER.map(k=>`<option value="${k}" ${STAGE_OVERRIDE===k?"selected":""}>${STAGES[k].icon} ${STAGES[k].label} (${STAGES[k].grades})</option>`).join("")}</select></label><button class="chipbtn stg-snd" id="sndDemo" type="button" title="اسمع أصوات هالمرحلة وهالمادة">🎵 اسمع</button>`;}
function applyStage(){const st=stageNow();document.body.dataset.stage=st;
  const sel=document.getElementById("stageSel");if(sel&&!sel.__wired){sel.__wired=true;sel.addEventListener("change",()=>{STAGE_OVERRIDE=sel.value||null;sfx("pop");
    /* 🆕 batch 29: choosing a stage TAKES you to its books (the first one of that stage); its look then follows the book by itself.
       No book of that stage on this page (e.g. a page with one book) → only the look changes, as before. */
    const want=STAGE_OVERRIDE,gi=want?DATA.graphs.findIndex(g=>(g.audience||{}).stage===want):-1;
    if(gi>=0){if((DATA.graphs[EG].audience||{}).stage!==want){EG=gi;EL=0;POS=0;STEP=0;}STAGE_OVERRIDE=null;}
    renderAll2();
    if(gi>=0){const side=document.getElementById("side"),h=document.getElementById("stg-"+want);if(side&&h)side.scrollTop+=h.getBoundingClientRect().top-side.getBoundingClientRect().top;window.scrollTo({top:0});}});}
  const sd=document.getElementById("sndDemo");if(sd&&!sd.__wired){sd.__wired=true;sd.addEventListener("click",()=>{clearTimeout(TUNE_T);SOUND.demo();});}
  stageArrive();}
/* 🆕 batch 30 (Hareth): ARRIVING at a stage plays its tune by itself (the same tune as «🎵 اسمع»: this stage's character + this subject's instrument):
   choosing a stage, opening a book of another stage, or opening the page. «🎵 اسمع» stays, to hear it again.
   · the browser lets a page make a sound only after the student's FIRST touch / click / key: on opening the page the tune waits for that touch;
   · the same stage again (another lesson, another book of the same stage) = no tune; the mute button (🔇) = no tune;
   · one tune at a time: a new stage cancels the one waiting / playing. */
let ARRIVED=null,TUNE_T=0,TUNE_WAIT=false,EVER_TOUCHED=false;
function tuneSoon(){clearTimeout(TUNE_T);TUNE_T=setTimeout(()=>{TUNE_WAIT=false;SOUND.demo();},160);}   /* the stage on the screen when it plays is the one heard */
function stageArrive(){const st=stageNow();if(st===ARRIVED)return;ARRIVED=st;if(EVER_TOUCHED)tuneSoon();else TUNE_WAIT=true;}
["pointerup","keydown","touchend"].forEach(ev=>window.addEventListener(ev,e=>{if(!e.isTrusted)return;const first=!EVER_TOUCHED;EVER_TOUCHED=true;
  if(first&&soundOn)try{ac();}catch(err){}                          /* wake the sound up INSIDE the touch (phones need this) */
  if(TUNE_WAIT&&!(e.target&&e.target.closest&&e.target.closest("#stageSel")))tuneSoon();},{capture:true,passive:true}));
/* for tools only (exporting the drawings for the API, and the test that the API draws the same): */ try{window.__ART={artSVG,ART_OF,ARTS,SUBJ_ART,LEGO_MAIN,LEGO_EXTRA,LEGO_SPOTS,LEGO_MOTIONS,legoMainTemplate,legoExtraTemplate,LEGO_BADGE,legoSVG};}catch(e){}
