"""Fills the templates from the graph alone, with no LLM, for EVERY CONCEPT of the lesson."""
import random
import re

import config
from graph_reader import Concept, Graph, Lesson
from templates import blank


def short(text: str) -> str:
    words = text.strip().rstrip(".").split()
    return " ".join(words[:config.DESCRIPTION_MAX_WORDS]) + ("…" if len(words) > config.DESCRIPTION_MAX_WORDS else "")


FRAGMENT_SPLIT = re.compile(r"[؛،;]| و(?=[يتأ])")


def fragments(text: str) -> list:
    """Split a meaning into short pieces about the thing itself:
    'الجزء تحت الأرض؛ يثبّت النبتة ويمتص الماء…' -> ['الجزء تحت الأرض', 'يثبّت النبتة', 'يمتص الماء…']"""
    parts = [p.strip(" .:") for p in FRAGMENT_SPLIT.split(text or "")]
    return [p for p in parts if len(p.split()) >= 2]


def tiny(text: str, words: int = 6) -> str:
    """A short but COMPLETE meaning (never cut with "…"): the shortest whole piece that still says something,
    or the first piece if all pieces are long."""
    parts = fragments(text) or [(text or "").strip(" .")]
    fitting = [p for p in parts if len(p.split()) <= max(words, 4) * 2]
    return (fitting or parts)[0]


def is_entity(g: Graph, x: str) -> bool:
    """Only real concepts (entities) go into questions, never units/topics/lessons."""
    return g.format == "old" or g.concepts[x].level == "entity"


def entities(g: Graph) -> list:
    return sorted(x for x in g.concepts if is_entity(g, x))


def tiered(g: Graph, lesson: Lesson, rng: random.Random, exclude=()) -> list:
    """Wrong options, closest first: same lesson, then same topic, then same unit, then the rest of the book.
    Close distractors make the student think (far ones were too easy)."""
    lesson_ids = [k.id for k in lesson.concepts]
    topic_ids, unit_ids = [], []
    for les in g.children.get(lesson.topic_id, []):
        topic_ids += g.children.get(les, [])
    for top in g.children.get(lesson.unit_id, []):
        for les in g.children.get(top, []):
            unit_ids += g.children.get(les, [])
    out, seen = [], set(exclude)
    for tier in (lesson_ids, topic_ids, unit_ids, entities(g)):
        tier = [x for x in dict.fromkeys(tier) if x not in seen and is_entity(g, x)]
        rng.shuffle(tier)
        for x in tier:
            seen.add(x); out.append(x)
    return out


def make_meaning(g: Graph, lesson: Lesson, c: Concept, rng: random.Random):
    if not c.description:
        return None, f"meaning({c.id}): no description in the graph"
    others = [x for x in tiered(g, lesson, rng, exclude={c.id}) if g.concepts[x].description]
    wrong = []
    for x in others:
        d = short(g.concepts[x].description)
        if d != short(c.description) and d not in wrong:
            wrong.append(d)
        if len(wrong) == config.MEANING_DISTRACTORS:
            break
    if len(wrong) < 2:
        return None, f"meaning({c.id}): not enough other meanings"
    options = [short(c.description)] + wrong
    rng.shuffle(options)
    q = blank("meaning", c.text)
    q.update(target=c.id, options=options, answer=short(c.description), concepts=[c.id])
    q["solution"] = [f"{c.text}: {short(c.description)}"]
    return q, None


def chain_through(g: Graph, cid: str, before: int, after: int) -> list:
    """A chain around the concept: up to `before` concepts before it and `after` concepts after it."""
    def back(x, depth, used):
        if depth == 0: return [x]
        best = [x]
        for p in sorted(g.prereq_in.get(x, [])):
            if is_entity(g, p) and p not in used:
                cand = back(p, depth - 1, used | {p}) + [x]
                if len(cand) > len(best): best = cand
        return best
    def fwd(x, depth, used):
        if depth == 0: return [x]
        best = [x]
        for n in sorted(g.prereq_out.get(x, [])):
            if is_entity(g, n) and n not in used:
                cand = [x] + fwd(n, depth - 1, used | {n})
                if len(cand) > len(best): best = cand
        return best
    left = back(cid, before, {cid})
    right = fwd(cid, after, set(left))
    return left + right[1:]


# Windows to try, so that two concepts of the same lesson do not get the same bridge (the student would get bored)
WINDOWS = ((1, 1), (0, 2), (2, 0), (2, 1), (1, 2), (3, 0), (0, 3), (1, 0), (0, 1))


def make_sequence(g: Graph, lesson: Lesson, c: Concept, rng: random.Random, used: set = None):
    used = used if used is not None else set()
    chain = None
    for shortest in (3, config.SEQUENCE_MIN_LENGTH):      # prefer chains of 3+ (2 items are too easy to guess)
        for b, a in WINDOWS:
            cand = chain_through(g, c.id, b, a)
            if max(shortest, config.SEQUENCE_MIN_LENGTH) <= len(cand) <= config.SEQUENCE_MAX_LENGTH and tuple(cand) not in used:
                chain = cand
                break
        if chain:
            break
    if chain is None:
        return None, f"sequence({c.id}): no new chain (all chains around it are already used in this lesson)"
    used.add(tuple(chain))
    q = blank("sequence", c.text)
    q.update(target=c.id, order=chain, concepts=[c.id] + [x for x in chain if x != c.id])
    q["solution"] = [g.justification.get((a, b, "prerequisiteOf")) or f"{g.concepts[a].text} قبل {g.concepts[b].text}"
                     for a, b in zip(chain, chain[1:])]
    return q, None


