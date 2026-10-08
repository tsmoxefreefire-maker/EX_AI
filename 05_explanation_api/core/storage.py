"""Reading what the factory saved: books, lessons, concepts (JSON files on disk). No logic about HOW to explain — only WHERE things are."""
import json
import os
import shutil

from core import settings


def _read(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def book_dir(book_id: str) -> str:
    return os.path.join(settings.BOOKS_DIR, book_id)


def save_meta(book_id: str, meta: dict) -> None:
    os.makedirs(book_dir(book_id), exist_ok=True)
    with open(os.path.join(book_dir(book_id), "meta.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)


def list_books() -> list:
    if not os.path.isdir(settings.BOOKS_DIR):
        return []
    out = []
    for b in sorted(os.listdir(settings.BOOKS_DIR)):
        p = os.path.join(settings.BOOKS_DIR, b, "meta.json")
        if os.path.exists(p):
            out.append(_read(p))
    return out


def book_meta(book_id: str):
    p = os.path.join(book_dir(book_id), "meta.json")
    return _read(p) if os.path.exists(p) else None


def lesson_ids(book_id: str) -> list:
    p = os.path.join(book_dir(book_id), "explain_index.json")
    return _read(p)["lessons"] if os.path.exists(p) else []


def load_lesson(book_id: str, lesson_id: str):
    p = os.path.join(book_dir(book_id), "lessons", lesson_id, "explanations.json")
    return _read(p) if os.path.exists(p) else None


def save_lesson(book_id: str, lesson_id: str, rec: dict) -> None:
    """Write a lesson back (used when a teacher picks another Lego drawing: only its picture keys change)."""
    p = os.path.join(book_dir(book_id), "lessons", lesson_id, "explanations.json")
    with open(p, "w", encoding="utf-8") as f:
        json.dump(rec, f, ensure_ascii=False, indent=2)


def find_lesson(lesson_id: str, book_id: str = None):
    """The lesson in a given book, or in any book (lesson ids are unique inside the platform's graph)."""
    books = [book_id] if book_id else [m["book_id"] for m in list_books()]
    for b in books:
        rec = load_lesson(b, lesson_id)
        if rec is not None:
            return b, rec
    return None, None


def delete_book(book_id: str) -> None:
    """Remove a book's explanations (its folder)."""
    shutil.rmtree(book_dir(book_id), ignore_errors=True)
