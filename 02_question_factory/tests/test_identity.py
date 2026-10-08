"""🎭 Every subject's identity (batch 27): the subjects we know keep exactly what they had; a NEW subject gets its own
sound and its own characters — by its words (computer, music, art…) or, if nothing matches, a stable one from its name."""
import json
import os
import re
import sys
import unittest

import identity as I
import offline_generator as og
from graph_reader import Graph

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(HERE, "player"))
import build_explain_player as player  # noqa: E402

BOOKS = sorted(f for f in os.listdir(HERE) if f.endswith("_book_graph.json"))
COMPUTER = os.path.join(HERE, "examples", "new_subject_computer_g7.json")
SOUND_JS = os.path.join(os.path.dirname(HERE), "03_explain_player_src", "sound.js")
PAGE_JS = os.path.join(os.path.dirname(HERE), "03_explain_player_src", "part3_core.js")


class TestKnownSubjectsStayTheSame(unittest.TestCase):
    def test_the_12_books_keep_their_subject_and_get_no_new_identity(self):
        old_kinds = (("math", ("math", "رياضيات")), ("science", ("science", "biology", "علوم", "أحياء")), ("physics", ("physics", "فيزياء")),
                     ("chemistry", ("chem", "كيمياء")), ("geography", ("geograph", "جغرافيا")), ("history", ("history", "تاريخ")),
                     ("language", ("arabic", "english", "language", "لغة", "عربي")))
        for f in BOOKS:
            book = json.load(open(os.path.join(HERE, f), encoding="utf-8"))["book"]
            old = next((k for k, w in old_kinds if any(x in str(book.get("subject", "")).lower() for x in w)), "general")
            idn = I.of_book(book)
            self.assertEqual(idn["kind"], old, f); self.assertFalse(idn["new"], f); self.assertIsNone(idn["sound"], f)

    def test_the_page_data_of_a_known_book_has_no_identity_keys(self):
        """(so the published page stays byte-for-byte the same)"""
        g = player.pack(os.path.join(HERE, "plants_book_graph.json"), self._out("plants_book_graph.json"))
        self.assertNotIn("identity", g); self.assertNotIn("sound", g); self.assertEqual(g["subject"], "science")

    def _out(self, f):
        import tempfile, explain_main
        d = tempfile.mkdtemp(); explain_main.run(os.path.join(HERE, f), d); return d


class TestNewSubjects(unittest.TestCase):
    def test_families_by_their_words(self):
        for sub, fam in [("Computer Science", "computer"), ("علوم الحاسوب", "computer"), ("Robotics", "computer"), ("Music", "music"),
                         ("الفنون", "art"), ("Economics", "economy"), ("التربية الإسلامية", "religion"), ("التربية البدنية", "sport"),
                         ("Physical Education", "sport"), ("الصحة والتغذية", "health"), ("Social Studies", "civics"), ("Philosophy", "thinking"),
                         ("علم الفلك", "space"), ("الزراعة", "farming")]:
            idn = I.of_book({"subject": sub})
            self.assertTrue(idn["new"], sub); self.assertEqual(idn["family"], fam, sub); self.assertEqual(idn["kind"], "general")

    def test_a_word_never_matches_inside_another_word(self):
        self.assertEqual(I.of_book({"subject": "Earth Science"})["kind"], "science")      # «art» is not inside «Earth»
        self.assertEqual(I.of_book({"subject": "رياضيات تطبيقية"})["kind"], "math")        # «طب» is not inside «تطبيقية»
        self.assertNotEqual(I.of_book({"subject": "مدينتي"})["family"], "religion")         # «دين» is not inside «مدينتي»

    def test_anything_else_gets_a_stable_identity_of_its_own(self):
        a1, a2 = I.of_book({"subject": "عالم الحشرات"}), I.of_book({"subject": "عالم الحشرات"})
        self.assertEqual(a1, a2)                                                            # the same name → the same identity
        self.assertEqual(a1["family"], "new"); self.assertTrue(a1["emblem"].startswith("✦"))
        others = {json.dumps(I.of_book({"subject": s})["sound"], sort_keys=True) for s in ("عالم الحشرات", "الأحجار الكريمة", "Cooking", "Origami", "Chess")}
        self.assertGreaterEqual(len(others), 4, "different new subjects should almost never sound the same")

    def test_no_subject_at_all_behaves_as_before(self):
        idn = I.of_book({"subject": ""}); self.assertFalse(idn["new"]); self.assertEqual(idn["kind"], "general")

    def test_every_sound_and_scale_exists_in_the_page(self):
        js = open(SOUND_JS, encoding="utf-8").read()
        voices = set(re.findall(r"^\s{4}(\w+):\(a,d,f,t,v,L\)=>", js, re.M))
        scales = set(re.findall(r"(\w+):\[0,", js.split("const SCALE=")[1].split(";")[0]))
        for f in list(I.FAMILIES) + [I.generic(s) for s in ("x", "y", "z", "عالم الحشرات", "Chess", "Origami")]:
            self.assertIn(f["sound"]["instr"], voices, f["id"]); self.assertIn(f["sound"]["scale"], scales, f["id"])

    def test_every_emblem_has_a_drawing_in_the_page(self):
        js = open(PAGE_JS, encoding="utf-8").read().split("const SUBJ_ART={")[1].split("};")[0]
        drawn = set(re.findall(r'^\s+"([^"]+)":\(C,N\)=>', js, re.M))
        for e in [f["emblem"] for f in I.FAMILIES] + list(I.GENERIC_EMBLEMS):
            self.assertIn(e, drawn, e)