def _choice(g: Graph, lesson: Lesson, c: Concept, rng, template: str, correct: list, exclude: set):
    wrong = [x for x in tiered(g, lesson, rng, exclude=set(exclude) | {c.id} | set(correct))][:config.PREREQ_DISTRACTORS]
    if len(wrong) < 2:
        return None, f"{template}({c.id}): not enough wrong options"
    options = correct + wrong
    rng.shuffle(options)
    q = blank(template, c.text)
    q.update(target=c.id, correct=correct, options=options, concepts=[c.id] + correct)
    return q, None


def make_prereq(g: Graph, lesson: Lesson, c: Concept, rng: random.Random):
    correct = sorted(x for x in g.prereq_in.get(c.id, []) if is_entity(g, x))
    if not correct:
        return None, f"prereq({c.id}): nothing comes before it"
    q, why = _choice(g, lesson, c, rng, "prereq", correct, g.ancestors(c.id))   # indirect ones are not "wrong"
    if q:
        q["solution"] = [g.justification.get((x, c.id, "prerequisiteOf")) or f"{g.concepts[x].text} لازم قبل {c.text}" for x in correct]
    return q, why


def make_unlocks(g: Graph, lesson: Lesson, c: Concept, rng: random.Random):
    """A journey that starts at the concept: at every crossroads, the student picks the next stop.
    route = [concept, next, next...]; each crossroads has ONE right road and wrong roads that are not linked."""
    route = chain_through(g, c.id, 0, config.JOURNEY_MAX_STEPS)
    if len(route) < 2:
        return None, f"unlocks({c.id}): nothing comes after it"
    junctions = []
    for here, nxt in zip(route, route[1:]):
        related = g.descendants(here) | g.ancestors(here) | set(route)
        wrong = [x for x in tiered(g, lesson, rng, exclude=related | {here}) if x not in g.prereq_out.get(here, [])][:config.JOURNEY_WRONG_ROADS]
        if len(wrong) < 2:
            return None, f"unlocks({c.id}): not enough wrong roads"
        opts = [nxt] + wrong
        rng.shuffle(opts)
        junctions.append(opts)
    hints = []
    for here, nxt in zip(route, route[1:]):
        hints.append([f"فكّر: مين بيستعمل «{g.concepts[here].text}» أو بيطلع منه؟",
                      f"تذكّر: {tiny(g.concepts[here].description, 8)}",
                      f"المحطة الجاية اسمها بيبلش بـ «{g.concepts[nxt].text[:2]}…»"])
    # each step says WHY, in the child's words: the next one's meaning (the piece that mentions this one, if any)
    whys = []
    for here, nxt in zip(route, route[1:]):
        parts = fragments(g.concepts[nxt].description) or [tiny(g.concepts[nxt].description, 10)]
        word = g.concepts[here].text.replace("ال", "", 1)
        pick = next((p for p in parts if word and word in p), parts[0])
        whys.append(f"«{g.concepts[nxt].text}»: {pick}")
    q = blank("unlocks", c.text)
    q.update(target=c.id, route=route, junctions=junctions, hints=hints, whys=whys, concepts=list(route))
    q["solution"] = [" ← ".join(g.concepts[x].text for x in route)] + [
        f"بعد «{g.concepts[a].text}» بييجي «{g.concepts[b].text}»" for a, b in zip(route, route[1:])]
    return q, None


def make_match(g: Graph, lesson: Lesson, c: Concept, rng: random.Random):
    if not c.description:
        return None, f"match({c.id}): no description in the graph"
    near = sorted(g.prereq_in.get(c.id, [])) + sorted(g.prereq_out.get(c.id, [])) + [k.id for k in lesson.concepts]
    near = [x for x in dict.fromkeys(near) if x != c.id and is_entity(g, x) and g.concepts[x].description]
    near = [x for x in near if short(g.concepts[x].description) != short(c.description)][:config.MATCH_NEIGHBOURS]
    if len(near) < 2:
        return None, f"match({c.id}): not enough neighbours with meanings"
    pool = [c.id] + near
    q = blank("match", c.text)
    q.update(target=c.id, pairs=[[x, short(g.concepts[x].description)] for x in pool], concepts=pool)
    q["solution"] = [f"{g.concepts[x].text}: {short(g.concepts[x].description)}" for x in pool]
    return q, None


