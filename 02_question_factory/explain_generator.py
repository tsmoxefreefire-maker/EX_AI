import re
"""The EXPLANATION factory (interactive explanation, not questions): for each lesson → for each concept → scenes that TEACH.
Rule: the picture is the explanation. Every scene says WHAT moves WHERE (flows, journeys, dominoes); the text only helps.

Scenes (all built from the graph only — no invented facts, no cost):
  overview  — the whole lesson: every concept, and arrows showing who feeds whom (learning order).
  meet      — one concept in the middle: what comes INTO it (left) and what it gives OUT (right); its meaning, piece by piece.
  journey   — a traveller goes along a chain (water → root → stem → leaf); each station wakes up and says its role.
  what_if   — switch the concept off: who needs it gets tired, one after the other (domino); switch it on again.
"""
import audience as A
import offline_generator as og
from graph_reader import Graph, Lesson

MOVERS = {"💧", "💨", "☀️"}     # things that REALLY travel (water rises, air enters, light falls). Anything else: a neutral spark.


def _she(text: str) -> bool:
    w = (text or "").split()
    if not w:
        return False
    # «الورقة» · «النباتات» (plural -ات) · «الكسور المتكافئة» (a thing-plural + a feminine adjective)
    plural_at = w[0].endswith("ات") and w[0].removeprefix("ال") not in ("إنبات", "انبات", "نبات", "ثبات", "سبات", "فتات")   # «الإنبات» is ONE thing (he)
    return w[0].endswith("ة") or plural_at or (len(w) > 1 and w[1].startswith("ال") and w[1].endswith("ة"))


def _v(text: str, he: str, she: str) -> str:
    """Arabic verb that agrees with the concept: «الجذر بيحتاج» / «الورقة بتحتاج»."""
    return she if _she(text) else he


def _join(items: list) -> str:
    items = [f"«{x}»" for x in items]
    return items[0] if len(items) == 1 else "، ".join(items[:-1]) + " و" + items[-1]


MAX_SIDE = 2          # at most 2 neighbours on each side of «meet» (clear, not crowded)


def _name(g, x):
    return g.concepts[x].text


def _role(g, nxt, here):
    """The piece of `nxt`'s meaning that mentions `here` (why the arrow exists), else its first piece."""
    parts = og.fragments(g.concepts[nxt].description) or ([og.tiny(g.concepts[nxt].description, 10)] if g.concepts[nxt].description else [])
    word = _name(g, here).replace("ال", "", 1)
    return next((p for p in parts if word and word in p), parts[0] if parts else "")


def _overview_paragraph(g, lesson, ids, edges, level):
    order = sorted(ids, key=lambda c: (level[c], ids.index(c)))
    first = [c for c in order if not any(e[1] == c for e in edges)]
    text = f"بدرس «{lesson.title}» رح نتعرّف على {len(ids)} مفاهيم: {_join([_name(g, c) for c in order])}. "
    if first:
        text += f"بنبلش بـ{_join([_name(g, c) for c in first[:2]])}، لأنه ما {('بيحتاج' if len(first) == 1 and not _she(_name(g, first[0])) else 'بتحتاج' if len(first) == 1 else 'بيحتاجوا')} إشي قبله. "
    for a, b in edges[:2]:
        text += f"«{_name(g, b)}» {_v(_name(g, b), 'بيحتاج', 'بتحتاج')} «{_name(g, a)}». "
    return text.strip()


def scene_overview(g: Graph, lesson: Lesson) -> dict:
    ids = [c.id for c in lesson.concepts]
    edges = [[a, b] for a in ids for b in g.prereq_out.get(a, []) if b in ids]
    level = {c: g.depth(c) for c in ids}
    base = min(level.values()) if level else 0
    return {"kind": "overview", "concepts": ids, "edges": edges, "levels": {c: level[c] - base for c in ids},
            "steps": [f"هاد درس «{lesson.title}»: فيه {len(ids)} مفاهيم، مرقّمة بترتيب ما بنتعلمها.",
                      "السهم معناه «بيحتاج»: اللي بعد السهم ما بيصير إلا إذا اللي قبله موجود.",
                      "اكبس على أي مفهوم، وشوف مين بيحتاج مين."],
            "paragraph": _overview_paragraph(g, lesson, ids, edges, level)}


def scene_meet(g: Graph, lesson: Lesson, cid: str) -> dict:
    ins = [p for p in sorted(g.prereq_in.get(cid, [])) if og.is_entity(g, p)][:MAX_SIDE]
    outs = [n for n in sorted(g.prereq_out.get(cid, [])) if og.is_entity(g, n)][:MAX_SIDE]
    pieces = og.fragments(g.concepts[cid].description) or ([g.concepts[cid].description.strip(" .")] if g.concepts[cid].description else [])
    st = A.stage(g)                                         # 👥 the bigger the student, the less «أهلاً! أنا…»
    first = {"teen": f"هاد «{_name(g, cid)}».", "senior": f"تعريف «{_name(g, cid)}»."}.get(st, f"أهلاً! أنا «{_name(g, cid)}».")
    bullet = "•" if st in ("teen", "senior") else "📌"
    steps = [first] + [f"{bullet} {p}." for p in pieces[:3]]   # captions on the picture (always correct Arabic)
    me = _name(g, cid)
    focus = ["target"] * len(steps)                       # what each step talks about (the camera goes THERE)
    if ins:                                                # names, not «me»: «الجذر بيحتاج «التربة» و«الماء»»
        steps.append(f"«{me}» {_v(me, 'بيحتاج', 'بتحتاج')} {_join([_name(g, x) for x in ins])}."); focus.append("ins")
    for x in outs:                                         # one sentence per character that needs it
        steps.append(f"«{_name(g, x)}» {_v(_name(g, x), 'بيحتاج', 'بتحتاج')} «{me}»."); focus.append("out:" + x)
    roles = {x: _role(g, cid, x) for x in ins}
    roles.update({x: _role(g, x, cid) for x in outs})
    para = f"«{me}»: " + (("، ".join(pieces[:2]) + ".") if pieces else "")
    if ins:
        para += f" عشان {_v(me, 'يشتغل', 'تشتغل')}، {_v(me, 'بيحتاج', 'بتحتاج')} {_join([_name(g, x) for x in ins])}."
    if outs:
        why = roles.get(outs[0], "")
        para += f" {_v(me, 'وهو مهم', 'وهي مهمة')} لـ{_join([_name(g, x) for x in outs])}" + (f"، لأنه «{_name(g, outs[0])}» {why}." if why else ".")
    return {"kind": "meet", "target": cid, "ins": ins, "outs": outs, "roles": roles, "steps": steps, "focus": focus, "paragraph": para.strip()}


