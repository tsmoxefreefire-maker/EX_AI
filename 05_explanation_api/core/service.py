"""The service: everything the API can do, as plain Python (no web code here, so it is easy to test and reuse).

   graph → the factory makes the explanation of EVERY lesson and keeps it → then:
     · the PAGE itself (/explain): the same interactive page as the published one (scenes, the 5 activities, films,
       sounds per subject and per age stage), built from what is kept on the server — for any graph;
     · the DATA (books / lessons / concepts / pictures) for any other front end.
   A NEW subject gets its own identity (identity.py in the factory): its own sound and its own characters.
   No AI unless asked (use_llm), and then only to polish the «ليش؟» paragraphs."""
import datetime
import json
import os
import re
import sys

from core import art, settings, storage

sys.path.insert(0, settings.FACTORY_DIR)          # the explanation factory (plain Python) — the SAME code that built the published page
sys.path.insert(0, settings.PLAYER_DIR)           # the page builder (pack + the template)
import audience  # noqa: E402
import build_all_books  # noqa: E402
import build_explain_player as player  # noqa: E402
import explain_main  # noqa: E402
import identity  # noqa: E402
import lego  # noqa: E402
import offline_generator as og  # noqa: E402
import llm_gateway  # noqa: E402
from graph_reader import Graph  # noqa: E402

identity.set_store(os.path.join(settings.DATA_DIR, "subject_identities.json"))   # 🤖 identities the model chose (one per new subject)
lego.set_store(os.path.join(settings.DATA_DIR, "lego_library.json"))              # 🧱 drawings BUILT from parts (the library grows)


class NotFound(Exception):
    """Asked for something that does not exist (→ 404)."""


class BadInput(Exception):
    """The request itself is wrong (→ 400)."""


_SAFE_ID = re.compile(r"^[\w\-؀-ۿ]{1,80}$")


def _book_id_of(graph: dict) -> str:
    bid = (graph.get("book") or {}).get("id")
    if not bid:
        bid = next((n.get("id") for n in graph.get("nodes", []) if n.get("level") == "book"), None)
    if not bid:
        raise BadInput("الجراف ما فيه كتاب (book.id أو node level=book)")
    bid = str(bid)
    if not _SAFE_ID.match(bid):                       # it becomes a folder name: letters, digits, _ and - only (never «../»)
        raise BadInput("رقم الكتاب (book.id) لازم يكون حروف وأرقام و _ - بس")
    return bid


def _graph_file(book_id: str) -> str:
    return os.path.join(settings.GRAPHS_DIR, f"{book_id}.json")


def _find_graph(name: str) -> str:
    """A graph by name: a saved one (data/graphs) or one of the sample books (02_question_factory)."""
    if os.path.isabs(name):
        return name
    for base in (settings.GRAPHS_DIR, settings.SAMPLES_DIR):
        p = os.path.join(base, os.path.basename(name))
        if os.path.exists(p):
            return p
    raise NotFound(f"ما في جراف اسمه {name}")