def make_sort(g: Graph, lesson: Lesson, c: Concept, rng: random.Random):
    def closest(start, step):
        """Nearest first: direct links, then the next ring."""
        seen, ring, out = {c.id}, list(start), []
        while ring and len(out) < config.SORT_MAX_PER_SIDE:
            nxt = []
            for x in sorted(ring):
                if x not in seen and is_entity(g, x):
                    seen.add(x); out.append(x); nxt += step(x)
            ring = nxt
        return out[:config.SORT_MAX_PER_SIDE]
    before = closest(g.prereq_in.get(c.id, []), lambda x: g.prereq_in.get(x, []))
    after = closest(g.prereq_out.get(c.id, []), lambda x: g.prereq_out.get(x, []))
    if not before or not after or len(before) + len(after) < 3:
        return None, f"sort({c.id}): needs concepts both before and after it"
    q = blank("sort", c.text)
    q.update(target=c.id, before=before, after=after, concepts=[c.id] + before + after)
    q["solution"] = ["قبل «" + c.text + "»: " + "، ".join(g.concepts[x].text for x in before),
                     "بعد «" + c.text + "»: " + "، ".join(g.concepts[x].text for x in after)]
    return q, None


def numeric_subject(g: Graph) -> bool:
    subject = str(g.book.get("subject", "")).strip().lower()
    return any(s in subject for s in config.NUMERIC_SUBJECTS)


def make_adjust(g: Graph, lesson: Lesson, c: Concept, rng: random.Random):
    f = c.quantity
    if not numeric_subject(g):
        return None, f"adjust({c.id}): not a numeric subject (memorise/understand lessons do not get number sliders)"
    if not f:
        return None, f"adjust({c.id}): no numbers in the graph for this concept"
    q = blank("adjust", f["label"])
    f = dict(f)
    if c.description:
        f["hint"] = short(c.description)          # what the book says: the student reasons from it (note 30)
    q.update(target=c.id, factor=f, concepts=[c.id])
    q["solution"] = [f"الصح بين {f['ok_min']} و {f['ok_max']} {f['unit']}."] + [m for m in (f.get("low"), f.get("high")) if m]
    return q, None


def neighbours_with_meaning(g: Graph, lesson: Lesson, c: Concept, k: int) -> list:
    near = sorted(g.prereq_in.get(c.id, [])) + sorted(g.prereq_out.get(c.id, [])) + [x.id for x in lesson.concepts]
    near = [x for x in dict.fromkeys(near) if x != c.id and is_entity(g, x) and g.concepts[x].description]
    return [x for x in near if short(g.concepts[x].description) != short(c.description)][:k]


def make_memory(g: Graph, lesson: Lesson, c: Concept, rng: random.Random):
    if not c.description:
        return None, f"memory({c.id}): no description"
    near = neighbours_with_meaning(g, lesson, c, config.MEMORY_NEIGHBOURS)
    if len(near) < 2:
        return None, f"memory({c.id}): not enough neighbours with meanings"
    pool = [c.id] + near
    q = blank("memory", c.text)
    cards = [[x, tiny(g.concepts[x].description)] for x in pool]
    if len({m for _, m in cards}) != len(cards):
        return None, f"memory({c.id}): two short meanings are the same"
    q.update(target=c.id, pairs=cards, concepts=pool)
    q["solution"] = [f"{g.concepts[x].text}: {short(g.concepts[x].description)}" for x in pool]
    return q, None


def make_spell(g: Graph, lesson: Lesson, c: Concept, rng: random.Random):
    letters = [ch for ch in c.text if not ch.isspace()]
    if not c.description or not (2 <= len(letters) <= 14):
        return None, f"spell({c.id}): no meaning or the name is too short/long"
    q = blank("spell", c.text)
    q.update(target=c.id, word=c.text, clue=short(c.description), concepts=[c.id])
    q["solution"] = [f"«{short(c.description)}» = {c.text}"]
    return q, None


def _verb_gender(text: str) -> str:
    """'ي…' = he, 'ت…' = she (Arabic present verbs); '' when the piece is not a verb."""
    w = (text or "").strip().split()
    return {"ي": "m", "ت": "f"}.get(w[0][0], "") if w else ""


def make_true_false(g: Graph, lesson: Lesson, c: Concept, rng: random.Random):
    """Science sentences only, from the lesson's content (never the order of lessons):
    TRUE  = a piece of the concept's own meaning ('«الجذر»: يثبّت النبتة')
    FALSE = a piece of a NEARBY concept's meaning given to this one ('«الجذر»: يصنع فيه النبات غذاءه…'),
            with the same grammatical gender, so the grammar never gives the answer away."""
    own = fragments(c.description) or ([c.description.strip(" .")] if c.description else [])
    if not own:
        return None, f"true_false({c.id}): no description"
    first = c.text.split()[0] if c.text.split() else ""
    genders = {"f" if first.endswith("ة") else "m"}      # the concept's own gender (الورقة = she, الجذر = he)
    base = c.text.replace("ال", "", 1)
    cards = [{"text": f"«{c.text}»: {p}", "answer": True} for p in own[:2]]
    wrong, used = [], set(own)
    for x in tiered(g, lesson, rng, exclude={c.id}):
        for p in fragments(g.concepts[x].description) or []:
            gender = _verb_gender(p)
            if p in used or (base and base in p) or (gender and gender not in genders):
                continue
            wrong.append((x, p)); used.add(p)
            break
        if len(wrong) == config.TRUE_FALSE_CARDS - len(cards):
            break
    if not wrong:
        return None, f"true_false({c.id}): no false sentence that fits"
    cards += [{"text": f"«{c.text}»: {p}", "answer": False, "really": x} for x, p in wrong]
    rng.shuffle(cards)
    q = blank("true_false", c.text)
    q.update(target=c.id, statements=[{k: v for k, v in card.items() if k != "really"} for card in cards], concepts=[c.id])
    q["solution"] = [("✅ " + card["text"]) if card["answer"] else
                     f"❌ {card['text']} ← هاد «{g.concepts[card['really']].text}» مش «{c.text}»" for card in cards]
    return q, None


