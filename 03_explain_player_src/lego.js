/* ===== 🧱 LEGO DRAWINGS (batch 29 · 💡 Hareth's idea «ليغو الرسومات + الاستعارة») =====
   A concept with NO drawing of its own gets one BUILT from ready parts drawn in our style:
     ONE main part (the metaphor: memory = drawers, processor = chip, error = bug…) + its face + up to 2 small badges.
   The picture key carries the whole recipe, so it needs nothing else:
     «lego:<main>:<extra>+<extra>:<colour 0-7>:<motion>»      e.g.  lego:drawers:gear+spark:3:wobble
   WHO decides the recipe: the factory (02_question_factory/lego.py) — by the concept's words (no AI), or the MODEL once
   (it only CHOOSES parts from these lists; it never draws). WHO draws: this code + the browser.
   The API draws the SAME pictures: every part is exported with holes ({{FILL}} {{INK}}) to art/art.json, and
   core/art.py puts them together exactly like legoSVG below (a browser test checks both give the same SVG). */
const LEGO_MAIN={   /* C = the concept's colours {f fill, k ink} · every main part: (C) → svg, + where its face goes [x, y, size] */
 drawers:{d:C=>`<rect x="14" y="8" width="72" height="86" rx="8" fill="${C.f}" ${OL}/>${[16,42,68].map(y=>`<rect x="22" y="${y}" width="56" height="20" rx="4" fill="#fff" opacity=".9" ${OL}/><circle cx="50" cy="${y+15}" r="2.6" fill="${C.k}"/>`).join("")}`,face:[50,25,.34]},
 chip:{d:C=>`${[30,42,54,66].map(v=>`<path d="M${v} 10 V22 M${v} 78 V90 M10 ${v} H22 M78 ${v} H90" stroke="#3b2a1a" stroke-width="3" stroke-linecap="round"/>`).join("")}<rect x="20" y="20" width="60" height="60" rx="8" fill="${C.f}" ${OL}/><rect x="31" y="31" width="38" height="38" rx="5" fill="#fff" opacity=".55"/>`,face:[50,51,.52]},
 screen:{d:C=>`<rect x="10" y="8" width="80" height="58" rx="8" fill="${C.f}" ${OL}/><rect x="16" y="14" width="68" height="46" rx="4" fill="#EAF6FB" ${OL}/><path d="M42 66 H58 L62 80 H38Z" fill="#C8CDD2" ${OL}/><rect x="26" y="80" width="48" height="9" rx="4" fill="#9AA6B2" ${OL}/>`,face:[50,38,.55]},
 keyboard:{d:C=>`<rect x="6" y="28" width="88" height="52" rx="9" fill="${C.f}" ${OL}/>${[14,28,42,56,70].map(x=>`<rect x="${x}" y="58" width="11" height="9" rx="2" fill="#fff" ${OL}/>`).join("")}<rect x="30" y="70" width="40" height="6" rx="2" fill="#fff" opacity=".9"/>`,face:[50,43,.42]},
 page:{d:C=>`<path d="M20 6 H62 L82 26 V94 H20Z" fill="#fff" ${OL}/><path d="M62 6 V26 H82Z" fill="${C.f}" ${OL}/>${[64,72,80].map(y=>`<path d="M30 ${y} H72" stroke="${C.k}" stroke-width="3" stroke-linecap="round"/>`).join("")}`,face:[50,40,.5]},
 code:{d:C=>`<rect x="8" y="16" width="84" height="68" rx="12" fill="${C.f}" ${OL}/><text x="50" y="76" text-anchor="middle" font-size="20" font-weight="900" fill="#fff" direction="ltr" font-family="monospace">&lt;/&gt;</text>`,face:[50,40,.46]},
 bug:{d:C=>`<path d="M28 44 L10 36 M26 60 L8 60 M28 76 L12 86 M72 44 L90 36 M74 60 L92 60 M72 76 L88 86 M44 16 L36 4 M56 16 L64 4" stroke="#3b2a1a" stroke-width="3" stroke-linecap="round"/><circle cx="50" cy="24" r="12" fill="#3b2a1a"/><ellipse cx="50" cy="60" rx="26" ry="32" fill="${C.f}" ${OL}/><path d="M50 30 V92" stroke="${C.k}" stroke-width="2.4"/>`,face:[50,58,.5]},
 stairs:{d:C=>`<path d="M8 92 V72 H30 V52 H52 V32 H74 V12 H92 V92Z" fill="${C.f}" ${OL}/><text x="19" y="86" text-anchor="middle" font-size="12" font-weight="900" fill="#fff" direction="ltr">1</text><text x="41" y="66" text-anchor="middle" font-size="12" font-weight="900" fill="#fff" direction="ltr">2</text><text x="63" y="46" text-anchor="middle" font-size="12" font-weight="900" fill="#fff" direction="ltr">3</text>`,face:[78,72,.42]},
 gear:{d:C=>`${[0,45,90,135,180,225,270,315].map(a=>`<rect x="43" y="6" width="14" height="18" rx="3" fill="${C.f}" ${OL} transform="rotate(${a} 50 50)"/>`).join("")}<circle cx="50" cy="50" r="33" fill="${C.f}" ${OL}/>`,face:[50,52,.58]},
 lock:{d:C=>`<path d="M32 46 V30 C32 10 68 10 68 30 V46" fill="none" stroke="#9AA6B2" stroke-width="8"/><rect x="16" y="42" width="68" height="52" rx="10" fill="${C.f}" ${OL}/><circle cx="50" cy="80" r="4" fill="${C.k}"/>`,face:[50,62,.48]},
 key:{d:C=>`<rect x="48" y="44" width="46" height="12" rx="3" fill="${C.f}" ${OL}/><rect x="78" y="54" width="6" height="12" fill="${C.f}" ${OL}/><rect x="88" y="54" width="6" height="16" fill="${C.f}" ${OL}/><circle cx="30" cy="50" r="24" fill="${C.f}" ${OL}/>`,face:[30,50,.48]},
 bulb:{d:C=>`<path d="M12 18 L4 12 M88 18 L96 12 M50 4 V0" stroke="#F2C230" stroke-width="3" stroke-linecap="round"/><circle cx="50" cy="40" r="30" fill="${C.f}" ${OL}/><rect x="37" y="68" width="26" height="9" rx="3" fill="#C8CDD2" ${OL}/><rect x="39" y="77" width="22" height="9" rx="3" fill="#9AA6B2" ${OL}/>`,face:[50,40,.58]},
 magnifier:{d:C=>`<path d="M64 64 L90 90" stroke="#7A4D2B" stroke-width="11" stroke-linecap="round"/><circle cx="42" cy="42" r="32" fill="#EAF6FB" ${OL}/><circle cx="42" cy="42" r="28" fill="none" stroke="${C.f}" stroke-width="7"/>`,face:[42,44,.52]},
 envelope:{d:C=>`<rect x="8" y="20" width="84" height="62" rx="8" fill="${C.f}" ${OL}/><path d="M10 24 L50 54 L90 24" fill="none" stroke="#fff" stroke-width="3.4" stroke-linejoin="round"/>`,face:[50,68,.42]},
 globe:{d:C=>`<circle cx="50" cy="50" r="42" fill="#62A8EE" ${OL}/><path d="M22 34 Q32 22 44 30 Q46 42 34 46 Q24 46 22 34Z M58 22 Q74 20 78 34 Q70 42 60 36Z M54 66 Q68 62 74 72 Q66 84 56 80Z" fill="${C.f}" ${OL}/><ellipse cx="50" cy="50" rx="18" ry="42" fill="none" stroke="#fff" stroke-width="2" opacity=".6"/>`,face:[44,58,.46]},
 flag:{d:C=>`<rect x="16" y="6" width="7" height="88" rx="3" fill="#9AA6B2" ${OL}/><path d="M23 10 H86 L74 30 L86 50 H23Z" fill="${C.f}" ${OL}/>`,face:[50,30,.46]},
 shield:{d:C=>`<path d="M50 6 L88 18 C88 58 72 82 50 94 C28 82 12 58 12 18Z" fill="${C.f}" ${OL}/><path d="M40 70 L48 78 L62 62" fill="none" stroke="#fff" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>`,face:[50,44,.54]},
 cube:{d:C=>`<path d="M12 28 L50 46 V94 L12 76Z" fill="${C.f}" ${OL}/><path d="M88 28 L50 46 V94 L88 76Z" fill="${C.f}" ${OL}/><path d="M88 28 L50 46 V94 L88 76Z" fill="#000" opacity=".12"/><path d="M50 10 L88 28 L50 46 L12 28Z" fill="${C.f}" ${OL}/><path d="M50 10 L88 28 L50 46 L12 28Z" fill="#fff" opacity=".45"/>`,face:[31,62,.36]},
 chart:{d:C=>`<rect x="6" y="8" width="88" height="84" rx="10" fill="#fff" ${OL}/><rect x="50" y="56" width="10" height="28" fill="${C.f}" ${OL}/><rect x="64" y="40" width="10" height="44" fill="${C.f}" ${OL}/><rect x="78" y="22" width="10" height="62" fill="${C.f}" ${OL}/><path d="M12 84 H90" stroke="#3b2a1a" stroke-width="2.6"/>`,face:[27,44,.4]},
 pot:{d:C=>`<path d="M36 22 Q32 14 38 8 M50 22 Q46 14 52 6 M64 22 Q60 14 66 8" fill="none" stroke="#9AA6B2" stroke-width="3" stroke-linecap="round"/><path d="M4 50 H14 M86 50 H96" stroke="#3b2a1a" stroke-width="6" stroke-linecap="round"/><path d="M14 40 H86 V72 C86 86 74 92 50 92 C26 92 14 86 14 72Z" fill="${C.f}" ${OL}/><rect x="8" y="32" width="84" height="10" rx="5" fill="#9AA6B2" ${OL}/>`,face:[50,66,.5]},
 puzzle:{d:C=>`<path d="M18 30 H40 C40 16 60 16 60 30 H82 V50 C96 50 96 72 82 72 V92 H18Z" fill="${C.f}" ${OL}/>`,face:[48,62,.52]},
 people:{d:C=>`<path d="M48 92 V68 C48 54 86 54 86 68 V92Z" fill="${C.k}" ${OL}/><circle cx="67" cy="38" r="12" fill="#F6C9A0" ${OL}/><circle cx="63" cy="37" r="1.8" fill="#2a1d12"/><circle cx="71" cy="37" r="1.8" fill="#2a1d12"/><path d="M12 92 V64 C12 48 56 48 56 64 V92Z" fill="${C.f}" ${OL}/><circle cx="34" cy="30" r="14" fill="#F6C9A0" ${OL}/>`,face:[34,31,.34]},
 trophy:{d:C=>`<path d="M28 18 C10 18 12 42 30 42 M72 18 C90 18 88 42 70 42" fill="none" stroke="${C.k}" stroke-width="5"/><path d="M28 8 H72 V30 C72 50 62 60 50 60 C38 60 28 50 28 30Z" fill="${C.f}" ${OL}/><rect x="44" y="60" width="12" height="16" fill="${C.f}" ${OL}/><rect x="28" y="76" width="44" height="14" rx="3" fill="${C.k}" ${OL}/>`,face:[50,32,.48]},
 note:{d:C=>`<path d="M40 74 V20 M84 64 V10" stroke="#3b2a1a" stroke-width="4"/><path d="M40 18 L84 8 V22 L40 32Z" fill="${C.k}" ${OL}/><ellipse cx="72" cy="66" rx="14" ry="10" fill="${C.f}" ${OL}/><ellipse cx="28" cy="76" rx="16" ry="12" fill="${C.f}" ${OL}/>`,face:[28,76,.34]},
 ball:{d:C=>`<circle cx="50" cy="52" r="40" fill="${C.f}" ${OL}/><path d="M14 40 C34 50 66 50 86 40 M50 12 C40 32 40 72 50 92" fill="none" stroke="#fff" stroke-width="3" opacity=".8"/>`,face:[50,58,.5]},
 bag:{d:C=>`<path d="M36 34 V24 C36 10 64 10 64 24 V34" fill="none" stroke="#7A4D2B" stroke-width="5"/><rect x="14" y="32" width="72" height="60" rx="10" fill="${C.f}" ${OL}/><rect x="14" y="44" width="72" height="8" fill="#fff" opacity=".45"/>`,face:[50,70,.5]},
 hourglass:{d:C=>`<path d="M26 14 H74 C74 36 56 44 56 50 C56 56 74 64 74 86 H26 C26 64 44 56 44 50 C44 44 26 36 26 14Z" fill="#EAF6FB" ${OL}/><path d="M32 22 H68 C66 34 54 40 50 46 C46 40 34 34 32 22Z" fill="${C.f}"/><path d="M30 84 C32 72 44 66 50 64 C56 66 68 72 70 84Z" fill="${C.f}"/><rect x="16" y="6" width="68" height="9" rx="4" fill="#9AA6B2" ${OL}/><rect x="16" y="85" width="68" height="9" rx="4" fill="#9AA6B2" ${OL}/>`,face:[50,76,.3]}};
