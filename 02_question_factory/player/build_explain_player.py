"""Builds the explanation page: python player/build_explain_player.py [graph.json explain_out] [graph2.json explain_out2] ...
It puts the saved explanations of one or many books into player/explain.html (one self-contained page)."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import offline_generator as og  # noqa: E402
import audience as A  # noqa: E402
import identity  # noqa: E402
from graph_reader import Graph  # noqa: E402

KINDS = identity.KNOWN                               # the subjects the page knows (kept here too: older code imports it)


ART_DIR = os.path.join(os.path.dirname(os.path.dirname(HERE)), "05_explanation_api", "art")
DEMO_DIR = os.path.join(os.path.dirname(HERE), "llm_scenes_demo")


def _art_svg(key):
    """Our drawing of a picture key as SVG text (the same one the API serves, from its ONE file art/art.json)."""
    try:
        return json.load(open(os.path.join(ART_DIR, "art.json"), encoding="utf-8"))["files"].get(key)
    except (OSError, ValueError, KeyError):
        return None


def demo_scenes(g):
    """🤖 Example «model-written» scenes (hand-written in the model's format, clearly labeled) → {(lesson, concept): scene}."""
    import scene_writer
    out = {}
    if not os.path.isdir(DEMO_DIR):
        return out
    lessons = {l.id: l for l in g.lessons()}
    for name in sorted(os.listdir(DEMO_DIR)):
        d = json.load(open(os.path.join(DEMO_DIR, name), encoding="utf-8"))
        if d.get("book_id") != g.book.get("id") or d.get("lesson_id") not in lessons or scene_writer.check_code(d["code"]):
            continue                                                     # only scenes that pass the same checks as the model's
        data = scene_writer.scene_data(g, lessons[d["lesson_id"]], d["concept_id"], art_svg=_art_svg)
        out[(d["lesson_id"], d["concept_id"])] = {"kind": "custom", "target": d["concept_id"], "source": "demo", "label": d.get("label", ""),
                                                  "runner_html": scene_writer.runner_html(d["code"], data),
                                                  "steps": [f"🤖 مشهد جديد عن «{data['concept']['name']}»"], "paragraph": data["concept"]["meaning"]}
    return out


def pack(graph_path, out_dir, extra=None):
    """One book for the page. extra = {(lesson_id, concept_id): [scene, …]}: more scenes to add after the factory's
    (the API passes the model-written scenes a TEACHER APPROVED; nothing else is added)."""
    g = Graph.load(graph_path)
    idx = json.load(open(os.path.join(out_dir, "explain_index.json"), encoding="utf-8"))
    by_id = {l.id: l for l in g.lessons()}
    lessons = []
    for lid in idx["lessons"]:
        rec = json.load(open(os.path.join(out_dir, "lessons", lid, "explanations.json"), encoding="utf-8"))
        rec["theme"] = og.choose_theme(g, by_id[lid])
        for c in rec["concepts"]:
            c["questions"] = []                      # the shared core expects it; the explanation page has no questions
        lessons.append(rec)
    order = {l.id: i for i, l in enumerate(g.learning_order([c for c in g.concepts.values() if og.is_entity(g, c.id)]))}
    lessons.sort(key=lambda r: min((order.get(c["concept_id"], 0) for c in r["concepts"]), default=0))   # the order to learn them
    demos = demo_scenes(g)
    for r in lessons:
        for c in r["concepts"]:
            if (r["lesson_id"], c["concept_id"]) in demos:
                c["scenes"].append(demos[(r["lesson_id"], c["concept_id"])])
            c["scenes"].extend((extra or {}).get((r["lesson_id"], c["concept_id"]), []))   # 🤖 approved model scenes (API)
    idn = identity.of_book(g.book)                  # 🎭 known subject → its own sounds/drawings · NEW subject → its own identity
    out = {"title": g.book.get("title", "الكتاب"), "subject": idn["kind"], "audience": A.audience(g),   # 👥 grade → stage (the page's look)
           "names": {k: c.text for k, c in g.concepts.items()}, "lessons": lessons}
    if idn["new"]:                                  # only for new subjects (the 12 books stay byte-for-byte what they were)
        out["identity"] = {k: idn[k] for k in ("family", "label", "emblem", "mascot", "mascot_name", "face")}
        out["sound"] = idn["sound"]
    return out


def page_html(graphs: list) -> str:
    """The whole page with these books inside (graphs = what pack() gives). Used here AND by the API (/explain)."""
    data = {"graphs": graphs}
    return open(os.path.join(HERE, "explain_template.html"), encoding="utf-8").read().replace(
        "/*DATA*/null", json.dumps(data, ensure_ascii=False).replace("</", "<\\/").replace("<!--", "<\\!--"))   # «</script>» inside the data must not end the page's script


if __name__ == "__main__":
    root = os.path.dirname(HERE)
    args = sys.argv[1:] or ["plants_book_graph.json", "explain_out"]
    if len(args) % 2:
        sys.exit("give pairs: graph.json explain_out_folder")
    data = {"graphs": [pack(os.path.join(root, gp), os.path.join(root, od)) for gp, od in zip(args[::2], args[1::2])]}
    html = page_html(data["graphs"])
    out = os.path.join(HERE, "explain.html")
    open(out, "w", encoding="utf-8").write(html)
    print("wrote", out, sum(len(c["scenes"]) for g in data["graphs"] for l in g["lessons"] for c in l["concepts"]) + sum(len(g["lessons"]) for g in data["graphs"]), "scenes from", len(data["graphs"]), "book(s)")