def make_fix_chain(g: Graph, lesson: Lesson, c: Concept, rng: random.Random):
    chain = None
    for b, a in ((1, 1), (2, 0), (0, 2), (2, 1), (1, 2)):
        cand = chain_through(g, c.id, b, a)
        if len(cand) >= 3:
            chain = cand; break
    if not chain:
        return None, f"fix_chain({c.id}): needs a chain of 3+"
    spots = [i for i, x in enumerate(chain) if x != c.id]
    wrong_index = spots[rng.randrange(len(spots))]
    pool = tiered(g, lesson, rng, exclude=set(chain))
    if len(pool) < 3:
        return None, f"fix_chain({c.id}): not enough other concepts"
    wrong, distract = pool[0], pool[1:3]
    options = [chain[wrong_index]] + distract
    rng.shuffle(options)
    q = blank("fix_chain", c.text)
    q.update(target=c.id, chain=chain, wrong_index=wrong_index, wrong=wrong, options=options,
             concepts=[c.id] + [x for x in chain if x != c.id])
    q["solution"] = [f"«{g.concepts[wrong].text}» مش من السلسلة، مكانه «{g.concepts[chain[wrong_index]].text}»",
                     " ← ".join(g.concepts[x].text for x in chain)]
    return q, None


def make_odd_one_out(g: Graph, lesson: Lesson, c: Concept, rng: random.Random):
    family = [c.id] + [k.id for k in lesson.concepts if k.id != c.id]
    rest = family[1:]; rng.shuffle(rest)
    family = [c.id] + rest[:2]
    outside = [x for x in tiered(g, lesson, rng, exclude=set(k.id for k in lesson.concepts))]
    if len(family) < 3 or not outside:
        return None, f"odd_one_out({c.id}): the lesson is too small or the book has no other lesson"
    q = blank("odd_one_out", c.text)
    intruder = outside[0]
    home = g.concepts[g.parent.get(intruder, "")].text if g.parent.get(intruder) in g.concepts else ""
    intros = {x: tiny(g.concepts[x].description, 7) for x in family + [intruder] if g.concepts[x].description}
    q["question"] = f"كلهم من «{lesson.title}» إلا واحد. مين الدخيل؟"
    q.update(target=c.id, family=family, intruder=intruder, intros=intros, concepts=family)
    q["solution"] = [f"«{g.concepts[intruder].text}»: {intros.get(intruder, '')}" + (f"، {'فهي' if g.concepts[intruder].text.split()[0].endswith('ة') else 'فهو'} من «{home}»" if home else "") + f"، مش من «{lesson.title}».",
                     f"أما «{lesson.title}»: " + "، ".join(g.concepts[x].text for x in family) + "."]
    return q, None


def make_who_am_i(g: Graph, lesson: Lesson, c: Concept, rng: random.Random):
    """Clues are about the thing itself (what it does, where it is), never about the curriculum.
    The first piece of a meaning is usually the most revealing, so it comes last."""
    parts = fragments(c.description)
    if len(parts) < 2:
        return None, f"who_am_i({c.id}): the meaning is too short for 2+ clues"
    clues = (parts[1:] + parts[:1])[:config.WHO_CLUES]
    suspects = [c.id] + tiered(g, lesson, rng, exclude={c.id})[:config.WHO_SUSPECTS - 1]
    if len(suspects) < 3:
        return None, f"who_am_i({c.id}): not enough suspects"
    rng.shuffle(suspects)
    q = blank("who_am_i", c.text)
    q["how"] = f"أنا مفهوم من درس «{lesson.title}». اقرأ التلميح واحزر مين أنا! كل تلميح زيادة بيكلّفك نجمة ⭐."
    q.update(target=c.id, clues=clues, options=suspects, concepts=[c.id])
    q["solution"] = [f"أنا «{c.text}»: {short(c.description)}"]
    return q, None


