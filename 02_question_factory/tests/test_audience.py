"""👥 The age stages: the grade decides the stage, the stage decides how the explanation talks (and which activities fit)."""
import json
import os
import unittest

import audience as A
import explain_generator as eg
from graph_reader import Graph

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOKS = {"plants_book_graph.json": ("kids", 4), "math_book_graph.json": ("kids", 4), "arabic_g4_book_graph.json": ("kids", 4),
         "history_book_graph.json": ("junior", 5), "geo_g5_book_graph.json": ("junior", 5), "phy_g6_book_graph.json": ("junior", 6),
         "chem_g7_book_graph.json": ("junior", 7), "sci_g8_book_graph.json": ("teen", 8), "math_g9_book_graph.json": ("teen", 9),
         "phy_g10_book_graph.json": ("senior", 10), "chem_g11_book_graph.json": ("senior", 11), "bio_g12_book_graph.json": ("senior", 12)}
EMOJI_FACES = "😄😢😟😎👋"


def lessons(name):
    g = Graph.load(os.path.join(HERE, name))
    return g, [eg.explain_lesson(g, l) for l in g.lessons()]


def texts(rec):
    out = []
    def walk(x, key=None):
        if isinstance(x, dict):
            for k, v in x.items():
                walk(v, k)
        elif isinstance(x, list):
            for v in x:
                walk(v, key)
        elif isinstance(x, str) and key in A._TEXT_KEYS:
            out.append(x)
    walk(rec)
    return out


class TestGradeToStage(unittest.TestCase):
    def test_grade_from_field_title_or_id(self):
        self.assertEqual(A.grade_of({"grade": 10}), 10); self.assertEqual(A.grade_of({"grade": "g12"}), 12)
        self.assertEqual(A.grade_of({"title": "الكيمياء · الصف الحادي عشر"}), 11); self.assertEqual(A.grade_of({"title": "العلوم · الصف الثاني"}), 2)
        self.assertEqual(A.grade_of({"id": "phy_g10"}), 10); self.assertIsNone(A.grade_of({"title": "كتاب"}))

    def test_stages(self):
        self.assertEqual([A.stage_of_grade(n) for n in (1, 4, 5, 7, 8, 9, 10, 12, None)],
                         ["kids", "kids", "junior", "junior", "teen", "teen", "senior", "senior", "kids"])

    def test_every_sample_book_has_its_stage(self):
        for name, (st, gr) in BOOKS.items():
            g, recs = lessons(name)
            self.assertTrue(recs, name)
            self.assertEqual((recs[0]["audience"]["stage"], recs[0]["audience"]["grade"]), (st, gr), name)


class TestVoice(unittest.TestCase):
    def test_kids_unchanged_and_voice_is_stable(self):
        s = "«الساق» بيحتاج «الجذر» 😄"
        self.assertEqual(A.voice(s, "kids"), s)
        for st in ("junior", "teen", "senior"):
            once = A.voice(s, st)
            self.assertEqual(A.voice(once, st), once, st)          # saying it twice changes nothing

    def test_grown_words(self):
        self.assertEqual(A.voice("«الساق» بيحتاج «الجذر».", "teen"), "«الساق» بيعتمد على «الجذر».")
        self.assertEqual(A.voice("شو بتحتاجي؟", "teen"), "على شو بتعتمدي؟")
        self.assertEqual(A.voice("«الورقة» بتتعب 😢", "senior"), "«الورقة» بتتأثر")

    def test_teen_and_senior_books_talk_grown_up(self):
        for name, (st, _) in BOOKS.items():
            if st not in ("teen", "senior"):
                continue
            g, recs = lessons(name)
            all_text = " ".join(t for r in recs for t in texts(r))
            self.assertNotIn("بيحتاج", all_text, name); self.assertNotIn("بيتعب", all_text, name)
            self.assertFalse(any(e in all_text for e in EMOJI_FACES), name)
            if st == "senior":
                self.assertNotIn("مرحبا! أنا", all_text, name)       # a scientific discussion, not two cartoons

    def test_little_ones_keep_their_playful_friends(self):
        g, recs = lessons("plants_book_graph.json")
        all_text = " ".join(t for r in recs for t in texts(r))
        self.assertIn("بيحتاج", all_text); self.assertIn("أهلاً! أنا", all_text)


class TestActivitiesFitTheAge(unittest.TestCase):
    def kinds(self, name):
        g, recs = lessons(name)
        return [(s["kind"], s.get("mode")) for r in recs for c in r["concepts"] for s in c["scenes"]]

    def test_formula_sliders_only_from_grade_8(self):
        self.assertIn(("slider", "line"), self.kinds("math_g9_book_graph.json"))
        self.assertIn(("slider", "motion"), self.kinds("phy_g10_book_graph.json"))
        self.assertIn(("slider", "accel"), self.kinds("phy_g10_book_graph.json"))
        self.assertFalse([k for k in self.kinds("phy_g6_book_graph.json") if k[1] in ("motion", "accel", "line")])

    def test_senior_interview_asks_about_the_concept(self):
        g, recs = lessons("phy_g10_book_graph.json")
        qs = [x["q"] for r in recs for c in r["concepts"] for s in c["scenes"] if s["kind"] == "interview" for x in s["qa"]]
        self.assertTrue(qs and all("إنت" not in q for q in qs), qs)

    def test_every_new_concept_has_a_drawing(self):
        import offline_generator as og
        for name in ("sci_g8_book_graph.json", "math_g9_book_graph.json", "phy_g10_book_graph.json", "chem_g11_book_graph.json", "bio_g12_book_graph.json"):
            g, recs = lessons(name)
            missing = [k for k, v in recs[0]["icons"].items() if v not in og.ART_ICONS]
            self.assertFalse(missing, (name, missing))


if __name__ == "__main__":
    unittest.main()
