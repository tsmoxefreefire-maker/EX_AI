"""The HTTP API (FastAPI). Runs with the real FastAPI: pip install -r requirements.txt"""
import json
import os
import shutil
import tempfile
import unittest

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAMPLES = os.path.join(os.path.dirname(HERE), "02_question_factory")          # the sample books live in the factory (no copies here)
os.environ.setdefault("EXPLAIN_SEED", "0")                                   # tests make their own books
TMP = tempfile.mkdtemp()
os.environ["EXPLAIN_DATA_DIR"] = TMP
import sys  # noqa: E402
sys.path.insert(0, HERE)
try:
    from fastapi.testclient import TestClient
    from main import app
    HAVE = True
except ImportError:                                       # FastAPI not installed → these tests are skipped (the service tests still run)
    HAVE = False


@unittest.skipUnless(HAVE, "pip install -r requirements.txt")
class TestAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.c = TestClient(app)
        with open(os.path.join(SAMPLES, "math_book_graph.json"), encoding="utf-8") as f:
            cls.g = json.load(f)
        cls.r = cls.c.post("/explanations/generate", json={"graph": cls.g})

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(TMP, ignore_errors=True)

    def test_health(self):
        r = self.c.get("/health"); self.assertEqual(r.status_code, 200); self.assertEqual(r.json()["status"], "ok")

    def test_generate(self):
        self.assertEqual(self.r.status_code, 200); body = self.r.json()
        self.assertEqual(len(body["lessons"]), 4); self.assertGreater(body["scenes"], 30)

    def test_generate_bad_requests(self):
        self.assertEqual(self.c.post("/explanations/generate", json={}).status_code, 400)
        self.assertEqual(self.c.post("/explanations/generate", json={"graph_path": "nope.json"}).status_code, 404)

    def test_books_lessons_lesson_concept_picture(self):
        book = self.r.json()["book_id"]
        self.assertIn(book, [b["book_id"] for b in self.c.get("/books").json()])
        lessons = self.c.get(f"/books/{book}/lessons").json(); self.assertEqual(len(lessons), 4)
        lid = lessons[0]["lesson_id"]
        l = self.c.get(f"/lessons/{lid}/explanation", params={"book_id": book}).json()
        self.assertEqual(l["lesson_id"], lid); self.assertTrue(l["concepts"])
        cid = l["concepts"][0]["concept_id"]
        c = self.c.get(f"/concepts/{cid}/explanation").json(); self.assertEqual(c["concept_id"], cid)
        pic = self.c.get(l["art"][cid]); self.assertEqual(pic.status_code, 200)
        self.assertIn("svg", pic.headers.get("content-type", "")); self.assertTrue(pic.text.startswith("<svg"))

    def test_not_found(self):
        self.assertEqual(self.c.get("/lessons/nope/explanation").status_code, 404)
        self.assertEqual(self.c.get("/books/nope/lessons").status_code, 404)
        self.assertEqual(self.c.get("/art/nope.svg").status_code, 404)

    def test_home_page(self):
        r = self.c.get("/"); self.assertEqual(r.status_code, 200)
        self.assertIn("text/html", r.headers.get("content-type", "")); self.assertIn("سيرفر الشرح التفاعلي", r.text)

    def test_the_interactive_page_from_the_server(self):
        book = self.r.json()["book_id"]
        r = self.c.get(f"/explain/{book}"); self.assertEqual(r.status_code, 200)
        self.assertIn("text/html", r.headers.get("content-type", "")); self.assertIn("const DATA = ", r.text)
        self.assertEqual(self.c.get("/explain").status_code, 200)
        self.assertEqual(self.c.get("/explain/nope").status_code, 404)
        d = self.c.get("/explain-data", params={"books": book}).json(); self.assertEqual(len(d["graphs"]), 1)
        self.assertEqual(self.r.json()["page_url"], f"/explain/{book}")

    def test_a_new_subject_through_the_api(self):
        with open(os.path.join(SAMPLES, "examples", "new_subject_computer_g7.json"), encoding="utf-8") as f:
            r = self.c.post("/explanations/generate", json={"graph": json.load(f)}).json()
        self.assertEqual(r["identity"]["family"], "computer"); self.assertEqual(r["identity"]["sound"]["instr"], "chip")
        self.assertIn('"instr": "chip"', self.c.get(r["page_url"]).text)
        b = [x for x in self.c.get("/books").json() if x["book_id"] == r["book_id"]][0]
        self.assertTrue(b["identity"]["new"])
        self.assertEqual(self.c.delete(f"/books/{r['book_id']}").status_code, 200)
        self.assertEqual(self.c.get(r["page_url"]).status_code, 404)

    def test_picture_per_age_stage(self):
        r = self.c.get("/art/%F0%9F%90%9D.svg", params={"stage": "senior"}); self.assertEqual(r.status_code, 200)
        self.assertIn(".sface{display:none!important}", r.text)

    def test_contract(self):
        k = self.c.get("/scene-kinds").json(); self.assertIn("meet", k["scene_kinds"]); self.assertIn("relation", k)


if __name__ == "__main__":
    unittest.main()