def make_predict(g: Graph, lesson: Lesson, c: Concept, rng: random.Random):
    """Cause and effect, from the graph's links only: if this concept disappears, everything that needs it is touched,
    one after the other (a domino), and what does not need it is fine. No invented facts, no numbers."""
    chain = chain_through(g, c.id, 0, 3)[1:]
    if not chain:
        return None, f"predict({c.id}): nothing needs it"
    after = g.descendants(c.id)
    others = [x for x in tiered(g, lesson, rng, exclude={c.id}) if x not in after and x not in g.ancestors(c.id)]
    if not others:
        return None, f"predict({c.id}): no unrelated concept to compare with"
    calm = others[0]
    she = lambda t: t.split()[0].endswith("ة")                 # الورقة = she (بتـ), الجذر = he (بيـ)
    v = lambda t, verb: ("بت" if she(t) else "بي") + verb
    names = [g.concepts[x].text for x in chain]
    shown = "» ثم «".join(names)
    calm_t = g.concepts[calm].text
    options = [f"«{shown}» بيتأثروا، لأنه كل واحد بيحتاج اللي قبله",
               "ما في إشي بيتأثر، كل واحد لحاله",
               f"بس «{calm_t}» {v(calm_t, 'تأثر')}",
               f"«{names[-1]}» {v(names[-1], 'صير')} {'أقوى' if not she(names[-1]) else 'أقوى'}"]
    order = list(range(len(options))); rng.shuffle(order)
    q = blank("predict", c.text)
    q.update(target=c.id, options=[options[i] for i in order], answer=order.index(0), affected=chain, unaffected=[calm],
             concepts=[c.id] + chain)
    q["solution"] = [f"«{g.concepts[b].text}» {v(g.concepts[b].text, 'حتاج')} «{g.concepts[a].text}»" for a, b in zip([c.id] + chain, chain)] + \
                    [f"«{calm_t}» ما {v(calm_t, 'حتاج')} «{c.text}»، فما {v(calm_t, 'تأثر')}."]
    return q, None


MAKERS = {"meaning": make_meaning, "sequence": make_sequence, "prereq": make_prereq, "unlocks": make_unlocks,
          "match": make_match, "sort": make_sort, "adjust": make_adjust, "memory": make_memory, "spell": make_spell,
          "true_false": make_true_false, "fix_chain": make_fix_chain, "odd_one_out": make_odd_one_out,
          "who_am_i": make_who_am_i, "predict": make_predict}


def pick(candidates: dict, index: int, counts: dict, cap: int) -> list:
    """A varied mix for one concept:
    1) one "meaning" question, its kind rotating from concept to concept,
    2) the slider when the graph has numbers,
    3) "link" questions, rotating too,
    and no kind may be used in more than `cap` concepts of the lesson (the bridge used to be everywhere)."""
    chosen = []
    def take(t, ignore_cap=False):
        if t in candidates and t not in [q["template"] for q in chosen] and (ignore_cap or counts.get(t, 0) < cap):
            chosen.append(candidates[t]); counts[t] = counts.get(t, 0) + 1
            return True
        return False
    mk = config.MEANING_KINDS
    for t in mk[index % len(mk):] + mk[:index % len(mk)]:
        if take(t): break
    take("adjust", ignore_cap=True)
    lk = config.LINK_KINDS
    for t in lk[index % len(lk):] + lk[:index % len(lk)]:
        if len(chosen) >= config.MAX_QUESTIONS_PER_CONCEPT: break
        take(t)
    for t in mk[index % len(mk):] + mk[:index % len(mk)]:          # room left? a second "meaning" kind (within the cap)
        if len(chosen) >= config.MAX_QUESTIONS_PER_CONCEPT: break
        take(t)
    for t in list(lk) + list(mk):                                  # still too few? relax the cap
        if len(chosen) >= config.MIN_QUESTIONS_PER_CONCEPT: break
        take(t, ignore_cap=True)
    return chosen