class TestNewSubjectCharacters(unittest.TestCase):
    def test_the_computer_book_gets_computer_characters_with_whole_names(self):
        """A computer concept with no drawing of its own and no Lego part (batch 29) → the computer character, its WHOLE name on it."""
        g = Graph.load(COMPUTER)
        icons = {c.text: og.icon_for(c.text, c.description, g.book["subject"]) for c in g.concepts.values() if og.is_entity(g, c.id)}
        self.assertTrue(all(i.startswith(("subj:💻:", "lego:")) for i in icons.values()), icons)   # never the science flask
        self.assertEqual(og.icon_for("وحدة التحكم المركزية", "", g.book["subject"]), "subj:💻:وحدة التحكم المركزية")   # the WHOLE name
        self.assertEqual(og.icon_for("الأنظمة الموزعة الهجينة", "", g.book["subject"])[:5], "lego:")   # «أنظمة» → a part (the gear)

    def test_names_are_cut_only_at_a_space(self):
        self.assertEqual(og._label("الخبر"), "خبر")
        self.assertEqual(og._label("الخطأ البرمجي"), "الخطأ البرمجي")
        long = og._label("مفهوم طويل جداً جداً فيه كلمات كثيرة كثير")
        self.assertLessEqual(len(long), 28); self.assertTrue("مفهوم طويل جداً جداً فيه كلمات كثيرة كثير".startswith(long + " "))

    def test_the_page_data_of_a_new_subject_carries_its_identity(self):
        import tempfile, explain_main
        d = tempfile.mkdtemp(); explain_main.run(COMPUTER, d)
        g = player.pack(COMPUTER, d)
        self.assertEqual(g["subject"], "general")
        self.assertEqual(g["identity"]["emblem"], "💻"); self.assertEqual(g["identity"]["mascot"], "subj:💻:")
        self.assertEqual(g["identity"]["mascot_name"], "بِتّو"); self.assertEqual(g["sound"]["instr"], "chip")


if __name__ == "__main__":
    unittest.main()


