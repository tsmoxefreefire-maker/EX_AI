"""🧱 LEGO DRAWINGS (batch 29 · 💡 Hareth's idea «ليغو الرسومات + الاستعارة»).

A concept that has NO drawing in our library gets one BUILT from ready parts (drawn in our style in the page, lego.js):
    ONE main part = the metaphor (memory → drawers, processor → chip, error → bug…) + a face + up to 2 small badges.
The picture key carries the whole recipe:   lego:<main>:<extra>+<extra>:<colour 0-7>:<motion>
    e.g.  lego:drawers:binary:3:wobble

Where a recipe comes from (in this order):
    1) the LIBRARY of built drawings (saved): the model chose it once, or a teacher picked it → reused by every book, no cost;
    2) the concept's own WORDS (no AI): «الذاكرة» → drawers, «وحدة المعالجة» → chip, «الخطأ البرمجي» → bug …;
    3) nothing → None (the page then shows the subject's character with the name on it, as before).
The MODEL (optional, use_llm): ONE call for all the new concepts of a book. It only CHOOSES from the lists below
(it never draws); every answer is checked; the first good option is used at once, the others are kept for the teacher.
Plain Python (standard library only)."""
import json
import os
import re

# ---------- the parts (the SAME names as LEGO_MAIN / LEGO_EXTRA in 03_explain_player_src/lego.js — a test checks) ----------
# name: (what it can mean — told to the model, its usual motion, the words that pick it without AI)
MAINS = {
    "drawers":   ("رف أدراج: تخزين، حفظ، ذاكرة، أرشيف", "wobble", ("ذاكرة", "تخزين", "أرشيف", "memory", "storage", "archive")),
    "chip":      ("شريحة إلكترونية: معالج، عقل الجهاز، تحكم", "buzz", ("معالجة", "معالج", "شريحة", "processor", "cpu", "chip")),
    "screen":    ("شاشة: حاسوب، عرض، إخراج، تطبيق ظاهر", "bob", ("حاسوب", "حاسب", "شاشة", "إخراج", "عرض", "computer", "screen", "output", "display")),
    "keyboard":  ("لوحة مفاتيح: إدخال، كتابة، طباعة", "bounce", ("إدخال", "لوحة المفاتيح", "كتابة", "input", "keyboard", "typing")),
    "page":      ("ورقة مكتوبة: ملف، مستند، نص، برنامج مكتوب، تعليمات", "wiggle", ("ملف", "ملفات", "مستند", "برنامج", "برامج", "تعليمات", "file", "document", "program")),
    "code":      ("بطاقة كود </>: برمجة، لغة برمجة، شيفرة", "wobble", ("برمجة", "البرمجة", "كود", "شيفرة", "code", "coding", "programming")),
    "bug":       ("خنفسة: خطأ، علة، مشكلة بالبرنامج، حشرة", "wiggle", ("خطأ", "أخطاء", "علة", "حشرة", "حشرات", "bug", "error", "insect")),
    "stairs":    ("درج بخطوات ١-٢-٣: خطوات، مراحل، خوارزمية، تقدّم، ترتيب", "bounce", ("خوارزمية", "خوارزميات", "خطوات", "مراحل", "algorithm", "steps", "stages")),
    "gear":      ("ترس: آلة، نظام، عملية، تقنية، محرك", "sun", ("آلة", "آلات", "نظام", "أنظمة", "عملية", "تقنية", "ترس", "machine", "system", "process")),
    "lock":      ("قفل: أمان، حماية، خصوصية، سرية", "wobble", ("أمان", "حماية", "خصوصية", "قفل", "security", "privacy", "protection")),
    "key":       ("مفتاح: حل، وصول، كلمة سر، فتح", "sway", ("مفتاح", "كلمة السر", "كلمة المرور", "password", "key", "access")),
    "bulb":      ("مصباح: فكرة، إبداع، اختراع، فهم", "bob", ("فكرة", "أفكار", "إبداع", "اختراع", "idea", "invention", "creativity")),
    "magnifier": ("عدسة مكبّرة: بحث، فحص، استكشاف، تحقق، ملاحظة", "sway", ("بحث", "فحص", "استكشاف", "تحقق", "ملاحظة", "search", "research", "inspection")),
    "envelope":  ("ظرف: رسالة، تواصل، بريد، اتصال", "bounce", ("رسالة", "رسائل", "بريد", "تواصل", "message", "email", "communication")),
    "globe":     ("كرة أرضية: عالم، إنترنت، شبكة، دولي، عولمة", "sun", ("إنترنت", "الانترنت", "شبكة", "شبكات", "عالمي", "دولي", "internet", "network", "global")),
    "flag":      ("علم: وطن، دولة، هدف، إنجاز، بداية", "sway", ("وطن", "دولة", "هدف", "أهداف", "flag", "goal", "nation")),
    "shield":    ("درع: قانون، حقوق، دفاع، مناعة، أمن", "bob", ("قانون", "قوانين", "حقوق", "دفاع", "مناعة", "law", "rights", "defense", "immunity")),
    "cube":      ("مكعب/صندوق: منتج، شيء، مجسم، حجم، كتلة", "wobble", ("منتج", "منتجات", "مكعب", "مجسم", "صندوق", "product", "cube", "box")),
    "chart":     ("رسم بياني: إحصاء، أرقام، نمو، تحليل، اقتصاد", "bounce", ("إحصاء", "إحصائيات", "نمو", "تحليل", "رسم بياني", "statistics", "chart", "growth")),
    "pot":       ("طنجرة: طبخ، طهي، خلط، وصفة، تحضير", "wobble", ("طبخ", "طهي", "وصفة", "مطبخ", "خلط", "cooking", "recipe", "kitchen")),
    "puzzle":    ("قطعة بزل: جزء، مكوّن، تركيب، حل مشكلة", "wiggle", ("جزء", "أجزاء", "مكون", "مكونات", "تركيب", "puzzle", "component", "part")),
    "people":    ("شخصين: مجتمع، فريق، تعاون، عائلة، ناس", "sway", ("مجتمع", "فريق", "تعاون", "عائلة", "أسرة", "سكان", "society", "team", "family", "people")),
    "trophy":    ("كأس: فوز، مسابقة، بطولة، جائزة، إنجاز", "bounce", ("فوز", "مسابقة", "بطولة", "جائزة", "إنجاز", "trophy", "competition", "award")),
    "note":      ("نوتة موسيقية: لحن، نغمة، إيقاع، غناء", "sway", ("لحن", "ألحان", "نغمة", "إيقاع", "غناء", "melody", "rhythm", "song")),
    "ball":      ("كرة: رياضة، لعبة، تمرين", "bounce", ("كرة", "لعبة", "ألعاب", "تمرين", "ball", "game", "exercise")),
    "bag":       ("حقيبة: تجارة، سوق، شراء، بيع، سفر", "wobble", ("سوق", "أسواق", "تجارة", "شراء", "بيع", "حقيبة", "market", "trade", "shopping")),
    "hourglass": ("ساعة رملية: مدة، عصر، حقبة، انتظار", "wobble", ("مدة", "عصر", "حقبة", "انتظار", "duration", "era", "period")),
}
EXTRAS = {"plus": "زيادة/إضافة", "check": "صح/تم", "question": "سؤال/مجهول", "spark": "جديد/لامع", "arrow": "انتقال/ناتج/خروج",
          "heart": "حب/صحة", "star": "مميز/مهم", "link": "ربط/اتصال", "binary": "رقمي/بيانات", "drop": "ماء/سائل",
          "cog": "إعداد/آلة صغيرة", "tune": "صوت/موسيقى"}