const LEGO_EXTRA={  /* small badges (drawn around 0,0 inside a white circle r=13) */
 plus:C=>`<path d="M-6 0 H6 M0 -6 V6" stroke="${C.k}" stroke-width="4" stroke-linecap="round"/>`,
 check:C=>`<path d="M-6 0 L-2 5 L7 -5" fill="none" stroke="#2E9E5B" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>`,
 question:C=>`<text y="6" text-anchor="middle" font-size="17" font-weight="900" fill="${C.k}" direction="ltr">?</text>`,
 spark:C=>`<path d="M0 -9 L2.5 -2.5 L9 0 L2.5 2.5 L0 9 L-2.5 2.5 L-9 0 L-2.5 -2.5Z" fill="#F2C230" stroke="#3b2a1a" stroke-width="1.4"/>`,
 arrow:C=>`<path d="M-7 0 H5 M0 -5 L6 0 L0 5" fill="none" stroke="${C.k}" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"/>`,
 heart:C=>`<path d="M0 8 C-12 0 -8 -10 0 -4 C8 -10 12 0 0 8Z" fill="#E8574A" stroke="#3b2a1a" stroke-width="1.4"/>`,
 star:C=>`<path d="M0 -9 L2.6 -3 L9 -2.8 L4 1.4 L5.6 8 L0 4.4 L-5.6 8 L-4 1.4 L-9 -2.8 L-2.6 -3Z" fill="#F2C230" stroke="#3b2a1a" stroke-width="1.4"/>`,
 link:C=>`<rect x="-9" y="-4" width="11" height="8" rx="4" fill="none" stroke="${C.k}" stroke-width="2.6"/><rect x="-2" y="-4" width="11" height="8" rx="4" fill="none" stroke="${C.k}" stroke-width="2.6"/>`,
 binary:C=>`<text y="4" text-anchor="middle" font-size="10" font-weight="900" fill="${C.k}" direction="ltr" font-family="monospace">01</text>`,
 drop:C=>`<path d="M0 -9 C4 -3 7 0 7 3 C7 7 4 9 0 9 C-4 9 -7 7 -7 3 C-7 0 -4 -3 0 -9Z" fill="#62A8EE" stroke="#3b2a1a" stroke-width="1.4"/>`,
 cog:C=>`<circle r="5" fill="#9AA6B2" stroke="#3b2a1a" stroke-width="1.4"/><path d="M0 -9 V-5 M0 5 V9 M-9 0 H-5 M5 0 H9" stroke="#3b2a1a" stroke-width="2.4" stroke-linecap="round"/>`,
 tune:C=>`<path d="M-2 5 V-7 L6 -9 V3" fill="none" stroke="${C.k}" stroke-width="2.4"/><circle cx="-4" cy="5" r="3" fill="${C.k}"/><circle cx="4" cy="3" r="3" fill="${C.k}"/>`};
