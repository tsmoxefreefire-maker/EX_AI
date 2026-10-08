"""Builds code_tour/CODE_TOUR.html: the backend step by step, from the graph to the page (Hareth's idea).
Every step shows ITS function's real code, read from the files right now (with its line numbers), the Arabic card from
steps_ar.py, and which steps it uses / which steps use it (found by reading the code, not written by hand).
Run after changing the code:   python code_tour/build_code_tour.py        (plain Python, no installs)"""
import ast
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from steps_ar import PHASES, STEPS  # noqa: E402

NOT_OURS = {"json", "os", "re", "sys", "math", "zlib", "datetime", "random", "shutil", "urllib", "hashlib", "f", "s", "self_"}
COMMON = {"load", "get", "run", "generate", "page_html", "voice", "stage", "pick"}   # never matched by name alone (too common)


def mod_of(path):
    return os.path.splitext(os.path.basename(path))[0] if path else None


def find(tree, func):
    """The ast node of «name» or «Class.method» (None = the whole file)."""
    parts = func.split(".")
    nodes = tree.body
    found = None
    for i, p in enumerate(parts):
        found = next((n for n in nodes if isinstance(n, (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)) and n.name == p), None)
        if found is None:
            raise SystemExit(f"not found: {func}")
        nodes = found.body
    return found


def aliases(tree):
    """Every import of the file (anywhere in it): local name → module (last part)."""
    out = {}
    for n in ast.walk(tree):
        if isinstance(n, ast.Import):
            for a in n.names:
                out[a.asname or a.name.split(".")[0]] = a.name.split(".")[-1]
        elif isinstance(n, ast.ImportFrom) and n.module:
            for a in n.names:
                out[a.asname or a.name] = a.name if n.module in ("core", "api") else n.module.split(".")[-1]
    return out


def main():
    trees, codes = {}, []
    for i, st in enumerate(STEPS):
        st["n"] = i + 1
        st["mod"] = mod_of(st["file"])
        st["name"] = (st["func"] or "").split(".")[-1]
        if not st["file"]:
            st.update(code="", start=0, end=0)
            continue
        path = os.path.join(ROOT, st["file"])
        src = open(path, encoding="utf-8").read()
        tree = trees.setdefault(st["file"], ast.parse(src))
        lines = src.splitlines()
        if st["func"] is None:
            st.update(code=src.rstrip(), start=1, end=len(lines), node=tree)
        else:
            node = find(tree, st["func"])
            start = min([d.lineno for d in getattr(node, "decorator_list", [])] + [node.lineno])
            st.update(code="\n".join(lines[start - 1:node.end_lineno]), start=start, end=node.end_lineno, node=node)
    # ---- who uses whom (from the code itself) ----
    by_mod_name = {}
    by_name = {}
    for st in STEPS:
        if st["name"]:
            by_mod_name[(st["mod"], st["name"])] = st["n"]
            by_name.setdefault(st["name"], []).append(st["n"])
    for st in STEPS:
        st["calls"] = []
        if "node" not in st or st["func"] is None:
            continue
        al = aliases(trees[st["file"]])
        hits = []
        for n in ast.walk(st["node"]):
            target = None
            if isinstance(n, ast.Attribute) and isinstance(n.ctx, ast.Load):
                v = n.value.id if isinstance(n.value, ast.Name) else None
                if v == "self" or v == "cls":
                    target = by_mod_name.get((st["mod"], n.attr))
                elif v in al:
                    m = al[v]
                    if m not in NOT_OURS:
                        target = by_mod_name.get((m, n.attr))
                elif n.attr in by_name and len(by_name[n.attr]) == 1 and n.attr not in COMMON:
                    target = by_name[n.attr][0]
            elif isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load):
                # cls(...) inside a classmethod = the class's __init__
                target = by_mod_name.get((st["mod"], "__init__" if n.id == "cls" else n.id))
            if target and target != st["n"] and target not in hits:
                hits.append(target)
        st["calls"] = sorted(hits)
    for st in STEPS:
        st["called_by"] = sorted(o["n"] for o in STEPS if st["n"] in o["calls"])
    data = {"phases": [{"id": a, "title": b, "desc": c} for a, b, c in PHASES],
            "steps": [{k: st.get(k) for k in ("n", "phase", "file", "func", "title", "what", "takes", "does", "gives", "optional", "note",
                                              "code", "start", "end", "calls", "called_by")} for st in STEPS]}
    page = open(os.path.join(HERE, "page_template.html"), encoding="utf-8").read()
    out = page.replace("/*TOUR*/null", json.dumps(data, ensure_ascii=False).replace("</", "<\\/"))
    with open(os.path.join(HERE, "CODE_TOUR.html"), "w", encoding="utf-8") as f:
        f.write(out)
    print(f"CODE_TOUR.html: {len(STEPS)} steps, {sum(len(s['calls']) for s in STEPS)} links")
    for st in STEPS:
        print(f"  {st['n']:>2} {st['func'] or st['file'] or '—'}  ← calls {st['calls']}  · called by {st['called_by']}")


if __name__ == "__main__":
    main()
