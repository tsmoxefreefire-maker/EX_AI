"""Reads the WHOLE project (plain Python, no installs) for the project explorer page (💡 Hareth's idea):
every file, its language, its functions / classes / data with their line numbers, and the links between the files
(who imports / uses whom). Nothing here is written by hand except the few links Python's imports cannot see (EXTRA_LINKS).
    python code_tour/explorer_scan.py      → prints a summary and writes code_tour/notes/_structure.json"""
import ast
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

SKIP_DIRS = {"__pycache__", "data", "shots", "notes", ".git"}
SKIP_FILES = {"api_key.txt", ".env", "lego_library.json", "subject_identities.json", "PROJECT_EXPLORER.html", "CODE_TOUR.html"}
# files made by a build: shown with their card, but only their first lines (they are huge and nobody edits them)
GENERATED = {"02_question_factory/player/explain.html": "02_question_factory/build_all_books.py",
             "02_question_factory/player/explain_template.html": "03_explain_player_src/build_explain_template.py",
             "05_explanation_api/art/art.json": "05_explanation_api/scripts/export_art.py"}
GEN_LINES = 60
LANG = {".py": "python", ".js": "js", ".css": "css", ".css2": "css", ".css3": "css", ".html": "html", ".json": "json",
        ".md": "md", ".txt": "text", "": "text"}

# links Python's imports cannot see (a file reads another one by its path, or a build glues files together)
_SRC = "03_explain_player_src/"
_PAGE_JS = ["part3_core.js", "explain.js", "world.js", "narrator.js", "play.js", "more_scenes.js", "more_scenes2.js",
            "art_secondary.js", "art_more.js", "lego.js", "stage.js", "sound.js", "more_scenes3.js"]
_PAGE_CSS = ["part2_games.css", "new_css.css", "alive.css", "more.css", "chars.css", "order.css", "throw.css", "art.css", "batch10.css",
             "predict.css", "explain_w.css", "narrator.css", "play.css", "more.css2", "more.css3", "polish.css", "stage.css", "acts.css"]
EXTRA_LINKS = {
    "03_explain_player_src/build_explain_template.py": [_SRC + "explain_shell.html"] + [_SRC + f for f in _PAGE_JS + _PAGE_CSS],
    "02_question_factory/player/build_explain_player.py": ["02_question_factory/player/explain_template.html", "05_explanation_api/art/art.json"],
    "02_question_factory/build_all_books.py": ["02_question_factory/explain_main.py", "02_question_factory/player/build_explain_player.py"],
    "05_explanation_api/core/art.py": ["05_explanation_api/art/art.json"],
    "05_explanation_api/scripts/export_art.py": ["02_question_factory/player/explain.html"],
    "05_explanation_api/scripts/refresh_doc.py": ["05_explanation_api/EXPLANATION_API_AR.md"],
    "05_explanation_api/core/service.py": ["05_explanation_api/static/home.html"],
    "code_tour/build_code_tour.py": ["code_tour/page_template.html"],
    "code_tour/build_project_explorer.py": ["code_tour/explorer_template.html"],
}
JS_STOP = {"name", "list", "data", "node", "text", "show", "step", "play", "render", "size", "color", "draw", "line", "pick",
           "init", "wire", "make", "move", "next", "prev", "done", "test", "load", "save", "find", "fill", "tick", "item"}


def rel(p):
    return os.path.relpath(p, ROOT).replace(os.sep, "/")


def all_files():
    out = []
    for root, dirs, files in os.walk(ROOT):
        dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS and not d.startswith("explain_out") and not d.startswith("."))
        for f in sorted(files):
            if f in SKIP_FILES or f.endswith(".pyc"):
                continue
            out.append(rel(os.path.join(root, f)))
    return out


def lang_of(path):
    base = os.path.basename(path)
    if base.startswith(".git"):
        return "text"
    return LANG.get(os.path.splitext(base)[1], "text")


# ------------------------------------------------------------------ Python
def _doc1(node):
    d = ast.get_docstring(node) if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Module)) else None
    return (d or "").strip().split("\n")[0][:160]