const LEGO_SPOTS=[[16,14],[84,86]];                                   /* where the badges sit: top-left + bottom-right (away from the faces, and from the scene number at the top-right) */
const LEGO_MOTIONS=["bob","wobble","bounce","sway","sun","buzz","wiggle","drip"];   /* the moves the page already has (alive.css) */
const LEGO_BADGE=i=>`<g transform="translate(${LEGO_SPOTS[i][0]} ${LEGO_SPOTS[i][1]})"><circle r="13" fill="#fff" ${OL}/>`;
function legoParts(e){if(typeof e!=="string"||!e.startsWith("lego:"))return null;const p=e.split(":");const m=p[1];if(!LEGO_MAIN[m])return null;
  const x=(p[2]||"").split("+").filter(k=>LEGO_EXTRA[k]).slice(0,2);const c=Math.abs(parseInt(p[3],10)||0)%SUBJ_COLORS.length;
  return {m:m,x:x,c:c,mo:LEGO_MOTIONS.includes(p[4])?p[4]:"bob"};}
/* the drawing with holes for the colours: what the API gets (art.json → lego) and what the page fills below */
const LEGO_HOLES={f:"{{FILL}}",k:"{{INK}}"};
const legoMainTemplate=m=>{const P=LEGO_MAIN[m];return P.d(LEGO_HOLES)+faceSVG(P.face[0],P.face[1],P.face[2]);};
const legoExtraTemplate=k=>LEGO_EXTRA[k](LEGO_HOLES);
function legoSVG(e){const p=legoParts(e);if(!p)return null;const col=SUBJ_COLORS[p.c];
  const s=legoMainTemplate(p.m)+p.x.map((k,i)=>LEGO_BADGE(i)+legoExtraTemplate(k)+"</g>").join("");
  return s.split("{{FILL}}").join(col[0]).split("{{INK}}").join(col[1]);}
ARTS.lego=legoSVG;
