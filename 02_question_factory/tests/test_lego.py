"""🧱 Lego drawings (batch 29 · 💡 Hareth's idea): a concept with no drawing gets one BUILT from our parts.
By its words (no AI) · the model only CHOOSES parts (once per concept, checked, saved) · the teacher can pick another or say no."""
import json
import os
import re
import tempfile
import unittest

import lego
import offline_generator as og

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEGO_JS = os.path.join(os.path.dirname(HERE), "03_explain_player_src", "lego.js")
COMPUTER = os.path.join(HERE, "examples", "new_subject_computer_g7.json")


def fake_model(answer_for):
    """A fake model: reads the concept names from the prompt and answers with answer_for(name) → options (counts its calls)."""
    calls = []

    def llm(system, user):
        calls.append(user)
        names = re.findall(r"^  (.+?) — ", user, re.M)
        return "here: " + json.dumps({"items": [{"name": n, "metaphor": "استعارة", "options": answer_for(n)} for n in names]}, ensure_ascii=False)
    llm.calls = calls
    return llm


class TestLego(unittest.TestCase):
    def setUp(self):
        self.store = tempfile.mktemp(suffix=".json")
        lego.set_store(self.store)

    def tearDown(self):
        if os.path.exists(self.store):
            os.remove(self.store)

    def test_parts_are_the_same_in_python_and_in_the_page(self):
        js = open(LEGO_JS, encoding="utf-8").read()
        for m in lego.MAINS:
            self.assertIn(f"\n {m}:{{d:", js, m)
        for x in lego.EXTRAS:
            self.assertIn(f"\n {x}:C=>", js, x)
        self.assertIn("const LEGO_MOTIONS=" + json.dumps(list(lego.MOTIONS)).replace(", ", ","), js)

    def test_key_round_trip_and_bad_keys(self):
        k = lego.make_key("drawers", ["binary", "nope", "spark", "star"], 11, "wobble")
        self.assertEqual(k, "lego:drawers:binary+spark:3:wobble")                 # unknown badge dropped, at most 2, colour % 8
        self.assertEqual(lego.parse(k), {"main": "drawers", "extras": ["binary", "spark"], "color": 3, "motion": "wobble"})
        for bad in ("subj:💻:x", "lego:pizza::1:bob", "lego", "", None):
            self.assertIsNone(lego.parse(bad), bad)
        self.assertEqual(lego.parse("lego:chip::x:fly")["color"], 0); self.assertEqual(lego.parse("lego:chip::x:fly")["motion"], "bob")

    def test_by_words_the_computer_book(self):
        g = json.load(open(COMPUTER, encoding="utf-8"))
        got = {n["title"]: og.icon_for(n["title"], "", g["book"]["subject"]) for n in g["nodes"] if n.get("level") == "entity"}
        want = {"الحاسوب": "screen", "وحدات الإدخال": "keyboard", "وحدة المعالجة المركزية": "chip", "الذاكرة": "drawers",
                "وحدات الإخراج": "screen", "الخوارزمية": "stairs", "البرنامج": "page", "لغة البرمجة": "code", "الخطأ البرمجي": "bug"}
        for name, main in want.items():
            self.assertEqual(lego.parse(got[name])["main"], main, (name, got[name]))
        self.assertIn("arrow", got["وحدات الإخراج"])                             # «إخراج» adds an arrow going out
        self.assertNotEqual(got["الحاسوب"], got["وحدات الإخراج"])                # two screens in one lesson still differ

    def test_name_only_never_the_meaning(self):
        self.assertIsNone(lego.by_words("الفاعل"))                                # its meaning says «اسم»… the name says nothing
        self.assertIsNone(lego.by_words("علم الأحياء"))                          # «علم» is not the flag
        self.assertEqual(lego.parse(lego.by_words("الحماية"))["main"], "lock")       # «ال» in front is fine

    def test_library_books_are_untouched(self):
        for book in ("plants", "math", "arabic_g4", "history", "geo_g5", "phy_g6", "chem_g7", "sci_g8", "math_g9", "phy_g10", "chem_g11", "bio_g12"):
            g = json.load(open(os.path.join(HERE, book + "_book_graph.json"), encoding="utf-8"))
            for n in g["nodes"]:
                if n.get("level") == "entity":
                    self.assertFalse(og.icon_for(n.get("title", ""), "", g["book"]["subject"]).startswith("lego:"), (book, n.get("title")))

    def test_model_chooses_once_checked_and_saved(self):
        llm = fake_model(lambda n: [{"main": "pot", "extras": ["spark"], "motion": "wobble"}, {"main": "pizza"},
                                    {"main": "bag", "extras": ["heart", "x", "star", "plus"], "motion": "fly"}])
        names = ["التتبيلة", "العجين"]
        self.assertEqual([og.icon_for(n, "", "الطبخ")[:5] for n in names], ["subj:", "subj:"])   # before: the subject character
        out = lego.ask_model(names, llm, "الطبخ", {"التتبيلة": "خلطة للنكهة"})
        self.assertEqual(set(out), set(names)); self.assertEqual(len(llm.calls), 1)               # ONE call for the whole book
        self.assertIn("pot:", out["التتبيلة"]); self.assertIn("خلطة للنكهة", llm.calls[0])
        e = lego.library()[lego._key_of("التتبيلة")]
        self.assertEqual(e["status"], "auto"); self.assertEqual(len(e["suggestions"]), 2)        # «pizza» is not a part → dropped
        self.assertTrue(e["suggestions"][1].startswith("lego:bag:heart+star:"))                  # bad badge dropped, max 2, bad motion → the part's own
        self.assertEqual(og.icon_for("التتبيلة", "", "الطبخ"), out["التتبيلة"])                  # the page now gets the built drawing
        lego.ask_model(names, llm, "الطبخ")
        self.assertEqual(len(llm.calls), 1)                                                      # saved: no second cost

    def test_bad_or_missing_model_changes_nothing(self):
        for llm in (fake_model(lambda n: [{"main": "pizza"}]), lambda s, u: "no json", lambda s, u: (_ for _ in ()).throw(RuntimeError("no key"))):
            self.assertEqual(lego.ask_model(["التخمير"], llm, "الطبخ"), {})
        self.assertTrue(og.icon_for("التخمير", "", "الطبخ").startswith("subj:"))
        odd_answer = lambda s, u: json.dumps({"items": [{"name": "اسم ما طلبناه", "options": [{"main": "pot"}]}]})
        self.assertEqual(lego.ask_model(["التخمير"], odd_answer, "الطبخ"), {})                   # a name we did not ask for: ignored

    def test_teacher_picks_or_rejects(self):
        lego.ask_model(["العجين"], fake_model(lambda n: [{"main": "pot"}, {"main": "cube"}]), "الطبخ")
        r = lego.choose("العجين", pick=1)
        self.assertTrue(r["old"].startswith("lego:pot:")); self.assertTrue(r["new"].startswith("lego:cube:"))
        self.assertEqual(lego.library()[lego._key_of("العجين")]["status"], "approved")
        with self.assertRaises(ValueError):
            lego.choose("العجين", pick=5)
        r = lego.choose("العجين", reject=True)
        self.assertIsNone(r["new"]); self.assertTrue(og.icon_for("العجين", "", "الطبخ").startswith("subj:"))
        with self.assertRaises(KeyError):
            lego.choose("ما في هيك مفهوم", pick=0)


if __name__ == "__main__":
    unittest.main()