ICON_WORDS = (# 📐 the bigger grades first (specific words win): the cell · coordinates & lines · heredity
              ("غشاء", "sec:membrane"), ("سيتوبلازم", "sec:cytoplasm"), ("ميتوكندريا", "sec:mito"), ("بلاستيدات", "sec:chloroplast"),
              ("جدار", "sec:cellwall"), ("فجوة", "sec:vacuole"), ("نواة", "sec:nucleus"),
              ("مستوى الإحداثي", "sec:axes"), ("إحداثي", "sec:axes"), ("زوج مرتب", "sec:pair"), ("مرتب", "sec:pair"), ("ميل", "sec:slope"),
              ("مقطع", "sec:yint"), ("الخط المستقيم", "sec:lineq"), ("الاقتران الخطي", "sec:lineq"), ("اقتران", "sec:func"),
              ("dna", "sec:dna"), ("نووي", "sec:dna"), ("كروموسوم", "sec:chromosome"), ("كروموسومات", "sec:chromosome"), ("صبغي", "sec:chromosome"),
              ("أليل", "sec:allele"), ("أليلات", "sec:allele"), ("جين", "sec:gene"), ("جينات", "sec:gene"), ("سائدة", "sec:dominant"), ("سائد", "sec:dominant"),
              ("متنحية", "sec:recessive"), ("متنحي", "sec:recessive"), ("بانيت", "sec:punnett"), ("طراز", "sec:allele"), ("زمن", "⏰"), ("ضوئي", "🍃"),
              ("جذر", "🫚"), ("ساق", "🌿"), ("ورق", "🍃"), ("زهر", "🌸"), ("ثمر", "🍎"), ("بذر", "🌰"),
              ("ماء", "💧"), ("مي", "💧"), ("شمس", "☀️"), ("ضوء", "☀️"), ("هواء", "💨"), ("ترب", "🟫"),
              ("إنبات", "🌱"), ("تلقيح", "🐝"), ("انتشار", "🌬️"),
              # maths (the specific words first: «مقارنة الكسور» is a comparison, «الكسور المتكافئة» an equality)
              ("متكافئ", "🟰"), ("مقارنة", "⚖️"), ("بسط", "🔼"), ("مقام", "🔽"), ("كسور", "🍕"), ("كسر", "🍕"),
              ("جمع", "➕"), ("طرح", "➖"), ("ضرب", "✖️"), ("قسمة", "➗"), ("أعداد", "🔢"), ("عدد", "🔢"),
              ("مثلث", "🔺"), ("مربع", "⏹️"), ("دائرة", "⚪"), ("قياس", "📏"), ("طول", "📏"),
              # physics and chemistry
              ("مغناطيس", "🧲"), ("كهرب", "⚡"), ("قوة", "➡️"), ("ذرة", "⚛️"), ("تفاعل", "🧪"),
              # history: each idea its own picture
              ("أهرامات", "hist:pyramid"), ("أهرام", "hist:pyramid"), ("هرم", "hist:pyramid"),
              ("فراعنة", "hist:pharaoh"), ("فرعون", "hist:pharaoh"), ("ملك", "hist:pharaoh"), ("حكام", "hist:pharaoh"), ("حاكم", "hist:pharaoh"),
              ("هيروغليفية", "hist:glyphs"), ("كتابة", "hist:glyphs"), ("نقوش", "hist:glyphs"),
              ("نهر", "hist:river"), ("نيل", "hist:river"), ("فرات", "hist:river"), ("دجلة", "hist:river"),
              ("زراعة", "hist:wheat"), ("قمح", "hist:wheat"), ("حصاد", "hist:wheat"), ("تجارة", "💰"),
              ("سفينة", "hist:boat"), ("قارب", "hist:boat"), ("سفن", "hist:boat"), ("معبد", "🏛️"),
              ("جيش", "hist:shield"), ("حرب", "hist:shield"), ("معركة", "hist:shield"),
              # geography, history, language, everyday
              ("أرض", "🌍"), ("خريطة", "🗺️"), ("جبل", "⛰️"), ("تاريخ", "📜"), ("حضارة", "🏛️"),
              ("حرف", "🔤"), ("كلمة", "🔤"), ("قراءة", "📖"), ("جملة", "📖"), ("وقت", "⏰"), ("ساعة", "⏰"), ("نقود", "💰"),
              # English graphs
              ("زاوية", "📐"), ("زوايا", "📐"), ("معادل", "🟰"), ("مئوي", "💯"), ("نسبة", "💯"), ("احتمال", "🎲"),
              ("بيانات", "📊"), ("رسم بياني", "📊"), ("إحصاء", "📊"), ("مساحة", "⏹️"), ("محيط", "⭕"), ("حجم", "🧊"),
              ("منزل", "🔢"), ("نمط", "🔁"), ("أنماط", "🔁"), ("عشري", "🔢"), ("تماثل", "🦋"),
              ("خلية", "🦠"), ("قلب", "❤️"), ("حيوان", "🐾"), ("صوت", "🔊"), ("حرارة", "🌡️"), ("صخر", "🪨"),
              ("طقس", "🌧️"), ("مطر", "🌧️"), ("كوكب", "🪐"), ("كواكب", "🪐"), ("قمر", "🌙"), ("نجم", "⭐"), ("فضاء", "🪐"),
              ("angle", "📐"), ("equation", "🟰"), ("percent", "💯"), ("probability", "🎲"), ("data", "📊"), ("area", "⏹️"),
              ("cell", "🦠"), ("heart", "❤️"), ("animal", "🐾"), ("sound", "🔊"), ("heat", "🌡️"), ("planet", "🪐"), ("moon", "🌙"),
              ("addition", "➕"), ("subtraction", "➖"), ("multiplication", "✖️"), ("division", "➗"), ("fraction", "🍕"),
              ("number", "🔢"), ("magnet", "🧲"), ("electric", "⚡"), ("force", "➡️"), ("atom", "⚛️"), ("earth", "🌍"),
              ("map", "🗺️"), ("history", "📜"), ("letter", "🔤"), ("time", "⏰"), ("money", "💰"))

