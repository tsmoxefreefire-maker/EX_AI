"""The explanation factory's door:  python explain_main.py <graph.json> <out_dir>
For EACH lesson → for EACH concept → scenes that teach → checked → saved (lessons/<id>/explanations.json)."""
import json
import os
import sys

import explain_generator as eg
from graph_reader import Graph


def run(graph_path: str, out_dir: str, llm=None) -> list:
    g = Graph.load(graph_path)
    records = []
    for lesson in g.lessons():
        rec = eg.explain_lesson(g, lesson)
        if llm is not None:                                       # the model writes the paragraphs more clearly (checked)
            import explain_llm
            rec = explain_llm.polish_lesson(rec, llm)
        problems = eg.check_scene(g, rec["overview"])
        if rec.get("world") and eg.check_scene(g, rec["world"]):
            problems += eg.check_scene(g, rec["world"]); rec["world"] = None
        for c in rec["concepts"]:
            good = []
            for s in c["scenes"]:
                errs = eg.check_scene(g, s)
                (problems.extend(errs) if errs else good.append(s))
            c["scenes"] = good                                   # a wrong scene never reaches the student
        rec["warnings"] = rec.get("warnings", []) + problems            # keep the model's own warning (why it failed)
        rec["status"] = "needs_review"
        path = os.path.join(out_dir, "lessons", lesson.id)
        os.makedirs(path, exist_ok=True)
        with open(os.path.join(path, "explanations.json"), "w", encoding="utf-8") as f:
            json.dump(rec, f, ensure_ascii=False, indent=2)
        records.append(rec)
    with open(os.path.join(out_dir, "explain_index.json"), "w", encoding="utf-8") as f:
        json.dump({"graph": os.path.basename(graph_path), "lessons": [r["lesson_id"] for r in records]}, f, ensure_ascii=False)
    return records


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    graph, out = (args[0], args[1]) if len(args) == 2 else ("plants_book_graph.json", "explain_out")
    llm = None
    if "--llm" in sys.argv:
        import llm_gateway
        if not llm_gateway.api_key_from_anywhere():
            print(f"⚠️ ما في مفتاح: الصقه بملف {llm_gateway.PROJECT_KEY_FILE} (gemini: … / openai: … / claude: …)، أو شغّل بدون --llm.")
            sys.exit(1)
        llm = llm_gateway.generate
        print("LLM: on (Gemini → GPT → Claude: the first that works writes the paragraphs; names and facts stay the same)")
    recs = run(graph, out, llm)
    print(f"{len(recs)} lessons, {sum(len(c['scenes']) for r in recs for c in r['concepts']) + len(recs)} scenes -> {out}/")
    for r in recs:
        extra = f"  · LLM rewrote {r['llm']['rewritten']}/{r['llm']['paragraphs']} paragraphs" if r.get("llm") else ""
        print(f"  {r['lesson_title']}{extra}")
        for w in r.get("warnings", []):
            if w.startswith("llm"):
                print("     ⚠️", w[:400])                         # say WHY the model did not work (no credit, no key…)
    if llm is not None:
        import llm_gateway
        print("model used:", llm_gateway.LAST_PROVIDER or "none")
