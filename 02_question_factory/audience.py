"""👥 Who is the lesson for? The book's GRADE decides the STAGE, and the stage decides how the explanation TALKS.

Stages (the same four the page uses, stage.js):
  kids   (grades 1–4)   a playful friend      — the original words (nothing changes)
  junior (grades 5–7)   a curious explorer    — the same words, a few emoji less
  teen   (grades 8–9)   a confident classmate — «بيعتمد على» instead of «بيحتاج», «بيتأثر» instead of «بيتعب», no face emoji
  senior (grades 10–12) a calm expert         — like teen, and no emoji inside the words at all

Plain Python, no AI: a grade lookup + word replacements. The page applies the same rules (VOICE in stage.js),
so a lesson looks right even when someone tries another stage with the switcher."""
import re

STAGES = {
    "kids": {"label": "الصغار", "grades": (1, 4), "persona": "رفيق مرح"},
    "junior": {"label": "ابتدائي عليا", "grades": (5, 7), "persona": "مستكشف فضولي"},
    "teen": {"label": "إعدادي", "grades": (8, 9), "persona": "زميل واثق"},
    "senior": {"label": "ثانوي", "grades": (10, 12), "persona": "خبير هادي"},
}

# «الصف العاشر» → 10 (the longer names first: «الحادي عشر» before «الأول», «الثاني عشر» before «الثاني»)
_ORDINALS = (("الحادي عشر", 11), ("الثاني عشر", 12), ("العاشر", 10), ("التاسع", 9), ("الثامن", 8), ("السابع", 7), ("السادس", 6),
             ("الخامس", 5), ("الرابع", 4), ("الثالث", 3), ("الثاني", 2), ("الأول", 1))


def grade_of(book: dict):
    """The book's grade (1–12) from its «grade» field, or its title («الصف العاشر»), or its id («…_g10»). None if unknown."""
    book = book or {}
    g = book.get("grade")
    if isinstance(g, int) and 1 <= g <= 12:
        return g
    if isinstance(g, str):
        m = re.search(r"\d+", g)
        if m and 1 <= int(m.group()) <= 12:
            return int(m.group())
    title = str(book.get("title", ""))
    for word, n in _ORDINALS:
        if word in title:
            return n
    m = re.search(r"g(\d{1,2})\b", str(book.get("id", "")))
    return int(m.group(1)) if m and 1 <= int(m.group(1)) <= 12 else None


def stage_of_grade(grade) -> str:
    """1–4 kids · 5–7 junior · 8–9 teen · 10–12 senior (unknown → kids, the original look)."""
    if not grade:
        return "kids"
    return next((k for k, v in STAGES.items() if v["grades"][0] <= grade <= v["grades"][1]), "kids")


def stage(g) -> str:
    return stage_of_grade(grade_of(getattr(g, "book", {}) or {}))


def audience(g) -> dict:
    """What the lesson carries for the page / the front end: {grade, stage, label, persona}."""
    grade = grade_of(getattr(g, "book", {}) or {})
    st = stage_of_grade(grade)
    return {"grade": grade, "stage": st, "label": STAGES[st]["label"], "persona": STAGES[st]["persona"]}


