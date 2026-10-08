"""📚 One command for the whole explanation page: every book (grade 4 → 12) → explanations → player/explain.html.
   python build_all_books.py            (no AI)
   python build_all_books.py --llm      (the model polishes the «ليش؟» paragraphs; needs keys in api_key.txt)
Books are put in grade order, so the page goes from the little ones to the secondary school."""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
# (graph file, output folder) — the order on the page is by grade (from the book's «grade»)
BOOKS = ["plants_book_graph.json", "math_book_graph.json", "arabic_g4_book_graph.json", "history_book_graph.json", "geo_g5_book_graph.json",
         "phy_g6_book_graph.json", "chem_g7_book_graph.json", "sci_g8_book_graph.json", "math_g9_book_graph.json",
         "phy_g10_book_graph.json", "chem_g11_book_graph.json", "bio_g12_book_graph.json"]


def out_dir(graph_file: str) -> str:
    return "explain_out_" + graph_file.replace("_book_graph.json", "")


def grade(graph_file: str) -> int:
    with open(os.path.join(HERE, graph_file), encoding="utf-8") as f:
        return int(json.load(f)["book"].get("grade") or 0)


if __name__ == "__main__":
    extra = ["--llm"] if "--llm" in sys.argv else []
    books = sorted(BOOKS, key=grade)
    for gf in books:
        r = subprocess.run([sys.executable, os.path.join(HERE, "explain_main.py"), gf, out_dir(gf)] + extra, cwd=HERE, capture_output=True, text=True)
        print(("✅ " if r.returncode == 0 else "❌ ") + gf, "" if r.returncode == 0 else r.stderr[-400:])
    pairs = [x for gf in books for x in (gf, out_dir(gf))]
    subprocess.run([sys.executable, os.path.join(HERE, "player", "build_explain_player.py")] + pairs, cwd=HERE, check=True)