MOTIONS = ("bob", "wobble", "bounce", "sway", "sun", "buzz", "wiggle", "drip")   # the moves the page already has
COLORS = 8                                                                      # SUBJ_COLORS in the page
# a word that also adds a badge (no AI): «وحدات الإخراج» → the screen + an arrow going out
WORD_EXTRAS = (("إخراج", "arrow"), ("output", "arrow"), ("إدخال", "arrow"), ("بيانات", "binary"), ("data", "binary"),
               ("رقمي", "binary"), ("digital", "binary"), ("خطأ", "question"), ("جديد", "spark"))


# ---------- keys ----------
def color_of(name: str) -> int:
    """The concept's own colour: the same formula as the page (sum of the UTF-16 codes % 8)."""
    b = str(name or "").encode("utf-16-le")
    return sum(int.from_bytes(b[i:i + 2], "little") for i in range(0, len(b), 2)) % COLORS


def make_key(main: str, extras=(), color: int = 0, motion: str = None) -> str:
    extras = [x for x in (extras or []) if x in EXTRAS][:2]
    motion = motion if motion in MOTIONS else MAINS[main][1]
    return f"lego:{main}:{'+'.join(extras)}:{int(color) % COLORS}:{motion}"


def parse(key: str):
    """«lego:drawers:binary:3:wobble» → {"main", "extras", "color", "motion"} (the same rules as legoParts in the page), or None."""
    if not isinstance(key, str) or not key.startswith("lego:"):
        return None
    p = key.split(":") + ["", "", "", ""]
    if p[1] not in MAINS:
        return None
    m = re.match(r"-?\d+", p[3] or "")
    return {"main": p[1], "extras": [x for x in p[2].split("+") if x in EXTRAS][:2],
            "color": abs(int(m.group())) % COLORS if m else 0, "motion": p[4] if p[4] in MOTIONS else "bob"}