def generate(graph: dict = None, graph_path: str = None, use_llm: bool = False, llm=None, _sample: str = None) -> dict:
    """Turn a graph into explanations for EVERY lesson and keep them. Give the graph itself (JSON) or the name of a saved graph."""
    if graph is None and not graph_path:
        raise BadInput("ابعت الجراف (graph) أو اسم ملفه (graph_path)")
    if graph is None:
        with open(_find_graph(graph_path), encoding="utf-8") as f:
            graph = json.load(f)
    if not isinstance(graph, dict) or not isinstance(graph.get("nodes"), list):
        raise BadInput("الجراف لازم يكون JSON فيه nodes")
    book_id = _book_id_of(graph)
    os.makedirs(settings.GRAPHS_DIR, exist_ok=True)
    path = _graph_file(book_id)
    with open(path, "w", encoding="utf-8") as f:                     # a copy of the graph is kept: the page is built from it later
        json.dump(graph, f, ensure_ascii=False)
    warnings = []
    if llm is None and use_llm:
        if llm_gateway.api_key_from_anywhere():
            llm = llm_gateway.generate
        else:
            warnings.append("ما في مفتاح موديل على السيرفر: انعمل الشرح بدون AI")
    try:
        g = Graph.load(path)
        if not g.lessons():
            raise BadInput("الجراف ما فيه ولا درس (node level=lesson فيه مفاهيم)")
        if llm and identity.needs_model(g.book.get("subject")):          # 🤖 a new subject: ONE call → an identity that fits its meaning (saved)
            if identity.ask_model(g.book.get("subject"), llm) is None:
                warnings.append("الموديل ما أعطى هوية صالحة للمادة: أخذت هوية ثابتة من اسمها")
        lego_new = _lego_for_book(g, llm) if llm else {}                 # 🧱 concepts with no drawing: the model picks parts (ONE call)
        recs = explain_main.run(path, storage.book_dir(book_id), llm)
    except BadInput:
        raise
    except Exception as e:                                           # a broken graph says WHY, not «500»
        raise BadInput(f"ما قدرت أقرأ الجراف: {e}")
    lessons = [{"lesson_id": r["lesson_id"], "title": r["lesson_title"], "concepts": len(r["concepts"]),
                "scenes": 1 + bool(r.get("world")) + bool(r.get("assemble")) + sum(len(c["scenes"]) for c in r["concepts"])} for r in recs]
    for r in recs:
        warnings += [w for w in r.get("warnings", [])]
    idn = identity.of_book(g.book)
    meta = {"book_id": book_id, "title": g.book.get("title", book_id), "subject": g.book.get("subject", ""),
            "grade": g.book.get("grade"), "stage": audience.audience(g)["stage"],
            "lego": _lego_summary(g),
            "identity": {"new": idn["new"], "family": idn["family"], "by_model": idn["family"] == "chosen", "label": idn["label"], "emblem": idn["emblem"],
                         "mascot_name": idn["mascot_name"], "sound": idn["sound"]},
            "lessons": lessons, "scenes": sum(x["scenes"] for x in lessons),
            "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
            "llm": (llm_gateway.LAST_PROVIDER if llm is llm_gateway.generate else ("custom" if llm else None)),
            "version": settings.API_VERSION, "page_url": f"/explain/{book_id}"}
    if _sample:
        meta["sample"] = _sample                                     # (only for the order on the page)
    storage.save_meta(book_id, meta)
    return dict(meta, warnings=warnings)


# ---------- 🧱 Lego drawings (batch 29 · 💡 Hareth's idea) ----------
def _entities(g) -> list:
    return [c for c in g.concepts.values() if og.is_entity(g, c.id)]


def _lego_for_book(g, llm) -> dict:
    """The concepts that would get only the subject's character (no drawing in the library, no word that fits a part):
    ONE model call for all of them → the model CHOOSES parts → saved in the library. Nothing to ask → no call, no cost."""
    subject = str(g.book.get("subject", ""))
    todo = [c for c in _entities(g) if og.icon_for(c.text, c.description, subject).startswith("subj:")]
    if not todo:
        return {}
    return lego.ask_model([c.text for c in todo], llm, subject, {c.text: c.description for c in todo})


def _lego_summary(g) -> dict:
    """How the book's concepts got their pictures: from the library · built (Lego) · the subject's character."""
    subject = str(g.book.get("subject", ""))
    keys = [og.icon_for(c.text, c.description, subject) for c in _entities(g)]
    return {"library": sum(1 for k in keys if not k.startswith(("lego:", "subj:"))), "built": sum(1 for k in keys if k.startswith("lego:")),
            "subject_character": sum(1 for k in keys if k.startswith("subj:"))}


def lego_parts() -> dict:
    """The parts a Lego drawing is built from: their names, what they can mean, and the motions (the model sees the same)."""
    return {"main": {k: v[0] for k, v in lego.MAINS.items()}, "extra": dict(lego.EXTRAS), "motions": list(lego.MOTIONS),
            "key": "lego:<main>:<extra>+<extra>:<colour 0-7>:<motion>", "example": art.art_url("lego:drawers:binary:3:wobble")}


