"""🎭 Every subject has its own IDENTITY: a SOUND (instrument + scale) and CHARACTERS (an emblem, a mascot with a name).

   · The 7 subjects we already know (science, maths, physics, chemistry, geography, history, language) keep exactly
     what they have: their sounds live in the page (sound.js) and their drawings in the drawing library.
   · A NEW subject gets its own identity:
       1) by its words (computer, music, art, economics, religion, sport, health, civics, thinking, farming) → a ready family;
       2) nothing matches → a stable identity made from the subject's own name (the same subject always sounds and
          looks the same, and two different subjects almost never share one).
   The families are checked BEFORE the known subjects, so «Computer Science» / «علوم الحاسوب» is the computer, not science.
   Plain Python, no AI. Used by: offline_generator.icon_for (the characters) and player/build_explain_player.pack (the page)."""
import json
import os
import re
import zlib

# the subjects we know (their sounds + drawings already exist in the page) — the page's «subject» value
KNOWN = (("math", ("math", "رياضيات")), ("science", ("science", "biology", "علوم", "أحياء")), ("physics", ("physics", "فيزياء")),
         ("chemistry", ("chem", "كيمياء")), ("geography", ("geograph", "جغرافيا")), ("history", ("history", "تاريخ")),
         ("language", ("arabic", "english", "language", "لغة", "عربي")))

# the instruments and scales the page can play (sound.js → VOICES / SCALE). A test checks they are really there.
INSTRUMENTS = ("marimba", "pluck", "epiano", "glass", "kalimba", "wood", "flute", "bell", "chip", "harp", "vibes", "steel")
SCALES = ("major", "sus", "minor", "egypt")

# ready families for new subjects: words → emblem (the characters' shape) + mascot + sound
FAMILIES = (
    {"id": "computer", "label": "الحاسوب والتكنولوجيا", "emblem": "💻", "mascot": "بِتّو",
     "words": ("computer", "comput", "programming", "coding", "technology", "informatics", "ict", "robot", "حاسوب", "حاسب",
               "artificial intelligence", "ai", "برمجة", "تكنولوجيا", "تقنية", "معلوماتية", "رقمي", "روبوت", "ذكاء اصطناعي"),
     "sound": {"instr": "chip", "root": 64, "scale": "major"}},
    {"id": "music", "label": "الموسيقى", "emblem": "🎵", "mascot": "نغّوم",
     "words": ("music", "موسيقى", "موسيقا", "أناشيد", "إيقاع"), "sound": {"instr": "harp", "root": 62, "scale": "sus"}},
    {"id": "art", "label": "الفنون", "emblem": "🎨", "mascot": "لوّون",
     "words": ("art", "drawing", "design", "فنون", "فن", "تربية فنية", "رسم", "تصميم"), "sound": {"instr": "vibes", "root": 65, "scale": "major"}},
    {"id": "economy", "label": "الاقتصاد والمال", "emblem": "💹", "mascot": "قرّوش",
     "words": ("economic", "business", "finance", "accounting", "entrepreneur", "اقتصاد", "مالية", "محاسبة", "أعمال", "ريادة"),
     "sound": {"instr": "steel", "root": 60, "scale": "major"}},
    {"id": "religion", "label": "التربية الإسلامية", "emblem": "📗", "mascot": "نور", "face": False,
     "words": ("islamic", "religio", "quran", "إسلامية", "دين", "قرآن", "فقه", "حديث", "سيرة", "عقيدة", "تلاوة"),
     "sound": {"instr": "harp", "root": 57, "scale": "egypt"}},
    {"id": "sport", "label": "التربية البدنية", "emblem": "⚽", "mascot": "كوّور",
     "words": ("sport", "physical education", "fitness", "تربية بدنية", "رياضة", "لياقة"), "sound": {"instr": "steel", "root": 67, "scale": "sus"}},
    {"id": "health", "label": "الصحة", "emblem": "🩺", "mascot": "صحّوح",
     "words": ("health", "nutrition", "medic", "first aid", "صحة", "صحية", "تغذية", "طب", "إسعاف"), "sound": {"instr": "vibes", "root": 60, "scale": "sus"}},
    {"id": "civics", "label": "التربية الوطنية والاجتماعية", "emblem": "🏛️", "mascot": "وطّون",
     "words": ("civic", "citizenship", "social studies", "sociology", "وطنية", "مواطنة", "اجتماعيات", "دراسات اجتماعية", "مجتمع"),
     "sound": {"instr": "marimba", "root": 57, "scale": "minor"}},
    {"id": "thinking", "label": "التفكير والفلسفة", "emblem": "💡", "mascot": "فكّور",
     "words": ("philosoph", "logic", "thinking", "psycholog", "فلسفة", "منطق", "تفكير", "علم نفس"), "sound": {"instr": "glass", "root": 64, "scale": "sus"}},
    {"id": "space", "label": "الفلك والفضاء", "emblem": "🪐", "mascot": "كوكوب",
     "words": ("astronom", "space", "فلك", "فضاء"), "sound": {"instr": "glass", "root": 66, "scale": "sus"}},
    {"id": "farming", "label": "الزراعة", "emblem": "🌾", "mascot": "سنبول",
     "words": ("agricultur", "farming", "زراعة", "زراعية"), "sound": {"instr": "kalimba", "root": 60, "scale": "major"}},
)