def scene_journey(g: Graph, lesson: Lesson, cid: str):
    route = og.chain_through(g, cid, 2, 2)
    if len(route) < 3:
        return None
    icon = og.icon_for(_name(g, route[0]), g.concepts[route[0]].description, str(g.book.get("subject", "")))
    moves = icon in MOVERS                                  # water really rises root→stem→leaf; a flower never walks to a bee
    stops = [{"id": x, "say": (f"«{_name(g, x)}» {_v(_name(g, x), 'بيحتاج', 'بتحتاج')} «{_name(g, a)}»" + (f": {_role(g, x, a)}" if _role(g, x, a) else ""))
              if a else f"من هون بتبلش: «{_name(g, x)}»."}
             for a, x in zip([None] + route[:-1], route)]
    names = [_name(g, x) for x in route]
    para = (f"هاي رحلة «{names[0]}»: {_v(names[0], 'بيمشي', 'بتمشي')} من {' ثم '.join(f'«{n}»' for n in names[1:])}، وكل محطة بتاخدها وبتكمّل فيها."
            if moves else
            f"هاي سلسلة: {' ← '.join(f'«{n}»' for n in names)}. كل مرحلة ما بتصير إلا إذا اللي قبلها صارت؛ "
            f"يعني «{names[1]}» {_v(names[1], 'بيحتاج', 'بتحتاج')} «{names[0]}»، و«{names[-1]}» آخر وحدة.")
    return {"kind": "journey", "target": cid, "route": route, "traveller": route[0] if moves else "spark", "stops": stops,
            "steps": [f"{'رحلة «' + names[0] + '»' if moves else 'سلسلة'} من «{names[0]}» لـ «{names[-1]}».",
                      "اسحب " + ("«" + names[0] + "»" if moves else "الشرارة ✨") + " للمحطة الجاية (أو اكبس عليها).",
                      "كل محطة بتصحى لما يصير اللي قبلها."],
            "paragraph": para}


def scene_what_if(g: Graph, lesson: Lesson, cid: str):
    after = g.descendants(cid)
    chain = og.chain_through(g, cid, 0, 3)[1:]
    if not chain:
        return None
    rng = __import__("random").Random(f"explain:{cid}")
    calm = [x for x in og.tiered(g, lesson, rng, exclude={cid}) if x not in after and x not in g.ancestors(cid)][:1]
    edges = [[a, b] for a, b in zip([cid] + chain, chain)]
    return {"kind": "what_if", "target": cid, "affected": chain, "calm": calm, "edges": edges,
            "paragraph": (f"«{_name(g, cid)}» {_v(_name(g, cid), 'مهم', 'مهمة')} لأنه في مفاهيم {_v(_name(g, cid), 'بتحتاجه', 'بتحتاجها')}. لو {_v(_name(g, cid), 'اختفى', 'اختفت')}، "
                          f"«{_name(g, chain[0])}» {_v(_name(g, chain[0]), 'بيتأثر', 'بتتأثر')} أول"
                          + (f"، وبعدين {_join([_name(g, x) for x in chain[1:]])} ورا بعض، لأنه كل واحد بيحتاج اللي قبله" if len(chain) > 1 else "")
                          + (f". أما «{_name(g, calm[0])}» ما {_v(_name(g, calm[0]), 'بيتأثر', 'بتتأثر')}، لأنه ما {_v(_name(g, calm[0]), 'بيحتاج', 'بتحتاج')} «{_name(g, cid)}»." if calm else ".")),
            "steps": [f"شو بيصير لو اختفى «{_name(g, cid)}»؟",
                      "طفّي المفتاح وشوف مين بيتعب… وبعدين شغّله ثاني.",
                      ("اللي بيحتاج «" + _name(g, cid) + "» بيتعب، واللي ما بيحتاجه بيضل مبسوط.")]}


def _teaching(g: Graph, lesson: Lesson, cid: str, prev):
    """How a good teacher frames a concept: a question first (curiosity), a link to what we just learned, and one sentence to keep."""
    me = _name(g, cid)
    ins = [p for p in sorted(g.prereq_in.get(cid, [])) if og.is_entity(g, p)]
    outs = [n for n in sorted(g.prereq_out.get(cid, [])) if og.is_entity(g, n)]
    if outs:
        hook = f"شو بيصير لـ«{_name(g, outs[0])}» لو ما في «{me}»؟"
        answer = f"«{_name(g, outs[0])}» {_v(_name(g, outs[0]), 'بيتعب', 'بتتعب')}، لأنه {_v(_name(g, outs[0]), 'بيحتاج', 'بتحتاج')} «{me}»."
    elif ins:
        hook = f"«{me}» شو {_v(me, 'بيحتاج', 'بتحتاج')} عشان {_v(me, 'يشتغل', 'تشتغل')}؟"
        answer = f"{_v(me, 'بيحتاج', 'بتحتاج')} {_join([_name(g, x) for x in ins])}."
    else:
        hook = f"مين {_v(me, 'هو', 'هي')} «{me}»؟ وليش {_v(me, 'مهم', 'مهمة')}؟"
        answer = ""
    pieces = og.fragments(g.concepts[cid].description) or ([og.tiny(g.concepts[cid].description, 10)] if g.concepts[cid].description else [])
    summary = f"«{me}»" + (f": {pieces[0]}" if pieces else "") + "." + (f" {answer}" if answer else "")
    recap = None
    if prev:
        recap = f"تذكّر: تعرّفنا على «{_name(g, prev)}». هلأ دور «{me}»" + (f"، و«{me}» {_v(me, 'بيحتاج', 'بتحتاج')} «{_name(g, prev)}»!" if g.is_prereq(prev, cid) else ".")
    return {"hook": hook, "answer": answer, "summary": summary, "recap": recap}