# pictures the player can draw (SVG library). Anything else gets a drawing from the LLM (when on) or the generic character.
ART_ICONS = {"sec:membrane", "sec:cytoplasm", "sec:nucleus", "sec:mito", "sec:chloroplast", "sec:cellwall", "sec:vacuole",
             "sec:position", "sec:displacement", "sec:distance", "sec:speed", "sec:velocity", "sec:accel", "sec:axes", "sec:pair", "sec:func",
             "sec:slope", "sec:yint", "sec:lineq", "sec:electron", "sec:valence", "sec:ion", "sec:ionic", "sec:covalent", "sec:molecule",
             "sec:dna", "sec:gene", "sec:chromosome", "sec:allele", "sec:dominant", "sec:recessive", "sec:punnett",
             "💧", "☀️", "🍃", "🫚", "🌿", "🌸", "🍎", "🌰", "🟫", "💨", "🌱", "🐝", "🌬️",
             "🟰", "⚖️", "🔼", "🔽", "🍕", "➕", "➖", "✖️", "➗", "🔢", "🔺", "⏹️", "⚪", "📏",
             "🧲", "⚡", "➡️", "⚛️", "🧪", "🌍", "🗺️", "⛰️", "📜", "🏛️", "🔤", "📖", "⏰", "💰",
             "📐", "💯", "🎲", "📊", "⭕", "🧊", "🔁", "🦋", "🦠", "❤️", "🐾", "🔊", "🌡️", "🪨", "🌧️", "🪐", "🌙", "⭐",
             "hist:pyramid", "hist:pharaoh", "hist:glyphs", "hist:river", "hist:wheat", "hist:boat", "hist:shield", "⛰️", "🌊", "🚂",
             "ara:harakat", "ara:word", "ara:noun", "ara:particle", "ara:nominal", "ara:verbal", "ara:mubtada", "chem:element", "chem:compound",
             "chem:acid", "chem:base", "phy:friction", "phy:battery", "phy:circuit", "geo:continents", "sec:genotype", "sec:linfunc", "sec:freefall"}   # + batch 28

# no picture found by name or meaning → the SUBJECT's character with the concept's name on it (never a meaningless blob)
SUBJECT_ICONS = (("math", "🧮"), ("رياضيات", "🧮"), ("physics", "🔭"), ("فيزياء", "🔭"), ("chem", "⚗️"), ("كيمياء", "⚗️"),
                 ("science", "🔬"), ("علوم", "🔬"), ("geograph", "🧭"), ("جغرافيا", "🧭"), ("history", "📜"), ("تاريخ", "📜"),
                 ("arabic", "📖"), ("عربي", "📖"), ("english", "📖"), ("language", "📖"), ("لغة", "📖"))


import re as _re
import identity
import lego
_PREFIXES = ("وال", "بال", "فال", "كال", "لل", "ال", "و", "ب", "ف", "ل")


def _tokens(text: str) -> list:
    """The words of a text, each also without «ال»/«و»/«ب»… in front (so «والجذور» → «جذور»)."""
    out = []
    for w in _re.findall(r"[\w\u0600-\u06FF]+", (text or "").lower()):
        out.append(w)
        for p in _PREFIXES:
            if w.startswith(p) and len(w) - len(p) >= 3:
                out.append(w[len(p):])
                break
    return out


def _has_word(tokens: list, key: str) -> bool:
    """A WHOLE word: «مي» never matches inside «الهيروغليفية». Longer keys may start a word («كسور» ← «كسورها»)."""
    key = key[2:] if key.startswith("ال") and len(key) > 4 else key
    if " " in key:
        return key in " ".join(tokens)
    endings = ("", "ة", "ه", "ات", "ان", "ين")          # short keys: «ورق» → «ورقة», «ترب» → «تربة»
    return any(t == key or any(t == key + e for e in endings) or (len(key) >= 4 and t.startswith(key)) for t in tokens)


# pictures that only make sense in MATHS (in Arabic grammar «كسرة» is a vowel mark; in geography «محيط» is an ocean)
MATH_ONLY = {"🍕", "⭕", "🔼", "🔽", "🟰", "⚖️", "➗", "✖️", "➕", "➖", "🔢", "📐", "🔺", "⏹️", "💯", "🎲", "📊",
             "sec:axes", "sec:pair", "sec:slope", "sec:yint", "sec:lineq", "sec:func"}   # «ميل» in geography is a tilt, not a slope
# words that come first in a subject (they win over general words)
SUBJECT_WORDS = {
    "arabic": [("حركات", "🔤"), ("حروف", "🔤"), ("كسرة", "🔤"), ("فتحة", "🔤")],
    "chem": [("المركب الأيوني", "🧪"), ("تكافؤ", "sec:valence"), ("إلكترونات", "sec:electron"), ("إلكترون", "sec:electron"), ("أيونية", "sec:ionic"), ("أيوني", "sec:ionic"),
             ("أيون", "sec:ion"), ("أيونات", "sec:ion"), ("تساهمية", "sec:covalent"), ("تساهمي", "sec:covalent"), ("جزيء", "sec:molecule"), ("نواة", "⚛️"),
             ("حمض", "🧪"), ("قاعدة", "🧪"), ("عنصر", "⚛️"), ("مركب", "🧪")],
    "geo": [("محيطات", "🌊"), ("محيط", "🌊"), ("بحار", "🌊"), ("جبال", "⛰️"), ("جبل", "⛰️"), ("قارات", "🗺️"), ("أنهار", "hist:river"), ("مناخ", "🌧️")],
    "phys": [("متجهة", "sec:velocity"), ("تسارع", "sec:accel"), ("إزاحة", "sec:displacement"), ("مسافة", "sec:distance"), ("موقع", "sec:position"),
             ("سرعة", "sec:speed"), ("سقوط", "sec:accel"), ("حركة", "➡️"), ("طاقة", "⚡")],
}
_SUBJECT_KEYS = {"arabic": ("arabic", "عربي", "لغة"), "chem": ("chem", "كيمياء"), "geo": ("geograph", "جغرافيا"), "phys": ("physic", "فيزياء")}

