"""Checks one notes file:  python code_tour/notes/_check.py code_tour/notes/<group>.py  file1 file2 ...
(the files = the project paths this group must cover). Prints what is missing or wrong; exit code 0 = all good."""
import importlib.util
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
S = json.load(open(os.path.join(HERE, "_structure.json"), encoding="utf-8"))
NEED = ("title", "one", "role", "how")
ALLOWED = {"title", "one", "role", "how", "ideas", "tip", "items"}


def main():
    path, files = sys.argv[1], sys.argv[2:]
    spec = importlib.util.spec_from_file_location("notes_mod", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    F = mod.FILES
    probs = []
    for p in files:
        if p not in S:
            probs.append(f"not a project file: {p}")
            continue
        if p not in F:
            probs.append(f"MISSING file card: {p}")
            continue
        c = F[p]
        for k in NEED:
            if not c.get(k):
                probs.append(f"{p}: missing «{k}»")
        for k in c:
            if k not in ALLOWED:
                probs.append(f"{p}: unknown field «{k}»")
        if not isinstance(c.get("how", []), list) or not (2 <= len(c.get("how", [])) <= 9):
            probs.append(f"{p}: «how» must be a list of 2–9 steps")
        for pair in c.get("ideas", []):
            if not (isinstance(pair, (list, tuple)) and len(pair) == 2):
                probs.append(f"{p}: every idea must be [word, meaning]")
        want = [i["key"] for i in S[p]["items"] if i["kind"] != "section"]
        have = c.get("items", {})
        miss = [k for k in want if not (have.get(k) or "").strip()]
        extra = [k for k in have if k not in want]
        if miss:
            probs.append(f"{p}: {len(miss)} items without explanation: {miss[:12]}")
        if extra:
            probs.append(f"{p}: unknown item keys (check spelling): {extra[:12]}")
    for p in F:
        if p not in files:
            probs.append(f"card for a file outside this group: {p}")
    print("\n".join(probs) if probs else f"OK · {len(files)} files · {sum(len(F[p].get('items', {})) for p in files if p in F)} items")
    sys.exit(1 if probs else 0)


if __name__ == "__main__":
    main()
