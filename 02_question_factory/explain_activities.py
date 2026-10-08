"""🆕 Five more ways to UNDERSTAND a concept (batch 26). Everything comes from the graph only, and every move is explained.

  recipe   🧪 الشروط        the things a concept needs, as switches: it is complete only when ALL of them are there
  connect  ✏️ ارسم الأسهم   the student draws the «needs» arrows himself; a reversed arrow is explained (the most common mistake)
  compare  ⚖️ قارن          two close concepts; each fact goes to one of them or to «الاثنين» (the same / the different)
  teach    🧑‍🏫 اشرح لزميلك  a classmate does not get it; the student picks the right explanation (a wrong pick is explained)
  ladder   🪜 سلّم «ليش؟»   ask «ليش؟» again and again: each answer is the reason one step deeper, down to the base

No points and no failing: a wrong move = an explanation. Plain Python, no AI.
Truth rule (like the other scenes): a sentence says «X needs Y» only if the graph has that arrow, and «X does NOT need Y»
only if Y is not before X at all (not even through a chain). check() re-checks every scene against the graph."""
import random

import audience as A
import explain_generator as eg
import offline_generator as og

N = eg._name
V = eg._v


def _ins(g, x):
    return [p for p in sorted(g.prereq_in.get(x, [])) if og.is_entity(g, p)]


def _outs(g, x):
    return [n for n in sorted(g.prereq_out.get(x, [])) if og.is_entity(g, n)]


def _pieces(g, x):
    d = g.concepts[x].description
    return og.fragments(d) or ([d.strip(" .")] if d else [])


def _needs(g, x):
    """«بيحتاج» / «بتحتاج» — agrees with the concept (the page says «بيعتمد على» for the bigger grades)."""
    return V(N(g, x), "بيحتاج", "بتحتاج")


def _because(g, x):
    return V(N(g, x), "لأنه", "لأنها")


def _short_def(g, x):
    """The first piece of the meaning, not too long for a card (a shorter whole piece if the first one is very long)."""
    p = _pieces(g, x)
    if not p:
        return ""
    return p[0] if len(p[0].split()) <= 16 else og.tiny(g.concepts[x].description, 8)


def _rng(*key):
    return random.Random("act:" + ":".join(key))


# ---------------------------------------------------------------- 🧪 recipe
def scene_recipe(g, lesson, cid, used=None):
    """🧪 The things «X» needs, as switches. Starts empty; X is complete only when ALL are on (turn one off → you see why)."""
    ins = _ins(g, cid)
    if len(ins) < 2:                                       # one thing only is not a recipe (meet / dialogue already say it)
        return None
    ins = ins[:4]
    me, st = N(g, cid), A.stage(g)
    needs = []
    for a in ins:
        why = eg._why(g, a, cid)
        needs.append({"id": a, "why": f"«{me}» {_needs(g, cid)} «{N(g, a)}»" + (f": {why}." if why else ".")})
    done = V(me, "جاهز", "جاهزة") if st in ("kids", "junior") else V(me, "مكتمل", "مكتملة")
    has_all = V(me, "بيحتاجه", "بتحتاجه")
    ready = {"kids": f"✅ كل اللي {has_all} «{me}» موجود، فـ«{me}» {done}! 🎉",
             "junior": f"✅ كل اللي {has_all} «{me}» موجود، فـ«{me}» {done}!",
             "teen": f"✅ كل الشروط موجودة، فـ«{me}» {done}.",
             "senior": f"✅ الشروط كلها متحققة، فـ«{me}» {done}."}[st]
    names = eg._join([N(g, a) for a in ins])
    return {"kind": "recipe", "target": cid, "needs": needs, "ready": ready,
            "steps": [f"🧪 «{me}» شو {_needs(g, cid)}؟",
                      f"شغّل اللي تحت واحد واحد، وشوف إمتى «{me}» {V(me, 'بيصير', 'بتصير')} {done}.",
                      "وجرّب تطفي واحد منهم: شو بيصير؟"],
            "paragraph": f"«{me}» {_needs(g, cid)} {names} مع بعض، مش واحد بس. إذا غاب واحد منهم، «{me}» {V(me, 'بيضل', 'بتضل')} {V(me, 'ناقصه', 'ناقصها')} إشي."}


