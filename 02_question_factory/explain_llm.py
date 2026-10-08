"""The LLM as a WRITER for the explanation: it rewrites each scene's paragraph (and short step lines)
in clear, warm Arabic for children — same facts, same concept names. Every text is checked; anything that fails keeps its original."""
import json
import re

NAME = re.compile(r"«([^»]+)»")
SYSTEM = """You are a children's teacher writing short explanations in clear, simple Arabic (easy Modern Standard, friendly).
For each text: explain the same idea more clearly for a 9-year-old, in 2-4 short sentences. You may add ONE everyday comparison
(like "زي المرساة") if it fits. Rules:
1. Same facts only. Never add a new fact, number or concept.
2. Keep every name written inside «…» exactly as it is, inside «…». Do not add new «…» names.
3. A text that says X needs Y must still say X needs Y (do not reverse it).
Return ONLY one JSON object with exactly the same keys, each value a string."""


def acceptable(old: str, new) -> bool:
    if not isinstance(new, str) or not new.strip() or len(new) > len(old) * 2.5 + 80:
        return False
    return set(NAME.findall(old)) == set(NAME.findall(new))


def polish_lesson(rec: dict, llm_generate) -> dict:
    texts, where = {}, []
    scenes = [rec["overview"]] + [s for c in rec["concepts"] for s in c["scenes"]]
    for s in scenes:
        if s.get("paragraph"):
            k = f"p{len(texts) + 1}"; texts[k] = s["paragraph"]; where.append((s, k))
    if not texts:
        return rec
    try:
        reply = llm_generate(SYSTEM, json.dumps(texts, ensure_ascii=False))
        a, b = reply.find("{"), reply.rfind("}")
        if a < 0 or b <= a:
            raise ValueError("no JSON object")
        new = json.loads(reply[a:b + 1])
    except Exception as e:
        rec.setdefault("warnings", []).append(f"llm writer failed, kept the original texts: {e}")
        return rec
    kept = 0
    for s, k in where:
        if acceptable(texts[k], new.get(k)):
            s["paragraph_plain"] = s["paragraph"]; s["paragraph"] = new[k].strip(); kept += 1
    rec["llm"] = {"paragraphs": len(texts), "rewritten": kept}
    rec["generator"] = "explain+llm-writer"
    return rec