# anything else: one of these friendly shapes (the page draws each one), chosen from the subject's name
GENERIC_EMBLEMS = ("✦hex", "✦star", "✦cloud", "✦shield", "✦drop", "✦gem")
GENERIC_MASCOTS = ("زهّور", "لمّوع", "نجّوم", "سحّوب", "قطّور", "ماسو")
NEW_INSTRUMENTS = ("chip", "harp", "vibes", "steel", "bell", "glass", "kalimba", "marimba")
# what the known subjects already use (a generic identity never copies one of them exactly)
_TAKEN = {("marimba", 65), ("pluck", 60), ("epiano", 62), ("glass", 69), ("kalimba", 67), ("wood", 57), ("flute", 62), ("bell", 60)}


def _text(subject) -> str:
    return " " + str(subject or "").lower().strip() + " "


_PREFIXES = ("وال", "بال", "فال", "لل", "ال", "و", "ب", "ل")


def _tokens(s: str) -> list:
    """The Arabic words, each also without «ال»/«و»… in front (so «والفنون» → «فنون»)."""
    out = []
    for w in re.findall(r"[\u0600-\u06FF]+", s):
        out.append(w)
        for p in _PREFIXES:
            if w.startswith(p) and len(w) - len(p) >= 2:
                out.append(w[len(p):])
                break
    return out


def _has(s: str, word: str) -> bool:
    """A WHOLE word, never a piece of another one: «طب» is not inside «تطبيقات», «art» is not inside «Earth»."""
    if re.match(r"^[a-z ]+$", word):                  # English: a word that starts here (long words may go on: «comput» → «computer»)
        tail = r"[a-z]*" if len(word) >= 5 else r"s?"
        return re.search(r"\b" + re.escape(word) + tail + r"\b", s) is not None
    if " " in word:                                   # an Arabic phrase: every word without «ال» («التربية البدنية» = «تربية بدنية»)
        bare = lambda x: " ".join(w[2:] if w.startswith("ال") and len(w) > 4 else w for w in x.split())
        return bare(word) in bare(s)
    return any(t == word or (len(word) >= 4 and t.startswith(word)) for t in _tokens(s))


def family(subject):
    """The ready family of a NEW subject (by its words), or None."""
    s = _text(subject)
    for f in FAMILIES:
        if any(_has(s, w) for w in f["words"]):
            return f
    return None


def known_kind(subject):
    """«science» / «math» / … for the subjects the page already knows, or None."""
    s = _text(subject)
    if family(subject):
        return None                                   # «Computer Science» is a new subject, not «science»
    return next((k for k, words in KNOWN if any(w in s for w in words)), None)


def _num(subject, salt: str) -> int:
    return zlib.crc32((salt + "|" + str(subject or "").strip().lower()).encode("utf-8"))