# ---------------------------------------------------------------- ✏️ connect
def _link(g, needer, needed, required=True):
    hn, dn = N(g, needer), N(g, needed)
    why = eg._why(g, needed, needer)
    return {"from": needer, "to": needed, "required": required,
            "ok_say": f"✅ «{hn}» {_needs(g, needer)} «{dn}»" + (f": {why}." if why else "."),
            "rev_say": f"↩️ السهم بالعكس: «{hn}» {V(hn, 'هو', 'هي')} اللي {_needs(g, needer)} «{dn}»، مش العكس."}


def scene_connect(g, lesson, cid, used=None):
    """✏️ The student draws the arrows around «X» (drag, or tap one then the other). Right → the reason. Reversed → why it is the other way."""
    ins, outs = _ins(g, cid)[:2], _outs(g, cid)[:2]
    if len(ins) + len(outs) < 2:
        return None
    me, st = N(g, cid), A.stage(g)
    near = set(ins + outs) | g.ancestors(cid) | g.descendants(cid) | {cid}
    calm = [x for x in og.tiered(g, lesson, _rng("connect", cid), exclude=near)][:1]   # one with NO arrow to «X» (not even through a chain)
    nodes = [cid] + ins + outs + calm
    links = [_link(g, cid, a) for a in ins] + [_link(g, x, cid) for x in outs]
    have = {(l["from"], l["to"]) for l in links}
    for a in nodes:                                        # a real arrow between two of the others is accepted too (never called wrong)
        for b in nodes:
            if a != b and g.is_prereq(a, b) and (b, a) not in have:
                links.append(_link(g, b, a, required=False)); have.add((b, a))
    how = ("اسحب من اللي بيحتاج، للي بيحتاجه (أو اكبس على الاثنين بالترتيب)." if st in ("kids", "junior")
           else "اسحب السهم من المفهوم اللي بيعتمد، للمفهوم اللي بيعتمد عليه (أو اكبس عليهم بالترتيب).")
    req = [l for l in links if l["required"]]
    end = "🎉 رسمت كل الأسهم! " + " ".join(l["ok_say"].removeprefix("✅ ") for l in req)
    return {"kind": "connect", "target": cid, "nodes": nodes, "links": links, "calm": calm, "end_say": end,
            "steps": [f"✏️ ارسم الأسهم حول «{me}».", how, "كل سهم صح بيحكيلك ليش، والسهم المقلوب بيحكيلك كمان ليش."],
            "paragraph": " ".join(l["ok_say"].removeprefix("✅ ") for l in req)
                         + (f" أما «{N(g, calm[0])}» فما في سهم مباشر {V(N(g, calm[0]), 'بينه', 'بينها')} وبين «{me}»." if calm else "")}


# ---------------------------------------------------------------- ⚖️ compare
def _sibling(g, lesson, cid, used):
    """A close concept to compare with: shares something it needs or something that needs it, and is not before/after it."""
    me_in, me_out = set(_ins(g, cid)), set(_outs(g, cid))
    anc, desc = g.ancestors(cid), g.descendants(cid)
    here = [c.id for c in lesson.concepts]
    cands = []
    for x in sorted(g.concepts):
        if x == cid or not og.is_entity(g, x) or x in anc or x in desc or not _pieces(g, x):
            continue
        shared = (me_in & set(_ins(g, x))) | (me_out & set(_outs(g, x)))
        if shared and frozenset((cid, x)) not in used:
            cands.append((x not in here, -len(shared), x))
    return sorted(cands)[0][2] if cands else None