# ---- the VOICE: the same sentence the way that age talks (same lists as stage.js) ----
VOICE_WORDS = (("من اللي بيحتاج، للي بيحتاجه", "من اللي بيعتمد، للي بيعتمد عليه"),   # (the legend: never a dangling «على،»)
               ("شو بتحتاجي؟", "على شو بتعتمدي؟"), ("شو بتحتاج؟", "على شو بتعتمد؟"), ("شو بيحتاج", "على شو بيعتمد"), ("بيحتاجك", "بيعتمد عليك"),
               ("بتحتاجي", "بتعتمدي على"), ("خلص الحوار!", "خلص النقاش."), ("«يلا ←»", "«التالي ←»"), ("الشريط السحري", "جرّب المتغيّرات"),
               ("بيحتاجوه", "بيعتمدوا عليه"), ("بيحتاجوها", "بيعتمدوا عليها"), ("بيحتاجوا", "بيعتمدوا على"), ("بيحتاجه", "بيعتمد عليه"), ("بيحتاجها", "بيعتمد عليها"),
               ("بتحتاجه", "بتعتمد عليه"), ("بتحتاجها", "بتعتمد عليها"), ("بتحتاجيني", "بتعتمدي عليّ"), ("بتحتاجني", "بتعتمد عليّ"), ("بيحتاجني", "بيعتمد عليّ"), ("بحتاجك", "بعتمد عليك"),
               ("بيحتاج", "بيعتمد على"), ("بتحتاج", "بتعتمد على"), ("بيتعبوا", "بيتأثروا"), ("بيتعب", "بيتأثر"), ("بتتعب", "بتتأثر"), ("بيضل مبسوط", "ما بيتأثر"),
               ("بترجع مبسوطة", "بترجع طبيعية"), ("بتصحى", "بتتفعّل"), ("بيصحى", "بيتفعّل"), ("صحيت", "تفعّلت"), ("برافو!", "ممتاز."), ("يلا نشوف", "خلينا نشوف"))
_FACES = re.compile("[\U0001F600-\U0001F64F\U0001F917-\U0001F92F\U0001F970-\U0001F97A\U0001F60E\U0001F44B\U0001F463\U0001F446\U0001F642]")
_ANY_EMOJI = re.compile("[\U0001F000-\U0001FAFF⌀-⏿☀-➿⬀-⯿\U0001F1E6-\U0001F1FF]️?")
_KEEP = {"✅", "✔", "✔️", "⚠", "⚠️"}


def voice(text, st: str):
    """One sentence, said for this stage. kids: unchanged. junior: a few face emoji less. teen/senior: the grown-up words."""
    if not isinstance(text, str) or st == "kids":
        return text
    if st == "junior":
        return re.sub(r"\s{2,}", " ", re.sub(r"\s*[😄😢😟😎]+", "", text)).strip()
    s = re.sub(r"^أهلاً! أنا «([^»]+)»\.?$", lambda m: (f"تعريف «{m.group(1)}»." if st == "senior" else f"هاد «{m.group(1)}»."), text)
    s = re.sub(r"^📌\s*", "• ", s)                                       # the first line + the captions of «تعرّف عليّ»
    for a, b in VOICE_WORDS:
        s = s.replace(a, b)
    s = _FACES.sub("", s)
    if st == "senior":
        s = _ANY_EMOJI.sub(lambda m: m.group() if m.group() in _KEEP else "", s)
        s = re.sub("(?<![✅✔⚠])[\u200d\ufe0f]", "", s)                   # the glue of a removed emoji (🧑‍🏫) must not stay as an invisible mark
    s = re.sub(r"\s+([.،!؟:])", r"\1", s)
    return re.sub(r"\s{2,}", " ", s).strip()


# the human words inside a lesson record (ids, kinds and numbers are never touched)
_TEXT_KEYS = {"steps", "paragraph", "say", "says", "q", "a", "front", "back", "facts", "hook", "answer", "summary", "recap", "why", "drive", "info",
              "ready", "ok_say", "rev_say", "end_say", "fact", "ask", "opt", "reply", "learnt", "because", "short"}   # + the 5 new activities


def voice_record(rec, st: str):
    """The whole lesson, said for this stage (walks the record; only the text fields change)."""
    if st == "kids":
        return rec
    if isinstance(rec, list):
        return [voice_record(x, st) for x in rec]
    if not isinstance(rec, dict):
        return rec
    out = {}
    for k, v in rec.items():
        if k in _TEXT_KEYS:
            if isinstance(v, str):
                out[k] = voice(v, st)
            elif isinstance(v, list):
                out[k] = [voice(x, st) if isinstance(x, str) else voice_record(x, st) for x in v]
            elif isinstance(v, dict):
                out[k] = {kk: voice(vv, st) if isinstance(vv, str) else voice_record(vv, st) for kk, vv in v.items()}
            else:
                out[k] = v
        else:
            out[k] = voice_record(v, st)
    return out