class TestBatch28(unittest.TestCase):
    """🆕 batch 28: the model picks an identity that FITS (once per subject) · each concept its own drawing."""
    def setUp(self):
        import tempfile
        self.store = tempfile.mktemp(suffix=".json")
        I.set_store(self.store)

    def tearDown(self):
        import os
        if os.path.exists(self.store):
            os.remove(self.store)

    def test_model_choice_is_checked_saved_and_used(self):
        calls = []
        good = lambda s, u: (calls.append(u), 'ok {"emblem": "🩺", "instrument": "kalimba", "scale": "major", "root": 62, "mascot_name": "طبّوخ", "label": "الطبخ", "face": true}')[1]
        self.assertTrue(I.needs_model("الطبخ"))
        before = I.of_book({"subject": "الطبخ"})["emblem"]
        self.assertIn(before, I.GENERIC_EMBLEMS)                          # without the model: the name identity
        got = I.ask_model("الطبخ", good)
        self.assertEqual(got["mascot"], "طبّوخ")
        idn = I.of_book({"subject": "الطبخ"})
        self.assertEqual((idn["emblem"], idn["mascot_name"], idn["family"], idn["sound"]["instr"]), ("🩺", "طبّوخ", "chosen", "kalimba"))
        self.assertEqual(I.emblem("الطبخ"), "🩺")
        I.ask_model("الطبخ", good)
        self.assertEqual(len(calls), 1)                                          # once per subject: saved, no second cost
        self.assertIn("🩺", calls[0]); self.assertIn("kalimba", calls[0])          # the model only sees OUR lists

    def test_bad_answers_change_nothing(self):
        for bad in ['{"emblem": "🍳", "instrument": "kalimba", "scale": "major", "root": 60, "mascot_name": "طبوخ"}',   # a shape we can't draw
                    '{"emblem": "🩺", "instrument": "guitar", "scale": "major", "root": 60, "mascot_name": "طبوخ"}',   # an instrument we don't have
                    '{"emblem": "🩺", "instrument": "harp", "scale": "major", "root": 99, "mascot_name": "طبوخ"}',     # out of range
                    '{"emblem": "🩺", "instrument": "harp", "scale": "major", "root": 60, "mascot_name": "<b>x</b>"}', # not an Arabic name
                    "no json at all"]:
            self.assertIsNone(I.ask_model("علم البحار", lambda s, u, b=bad: b), bad)
        self.assertIn(I.of_book({"subject": "علم البحار"})["emblem"], I.GENERIC_EMBLEMS)
        def broken(s, u):
            raise RuntimeError("no key")
        self.assertIsNone(I.ask_model("علم البحار", broken))             # no key / network: the book still works

    def test_known_and_family_subjects_never_ask(self):
        boom = lambda s, u: self.fail("must not ask the model")
        for sub in ("Physics", "علوم", "الروبوتات", "التربية الإسلامية", ""):
            self.assertFalse(I.needs_model(sub), sub)
            I.ask_model(sub, boom)

    def test_every_concept_its_own_drawing(self):
        import offline_generator as og
        for book, subject in (("arabic_g4", "Arabic language"), ("phy_g6", "Physics"), ("chem_g7", "Chemistry"), ("geo_g5", "Geography"),
                              ("phy_g10", "Physics"), ("math_g9", "Mathematics"), ("bio_g12", "Biology")):
            g = json.load(open(os.path.join(HERE, book + "_book_graph.json"), encoding="utf-8"))
            ents = [n for n in g["nodes"] if n.get("level") == "entity"]
            icons = [og.icon_for(n.get("title") or n.get("name", ""), "", subject) for n in ents]
            drawn = [i for i in icons if not i.startswith("subj:")]
            self.assertEqual(len(drawn), len(set(drawn)), (book, [(n.get("title"), i) for n, i in zip(ents, icons)]))

    def test_new_drawings_exist_in_the_page(self):
        page = open(os.path.join(HERE, "player", "explain_template.html"), encoding="utf-8").read()
        for key in ("ara:harakat", "ara:word", "ara:noun", "ara:particle", "ara:nominal", "ara:verbal", "ara:mubtada", "chem:element", "chem:compound",
                    "chem:acid", "chem:base", "phy:friction", "phy:battery", "phy:circuit", "geo:continents", "sec:genotype", "sec:linfunc", "sec:freefall"):
            self.assertIn(f'"{key}":["x_', page, key)