def scene_compare(g, lesson, cid, used=None):
    """⚖️ «X» and a close concept «Y»: each fact card goes to «X», to «Y», or to «الاثنين». The same + the different."""
    used = used if used is not None else set()
    o = _sibling(g, lesson, cid, used)
    if not o or not _pieces(g, cid) or _short_def(g, o) == _short_def(g, cid):
        return None
    me, on = N(g, cid), N(g, o)
    facts = [{"fact": _short_def(g, cid), "side": "a", "ref": cid, "type": "def", "why": f"هاد تعريف «{me}»."},
             {"fact": _short_def(g, o), "side": "b", "ref": o, "type": "def", "why": f"هاد تعريف «{on}»."}]
    for s in sorted(set(_ins(g, cid)) & set(_ins(g, o)))[:1]:
        facts.append({"fact": f"بحاجة لـ«{N(g, s)}»", "side": "both", "ref": s, "type": "need",
                      "why": f"«{me}» و«{on}» الاثنين بيحتاجوا «{N(g, s)}»."})
    for x in sorted(set(_outs(g, cid)) & set(_outs(g, o)))[:1]:
        facts.append({"fact": f"شرط لـ«{N(g, x)}»", "side": "both", "ref": x, "type": "feed",
                      "why": f"«{N(g, x)}» {_needs(g, x)} «{me}» و«{on}» الاثنين."})
    for side, a, b in (("a", cid, o), ("b", o, cid)):          # different: true for one, and NOT true for the other (not even through a chain)
        an, bn = N(g, a), N(g, b)
        for i in [i for i in _ins(g, a) if i != b and i not in g.ancestors(b)][:1]:
            facts.append({"fact": f"بحاجة لـ«{N(g, i)}»", "side": side, "ref": i, "type": "need",
                          "why": f"«{an}» {_needs(g, a)} «{N(g, i)}»، و«{bn}» لأ."})
        for x in [x for x in _outs(g, a) if x != b and x not in g.descendants(b)][:1]:
            facts.append({"fact": f"شرط لـ«{N(g, x)}»", "side": side, "ref": x, "type": "feed",
                          "why": f"«{N(g, x)}» {_needs(g, x)} «{an}»، مش «{bn}»."})
    if not any(f["side"] == "both" for f in facts):
        return None
    keep = facts[:2] + [f for f in facts[2:] if f["side"] == "both"][:1]
    keep += [f for f in facts[2:] if f not in keep][:6 - len(keep)]
    used.add(frozenset((cid, o)))
    order = keep[:]
    _rng("compare", cid).shuffle(order)                          # the tray is mixed (the same mix every time)
    same = next(f for f in keep if f["side"] == "both")["why"]
    return {"kind": "compare", "target": cid, "other": o, "facts": order,
            "end_say": f"🎉 رتّبت كل البطاقات! الشبه: {same} والفرق بالتعريف: «{me}»: {_short_def(g, cid)}، و«{on}»: {_short_def(g, o)}.",
            "steps": [f"⚖️ «{me}» و«{on}»: شو الشبه وشو الفرق؟",
                      f"اكبس على بطاقة، وبعدين اكبس على مكانها: عند «{me}»، عند «{on}»، ولا عند الاثنين.",
                      "الشبه بيربطهم ببعض، والفرق بيخليك ما تخلط بينهم."],
            "paragraph": f"«{me}» و«{on}» قريبين من بعض: {same} بس كل واحد إله تعريفه: «{me}»: {_short_def(g, cid)}. و«{on}»: {_short_def(g, o)}."}


# ---------------------------------------------------------------- 🧑‍🏫 teach
def scene_teach(g, lesson, cid, used=None):
    """🧑‍🏫 A classmate does not get «X». Three questions; the student picks the right answer. A wrong pick is explained
    (the other definition belongs to «Y» · the arrow is the other way) — the classic mistakes, said out loud."""
    pa = _pieces(g, cid)
    if not pa:
        return None
    me, st = N(g, cid), A.stage(g)
    ins, outs = _ins(g, cid), _outs(g, cid)
    anc, desc = g.ancestors(cid), g.descendants(cid)
    rng = _rng("teach", cid)
    others = [x for x in og.tiered(g, lesson, rng, exclude={cid}) if _pieces(g, x) and _short_def(g, x) != _short_def(g, cid)]
    if not others:
        return None
    o = others[0]
    rounds = [{"ask": f"شو يعني «{me}»؟", "rel": "def",
               "options": [{"opt": _short_def(g, cid), "id": cid, "ok": True, "reply": f"آها! يعني «{me}»: {_short_def(g, cid)}."},
                           {"opt": _short_def(g, o), "id": o, "ok": False, "reply": f"لأ، هاد تعريف «{N(g, o)}»، مش «{me}»."}]}]
    if ins:
        a = ins[0]
        why = eg._why(g, a, cid)
        wrong = outs[0] if outs else next((x for x in others if x not in anc), None)
        if wrong:
            wn = N(g, wrong)
            wr = (f"لأ، بالعكس: «{wn}» {V(wn, 'هو', 'هي')} اللي {_needs(g, wrong)} «{me}»." if wrong in outs
                  else f"لأ، «{me}» ما {_needs(g, cid)} «{wn}».")
            rounds.append({"ask": f"طيب، «{me}» شو {_needs(g, cid)}؟", "rel": "needs",
                           "options": [{"opt": f"«{N(g, a)}»", "id": a, "ok": True,
                                        "reply": f"آها! «{me}» {_needs(g, cid)} «{N(g, a)}»" + (f"، {_because(g, cid)} {why}." if why else ".")},
                                       {"opt": f"«{wn}»", "id": wrong, "ok": False, "reply": wr}]})
    if outs:
        x = outs[0]
        why = eg._why(g, cid, x)
        wrong = ins[0] if ins else next((y for y in others if y not in desc and y not in anc), None)
        if wrong:
            wn = N(g, wrong)
            wr = (f"لأ، بالعكس: «{me}» {V(me, 'هو', 'هي')} اللي {_needs(g, cid)} «{wn}»." if wrong in ins
                  else f"لأ، «{wn}» ما {_needs(g, wrong)} «{me}».")
            rounds.append({"ask": f"وليش «{me}» {V(me, 'مهم', 'مهمة')}؟ مين {V(me, 'بيحتاجه', 'بيحتاجها')}؟", "rel": "needed_by",
                           "options": [{"opt": f"«{N(g, x)}»", "id": x, "ok": True,
                                        "reply": f"آها! «{N(g, x)}» {_needs(g, x)} «{me}»" + (f"، {_because(g, x)} {why}." if why else ".")},
                                       {"opt": f"«{wn}»", "id": wrong, "ok": False, "reply": wr}]})
    if len(rounds) < 2:
        return None
    for r in rounds:
        rng.shuffle(r["options"])
    said = [next(op["reply"] for op in r["options"] if op["ok"]).removeprefix("آها! ").removeprefix("يعني ") for r in rounds]
    kid = st in ("kids", "junior")
    return {"kind": "teach", "target": cid, "rounds": rounds, "learnt": "📝 هيك شرحتها: " + " ".join(said),
            "steps": ([f"🧑‍🏫 صاحبك مش فاهم «{me}»… ساعده!", "اختار الجواب الصح لكل سؤال. ولو غلطت، رح تعرف ليش.", "لما تشرح لغيرك، إنت بتفهم أكثر 💡"] if kid else
                      [f"🧑‍🏫 زميلك مش فاهم «{me}»، اشرحله.", "اختار الجواب الصح لكل سؤال، وأي غلط رح ينشرح.", "الشرح لغيرك بيثبّت الفكرة عندك."]),
            "paragraph": " ".join(said)}