PLANT_KIT = {"water": ("💧", "water"), "sunlight": ("☀️", "sun"), "air": ("💨", "air"), "soil": ("🟫", "soil"),
             "root": ("🫚", "root"), "stem": ("🌿", "stem"), "leaf": ("🍃", "leaf")}


def scene_world(g: Graph, lesson: Lesson):
    """A WORLD instead of a diagram: one real plant (soil, roots, stem, leaves), the student waters it, moves the sun,
    opens the window — and SEES water rise, leaves turn green, food made, the plant grow. Only for plant lessons (the plant kit)."""
    by_icon = {}
    for x in g.concepts:
        if og.is_entity(g, x):
            ic = og.icon_for(g.concepts[x].text, g.concepts[x].description, str(g.book.get("subject", "")))
            for key, (emoji, part) in PLANT_KIT.items():
                if ic == emoji and part not in by_icon:
                    by_icon[part] = x
    needs = [p for p in ("water", "sun", "air") if p in by_icon and by_icon[p] in [c.id for c in lesson.concepts]]
    if len(needs) < 2:
        return None
    nm = lambda part: _name(g, by_icon[part]) if part in by_icon else ""
    meaning = {part: (og.fragments(g.concepts[cid].description) or [g.concepts[cid].description])[:2] for part, cid in by_icon.items()}
    steps = ["🌱 هاي «بذور»، نبتة صغيرة بالتربة… بدها تكبر! خلينا نساعدها."]
    if "water" in needs: steps.append(f"🚿 اسحب الإبريق واسقيها: شوف «{nm('water')}» كيف بيطلع جوا {('«' + nm('root') + '»') if nm('root') else 'الجذور'} و{('«' + nm('stem') + '»') if nm('stem') else 'الساق'} لحد الأوراق!")
    if "sun" in needs: steps.append(f"☀️ اسحب «{nm('sun')}» لفوق السما: الأوراق بتخضرّ. نزّلها: النبتة بتضعف وبتصفرّ.")
    if "air" in needs: steps.append(f"💨 افتح الشباك: «{nm('air')}» بيدخل للأوراق.")
    steps.append("✨ لما يكونوا كلهم موجودين، الورقة بتصنع غذاء، والنبتة بتكبر وبتزهر! جرّب تشيل واحد وشوف شو بيصير.")
    para = f"النبتة بتحتاج {_join([nm(p) for p in needs])} عشان تعيش وتكبر. "
    if "water" in needs: para += f"«{nm('water')}» {meaning.get('water', [''])[0]}. "
    if "sun" in needs: para += f"و«{nm('sun')}» {meaning.get('sun', [''])[0]}، {meaning.get('sun', ['', ''])[-1]}. "
    if "air" in needs: para += f"و«{nm('air')}» {meaning.get('air', [''])[0]}. "
    para += "لما يجتمعوا، الورقة بتصنع الغذاء، والنبتة بتكبر."
    return {"kind": "world", "kit": "plant", "parts": by_icon, "needs": needs, "steps": steps, "paragraph": " ".join(para.split()),
            "info": {part: " ".join(m) for part, m in meaning.items()}}


# ===== 🎞️ motion scripts: what REALLY happens (who moves, where to, what comes out) — general verbs for every subject =====
VERBS = {"🐝": "visit", "🌬️": "carry", "🌱": "transform", "hist:wheat": "transform",
         "➕": "combine", "➖": "take_away", "✖️": "groups", "➗": "share",
         "🍕": "cut", "🔼": "cut", "🔽": "cut", "🟰": "equivalent", "⚖️": "compare",
         "hist:pyramid": "build", "💰": "exchange", "hist:river": "flow_river", "hist:glyphs": "write"}
ACTORS = {"🐝": ("النحلة", "f"), "🌬️": ("الريح", "f"), "🌱": ("البذرة", "f"), "hist:wheat": ("الفلاحين", "pl"),
          "💰": ("الناس", "pl"), "hist:pyramid": ("العمّال", "pl"), "hist:river": ("النهر", "m"), "hist:glyphs": ("الكاتب", "m")}


def _icon(g, x):
    return og.icon_for(g.concepts[x].text, g.concepts[x].description, str(g.book.get("subject", "")))