def generic(subject) -> dict:
    """A stable identity for a subject nothing matched: the same name → always the same sound and shape."""
    n = _num(subject, "id")
    instr = NEW_INSTRUMENTS[n % len(NEW_INSTRUMENTS)]
    root = 55 + (n // 7) % 15                         # 55..69: a comfortable middle range
    if (instr, root) in _TAKEN:
        root += 2
    i = (n // 131) % len(GENERIC_EMBLEMS)
    return {"id": "new", "label": str(subject or "مادة جديدة").strip() or "مادة جديدة", "emblem": GENERIC_EMBLEMS[i],
            "mascot": GENERIC_MASCOTS[i],
            "sound": {"instr": instr, "root": root, "scale": SCALES[(n // 977) % len(SCALES)]}}


# ---------- 🤖 batch 28: the MODEL picks an identity that FITS the meaning (once per subject, then it is saved) ----------
# Only for a subject that is not one of the 7 known and not one of the 11 families. The model chooses ONLY from what the page
# can draw and play (the lists above); its answer is checked; no key / bad answer → the stable identity from the name (as before).
EMBLEMS = tuple(f["emblem"] for f in FAMILIES) + GENERIC_EMBLEMS + ("📜", "🧮", "🔬", "📖", "🧭", "🔭", "⚗️")   # every shape the page draws
_STORE = os.environ.get("EXPLAIN_IDENTITY_FILE") or os.path.join(os.path.dirname(os.path.abspath(__file__)), "subject_identities.json")
_CACHE = {"mtime": None, "data": {}}


def set_store(path: str) -> None:
    """Where the chosen identities are saved (the API puts it in its data folder)."""
    global _STORE
    _STORE = path
    _CACHE["mtime"] = None


def _key(subject) -> str:
    return " ".join(str(subject or "").lower().split())


def _saved() -> dict:
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


def chosen(subject):
    """The identity the model chose for this subject (already checked), or None."""
    return _saved().get(_key(subject))


def clean(ans, subject) -> dict:
    """Check the model's answer: only things the page can draw and play. Anything wrong → None (the name identity stays)."""
    if not isinstance(ans, dict):
        return None
    emb, instr, scale, name = ans.get("emblem"), ans.get("instrument"), ans.get("scale"), str(ans.get("mascot_name") or "").strip()
    try:
        root = int(ans.get("root"))
    except (TypeError, ValueError):
        return None
    if emb not in EMBLEMS or instr not in INSTRUMENTS or scale not in SCALES or not (55 <= root <= 69):
        return None
    if not re.fullmatch(r"[\u0621-\u064A\u0651]{2,10}", name):            # one short Arabic name (letters + shadda), nothing else
        return None
    label = str(ans.get("label") or subject or "").strip()[:30] or str(subject)
    return {"id": "chosen", "label": label, "emblem": emb, "mascot": name, "face": bool(ans.get("face", True)),
            "sound": {"instr": instr, "root": root, "scale": scale}}


PROMPT = """You give a NEW school subject its own identity on an Arabic learning page for students.
Subject: «{subject}»
Choose ONLY from these lists (the page can draw and play nothing else):
- emblem (the shape of all its characters; pick the one whose MEANING fits best): {emblems}
- instrument: {instruments}
- scale: {scales}   (major = bright, sus = open/calm, minor = serious, egypt = oriental)
- root: a number 55..69 (lower = deeper)
- mascot_name: ONE short friendly Arabic name for its main character, from the subject's own world, in the style of
  «بِتّو» (computer), «نغّوم» (music), «سنبول» (farming), «كوكوب» (space): 3-8 Arabic letters, a shadda allowed, no vowels, no spaces
- label: the subject's Arabic name for the page
- face: false only if faces would be disrespectful for this subject (e.g. religion), else true
Answer with ONE JSON object and nothing else:
{{"emblem": "…", "instrument": "…", "scale": "…", "root": 60, "mascot_name": "…", "label": "…", "face": true}}"""


def needs_model(subject) -> bool:
    """True when a model could give a better identity: a new subject, not a family, not chosen yet."""
    return bool(str(subject or "").strip()) and not known_kind(subject) and not family(subject) and chosen(subject) is None


def ask_model(subject, llm) -> dict:
    """ONE model call for a new subject → checked → saved (the next books of this subject reuse it, no new cost).
    llm(system, user) -> text. Returns the chosen identity, or None (no change: the name identity stays)."""
    if not needs_model(subject):
        return chosen(subject)
    user = PROMPT.format(subject=str(subject).strip(), emblems=" ".join(EMBLEMS), instruments=", ".join(INSTRUMENTS), scales=", ".join(SCALES))
    try:
        text = llm("You answer with one JSON object only.", user)
        m = re.search(r"\{.*\}", text or "", re.S)
        ans = clean(json.loads(m.group(0)) if m else None, subject)
    except Exception:                                    # no key, network, bad JSON… → the stable name identity (never breaks a book)
        return None
    if ans:
        data = dict(_saved())
        data[_key(subject)] = ans
        os.makedirs(os.path.dirname(_STORE) or ".", exist_ok=True)
        with open(_STORE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=1)
        _CACHE["mtime"] = None
    return ans


def of_book(book: dict) -> dict:
    """Everything the page needs about the book's identity.
    known subject → {"kind": "science", "sound": None, ...} (the page keeps what it has)
    new subject   → {"kind": "general", "family": "computer", "sound": {...}, "emblem": "💻", "mascot": "subj:💻:", "mascot_name": "بِتّو", ...}"""
    subject = (book or {}).get("subject", "")
    kind = known_kind(subject) or ("general" if not str(subject or "").strip() else None)   # no subject at all: as before
    if kind:
        return {"kind": kind, "family": None, "new": False, "label": str(subject), "emblem": None, "mascot": None,
                "mascot_name": None, "face": True, "sound": None}
    f = family(subject) or chosen(subject) or generic(subject)     # family (by words) → the model's choice (saved) → from the name
    return {"kind": "general", "family": f["id"], "new": True, "label": f["label"], "emblem": f["emblem"],
            "mascot": f"subj:{f['emblem']}:", "mascot_name": f["mascot"],
            "face": f.get("face", True), "sound": dict(f["sound"])}   # (how they MOVE is decided by the page: SUBJ_ANIM in part3_core.js)


def emblem(subject):
    """The emblem of a NEW subject's characters (None for the subjects we know: they keep their own)."""
    if known_kind(subject) or not str(subject or "").strip():
        return None
    return (family(subject) or chosen(subject) or generic(subject))["emblem"]