def lego_library() -> list:
    """Every drawing BUILT so far (the library that grows), with its suggestions for the teacher and a picture URL for each."""
    out = []
    for e in lego.library().values():
        out.append(dict(e, art=art.art_url(e["key"]), suggestion_art=[art.art_url(k) for k in e.get("suggestions", [])]))
    return sorted(out, key=lambda e: (e.get("status") != "auto", e.get("name", "")))


def lego_choose(name: str, pick: int = None, reject: bool = False) -> dict:
    """The teacher's choice (one of the model's suggestions, or «no» → the subject character). Every saved book that shows
    this concept gets the new picture at once (only the picture key changes in its lessons, nothing else)."""
    try:
        r = lego.choose(name, pick, reject)
    except KeyError:
        raise NotFound(f"ما في رسمة ليغو محفوظة لـ «{name}»")
    except ValueError as e:
        raise BadInput(str(e))
    updated = []
    for m in storage.list_books():
        b = m["book_id"]
        if not os.path.exists(_graph_file(b)):
            continue
        g = Graph.load(_graph_file(b))
        subject = str(g.book.get("subject", ""))
        for lid in storage.lesson_ids(b):
            rec = storage.load_lesson(b, lid)
            icons, changed = (rec or {}).get("icons", {}), False
            for cid, old in list(icons.items()):                       # a lesson keeps the picture key of every concept it shows
                if cid in g.concepts and lego._key_of(g.concepts[cid].text) == lego._key_of(name):
                    new = og.icon_for(g.concepts[cid].text, g.concepts[cid].description, subject)
                    if new != old:
                        icons[cid], changed = new, True                # only THIS concept (another one may share the same key)
            if changed:
                storage.save_lesson(b, lid, rec)
                updated.append(f"{b}/{lid}")
    return dict(r, art=art.art_url(r["new"]) if r["new"] else None, updated_lessons=updated)


# ---------- the 12 sample books ----------
def sample_files() -> list:
    return sorted(f for f in os.listdir(settings.SAMPLES_DIR) if f.endswith("_book_graph.json"))


def seed_samples(force: bool = False) -> list:
    """Make the sample books (grade 4 → 12). force=False: only the ones not made yet."""
    have = {m["book_id"] for m in storage.list_books()}
    out = []
    for name in sample_files():
        with open(os.path.join(settings.SAMPLES_DIR, name), encoding="utf-8") as f:
            graph = json.load(f)
        if force or _book_id_of(graph) not in have:
            out.append(generate(graph=graph, _sample=name.replace("_book_graph.json", "")))
    return out


def ensure_samples() -> None:
    """The first time the server has no book at all: make the samples, so the page is never empty (EXPLAIN_SEED=0 turns it off)."""
    if settings.SEED_SAMPLES and not storage.list_books():
        seed_samples()


def delete_book(book_id: str) -> dict:
    if not _SAFE_ID.match(book_id or "") or storage.book_meta(book_id) is None:
        raise NotFound(f"ما في كتاب {book_id}")
    storage.delete_book(book_id)
    if os.path.exists(_graph_file(book_id)):
        os.remove(_graph_file(book_id))
    return {"deleted": book_id}


# ---------- books / lessons / concepts / pictures (the data) ----------
def _order(m: dict) -> tuple:
    """Grade 4 → 12 (like the published page); in one grade, the samples in the page's own order, then the new books by title."""
    try:
        grade = int(m.get("grade") or 99)
    except (TypeError, ValueError):
        grade = 99
    first = {f.replace("_book_graph.json", ""): i for i, f in enumerate(build_all_books.BOOKS)}
    return (grade, first.get(m.get("sample") or "", 99), m.get("title") or "")


def list_books() -> list:
    keys = ("book_id", "title", "subject", "grade", "stage", "identity", "scenes", "generated_at", "page_url")
    return [{k: m.get(k) for k in keys} for m in sorted(storage.list_books(), key=_order)]


def list_lessons(book_id: str) -> list:
    meta = storage.book_meta(book_id)
    if meta is None:
        raise NotFound(f"ما في كتاب {book_id}")
    return meta["lessons"]