def scene_play(g: Graph, lesson: Lesson, cid: str):
    """A short film of the real process (cinema first, then the student drives it). Only from rules that are true in nature/maths/history."""
    icon = _icon(g, cid); verb = VERBS.get(icon)
    if not verb:
        return None
    me = _name(g, cid)
    ins = [p for p in sorted(g.prereq_in.get(cid, [])) if og.is_entity(g, p)]
    outs = [x for x in sorted(g.prereq_out.get(cid, [])) if og.is_entity(g, x)]
    who, gender = ACTORS.get(icon, (me, "f" if _she(me) else "m"))
    she = gender == "f"
    tgt = ins[0] if ins else None
    res = outs[0] if outs else None
    T = lambda x: f"«{_name(g, x)}»" if x else ""
    v = lambda he_, she_, pl_=None: (pl_ or he_ + "وا") if gender == "pl" else (she_ if she else he_)
    if verb == "visit":
        if not tgt:
            return None
        steps = [f"🐝 «{who}» {v('بيطير', 'بتطير')} لـ{T(tgt)}…",
                 f"{v('بينقل', 'بتنقل')} حبوب اللقاح بين الأزهار: هاد هو «{me}».",
                 (f"وبعد «{me}»، بتتكوّن {T(res)} من {T(tgt)} 🍎." if res else f"وهيك صار «{me}».")]
        drive = f"اسحب «{who}» لـ{T(tgt)} 🐝"
    elif verb == "carry":
        item = tgt
        if not item:
            return None
        steps = [f"🌬️ «{who}» {v('بيهب', 'بتهب')}…", f"{v('بيحمل', 'بتحمل')} {T(item)} لمكان بعيد: هاد هو «{me}».",
                 (f"بتوقع بأرض جديدة، وبيصير {T(res)} 🌱." if res else "وبتوقع بأرض جديدة 🌱.")]
        drive = f"اسحب {T(item)} مع «{who}» لبعيد 🌬️"
    elif verb == "transform":
        if not tgt:
            return None
        steps = [f"هاي {T(tgt)}…", f"شوف! {T(tgt)} {v('بيتغير', 'بتتغير')}: هاد هو «{me}».", (f"وبعدها بيصير {T(res)}." if res else "")]
        drive = f"اكبس على {T(tgt)} وشوف شو بيصير 👆"
    elif verb in ("combine", "take_away", "groups", "share"):
        ex = {"combine": (3, 4, 7, "+"), "take_away": (7, 3, 4, "−"), "groups": (3, 4, 12, "×"), "share": (12, 3, 4, "÷")}[verb]
        a, b, r, op = ex
        say_ = {"combine": f"عنا {a} و{b}… بنجمعهم مع بعض: {a} + {b} = {r}. هاد هو «{me}».",
                "take_away": f"عنا {a}… بناخد منهم {b}: بيضل {r}. {a} − {b} = {r}. هاد هو «{me}».",
                "groups": f"{a} صفوف، بكل صف {b}: كلهم {r}. {a} × {b} = {r}. هاد هو «{me}».",
                "share": f"عنا {a}، بنوزعهم على {b} مجموعات متساوية: كل مجموعة {r}. {a} ÷ {b} = {r}. هاد هو «{me}»."}[verb]
        steps = [f"🔢 مثال على «{me}»:", say_, (f"و«{me}» {v('بيحتاج', 'بتحتاج')} {T(tgt)}." if tgt else "")]
        drive = {"combine": "اسحب المجموعتين لبعض ➕", "take_away": "اسحب المكعبات لبرا ➖", "groups": "اكبس لتعمل صف جديد ✖️", "share": "اسحب المكعبات للمجموعات ➗"}[verb]
        return {"kind": "play", "verb": verb, "target": cid, "example": {"a": a, "b": b, "r": r, "op": op},
                "steps": [x for x in steps if x], "drive": drive, "paragraph": steps[1]}
    elif verb in ("cut", "equivalent", "compare"):
        ex = {"🍕": {"parts": 4, "shade": 1}, "🔼": {"parts": 8, "shade": 3, "show": "top"}, "🔽": {"parts": 8, "shade": 3, "show": "bottom"}}.get(icon, {"parts": 4, "shade": 2})
        if verb == "cut":
            say_ = (f"بنقطّع البيتزا لـ{ex['parts']} قطع متساوية، وبناخد {ex['shade']}: الكسر {ex['shade']}/{ex['parts']}." if icon == "🍕" else
                    f"البسط = عدد القطع اللي أخذناها: {ex['shade']}." if icon == "🔼" else f"المقام = كم قطعة متساوية بالكل: {ex['parts']}.")
        elif verb == "equivalent":
            say_ = "نص بيتزا (1/2) = قطعتين من أربع (2/4): نفس الكمية، شكل مختلف."
        else:
            say_ = "قارن: 1/2 أكبر من 1/4، لأنه القطعة أكبر لما نقسم على عدد أقل."
        steps = [f"🍕 مثال على «{me}»:", say_ + f" هاد هو «{me}».", (f"و«{me}» {v('بيحتاج', 'بتحتاج')} {T(tgt)}." if tgt else "")]
        drive = "اكبس على البيتزا لتقطّعها 🔪" if verb == "cut" else "اكبس لتشوف المقارنة 👆"
        return {"kind": "play", "verb": verb, "target": cid, "example": ex, "steps": [x for x in steps if x], "drive": drive, "paragraph": steps[1]}
    elif verb == "build":
        steps = [f"«{who}» {v('بيجيب', 'بتجيب', 'بيجيبوا')} الحجارة…", f"حجر فوق حجر… لحد ما {v('بيبني', 'بتبني', 'بيبنوا')} «{me}» 🔺.", (f"و{T(tgt)} هم اللي أمروا ببنائها." if tgt else "")]
        drive = "اسحب الحجارة وابني 🧱"
    elif verb == "exchange":
        steps = [f"هون في ناس عندهم بضاعة، وناس عندهم نقود…", f"بيتبادلوا: البضاعة بتروح والنقود بتيجي. هاد هو «{me}» 💰.", (f"و«{me}» {v('بتحتاج', 'بتحتاج')} {T(tgt)}." if tgt else "")]
        drive = "اسحب البضاعة للشاري 🛒"
    elif verb == "flow_river":
        steps = [f"«{me}» بيجري 🌊…", "المي بتوصل للأرض اللي حواليه…", (f"وبتصير {T(res)} 🌾." if res else "")]
        drive = "اكبس على النهر ليجري 🌊"
    elif verb == "write":
        steps = [f"«{who}» بيمسك اللوح…", f"وبيرسم صور بدل الحروف: هاي «{me}» 𓂀.", ""]
        drive = "اكبس لترسم صورة جديدة ✍️"
    else:
        return None
    return {"kind": "play", "verb": verb, "target": cid, "actor": who, "with": tgt, "result": res,
            "steps": [x for x in steps if x], "drive": drive, "paragraph": " ".join(x for x in steps[1:] if x)}