# 🆕 batch 28: a drawing of its own for concepts that used to share one — matched on the concept's NAME only
# (never on its meaning, so «الفاعل» whose meaning says «اسم» does not become the noun picture)
NAME_WORDS = {
    "arabic": [("الجملة الاسمية", "ara:nominal"), ("الجملة الفعلية", "ara:verbal"), ("مبتدأ", "ara:mubtada"), ("حرف المعنى", "ara:particle"),
               ("حركات", "ara:harakat"), ("كلمة", "ara:word"), ("اسم", "ara:noun")],
    "chem": [("عنصر", "chem:element"), ("مركب", "chem:compound"), ("حمض", "chem:acid"), ("قاعدة", "chem:base")],
    "phys": [("سقوط", "sec:freefall"), ("جاذبية", "🍎"), ("حركة", "🚂"), ("احتكاك", "phy:friction"), ("دارة", "phy:circuit"), ("كهرباء", "phy:battery")],
    "geo": [("قارات", "geo:continents"), ("مناخ", "🌡️")],
    "": [("الطراز الجيني", "sec:genotype"), ("الاقتران الخطي", "sec:linfunc")],     # any subject
}


def _subject_key(subject: str) -> str:
    sub = (subject or "").lower()
    return next((k for k, words in _SUBJECT_KEYS.items() if any(w in sub for w in words)), "")


def icon_for(text: str, meaning: str = "", subject: str = "") -> str:
    """A picture for a concept: by its NAME first, then by its MEANING, then the SUBJECT's character (with the name on it).
    A word means different things in different subjects: maths pictures are used ONLY in maths, and each subject's own words come first."""
    sub = (subject or "").lower()
    is_math = any(w in sub for w in ("math", "رياضيات")) or not sub
    own = SUBJECT_WORDS.get(_subject_key(subject), [])
    name_toks = _tokens(text)
    for word, icon in NAME_WORDS.get(_subject_key(subject), []) + NAME_WORDS[""]:   # its own drawing, by the NAME only
        if _has_word(name_toks, word.lower()):
            return icon
    for source in (text, meaning):
        toks = _tokens(source)
        for word, icon in list(own) + list(ICON_WORDS):
            if icon in MATH_ONLY and not is_math:
                continue
            if _has_word(toks, word.lower()):
                return icon
    built = lego.for_concept(text, subject)                # 🧱 batch 29: no drawing in the library → one BUILT from parts (saved / by its words)
    if built:
        return built
    label = _label(text)
    new = identity.emblem(subject)                         # a NEW subject: its own emblem (💻 for the computer…), never the science flask
    if new:
        return f"subj:{new}:{label}"
    sub = (subject or "").lower()
    for word, icon in SUBJECT_ICONS:
        if word in sub:
            return f"subj:{icon}:{label}"
    return f"subj:🔹:{label}"


def _label(text: str) -> str:
    """The name written on the character: the WHOLE name (the page writes it on 2 lines). One word loses its «ال» (as before:
    «الخبر» → «خبر»); longer names stay as they are («الخطأ البرمجي»). Very long names are cut at a SPACE, never inside a word."""
    t = " ".join(str(text or "").split())
    if " " not in t and t.startswith("ال") and len(t) > 3:
        t = t[2:]
    if len(t) > 28:
        t = t[:28].rsplit(" ", 1)[0]
    return t


def choose_theme(g: Graph, lesson: Lesson) -> str:
    """The lesson's skin (same games, different look), from a closed list."""
    text = " ".join([lesson.title, g.concepts.get(lesson.topic_id).text if lesson.topic_id in g.concepts else "",
                     g.concepts.get(lesson.unit_id).text if lesson.unit_id in g.concepts else "",
                     g.book.get("title", "")] + [c.text for c in lesson.concepts]).lower()
    for theme, words in config.THEME_KEYWORDS.items():
        if any(w in text for w in words):
            return theme
    return "default"


def generate(g: Graph, lesson: Lesson) -> tuple:
    """For every concept of the lesson: the questions that fit it, plus the reason for each template that did not."""
    per_concept, skipped = {}, []
    used_chains = set()                      # no two concepts of one lesson get the same chain
    counts = {}                              # how many concepts of the lesson already use each kind
    cap = max(1, -(-len(lesson.concepts) * config.MAX_KIND_SHARE // 1))
    cap = int(cap)
    for i, c in enumerate(lesson.concepts):
        rng = random.Random(f"{config.SEED}:{lesson.id}:{c.id}")
        candidates = {}
        for name in config.TEMPLATES:
            if name == "sequence":
                q, why = make_sequence(g, lesson, c, rng, set(used_chains))
            else:
                q, why = MAKERS[name](g, lesson, c, rng)
            if q:
                candidates[name] = q
            else:
                skipped.append(why)
        chosen = pick(candidates, i, counts, cap)
        for q in chosen:
            if q["template"] == "sequence":
                used_chains.add(tuple(q["order"]))
        per_concept[c.id] = chosen
    return per_concept, skipped