def _with_art(rec: dict) -> dict:
    rec = dict(rec)
    rec["art"] = {cid: art.art_url(icon) for cid, icon in rec.get("icons", {}).items()}
    return rec


def get_lesson(lesson_id: str, book_id: str = None, include_llm: bool = False) -> dict:
    """Everything the front end needs to show one lesson (scenes + texts + picture URLs + «audience» = the age stage).
    include_llm=True adds the scenes the model wrote AND a teacher approved ({"kind": "custom", "runner_url": …})."""
    b, rec = storage.find_lesson(lesson_id, book_id)
    if rec is None:
        raise NotFound(f"ما في درس {lesson_id}")
    rec = _with_art(rec)
    if include_llm:
        from core import llm_scenes                                   # (imported here: the model part is optional)
        extra = llm_scenes.approved_for_lesson(b, lesson_id)
        rec["concepts"] = [dict(c, scenes=c["scenes"] + extra.get(c["concept_id"], [])) for c in rec["concepts"]]
    return dict(rec, book_id=b)


def get_concept(concept_id: str, book_id: str = None) -> dict:
    """The scenes of ONE concept (and the lesson it belongs to)."""
    books = [book_id] if book_id else [m["book_id"] for m in storage.list_books()]
    for b in books:
        for lid in storage.lesson_ids(b):
            rec = storage.load_lesson(b, lid)
            for c in (rec or {}).get("concepts", []):
                if c["concept_id"] == concept_id:
                    icon = rec.get("icons", {}).get(concept_id)
                    return dict(c, book_id=b, lesson_id=lid, lesson_title=rec["lesson_title"], icon=icon, art=art.art_url(icon),
                                art_of_others={k: art.art_url(v) for k, v in rec.get("icons", {}).items()})
    raise NotFound(f"ما في مفهوم {concept_id}")


def get_art(key: str, stage: str = "kids") -> str:
    svg = art.art_svg(key, stage or "kids")
    if svg is None:
        raise NotFound(f"ما في رسمة للمفتاح {key}")
    return svg


# ---------- 📖 the PAGE (the same interactive page as the published one) ----------
def _books_for_page(book_ids=None) -> list:
    metas = sorted(storage.list_books(), key=_order)
    if book_ids:
        want = [b for b in book_ids if b]
        missing = [b for b in want if b not in {m["book_id"] for m in metas}]
        if missing:
            raise NotFound("ما في كتاب: " + "، ".join(missing))
        metas = [m for m in metas if m["book_id"] in want]
    return metas


def _approved_llm(book_id: str) -> dict:
    """The model scenes a teacher approved for this book (empty if none, or if the model part is not there)."""
    try:
        from core import llm_scenes
        return llm_scenes.approved_for_page(book_id)
    except Exception:                                                # the model part is optional: the page never breaks because of it
        return {}


def page_data(book_ids=None) -> dict:
    """What the page gets: every chosen book with its lessons, scenes, stage, subject and (for a new subject) its identity."""
    graphs = []
    for m in _books_for_page(book_ids):
        if os.path.exists(_graph_file(m["book_id"])):
            graphs.append(player.pack(_graph_file(m["book_id"]), storage.book_dir(m["book_id"]), extra=_approved_llm(m["book_id"])))
    if not graphs:
        raise NotFound("لسا ما في ولا كتاب: ابعت جراف لـ POST /explanations/generate")
    return {"graphs": graphs}


def page_html(book_ids=None) -> str:
    """The whole interactive page with the chosen books (all of them if none chosen), built from the server's data."""
    if not os.path.exists(settings.PAGE_TEMPLATE):
        raise NotFound("قالب الصفحة مش موجود: شغّل python 03_explain_player_src/build_explain_template.py")
    return player.page_html(page_data(book_ids)["graphs"])


def home_html() -> str:
    """The server's front page: the books + a box to send a NEW graph (then open its page)."""
    with open(os.path.join(settings.BASE_DIR, "static", "home.html"), encoding="utf-8") as f:
        return f.read()