# ===== more kinds of activity (so it never feels the same) =====
def scene_interview(g: Graph, lesson: Lesson, cid: str) -> dict:
    """🎤 The student interviews the character: taps a question, the character answers (from the graph)."""
    me = _name(g, cid)
    ins = [p for p in sorted(g.prereq_in.get(cid, [])) if og.is_entity(g, p)]
    outs = [x for x in sorted(g.prereq_out.get(cid, [])) if og.is_entity(g, x)]
    pieces = og.fragments(g.concepts[cid].description) or ([g.concepts[cid].description.strip(" .")] if g.concepts[cid].description else [])
    st = A.stage(g)
    if st == "senior":                                     # the expert: questions ABOUT the concept, answers in the third person
        qa = [{"q": f"شو {_v(me, 'هو', 'هي')} «{me}»؟", "a": f"«{me}»" + (f": {pieces[0]}." if pieces else ".")}]
        if len(pieces) > 1:
            qa.append({"q": f"شو {_v(me, 'وظيفته', 'وظيفتها')}؟", "a": "، ".join(pieces[1:3]) + "."})
        if ins:
            qa.append({"q": f"على شو {_v(me, 'بيعتمد', 'بتعتمد')}؟", "a": f"«{me}» {_v(me, 'بيحتاج', 'بتحتاج')} {_join([_name(g, x) for x in ins])}."})
        if outs:
            qa.append({"q": f"مين بيعتمد {_v(me, 'عليه', 'عليها')}؟", "a": " ".join(f"«{_name(g, x)}» {_v(_name(g, x), 'بيحتاج', 'بتحتاج')} «{me}»." for x in outs)})
            qa.append({"q": f"شو بيصير لو {_v(me, 'غاب', 'غابت')}؟", "a": f"{_join([_name(g, x) for x in outs])} {('بيتعب' if len(outs) == 1 and not _she(_name(g, outs[0])) else 'بتتعب' if len(outs) == 1 else 'بيتعبوا')}."})
    else:
        teen = st == "teen"
        qa = [{"q": (f"شو {_v(me, 'إنت', 'إنتِ')} بالضبط؟" if teen else f"مين {_v(me, 'إنت', 'إنتِ')}؟"), "a": f"أنا «{me}»" + (f": {pieces[0]}." if pieces else ".")}]
        if len(pieces) > 1:
            qa.append({"q": f"شو {_v(me, 'بتعمل', 'بتعملي')}؟", "a": "، ".join(pieces[1:3]) + "."})
        if ins:
            qa.append({"q": f"شو {_v(me, 'بتحتاج', 'بتحتاجي')}؟", "a": f"«{me}» {_v(me, 'بيحتاج', 'بتحتاج')} {_join([_name(g, x) for x in ins])}."})
        if outs:
            qa.append({"q": f"مين بيحتاجك؟", "a": " ".join(f"«{_name(g, x)}» {_v(_name(g, x), 'بيحتاج', 'بتحتاج')} «{me}»." for x in outs)})
            qa.append({"q": f"شو بيصير لو {_v(me, 'اختفيت', 'اختفيتِ')}؟", "a": f"{_join([_name(g, x) for x in outs])} {('بيتعب' if len(outs) == 1 and not _she(_name(g, outs[0])) else 'بتتعب' if len(outs) == 1 else 'بيتعبوا')}" + ("." if teen else " 😢")})
    return {"kind": "interview", "target": cid, "qa": qa,
            "steps": ([f"❓ أسئلة وأجوبة عن «{me}»", "اكبس أي سؤال وشوف الجواب."] if st == "senior" else [f"🎤 مقابلة مع «{me}»!", "اكبس على أي سؤال، و«" + me + "» بيجاوبك."]),
            "paragraph": " ".join(x["a"] for x in qa)}


def scene_flip(g: Graph, lesson: Lesson, cid: str) -> dict:
    """🎴 Cards to flip: each card hides one fact about the concept."""
    me = _name(g, cid)
    ins = [p for p in sorted(g.prereq_in.get(cid, [])) if og.is_entity(g, p)]
    outs = [x for x in sorted(g.prereq_out.get(cid, [])) if og.is_entity(g, x)]
    pieces = og.fragments(g.concepts[cid].description) or ([g.concepts[cid].description.strip(" .")] if g.concepts[cid].description else [])
    # every back is a WHOLE sentence that makes sense alone (the back no longer shows «الجذر .» by itself)
    cards = [{"front": "🔎 شو هو؟", "back": f"«{me}»: {pieces[0]}." if pieces else f"«{me}»."}]
    if len(pieces) > 1:
        cards.append({"front": f"⚙️ شو {_v(me, 'بيعمل', 'بتعمل')}؟", "back": f"«{me}» {pieces[1]}."})
    if ins:
        cards.append({"front": f"🧺 شو {_v(me, 'بيحتاج', 'بتحتاج')}؟", "back": f"«{me}» {_v(me, 'بيحتاج', 'بتحتاج')} {_join([_name(g, x) for x in ins])}."})
    if outs:
        cards.append({"front": f"🤝 مين {_v(me, 'بيحتاجه', 'بيحتاجها')}؟",
                      "back": " ".join(f"«{_name(g, x)}» {_v(_name(g, x), 'بيحتاج', 'بتحتاج')} «{me}»." for x in outs[:2])})
    return {"kind": "flip", "target": cid, "cards": cards,
            "steps": [f"🎴 بطاقات مراجعة: «{me}». اقلب كل بطاقة." if A.stage(g) == "senior" else f"🎴 بطاقات «{me}»: اقلب كل بطاقة وشوف شو وراها!"], "paragraph": " ".join(c["back"] for c in cards)}


