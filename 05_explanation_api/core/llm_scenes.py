"""🤖 Scenes WRITTEN BY THE MODEL (with our template's toolkit) — generate, check, keep, review, run in a sandbox.

The factory's own scenes never change; a model scene is an EXTRA, and a student sees it only after a teacher approves it.
  generate(book_id, lesson_id, concept_id=None, idea=None, max_scenes=1, force=False, llm=None)
      → for each concept: scene_writer.write_scene (model + checks + one repair round) → saved as data/llm_scenes/<book>/<scene_id>.json
  list_scenes / get_scene / review (approve | reject) / report (what the browser saw: drew? inside? errors?)
  runner(scene_id) → the sandbox HTML (CSP: no network) for <iframe sandbox="allow-scripts">
  approved_for_lesson(book, lesson) → the approved scenes as {"kind": "custom", ...} for /lessons/{id}/explanation?include_llm=true
Cost guard: max_scenes ≤ 10 per call, and an existing scene for the same concept + idea is returned instead of asking again (unless force)."""
import datetime
import hashlib
import json
import os
import sys

from core import art, settings, storage

sys.path.insert(0, settings.ENGINE_DIR)          # the factory + the scene writer (engine/) are plain Python modules
import llm_gateway  # noqa: E402
import scene_writer  # noqa: E402
from graph_reader import Graph  # noqa: E402

STATUSES = ("pending_review", "approved", "rejected")


class NotFound(Exception):
    pass


class BadInput(Exception):
    pass


def _dir(book_id: str) -> str:
    return os.path.join(settings.DATA_DIR, "llm_scenes", book_id)


def _now() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")


def _save(rec: dict) -> None:
    os.makedirs(_dir(rec["book_id"]), exist_ok=True)
    with open(os.path.join(_dir(rec["book_id"]), rec["scene_id"] + ".json"), "w", encoding="utf-8") as f:
        json.dump(rec, f, ensure_ascii=False, indent=1)


def _all(book_id: str = None) -> list:
    root = os.path.join(settings.DATA_DIR, "llm_scenes")
    books = [book_id] if book_id else (sorted(os.listdir(root)) if os.path.isdir(root) else [])
    out = []
    for b in books:
        d = _dir(b)
        if os.path.isdir(d):
            for name in sorted(os.listdir(d)):
                if name.endswith(".json"):
                    with open(os.path.join(d, name), encoding="utf-8") as f:
                        out.append(json.load(f))
    return out


def _graph(book_id: str):
    path = os.path.join(settings.GRAPHS_DIR, f"{book_id}.json")
    if not os.path.exists(path):                                 # graphs sent by name keep their file name: look them up by book id
        for name in (os.listdir(settings.GRAPHS_DIR) if os.path.isdir(settings.GRAPHS_DIR) else []):
            p = os.path.join(settings.GRAPHS_DIR, name)
            try:
                with open(p, encoding="utf-8") as f:
                    if (json.load(f).get("book") or {}).get("id") == book_id:
                        path = p
                        break
            except (OSError, ValueError):
                continue
    if not os.path.exists(path):
        raise NotFound(f"ما في جراف للكتاب {book_id} (اعمل /explanations/generate أول)")
    return Graph.load(path)


def _scene_id(book_id, lesson_id, cid, idea) -> str:
    h = hashlib.sha1(f"{book_id}|{lesson_id}|{cid}|{idea or ''}|{scene_writer.PROMPT_VERSION}".encode("utf-8")).hexdigest()[:10]
    return f"{cid}-{h}"


def generate(book_id: str, lesson_id: str, concept_id: str = None, idea: str = None, max_scenes: int = 1, force: bool = False, llm=None) -> dict:
    """Ask the model for new scenes (one per concept, at most max_scenes). Nothing is shown to students until approved."""
    if not (1 <= int(max_scenes) <= 10):
        raise BadInput("max_scenes لازم بين 1 و 10 (حد للتكلفة)")
    g = _graph(book_id)
    lesson = next((l for l in g.lessons() if l.id == lesson_id), None)
    if lesson is None:
        raise NotFound(f"ما في درس {lesson_id} بالكتاب {book_id}")
    ids = [c.id for c in lesson.concepts]
    if concept_id:
        if concept_id not in ids:
            raise NotFound(f"المفهوم {concept_id} مش بالدرس {lesson_id}")
        ids = [concept_id]
    warnings = []
    if llm is None:
        if not llm_gateway.api_key_from_anywhere():
            raise BadInput("ما في مفتاح موديل على السيرفر (api_key.txt أو GEMINI_API_KEY / OPENAI_API_KEY / ANTHROPIC_API_KEY)")
        llm = llm_gateway.generate
    out = []
    for cid in ids[:int(max_scenes)]:
        sid = _scene_id(book_id, lesson_id, cid, idea)
        old = next((r for r in _all(book_id) if r["scene_id"] == sid), None)
        if old and not force:                                    # already asked: no new cost
            out.append(_summary(old, reused=True))
            continue
        data = scene_writer.scene_data(g, lesson, cid, art_svg=art.art_svg)
        res = scene_writer.write_scene(data, llm, idea=idea)
        rec = {"scene_id": sid, "book_id": book_id, "lesson_id": lesson_id, "concept_id": cid, "concept": data["concept"]["name"],
               "idea": idea, "stage": data["stage"], "status": "pending_review" if res["ok"] else "rejected",
               "problems": res["problems"], "attempts": res["attempts"], "code": res["code"], "data": data,
               "provider": (llm_gateway.LAST_PROVIDER if llm is llm_gateway.generate else "custom"),
               "prompt_version": scene_writer.PROMPT_VERSION, "created_at": _now(), "review": None, "browser_check": None}
        _save(rec)
        out.append(_summary(rec))
        if not res["ok"]:
            warnings.append(f"«{data['concept']['name']}»: الكود انرفض ({'; '.join(res['problems'][:3])}) — المشهد العادي بيضل")
    return {"book_id": book_id, "lesson_id": lesson_id, "scenes": out, "warnings": warnings}


