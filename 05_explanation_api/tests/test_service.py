"""The service (pure Python): graph → explanations → books / lessons / concepts / pictures."""
import json
import os
import shutil
import tempfile
import unittest

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAMPLES = os.path.join(os.path.dirname(HERE), "02_question_factory")          # the sample books live in the factory (no copies here)
os.environ.setdefault("EXPLAIN_SEED", "0")                                   # tests make their own books
TMP = tempfile.mkdtemp()
os.environ["EXPLAIN_DATA_DIR"] = TMP                      # never touch the real data while testing
import sys  # noqa: E402
sys.path.insert(0, HERE)
from core import contract, service  # noqa: E402

GRAPHS = SAMPLES


class TestService(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.plants = service.generate(graph_path=os.path.join(GRAPHS, "plants_book_graph.json"))
        with open(os.path.join(GRAPHS, "math_book_graph.json"), encoding="utf-8") as f:
            cls.math = service.generate(graph=json.load(f))

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(TMP, ignore_errors=True)

    def test_generate_every_lesson(self):
        self.assertEqual(len(self.plants["lessons"]), 3); self.assertGreater(self.plants["scenes"], 50)
        self.assertEqual(len(self.math["lessons"]), 4)

    def test_books_and_lessons(self):
        self.assertEqual({b["book_id"] for b in service.list_books()}, {self.plants["book_id"], self.math["book_id"]})
        self.assertEqual(len(service.list_lessons(self.math["book_id"])), 4)

    def test_lesson_has_scenes_texts_and_picture_urls(self):
        l = service.get_lesson("l_parts")
        self.assertEqual(l["overview"]["kind"], "overview"); self.assertTrue(l["concepts"])
        self.assertTrue(all(u.startswith("/art/") and u.endswith(".svg") for u in l["art"].values()))
        self.assertEqual(set(l["art"]), set(l["icons"]))

    def test_every_scene_kind_is_in_the_contract(self):
        kinds = set()
        for b in service.list_books():
            for x in service.list_lessons(b["book_id"]):
                l = service.get_lesson(x["lesson_id"], b["book_id"])
                for s in [l["overview"], l.get("world"), l.get("assemble")] + [s for c in l["concepts"] for s in c["scenes"]]:
                    if s: kinds.add(s["kind"])
        self.assertEqual(kinds - set(contract.SCENE_KINDS), set(), "a scene kind the front end does not know")

    def test_concept(self):
        c = service.get_concept("root")
        self.assertEqual(c["lesson_id"], "l_parts"); self.assertTrue(c["scenes"]); self.assertTrue(c["art"].startswith("/art/"))

    def test_every_picture_of_every_lesson_exists(self):
        import urllib.parse
        for b in service.list_books():
            for x in service.list_lessons(b["book_id"]):
                for u in service.get_lesson(x["lesson_id"], b["book_id"])["art"].values():
                    key = urllib.parse.unquote(u[len("/art/"):-len(".svg")])
                    self.assertTrue(service.get_art(key).startswith("<svg"), key)

    def test_subject_fallback_picture_has_the_name(self):
        self.assertIn("أهرامات", service.get_art("subj:📜:أهرامات"))

    def test_errors(self):
        with self.assertRaises(service.BadInput): service.generate()
        with self.assertRaises(service.BadInput): service.generate(graph={"nodes": []})
        with self.assertRaises(service.NotFound): service.generate(graph_path="nope.json")
        with self.assertRaises(service.NotFound): service.get_lesson("nope")
        with self.assertRaises(service.NotFound): service.get_art("not-a-picture")

    def test_model_is_optional_and_checked(self):
        import explain_llm  # the writer: a fake model that rewrites every paragraph
        fake = lambda system, user: json.dumps({k: "ببساطة: " + v for k, v in json.loads(user).items()}, ensure_ascii=False)
        r = service.generate(graph_path=os.path.join(GRAPHS, "history_book_graph.json"), llm=fake)
        self.assertEqual(r["llm"], "custom")
        l = service.get_lesson(r["lessons"][0]["lesson_id"], r["book_id"])
        self.assertTrue(l["overview"]["paragraph"].startswith("ببساطة"))


class TestNewSubjectAndPage(unittest.TestCase):
    """🆕 batch 27: ANY graph → the whole interactive page from the server; a NEW subject gets its own sound and characters."""
    COMPUTER = os.path.join(SAMPLES, "examples", "new_subject_computer_g7.json")

    @classmethod
    def setUpClass(cls):
        from core import settings
        cls.settings = settings
        cls.keep = (settings.DATA_DIR, settings.GRAPHS_DIR, settings.BOOKS_DIR)     # its OWN data folder
        cls.tmp = tempfile.mkdtemp()
        settings.DATA_DIR, settings.GRAPHS_DIR, settings.BOOKS_DIR = cls.tmp, os.path.join(cls.tmp, "graphs"), os.path.join(cls.tmp, "books")
        with open(cls.COMPUTER, encoding="utf-8") as f:
            cls.cs = service.generate(graph=json.load(f))

    @classmethod
    def tearDownClass(cls):
        cls.settings.DATA_DIR, cls.settings.GRAPHS_DIR, cls.settings.BOOKS_DIR = cls.keep
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_a_new_subject_gets_its_own_identity(self):
        idn = self.cs["identity"]
        self.assertTrue(idn["new"]); self.assertEqual(idn["family"], "computer"); self.assertEqual(idn["emblem"], "💻")
        self.assertEqual(idn["sound"], {"instr": "chip", "root": 64, "scale": "major"}); self.assertEqual(idn["mascot_name"], "بِتّو")
        self.assertEqual(self.cs["stage"], "junior"); self.assertEqual(self.cs["page_url"], "/explain/cs_g7")
        self.assertGreater(self.cs["scenes"], 40); self.assertEqual(self.cs["warnings"], [])

    def test_its_characters_are_its_own_with_whole_names(self):
        """Batch 29: the computer concepts now get Lego drawings by their words (memory → drawers, processor → chip…);
        a computer concept with no part word still gets the computer character with its WHOLE name."""
        l = service.get_lesson("l_parts", "cs_g7")
        self.assertTrue(all(i.startswith(("lego:", "subj:💻:")) for i in l["icons"].values()), l["icons"])
        self.assertTrue(l["icons"]["cpu"].startswith("lego:chip:")); self.assertTrue(l["icons"]["memory"].startswith("lego:drawers:"))
        self.assertIn("<svg", service.get_art(l["icons"]["cpu"]))
        svg = service.get_art("subj:💻:وحدة المعالجة المركزية")
        self.assertIn(">وحدة المعالجة<", svg); self.assertIn(">المركزية<", svg)   # the whole name, on 2 lines

    def test_every_activity_kind_is_made_for_the_new_subject(self):
        kinds = set()
        for x in service.list_lessons("cs_g7"):
            for c in service.get_lesson(x["lesson_id"], "cs_g7")["concepts"]:
                kinds |= {s["kind"] for s in c["scenes"]}
        self.assertTrue({"meet", "connect", "compare", "teach", "ladder"} & kinds, kinds)
        self.assertGreaterEqual(len(kinds), 8, kinds)

    def test_the_page_of_one_book_and_of_all_books(self):
        one = service.page_html(["cs_g7"])
        self.assertIn('"emblem": "💻"', one); self.assertIn('"instr": "chip"', one); self.assertIn("الحاسوب · الصف السابع", one)
        data = service.page_data()
        self.assertEqual([g["title"] for g in data["graphs"]], ["الحاسوب · الصف السابع"])
        with self.assertRaises(service.NotFound):
            service.page_html(["not_a_book"])

    def test_the_server_page_of_the_12_samples_is_the_published_page(self):
        """The API's /explain for the 12 sample books is byte-for-byte the page we publish (same factory, same builder)."""
        built = os.path.join(SAMPLES, "player", "explain.html")
        service.seed_samples()
        service.delete_book("cs_g7")
        with open(built, encoding="utf-8") as f:
            self.assertEqual(service.page_html(), f.read())
        self.assertEqual(len(service.list_books()), 12)
        with open(self.COMPUTER, encoding="utf-8") as f:
            service.generate(graph=json.load(f))                           # put it back for the other tests
        grades = [b["grade"] for b in service.list_books()]
        self.assertEqual(grades, sorted(grades))                            # grade 4 → 12, the new grade-7 book in its place

    def test_delete_and_bad_ids(self):
        with self.assertRaises(service.NotFound):
            service.delete_book("nope")
        bad = {"book": {"id": "../evil", "title": "x", "grade": 5}, "nodes": [{"id": "../evil", "level": "book"}]}
        with self.assertRaises(service.BadInput):
            service.generate(graph=bad)
        with self.assertRaises(service.BadInput):                         # a graph with no lesson says so
            service.generate(graph={"book": {"id": "empty_b", "title": "x", "grade": 5}, "nodes": [{"id": "empty_b", "level": "book"}]})

    def test_drawings_carry_their_own_face_rules(self):
        """🐞 an <img> cannot see the page's CSS: the face showed 5 mouths. Every SVG now carries its face rules, per age stage."""
        kids, senior = service.get_art("🐝", "kids"), service.get_art("🐝", "senior")
        self.assertIn(".m-happy{display:inline}", kids); self.assertNotIn(".sface{display:none", kids)
        self.assertIn(".sface{display:none!important}", senior)


if __name__ == "__main__":
    unittest.main()