# «a» really TURNS INTO «b» (seed → sprouting) only when the graph's own words say so; otherwise it is «b needs a»
_GROW_FROM = ("تنمو من", "ينمو من", "يخرج منها", "يخرج منه", "تتكوّن من", "يتكوّن من", "تتكون من", "يتكون من")
_TURN_INTO = r"(?:يتحوّل|تتحوّل|يتحول|تتحول|لتصبح|ليصبح|تصبح|يصبح)\s+(?:إلى\s+|الى\s+)?(?:ال)?"


def _stem(g, x):
    """The concept's main word without «ال» («الجذر» → «جذر», «نهر النيل» → «نهر»): to find it inside a meaning."""
    w = _name(g, x).split()
    return w[0][2:] if w and w[0].startswith("ال") else (w[0] if w else "")


def _becomes(g, a, b) -> bool:
    """True if the graph's meanings say «a» turns into / grows into «b» (not just «b needs a»)."""
    wa, wb = _stem(g, a), _stem(g, b)
    for frag in og.fragments(g.concepts[b].description) or [g.concepts[b].description or ""]:
        if wa and wa in frag and any(v in frag for v in _GROW_FROM):
            return True
    return bool(wb) and re.search(_TURN_INTO + re.escape(wb), g.concepts[a].description or "") is not None


def _why(g, a, b) -> str:
    """WHY «b» needs «a», only from the graph: the piece of b's meaning that names «a» (else nothing — never a made-up reason)."""
    wa = _stem(g, a)
    return next((f.strip(" .") for f in (og.fragments(g.concepts[b].description) or []) if wa and wa in f), "")


def scene_before_after(g: Graph, lesson: Lesson, cid: str):
    """⏳ Before / after (only when the graph has a «before»). Two honest meanings:
    · «becomes»: «a» really turns into «b» (the seed sprouts) → قبل / بعد, the old one fades into the new one;
    · «needs»: «b» needs «a» (the stem needs the root) → أول / وبعدين, «a» STAYS, «b» comes after it, with the reason."""
    ins = [p for p in sorted(g.prereq_in.get(cid, [])) if og.is_entity(g, p)]
    if not ins:
        return None
    a, me = ins[0], _name(g, cid)
    an = _name(g, a)
    why = _why(g, a, cid)
    if _becomes(g, a, cid):
        steps = [f"⏳ اسحب الشريط، وشوف «{an}» كيف {_v(an, 'بيتغيّر', 'بتتغيّر')}.",
                 f"هيك من «{an}» {_v(me, 'بيطلع', 'بتطلع')} «{me}»" + (f". {why}." if why else ".")]
        para = f"قبل: «{an}». بعد: «{me}». من «{an}» {_v(me, 'بيطلع', 'بتطلع')} «{me}»" + (f". {why}." if why else ".")
        mode = "becomes"
    else:
        reason = (f"، {_v(me, 'لأنه', 'لأنها')} {why}" if why
                  else f"، وما {_v(me, 'بيصير', 'بتصير')} إلا إذا {_v(an, 'كان', 'كانت')} «{an}» {_v(an, 'موجود', 'موجودة')} {_v(me, 'قبله', 'قبلها')}")
        steps = [f"⏳ اسحب الشريط: أول لازم {_v(an, 'يكون', 'تكون')} في «{an}»، وبعدين {_v(me, 'بيجي', 'بتيجي')} «{me}».",
                 f"«{me}» {_v(me, 'بيحتاج', 'بتحتاج')} «{an}»{reason}."]
        para = (f"«{an}» ما {_v(an, 'بيتحوّل', 'بتتحوّل')} لـ«{me}»: {_v(an, 'بيضل', 'بتضل')} {_v(an, 'موجود', 'موجودة')}، و«{me}» {_v(me, 'بيجي', 'بتيجي')} {_v(an, 'بعده', 'بعدها')} "
                f"لأنه {_v(me, 'بيحتاجه', 'بتحتاجه') if not _she(an) else _v(me, 'بيحتاجها', 'بتحتاجها')}" + (f": {why}." if why else "."))
        mode = "needs"
    return {"kind": "before_after", "target": cid, "before": a, "mode": mode, "why": why, "steps": steps, "paragraph": para}


# ===== 4 more ways to EXPLAIN (no right/wrong, nothing graded): build, talk, slide, look closer =====
def scene_assemble(g: Graph, lesson: Lesson):
    """🧩 Build the lesson's picture like a puzzle: each character goes to ITS shadow; when it lands it wakes up and says what it is."""
    ids = [c.id for c in lesson.concepts]
    if len(ids) < 3:
        return None
    edges = [[a, b] for a in ids for b in g.prereq_out.get(a, []) if b in ids]
    level = {c: g.depth(c) for c in ids}
    base = min(level.values())
    says = {c: (og.fragments(g.concepts[c].description) or [g.concepts[c].description.strip(" .")])[0] for c in ids}
    return {"kind": "assemble", "concepts": ids, "edges": edges, "levels": {c: level[c] - base for c in ids}, "says": says,
            "steps": [f"🧩 ركّب صورة درس «{lesson.title}»!", "اسحب كل شخصية لظلها (اسمها مكتوب تحته): لما توصل بتصحى وبتحكيلك مين هي.",
                      "ولما يلتقي اثنين مربوطين، بيطلع السهم بينهم."],
            "paragraph": f"درس «{lesson.title}» فيه {len(ids)} مفاهيم مربوطة ببعض. لما تركّبهم، بتشوف مين بيحتاج مين."}


