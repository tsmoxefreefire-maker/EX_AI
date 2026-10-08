"""Refresh the full-code blocks of EXPLANATION_API_AR.md from the files themselves, so the doc always shows the code as it is now.
Every section «## `path`» that has a code block gets that file's current code (paths: 05_explanation_api/… or 02_question_factory/…).
Run:  python scripts/refresh_doc.py"""
import os
import re

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))          # 05_explanation_api/
ROOT = os.path.dirname(HERE)
DOC = os.path.join(HERE, "EXPLANATION_API_AR.md")


def file_of(rel: str):
    p = os.path.join(ROOT, rel) if rel.startswith("02_question_factory/") or rel.startswith("03_explain_player_src/") else os.path.join(HERE, rel)
    return p if os.path.isfile(p) else None


if __name__ == "__main__":
    s = open(DOC, encoding="utf-8").read()
    parts = re.split(r"(?m)^(## `[^`]+`.*)$", s)
    done, out = [], [parts[0]]
    for i in range(1, len(parts), 2):
        head, body = parts[i], parts[i + 1]
        rel = re.match(r"## `([^`]+)`", head).group(1)
        path = file_of(rel)
        m = re.search(r"```(\w+)\n", body)
        if path and m:
            j = body.index("\n```\n", m.end()) if "\n```\n" in body[m.end():] else None
            if j is not None:
                code = open(path, encoding="utf-8").read().rstrip()
                body = body[:m.end()] + code + body[j:]
                done.append(rel)
        out += [head, body]
    open(DOC, "w", encoding="utf-8").write("".join(out))
    print(f"refreshed {len(done)} code blocks: " + ", ".join(done))