# ---------- 2) by the concept's own words (no AI) ----------
_PREFIXES = ("وال", "بال", "فال", "كال", "لل", "ال", "و", "ب", "ف", "ل")


def _norm(s: str) -> str:
    return re.sub("[أإآ]", "ا", str(s or "").lower())


def _tokens(text: str) -> list:
    out = []
    for w in re.findall(r"[\w؀-ۿ]+", _norm(text)):
        out.append(w)
        for p in _PREFIXES:
            if w.startswith(p) and len(w) - len(p) >= 3:
                out.append(w[len(p):])
                break
    return out


def _has(toks: list, word: str) -> bool:
    """A WHOLE word (a few endings allowed: «ملف» → «ملفات»); a phrase: its words one after the other."""
    word = _norm(word)
    word = word[2:] if word.startswith("ال") and len(word) > 4 else word
    if " " in word:
        return word in " ".join(toks)
    return any(t == word or t in (word + "ة", word + "ات", word + "ين") for t in toks)


def by_words(name: str):
    """A recipe from the concept's NAME only (never from its meaning: that would mix things up). None if no word fits."""
    toks = _tokens(name)
    for main, (_, motion, words) in MAINS.items():
        if any(_has(toks, w) for w in words):
            extras = [x for w, x in WORD_EXTRAS if _has(toks, w)][:1]
            return make_key(main, extras, color_of(name), motion)
    return None


# ---------- 1) the library of built drawings (it grows: one entry per concept, reused by every book) ----------
_STORE = os.environ.get("EXPLAIN_LEGO_FILE") or os.path.join(os.path.dirname(os.path.abspath(__file__)), "lego_library.json")
_CACHE = {"mtime": None, "data": {}}


def set_store(path: str) -> None:
    global _STORE
    _STORE = path
    _CACHE["mtime"] = None


def store_path() -> str:
    return _STORE


def _key_of(name: str) -> str:
    return " ".join(_norm(name).split())


def library() -> dict:
    try:
        m = os.path.getmtime(_STORE)
    except OSError:
        return {}
    if _CACHE["mtime"] != m:
        try:
            with open(_STORE, encoding="utf-8") as f:
                _CACHE["data"] = json.load(f)
        except (OSError, ValueError):
            _CACHE["data"] = {}
        _CACHE["mtime"] = m
    return _CACHE["data"]