def scene_dialogue(g: Graph, lesson: Lesson, cid: str):
    """🗣️ Two characters talk about why one needs the other (the relation becomes a little story)."""
    ins = [p for p in sorted(g.prereq_in.get(cid, [])) if og.is_entity(g, p)]
    if not ins:
        return None
    a, me = ins[0], _name(g, cid)
    an = _name(g, a)
    a_says = (og.fragments(g.concepts[a].description) or [g.concepts[a].description.strip(" .")])[0]
    why = _role(g, cid, a)
    def first_person(t):
        """«ينقل الماء» → «بنقل الماء» (a character speaking about itself)."""
        w = t.split(" ", 1)
        return ("ب" + w[0][1:] + (" " + w[1] if len(w) > 1 else "")) if w and w[0][:1] in ("ي", "ت") and len(w[0]) > 2 else t
    st = A.stage(g)
    if st == "senior":                                      # 💬 a short scientific discussion (not two cartoons chatting)
        lines = [{"who": a, "say": f"«{an}»: {a_says}."},
                 {"who": cid, "say": f"«{me}» {_v(me, 'بيحتاج', 'بتحتاج')} «{an}»."},
                 {"who": a, "say": "ليش؟"},
                 {"who": cid, "say": (f"لأنه {why}." if why else f"ما {_v(me, 'بيشتغل', 'بتشتغل')} بدون «{an}».")}]
    elif st == "teen":                                      # two classmates: short, confident, no baby talk
        lines = [{"who": a, "say": f"أنا «{an}»: {a_says}."},
                 {"who": cid, "say": f"وأنا «{me}»، وبعتمد عليك."},
                 {"who": a, "say": "كيف يعني؟"},
                 {"who": cid, "say": (f"لأنه أنا {first_person(why)}." if why else "لأنه بدونك ما بقدر أشتغل.")},
                 {"who": a, "say": "منطقي 👌"}]
    else:
        lines = [{"who": a, "say": f"مرحبا! أنا «{an}»: {a_says}."},
                 {"who": cid, "say": f"وأنا «{me}». أنا بحتاجك كثير!"},
                 {"who": a, "say": f"ليش {_v(me, 'بتحتاجني', 'بتحتاجيني')}؟"},
                 {"who": cid, "say": (f"لأنه أنا {first_person(why)}." if why else "لأنه بدونك ما بقدر أشتغل.")},
                 {"who": a, "say": f"تكرم! أنا {_v(an, 'جاهز', 'جاهزة')} دايماً 😄"}]
    return {"kind": "dialogue", "target": cid, "with": a, "lines": lines,
            "steps": [f"💬 نقاش: «{me}» و«{an}». اكبس «كمّل ▶»." if st == "senior" else f"🗣️ «{me}» و«{an}» بيحكوا مع بعض… اكبس «كمّل ▶»."],
            "paragraph": f"«{me}» {_v(me, 'بيحتاج', 'بتحتاج')} «{an}»" + (f"، لأنه {why}." if why else ".")}


SLIDER_OF = {"➕": "add", "➖": "sub", "✖️": "mul", "➗": "div", "🍕": "frac", "🔼": "frac", "🔽": "frac", "🟰": "frac", "⚖️": "frac",
             # 📐 the bigger grades: the straight line (y = mx + b) · motion (distance = speed × time) · acceleration (v = a × t)
             "sec:slope": "line", "sec:yint": "line", "sec:lineq": "line", "sec:speed": "motion", "sec:velocity": "motion", "sec:accel": "accel",
             "sec:linfunc": "line", "sec:freefall": "accel"}   # batch 28: their own drawings, the same sliders as before


def scene_slider(g: Graph, lesson: Lesson, cid: str):
    """🎚️ The magic slider: move it and the picture changes at once — the student discovers the rule (maths)."""
    mode = SLIDER_OF.get(og.icon_for(_name(g, cid), g.concepts[cid].description, str(g.book.get("subject", ""))))
    if not mode or (mode in ("line", "motion", "accel") and A.stage(g) in ("kids", "junior")):   # formulas: from grade 8 up
        return None
    me = _name(g, cid)
    tip = {"add": "حرّك الشريطين: المكعبات بتنضاف لبعض، والمجموع بيتغير فوراً.",
           "sub": "حرّك الشريط: كم مكعب بناخد؟ شوف كم بيضل.",
           "mul": "حرّك الشريطين: صفوف × أعمدة = كل المكعبات.",
           "div": "حرّك الشريط: كم مجموعة؟ المكعبات بتتوزع بالتساوي.",
           "frac": "حرّك الشريطين: لكم قطعة نقطّع، وكم قطعة ناخد.",
           "line": "حرّك m (الميل) و b (المقطع الصادي): شوف الخط كيف بيدور وبيطلع وبينزل.",
           "motion": "حرّك السرعة والزمن: شوف المسافة اللي بتقطعها السيارة.",
           "accel": "حرّك التسارع والزمن: شوف السرعة كيف بتزيد مع الزمن."}[mode]
    return {"kind": "slider", "target": cid, "mode": mode,
            "steps": [f"🎚️ الشريط السحري: «{me}»", tip, "جرّب أرقام كثيرة… شو لاحظت؟"],
            "paragraph": {"line": f"«{me}»: بمعادلة الخط المستقيم y = mx + b، الرقم m هو الميل (قديش الخط مايل: كم بيطلع لما نمشي خطوة لليمين)، والرقم b هو المقطع الصادي (وين الخط بيقطع محور y).",
                          "motion": f"«{me}»: المسافة = السرعة × الزمن. إذا السرعة ثابتة، كل ثانية بتقطع نفس المسافة، فالمسافة بتكبر مع الزمن بخط مستقيم.",
                          "accel": f"«{me}»: التسارع هو قديش السرعة بتتغير كل ثانية. إذا بلشنا من السكون: السرعة = التسارع × الزمن، فالسرعة بتزيد بانتظام."}.get(
                              mode, f"مع «{me}»، كل ما تغيّر الأرقام، الصورة بتتغير قدامك، وهيك بتشوف القاعدة بعينك.")}


