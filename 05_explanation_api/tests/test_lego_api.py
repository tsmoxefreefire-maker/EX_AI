"""🧱 Lego drawings through the server (batch 29): a NEW subject whose concepts have no drawing and no part word →
ONE model call picks parts → saved in the library → the page and /art draw them → the teacher picks another or says no."""
import copy
import json
import os
import re
import tempfile
import unittest

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("EXPLAIN_SEED", "0")
os.environ.setdefault("EXPLAIN_DATA_DIR", tempfile.mkdtemp())
import sys  # noqa: E402
sys.path.insert(0, HERE)
from core import art, service  # noqa: E402
import lego  # noqa: E402
import offline_generator as og  # noqa: E402

COMPUTER = os.path.join(os.path.dirname(HERE), "02_question_factory", "examples", "new_subject_computer_g7.json")
COOKING = ["التتبيلة", "العجين", "التخمير", "الشوي", "السلطة", "الحساء", "الحلويات", "التوابل", "المقبلات"]
try:
    from fastapi.testclient import TestClient
    from main import app
    HAVE = True
except ImportError:
    HAVE = False


def cooking_graph():
    """The computer book with cooking concepts instead (words none of our drawings or parts know)."""
    g = copy.deepcopy(json.load(open(COMPUTER, encoding="utf-8")))
    g["book"].update({"id": "cook_g7", "title": "الطبخ · الصف السابع", "subject": "الطبخ"})
    ents = [n for n in g["nodes"] if n.get("level") == "entity"]
    for n, t in zip(ents, COOKING):
        n["title"] = t
    return g


class Model:
    """A fake model: answers the Lego question (reads the names from the prompt); anything else gets nothing useful."""
    def __init__(self):
        self.lego_calls = 0

    def __call__(self, system, user):
        if "BUILD each picture" not in user:
            return ""
        self.lego_calls += 1
        names = re.findall(r"^  (.+?) — ", user, re.M)
        return json.dumps({"items": [{"name": n, "metaphor": "طنجرة", "options": [{"main": "pot", "extras": ["spark"]}, {"main": "bag"}]}
                                     for n in names]}, ensure_ascii=False)


class TestLegoServer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.model = Model()
        cls.before = [og.icon_for(t, "", "الطبخ") for t in COOKING]
        cls.meta = service.generate(graph=cooking_graph(), llm=cls.model)

    @classmethod
    def tearDownClass(cls):
        service.delete_book("cook_g7")                                          # the other test files share the data folder

    def test_1_one_call_and_every_concept_is_built(self):
        self.assertTrue(all(k.startswith("subj:") for k in self.before))         # before: only the subject character
        self.assertEqual(self.model.lego_calls, 1)                                # ONE call for the whole book
        self.assertEqual(self.meta["lego"], {"library": 0, "built": 9, "subject_character": 0})
        icons = {k: v for l in service.page_data(["cook_g7"])["graphs"][0]["lessons"] for k, v in l["icons"].items()}
        self.assertTrue(icons and all(v.startswith("lego:pot:spark:") for v in icons.values()), icons)

    def test_2_the_server_draws_them(self):
        key = og.icon_for("العجين", "", "الطبخ")
        svg = service.get_art(key, "kids")
        self.assertTrue(svg.startswith("<svg") and "{{" not in svg and "<style>" in svg)
        self.assertIn('translate(16 14)', svg)                                    # the badge (spark) in its place
        self.assertIsNone(art.art_svg("lego:pizza::1:bob"))

    def test_3_library_grows_and_lists_suggestions(self):
        lib = {e["name"]: e for e in service.lego_library()}
        self.assertTrue(set(COOKING) <= set(lib))
        e = lib["العجين"]
        self.assertEqual(e["status"], "auto"); self.assertEqual(len(e["suggestion_art"]), 2); self.assertTrue(e["art"].startswith("/art/lego"))
        self.assertIn("pot", service.lego_parts()["main"])

    def test_4_teacher_picks_another_and_the_page_changes(self):
        r = service.lego_choose("العجين", pick=1)
        self.assertTrue(r["new"].startswith("lego:bag:")); self.assertTrue(r["updated_lessons"])
        icons = {k: v for l in service.page_data(["cook_g7"])["graphs"][0]["lessons"] for k, v in l["icons"].items()}
        self.assertIn(r["new"], icons.values())

    def test_5_teacher_says_no(self):
        r = service.lego_choose("الشوي", reject=True)
        self.assertIsNone(r["new"])
        icons = {k: v for l in service.page_data(["cook_g7"])["graphs"][0]["lessons"] for k, v in l["icons"].items()}
        self.assertIn("subj:", " ".join(icons.values()))
        with self.assertRaises(service.NotFound):
            service.lego_choose("ما في هيك مفهوم", pick=0)
        with self.assertRaises(service.BadInput):
            service.lego_choose("العجين", pick=9)

    @unittest.skipUnless(HAVE, "pip install -r requirements.txt")
    def test_6_http(self):
        c = TestClient(app)
        self.assertIn("drawers", c.get("/lego/parts").json()["main"])
        self.assertTrue(any(e["name"] == "التتبيلة" for e in c.get("/lego/drawings").json()))
        r = c.get("/art/" + "lego%3Achip%3Abinary%3A2%3Abuzz" + ".svg")
        self.assertEqual(r.status_code, 200); self.assertIn("<svg", r.text)
        self.assertEqual(c.post("/lego/drawings/choose", json={"name": "التتبيلة", "pick": 1}).status_code, 200)
        self.assertEqual(c.post("/lego/drawings/choose", json={"name": "غلط", "pick": 0}).status_code, 404)


if __name__ == "__main__":
    unittest.main()