def py_items(src):
    tree = ast.parse(src)
    items = []

    def start_of(n):
        return min([d.lineno for d in getattr(n, "decorator_list", [])] + [n.lineno])

    for n in tree.body:
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
            items.append({"key": n.name, "kind": "func", "start": start_of(n), "end": n.end_lineno, "doc": _doc1(n)})
        elif isinstance(n, ast.ClassDef):
            items.append({"key": n.name, "kind": "class", "start": start_of(n), "end": n.end_lineno, "doc": _doc1(n)})
            for m in n.body:
                if isinstance(m, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    items.append({"key": f"{n.name}.{m.name}", "kind": "method", "start": start_of(m), "end": m.end_lineno, "doc": _doc1(m)})
        elif isinstance(n, (ast.Assign, ast.AnnAssign)):
            targets = n.targets if isinstance(n, ast.Assign) else [n.target]
            for t in targets:
                if isinstance(t, ast.Name) and t.id.isupper() and len(t.id) > 1 and (n.end_lineno - n.lineno >= 2 or isinstance(n.value, (ast.Dict, ast.List, ast.Tuple, ast.Set))):
                    items.append({"key": t.id, "kind": "data", "start": n.lineno, "end": n.end_lineno, "doc": ""})
    return tree, items


def py_imports(tree):
    """[(module path parts)] — every import anywhere in the file."""
    mods = []
    for n in ast.walk(tree):
        if isinstance(n, ast.Import):
            for a in n.names:
                mods.append(a.name.split("."))
        elif isinstance(n, ast.ImportFrom) and n.module:
            base = n.module.split(".")
            mods.append(base)
            for a in n.names:            # from core import art  → core/art.py
                mods.append(base + [a.name])
    return mods


# ------------------------------------------------------------------ JS
_JS_DEF = re.compile(r"(?:(?<=[\s;{}(),])|^)(?:async\s+)?function\s+([A-Za-z_$][\w$]*)\s*\(|"
                     r"(?:(?<=[\s;{}])|^)(?:const|let|var)\s+([A-Za-z_$][\w$]*)\s*=\s*(?:async\s*)?(\([^()]*\)|[A-Za-z_$][\w$]*)\s*=>|"
                     r"(?:(?<=[\s;])|^)(?:const|let|var)\s+([A-Z][A-Z0-9_]{1,})\s*=\s*([\[{(])", re.M)


def _match_end(src, i):
    """From an opening bracket at src[i], the index of its partner (skips strings, template literals, comments)."""
    pairs = {"{": "}", "(": ")", "[": "]"}
    stack = [pairs[src[i]]]
    j = i + 1
    n = len(src)
    while j < n and stack:
        c = src[j]
        if c in "\"'":
            q = c
            j += 1
            while j < n and src[j] != q:
                j += 2 if src[j] == "\\" else 1
        elif c == "`":
            j += 1
            depth = 0
            while j < n:
                if src[j] == "\\":
                    j += 2
                    continue
                if src[j] == "`" and depth == 0:
                    break
                if src.startswith("${", j):
                    depth += 1
                    j += 2
                    continue
                if src[j] == "}" and depth:
                    depth -= 1
                j += 1
        elif src.startswith("/*", j):
            j = src.find("*/", j + 2)
            j = n if j < 0 else j + 1
        elif src.startswith("//", j) and (j == 0 or src[j - 1] != ":"):
            j = src.find("\n", j)
            j = n if j < 0 else j
        elif c == "/" and (src[:j].rstrip()[-1:] or "(") in "(,=:[!&|?{};+-*%<>~^":
            # a regular expression /…/ (its brackets do not count)
            j += 1
            cls = False
            while j < n and src[j] != "\n":
                if src[j] == "\\":
                    j += 2
                    continue
                if src[j] == "[":
                    cls = True
                elif src[j] == "]":
                    cls = False
                elif src[j] == "/" and not cls:
                    break
                j += 1
        elif c in pairs:
            stack.append(pairs[c])
        elif stack and c == stack[-1]:
            stack.pop()
            if not stack:
                return j
        j += 1
    return j


def js_items(src):
    items, seen = [], set()
    line_at = lambda pos: src.count("\n", 0, pos) + 1   # noqa: E731
    for m in _JS_DEF.finditer(src):
        name = m.group(1) or m.group(2) or m.group(4)
        if not name or name in seen:
            continue
        seen.add(name)
        kind = "data" if m.group(4) else "func"
        # where its body starts: the first «{» after the arrow / the parameters (or the bracket of the data)
        if kind == "data":
            b = m.end() - 1
        else:
            k = src.find("=>", m.end() - 2) if m.group(2) else src.find(")", m.end() - 1)
            b = k
            while b < len(src) and src[b] not in "{\n;":
                b += 1
        end_pos = _match_end(src, b) if b < len(src) and src[b] in "{([" else src.find("\n", m.start())
        items.append({"key": name, "kind": kind, "start": line_at(m.start()), "end": max(line_at(m.start()), line_at(max(end_pos, m.start()))), "doc": ""})
    items.sort(key=lambda x: (x["start"], x["key"]))
    return items


# ------------------------------------------------------------------ Markdown: the headings are the «items»
def md_items(src):
    items = []
    lines = src.split("\n")
    heads = [(i + 1, l) for i, l in enumerate(lines) if re.match(r"#{1,3} ", l)]
    for k, (ln, l) in enumerate(heads):
        end = heads[k + 1][0] - 1 if k + 1 < len(heads) else len(lines)
        items.append({"key": l.lstrip("#").strip()[:80], "kind": "section", "start": ln, "end": end, "doc": ""})
    return items[:120]


def scan():
    files = all_files()
    info = {}
    py_by_mod = {}
    for p in files:
        if p.endswith(".py"):
            py_by_mod.setdefault(os.path.splitext(os.path.basename(p))[0], []).append(p)
    for p in files:
        full = os.path.join(ROOT, p)
        lang = lang_of(p)
        try:
            src = open(full, encoding="utf-8").read()
        except UnicodeDecodeError:
            src = ""
        rec = {"path": p, "lang": lang, "lines": src.count("\n") + (0 if src.endswith("\n") or not src else 1), "bytes": len(src.encode("utf-8")),
               "items": [], "uses": [], "generated": GENERATED.get(p)}
        if lang == "python":
            try:
                tree, rec["items"] = py_items(src)
                uses = []
                for parts in py_imports(tree):
                    cands = py_by_mod.get(parts[-1], [])
                    if parts[0] in ("core", "api") and len(parts) >= 2:
                        cands = [c for c in cands if c.startswith("05_explanation_api/" + parts[0] + "/")]
                    if len(cands) > 1:   # the same module name in two places: the one next to this file wins
                        near = [c for c in cands if os.path.dirname(c).split("/")[0] == p.split("/")[0]]
                        cands = near or cands[:1]
                    for c in cands[:1]:
                        if c != p and c not in uses and "local_stub_only_for_sandbox" not in c:
                            uses.append(c)
                rec["uses"] = uses
            except SyntaxError:
                pass
        elif lang == "js":
            rec["items"] = js_items(src)
        elif lang == "md":
            rec["items"] = md_items(src)
        rec["uses"] = rec["uses"] + [x for x in EXTRA_LINKS.get(p, []) if x in files and x not in rec["uses"]]
        rec["_src"] = src
        info[p] = rec
    # JS: a page file USES another one when it calls a function defined there (they all live in one page)
    js = [p for p in files if info[p]["lang"] == "js" and p.startswith(_SRC)]
    defs = {}
    for p in js:
        for it in info[p]["items"]:
            if len(it["key"]) >= 4 and it["key"] not in JS_STOP:
                defs.setdefault(it["key"], p)
    for p in js:
        body = info[p]["_src"]
        mine = {it["key"] for it in info[p]["items"]}
        for name, owner in defs.items():
            if owner != p and name not in mine and owner not in info[p]["uses"] and re.search(r"(?<![\w$.])" + re.escape(name) + r"\s*\(", body):
                info[p]["uses"].append(owner)
    # tests that open the built page use it
    for p in files:
        if "/tests_browser/" in p and p.endswith(".py") and "explain.html" in info[p]["_src"] and "02_question_factory/player/explain.html" not in info[p]["uses"]:
            info[p]["uses"].append("02_question_factory/player/explain.html")
    for p in files:
        info[p]["used_by"] = sorted(q for q in files if p in info[q]["uses"])
    return files, info


if __name__ == "__main__":
    files, info = scan()
    os.makedirs(os.path.join(HERE, "notes"), exist_ok=True)
    out = {p: {k: v for k, v in info[p].items() if k != "_src"} for p in files}
    with open(os.path.join(HERE, "notes", "_structure.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    n_items = sum(len(info[p]["items"]) for p in files)
    print(f"{len(files)} files · {n_items} items · {sum(len(info[p]['uses']) for p in files)} links")
    for p in files:
        r = info[p]
        print(f"  {r['lang']:6} {len(r['items']):3} items  uses {len(r['uses']):2}  used by {len(r['used_by']):2}  {p}")