def scene_lens(g: Graph, lesson: Lesson, cid: str):
    """🔍 The magnifying glass: the character is in the fog; move the lens over it and its facts appear one by one."""
    pieces = og.fragments(g.concepts[cid].description) or ([g.concepts[cid].description.strip(" .")] if g.concepts[cid].description else [])
    ins = [p for p in sorted(g.prereq_in.get(cid, [])) if og.is_entity(g, p)]
    outs = [x for x in sorted(g.prereq_out.get(cid, [])) if og.is_entity(g, x)]
    me = _name(g, cid)
    facts = [p for p in pieces[:3]]
    if ins:
        facts.append(f"{_v(me, 'بيحتاج', 'بتحتاج')} {_join([_name(g, x) for x in ins])}")
    if outs:
        facts.append(f"{_join([_name(g, x) for x in outs])} {('بيحتاجه' if len(outs) == 1 else 'بيحتاجوه')}")
    if len(facts) < 2:
        return None
    return {"kind": "lens", "target": cid, "facts": facts[:4],
            "steps": [f"🔍 حرّك العدسة لتكشف معلومات «{me}»." if A.stage(g) == "senior" else f"🔍 «{me}» مخبّى بالضباب… حرّك العدسة عليه واكتشف أسراره!"],
            "paragraph": f"«{me}»: " + "، ".join(facts[:4]) + "."}


def explain_lesson(g: Graph, lesson: Lesson) -> dict:
    import explain_activities as activities                                                # (here, not on top: it imports this file)
    concepts = []
    prev = None
    used = set()                                                                           # ⚖️ a pair is compared once per lesson
    for c in lesson.concepts:
        i = len(concepts)
        intro = [scene_meet, scene_interview, scene_flip][i % 3](g, lesson, c.id)       # the first look changes every concept
        scenes = [intro] if intro["kind"] == "meet" else [scene_meet(g, lesson, c.id), intro] if i % 3 == 1 else [intro, scene_meet(g, lesson, c.id)]
        film = scene_play(g, lesson, c.id)
        if film:
            scenes.append(film)
        slider = scene_slider(g, lesson, c.id)
        if slider:
            scenes.append(slider)                                                          # maths: discover the rule by sliding
        new_way = [scene_dialogue, scene_lens][i % 2](g, lesson, c.id) or [scene_lens, scene_dialogue][i % 2](g, lesson, c.id)
        if new_way:
            scenes.append(new_way)
        act = activities.pick(g, lesson, c.id, i, used)                                     # 🆕 one of the 5 new activities (batch 26)
        if act:
            scenes.append(act)
        extra = [scene_journey, scene_what_if, scene_before_after]
        for maker in extra[i % 3:] + extra[:i % 3]:                                        # a different order every time
            s = maker(g, lesson, c.id)
            if s and s["kind"] == "journey" and act and act["kind"] == "ladder":
                continue                                                                   # the ladder already walks the chain
            if s and not (film and s["kind"] == "journey" and s["traveller"] == "spark") and len(scenes) < 5 + bool(act):
                scenes.append(s)
        concepts.append({"concept_id": c.id, "title": c.text, "scenes": scenes, "teach": _teaching(g, lesson, c.id, prev)})
        prev = c.id
    rec = {"lesson_id": lesson.id, "lesson_title": lesson.title, "unit_id": lesson.unit_id, "topic_id": lesson.topic_id,
           "audience": A.audience(g),                                                       # 👥 grade → stage (the page / front end picks the look from it)
           "overview": scene_overview(g, lesson), "world": scene_world(g, lesson), "assemble": scene_assemble(g, lesson), "concepts": concepts,
           "icons": {x: og.icon_for(g.concepts[x].text, g.concepts[x].description, str(g.book.get("subject", "")))
                     for x in g.concepts if og.is_entity(g, x)}}
    return A.voice_record(rec, rec["audience"]["stage"])                                   # the words, said the way this age talks


def check_scene(g: Graph, s: dict) -> list:
    """Every arrow and every journey must follow the graph (the picture must not teach something wrong)."""
    errors = []
    ok = lambda x: x in g.concepts and og.is_entity(g, x)
    if s["kind"] == "overview":
        errors += [f"overview: {a}->{b} is not a link" for a, b in s["edges"] if not g.is_prereq(a, b)]
    elif s["kind"] == "meet":
        errors += [f"meet: {x} does not come before" for x in s["ins"] if not g.is_prereq(x, s["target"])]
        errors += [f"meet: {x} does not come after" for x in s["outs"] if not g.is_prereq(s["target"], x)]
    elif s["kind"] == "journey":
        errors += [f"journey: {a}->{b} is not a link" for a, b in zip(s["route"], s["route"][1:]) if not g.is_prereq(a, b)]
    elif s["kind"] == "assemble":
        errors += [f"assemble: {a}->{b} is not a link" for a, b in s["edges"] if not g.is_prereq(a, b)]
    elif s["kind"] == "dialogue":
        if not g.is_prereq(s["with"], s["target"]): errors.append("dialogue: not a «needs»")
    elif s["kind"] == "before_after":
        if not g.is_prereq(s["before"], s["target"]): errors.append("before_after: not a «before»")
    elif s["kind"] == "play":
        if s.get("with") and not g.is_prereq(s["with"], s["target"]):
            errors.append(f"play: {s['target']} does not need {s['with']}")
        if s.get("result") and not g.is_prereq(s["target"], s["result"]):
            errors.append(f"play: {s['result']} does not need {s['target']}")
    elif s["kind"] == "world":
        errors += [f"world: {p} → {x} is not a concept" for p, x in s["parts"].items() if not ok(x)]
    elif s["kind"] == "what_if":
        errors += [f"what_if: {x} does not need it" for x in s["affected"] if x not in g.descendants(s["target"])]
        errors += [f"what_if: {x} actually needs it" for x in s["calm"] if x in g.descendants(s["target"])]
    elif s["kind"] in ("recipe", "connect", "compare", "teach", "ladder"):
        import explain_activities as activities
        return activities.check(g, s)
    for x in s.get("ins", []) + s.get("outs", []) + s.get("route", []) + s.get("affected", []) + s.get("calm", []):
        if not ok(x):
            errors.append(f"{s['kind']}: unknown concept {x}")
    return errors