# ---------------------------------------------------------------- 🪜 ladder
def scene_ladder(g, lesson, cid, used=None):
    """🪜 «ليش؟» again and again: «X» needs «A» because…, «A» needs «B» because… — down to the base (or «وبعدين؟» forward)."""
    me = N(g, cid)

    def climb(nexts, sentence):
        rungs, cur, seen = [], cid, {cid}
        while len(rungs) < 3:
            cands = [x for x in nexts(cur) if x not in seen]
            if not cands:
                break
            x = next((c for c in cands if sentence(cur, c)[1]), cands[0])   # prefer a step the graph explains
            text, _ = sentence(cur, x)
            rungs.append({"id": x, "because": text[0], "short": text[1]})
            seen.add(x); cur = x
        return rungs

    def why_step(cur, a):          # «cur» needs «a» (going down to the base)
        why = eg._why(g, a, cur)
        short = f"«{N(g, cur)}» {_needs(g, cur)} «{N(g, a)}»"
        return (short + (f"، {_because(g, cur)} {why}." if why else "."), short), why

    def then_step(cur, x):         # «x» needs «cur» (going on to what comes after)
        why = eg._why(g, cur, x)
        short = f"«{N(g, x)}» {_needs(g, x)} «{N(g, cur)}»"
        return (short + (f"، {_because(g, x)} {why}." if why else "."), short), why

    rungs, mode = climb(lambda c: _ins(g, c), why_step), "why"
    if len(rungs) < 2:
        rungs, mode = climb(lambda c: _outs(g, c), then_step), "then"
    if len(rungs) < 2:
        return None
    last = rungs[-1]["id"]
    ln = N(g, last)
    if mode == "why":
        end = (f"🏁 وصلنا للأساس: «{ln}» ما {_needs(g, last)} إشي {V(ln, 'قبله', 'قبلها')}." if not _ins(g, last)
               else f"🏁 وصلنا لـ«{ln}»، والسلسلة بتكمّل {V(ln, 'قبله', 'قبلها')} كمان.")
        steps = [f"🪜 شو ورا «{me}»؟ اكبس «ليش؟» وانزل درجة درجة.", "كل درجة بتحكيلك السبب: مين بيحتاج مين، وليش.", "لما توصل للأساس، بتشوف السلسلة كاملة."]
    else:
        end = (f"🏁 «{ln}» آخر وحدة بهالسلسلة." if not _outs(g, last)
               else f"🏁 وصلنا لـ«{ln}»، والسلسلة بتكمّل {V(ln, 'بعده', 'بعدها')} كمان.")
        steps = [f"🪜 شو بيجي بعد «{me}»؟ اكبس «وبعدين؟» وانزل درجة درجة.", "كل درجة بتحكيلك مين بيحتاج اللي قبله، وليش.", "لما توصل للآخر، بتشوف السلسلة كاملة."]
    return {"kind": "ladder", "target": cid, "mode": mode, "rungs": rungs, "end_say": end, "steps": steps,
            "paragraph": " ".join(r["because"] for r in rungs) + " " + end.removeprefix("🏁 ")}