def _save(data: dict) -> None:
    os.makedirs(os.path.dirname(_STORE) or ".", exist_ok=True)
    with open(_STORE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    _CACHE["mtime"] = None


def saved(name: str):
    e = library().get(_key_of(name))
    return e["key"] if e and e.get("status") != "rejected" and parse(e.get("key")) else None


def for_concept(name: str, subject: str = ""):
    """The Lego drawing of a concept: the saved one (model / teacher) → by its words → None."""
    return saved(name) or by_words(name)


# ---------- 🤖 the model chooses (once per concept; optional) ----------
PROMPT = """You choose PICTURES for school concepts on an Arabic learning page. You never draw: you BUILD each picture from ready parts.
Subject: «{subject}»
For EACH concept below, think of the best everyday METAPHOR a student understands (memory → a cabinet of drawers,
processor → a chip, a bug in a program → a beetle), then give up to 3 options, best first. Use ONLY these names:
- main (exactly one, the metaphor):
{mains}
- extras (0, 1 or 2 small badges):
{extras}
- motion (one): {motions}
Concepts (name — meaning):
{concepts}
Answer with ONE JSON object and nothing else:
{{"items": [{{"name": "<the concept name exactly>", "metaphor": "<a few Arabic words>", "options": [{{"main": "…", "extras": ["…"], "motion": "…"}}]}}]}}"""


def needs_picture(names: list) -> list:
    """The concepts that have NO saved Lego drawing yet (only those cost a model call)."""
    return [n for n in dict.fromkeys(names) if n and saved(n) is None]


def ask_model(names: list, llm, subject: str = "", meanings: dict = None, limit: int = 30) -> dict:
    """ONE model call for up to `limit` new concepts → checked → saved in the library (the first good option is used at once,
    status «auto»; all good options stay as suggestions for the teacher). Returns {name: key} of what was saved.
    No key / bad answer → {} (nothing changes: the words or the subject character stay)."""
    todo = needs_picture(names)[:limit]
    if not todo:
        return {}
    meanings = meanings or {}
    user = PROMPT.format(subject=str(subject or "").strip(),
                         mains="\n".join(f"  {k}: {v[0]}" for k, v in MAINS.items()),
                         extras="\n".join(f"  {k}: {v}" for k, v in EXTRAS.items()),
                         motions=", ".join(MOTIONS),
                         concepts="\n".join(f"  {n} — {str(meanings.get(n, ''))[:120]}" for n in todo))
    try:
        text = llm("You answer with one JSON object only.", user)
        m = re.search(r"\{.*\}", text or "", re.S)
        items = json.loads(m.group(0)).get("items", []) if m else []
    except Exception:                                    # no key, network, bad JSON… → nothing changes, the book still works
        return {}
    want = {_key_of(n): n for n in todo}
    data, out = dict(library()), {}
    for it in items if isinstance(items, list) else []:
        if not isinstance(it, dict):
            continue
        name = want.get(_key_of(it.get("name", "")))
        if not name:
            continue                                     # a name we did not ask for: ignored
        keys = []
        for o in (it.get("options") or [])[:3]:
            if isinstance(o, dict) and o.get("main") in MAINS:
                k = make_key(o["main"], [x for x in (o.get("extras") or []) if isinstance(x, str)], color_of(name), o.get("motion"))
                if k not in keys:
                    keys.append(k)
        if keys:
            data[_key_of(name)] = {"name": name, "key": keys[0], "suggestions": keys, "metaphor": str(it.get("metaphor") or "")[:60],
                                   "source": "model", "status": "auto", "subject": str(subject or "")}
            out[name] = keys[0]
    if out:
        _save(data)
    return out


def choose(name: str, pick: int = None, reject: bool = False) -> dict:
    """The teacher's decision: pick suggestion number `pick` (0, 1, 2) → «approved», or reject → the subject character again.
    Returns {"name", "old", "new"} (old/new keys, so the books that use it can be updated)."""
    data = dict(library())
    k = _key_of(name)
    e = data.get(k)
    if not e:
        raise KeyError(name)
    old = saved(name) or by_words(name)
    if reject:
        e["status"] = "rejected"
    else:
        sugg = e.get("suggestions") or [e["key"]]
        if pick is None or not (0 <= int(pick) < len(sugg)):
            raise ValueError(f"pick لازم بين 0 و {len(sugg) - 1}")
        e["key"], e["status"] = sugg[int(pick)], "approved"
    data[k] = e
    _save(data)
    return {"name": e.get("name", name), "old": old, "new": saved(name) or by_words(name)}