def _summary(rec: dict, reused: bool = False) -> dict:
    return {"scene_id": rec["scene_id"], "concept_id": rec["concept_id"], "concept": rec.get("concept"), "status": rec["status"],
            "problems": rec.get("problems", []), "attempts": rec.get("attempts"), "provider": rec.get("provider"), "reused": reused,
            "runner_url": f"/llm/scenes/{rec['scene_id']}/runner.html?book_id={rec['book_id']}"}


def list_scenes(book_id: str = None, lesson_id: str = None, status: str = None) -> list:
    if status and status not in STATUSES:
        raise BadInput(f"status لازم وحدة من {STATUSES}")
    return [_summary(r) for r in _all(book_id) if (not lesson_id or r["lesson_id"] == lesson_id) and (not status or r["status"] == status)]


def get_scene(scene_id: str, book_id: str = None) -> dict:
    rec = next((r for r in _all(book_id) if r["scene_id"] == scene_id), None)
    if rec is None:
        raise NotFound(f"ما في مشهد {scene_id}")
    return rec


def review(scene_id: str, approve: bool, note: str = None, book_id: str = None) -> dict:
    """The teacher's decision. A rejected-by-checks scene can never be approved (its code did not pass)."""
    rec = get_scene(scene_id, book_id)
    if approve and rec.get("problems"):
        raise BadInput("هالمشهد ما نجح بالفحص، فما بينفع ينقبل: " + "; ".join(rec["problems"][:3]))
    rec["status"] = "approved" if approve else "rejected"
    rec["review"] = {"approved": bool(approve), "note": note, "at": _now()}
    _save(rec)
    return _summary(rec)


def report(scene_id: str, result: dict, book_id: str = None) -> dict:
    """What the browser saw when the scene ran (from the teacher's preview): {ok, drawn, outside, errors}."""
    rec = get_scene(scene_id, book_id)
    keep = {k: result.get(k) for k in ("ok", "drawn", "outside", "errors", "done")}
    rec["browser_check"] = dict(keep, at=_now())
    _save(rec)
    return {"scene_id": scene_id, "browser_check": rec["browser_check"]}


def runner(scene_id: str, book_id: str = None) -> str:
    """The sandbox page (put it in <iframe sandbox="allow-scripts">). Pending scenes can be previewed; rejected ones too, to see why."""
    rec = get_scene(scene_id, book_id)
    return scene_writer.runner_html(rec["code"], rec["data"])


def approved_for_lesson(book_id: str, lesson_id: str) -> dict:
    """{concept_id: [custom scene, …]} — only APPROVED scenes, in the shape of the other scenes (+ where to run them)."""
    out = {}
    for r in _all(book_id):
        if r["lesson_id"] == lesson_id and r["status"] == "approved":
            out.setdefault(r["concept_id"], []).append({
                "kind": "custom", "scene_id": r["scene_id"], "target": r["concept_id"], "source": "llm", "provider": r.get("provider"),
                "runner_url": f"/llm/scenes/{r['scene_id']}/runner.html?book_id={book_id}",
                "steps": [f"🤖 مشهد جديد عن «{r['concept']}»"], "paragraph": r["data"]["concept"]["meaning"]})
    return out


def approved_for_page(book_id: str) -> dict:
    """{(lesson_id, concept_id): [scene, …]} — the APPROVED scenes of a book, ready to go INSIDE the page (/explain):
    the sandbox page is carried in the scene itself (runner_html), the same way the page shows its example scene."""
    out = {}
    for r in _all(book_id):
        if r["status"] == "approved":
            out.setdefault((r["lesson_id"], r["concept_id"]), []).append({
                "kind": "custom", "scene_id": r["scene_id"], "target": r["concept_id"], "source": "llm", "label": "🤖 مشهد من الموديل (وافق عليه المعلم)",
                "runner_html": scene_writer.runner_html(r["code"], r["data"]),
                "steps": [f"🤖 مشهد جديد عن «{r['concept']}»"], "paragraph": r["data"]["concept"]["meaning"]})
    return out


def sdk_doc() -> dict:
    """For the front end and the team: what the model may use, the rules it gets, and the version."""
    return {"prompt_version": scene_writer.PROMPT_VERSION, "max_code_chars": scene_writer.MAX_CODE,
            "sdk_reference": scene_writer.SDK_REFERENCE, "stage_rules": scene_writer.STAGE_RULES,
            "forbidden": [label for _, label in scene_writer.FORBIDDEN], "example": scene_writer.EXAMPLE,
            "sandbox": "<iframe sandbox=\"allow-scripts\" src=\"/llm/scenes/{scene_id}/runner.html\"> — CSP: default-src 'none' (no network)",
            "messages": {"llm-scene": "{ok, drawn, outside, errors, done} — POST it to /llm/scenes/{id}/report",
                         "llm-caption": "{text} — the narrator line (show it under the scene)"}}