MAKERS = [scene_recipe, scene_connect, scene_compare, scene_teach, scene_ladder]
KINDS = ("recipe", "connect", "compare", "teach", "ladder")


def pick(g, lesson, cid, i, used):
    """ONE new activity per concept: 🧪 the recipe when the concept needs 2+ things; otherwise a different one for each concept
    (each lesson starts somewhere else), the next one if the graph has not enough for it."""
    s = scene_recipe(g, lesson, cid, used)                 # needs 2+ things at once (the leaf: light + air + the stem): the recipe fits best
    if s:
        return s
    rest = MAKERS[1:]
    ids = [l.id for l in g.lessons()]
    start = (i + 2 * (ids.index(lesson.id) if lesson.id in ids else 0)) % len(rest)
    for maker in rest[start:] + rest[:start]:
        s = maker(g, lesson, cid, used)
        if s:
            return s
    return None


# ---------------------------------------------------------------- the check (the picture must never teach something wrong)
def check(g, s) -> list:
    k, t, errors = s["kind"], s.get("target"), []
    if k == "recipe":
        errors += [f"recipe: {t} does not need {n['id']}" for n in s["needs"] if not g.is_prereq(n["id"], t)]
        if len(s["needs"]) < 2:
            errors.append("recipe: fewer than 2 things")
    elif k == "connect":
        for l in s["links"]:
            if not g.is_prereq(l["to"], l["from"]):
                errors.append(f"connect: {l['from']} does not need {l['to']}")
        for c in s.get("calm", []):
            if c in g.ancestors(t) or c in g.descendants(t):
                errors.append(f"connect: {c} is linked to {t}")
        if not any(l["required"] for l in s["links"]):
            errors.append("connect: nothing to draw")
    elif k == "compare":
        o = s["other"]
        if o in g.ancestors(t) or o in g.descendants(t):
            errors.append("compare: the two are before/after each other")
        for f in s["facts"]:
            r, side = f["ref"], f["side"]
            if f["type"] == "def":
                ok = r == (t if side == "a" else o)
            elif f["type"] == "need":
                ok = (g.is_prereq(r, t) and g.is_prereq(r, o)) if side == "both" else (
                    g.is_prereq(r, t) and r not in g.ancestors(o) if side == "a" else g.is_prereq(r, o) and r not in g.ancestors(t))
            else:
                ok = (g.is_prereq(t, r) and g.is_prereq(o, r)) if side == "both" else (
                    g.is_prereq(t, r) and r not in g.descendants(o) if side == "a" else g.is_prereq(o, r) and r not in g.descendants(t))
            if not ok:
                errors.append(f"compare: «{f['fact']}» is not on side {side}")
    elif k == "teach":
        for r in s["rounds"]:
            for op in r["options"]:
                x = op["id"]
                if r["rel"] == "needs":
                    ok = g.is_prereq(x, t) if op["ok"] else (x not in g.ancestors(t))
                elif r["rel"] == "needed_by":
                    ok = g.is_prereq(t, x) if op["ok"] else (x not in g.descendants(t))
                else:
                    ok = (x == t) == op["ok"]
                if not ok:
                    errors.append(f"teach: option {x} ({r['rel']}) is not true")
    elif k == "ladder":
        prev = t
        for r in s["rungs"]:
            if not (g.is_prereq(r["id"], prev) if s["mode"] == "why" else g.is_prereq(prev, r["id"])):
                errors.append(f"ladder: {prev} → {r['id']} is not a link")
            prev = r["id"]
    ids = s.get("nodes", []) + [n["id"] for n in s.get("needs", [])] + [r["id"] for r in s.get("rungs", [])] + ([s["other"]] if s.get("other") else [])
    errors += [f"{k}: unknown concept {x}" for x in ids if x not in g.concepts or not og.is_entity(g, x)]
    return errors
