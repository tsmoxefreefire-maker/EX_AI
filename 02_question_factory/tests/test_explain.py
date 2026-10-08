"""The explanation factory: scenes that teach, built only from the graph, for any book."""
import os
import tempfile
import unittest

import explain_generator as eg
import explain_main
from graph_reader import Graph

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOKS = [os.path.join(HERE, b) for b in ("plants_book_graph.json", "math_book_graph.json", "history_book_graph.json")]


class TestScenes(unittest.TestCase):
    def test_every_book_every_lesson_every_concept(self):
        for book in BOOKS:
            g = Graph.load(book)
            for lesson in g.lessons():
                rec = eg.explain_lesson(g, lesson)
                self.assertEqual(rec["overview"]["kind"], "overview")
                for c in rec["concepts"]:
                    self.assertTrue(any(x["kind"] == "meet" for x in c["scenes"]))   # every concept is introduced (not always first: variety)
                    for s in c["scenes"]:
                        self.assertEqual(eg.check_scene(g, s), [], (book, c["concept_id"], s["kind"]))

    def test_the_picture_follows_the_graph(self):
        g = Graph.load(BOOKS[0])
        lesson = {l.id: l for l in g.lessons()}["l_parts"]
        root = [c for c in eg.explain_lesson(g, lesson)["concepts"] if c["concept_id"] == "root"][0]
        meet = next(s for s in root["scenes"] if s["kind"] == "meet")
        self.assertEqual(set(meet["ins"]), {"soil", "water"}); self.assertEqual(meet["outs"], ["stem"])
        journeys = [s for c in eg.explain_lesson(g, lesson)["concepts"] for s in c["scenes"] if s["kind"] == "journey"]
        self.assertTrue(journeys)
        for j in journeys:
            self.assertTrue(all(g.is_prereq(a, b) for a, b in zip(j["route"], j["route"][1:])))

    def test_a_wrong_scene_is_caught(self):
        g = Graph.load(BOOKS[0])
        self.assertTrue(eg.check_scene(g, {"kind": "journey", "route": ["leaf", "root"], "steps": []}))
        self.assertTrue(eg.check_scene(g, {"kind": "what_if", "target": "root", "affected": ["soil"], "calm": [], "steps": []}))

    def test_no_wrong_arabic_in_the_captions(self):
        for book in BOOKS:
            g = Graph.load(book)
            for lesson in g.lessons():
                for c in eg.explain_lesson(g, lesson)["concepts"]:
                    for line in next(x for x in c["scenes"] if x["kind"] == "meet")["steps"]:
                        self.assertNotRegex(line, r"أنا ي")                  # «أنا يثبّت» was wrong

    def test_realistic_journey(self):          # a flower never walks to a bee; water really rises
        g = Graph.load(BOOKS[0])
        recs = {l.id: eg.explain_lesson(g, l) for l in g.lessons()}
        js = [s for r in recs.values() for c in r["concepts"] for s in c["scenes"] if s["kind"] == "journey"]
        for s in js:
            first = s["route"][0]
            self.assertEqual(s["traveller"] != "spark", first in ("water", "air", "sunlight"), (first, s["traveller"]))

    def test_words_say_needs_not_gives(self):   # the graph says «needs», so the text says «needs»
        for book in BOOKS:
            g = Graph.load(book)
            for l in g.lessons():
                r = eg.explain_lesson(g, l)
                for c in r["concepts"]:
                    for s in c["scenes"]:
                        text = " ".join(s["steps"]) + s.get("paragraph", "")
                        self.assertNotIn("بيوصلّي", text); self.assertNotIn("بساعد", text)
                        self.assertTrue(s.get("paragraph"), (c["concept_id"], s["kind"]))

    def test_a_teacher_frames_every_concept(self):   # a question first, a link to the last concept, one sentence to keep
        for book in BOOKS:
            g = Graph.load(book)
            for l in g.lessons():
                cs = eg.explain_lesson(g, l)["concepts"]
                for i, c in enumerate(cs):
                    t = c["teach"]
                    self.assertTrue(t["hook"].endswith("؟")); self.assertTrue(t["summary"])
                    self.assertEqual(t["recap"] is None, i == 0)

    def test_plant_world_only_where_it_fits(self):   # a real plant world for «حاجات النبات»; none for maths
        g = Graph.load(BOOKS[0])
        worlds = {l.id: eg.explain_lesson(g, l)["world"] for l in g.lessons()}
        self.assertTrue(worlds["l_needs"]); self.assertEqual(set(worlds["l_needs"]["needs"]), {"water", "sun", "air"})
        self.assertEqual(eg.check_scene(g, worlds["l_needs"]), [])
        gm = Graph.load(BOOKS[1])
        self.assertTrue(all(eg.explain_lesson(gm, l)["world"] is None for l in gm.lessons()))

    def test_names_not_me(self):          # «الساق بيحتاج الجذر», never «بيحتاجوني» / «أنا بحتاج»
        for book in BOOKS:
            g = Graph.load(book)
            for l in g.lessons():
                for c in eg.explain_lesson(g, l)["concepts"]:
                    m = next(x for x in c["scenes"] if x["kind"] == "meet")
                    self.assertEqual(len(m["focus"]), len(m["steps"]))
                    for line in m["steps"]:
                        self.assertNotIn("بيحتاجوني", line); self.assertNotIn("أنا بحتاج", line)

    def test_films_tell_what_really_happens(self):     # the bee visits what pollination needs; the fruit is what needs it
        g = Graph.load(BOOKS[0])
        cyc = {l.id: l for l in g.lessons()}["l_cycle"]
        pol = [c for c in eg.explain_lesson(g, cyc)["concepts"] if c["concept_id"] == "pollination"][0]
        film = [s for s in pol["scenes"] if s["kind"] == "play"][0]
        self.assertEqual((film["verb"], film["actor"], film["with"], film["result"]), ("visit", "النحلة", "flower", "fruit"))
        self.assertEqual(eg.check_scene(g, film), [])
        self.assertFalse(any(s["kind"] == "journey" and s["traveller"] == "spark" for s in pol["scenes"]))   # no floating spark when a real film exists
        verbs = set()
        for book in BOOKS:
            gb = Graph.load(book)
            for l in gb.lessons():
                for c in eg.explain_lesson(gb, l)["concepts"]:
                    for s in c["scenes"]:
                        if s["kind"] == "play":
                            verbs.add(s["verb"]); self.assertEqual(eg.check_scene(gb, s), [])
        self.assertTrue({"visit", "carry", "combine", "cut", "build", "exchange"} <= verbs, verbs)

    def test_saved_for_every_lesson(self):
        with tempfile.TemporaryDirectory() as tmp:
            recs = explain_main.run(BOOKS[1], tmp)
            self.assertEqual(len(recs), 4)
            self.assertTrue(all(os.path.exists(os.path.join(tmp, "lessons", r["lesson_id"], "explanations.json")) for r in recs))
            self.assertTrue(all(r["status"] == "needs_review" for r in recs))


class TestWriter(unittest.TestCase):
    """The model rewrites the paragraphs; names stay, nothing new, a broken answer changes nothing."""
    def rec(self):
        g = Graph.load(BOOKS[0]); return eg.explain_lesson(g, {l.id: l for l in g.lessons()}["l_parts"])

    def test_good_rewrite_is_used(self):
        import explain_llm, json
        r = explain_llm.polish_lesson(self.rec(), lambda s, u: json.dumps({k: "بكل بساطة: " + v for k, v in json.loads(u).items()}, ensure_ascii=False))
        self.assertTrue(r["overview"]["paragraph"].startswith("بكل بساطة"))
        self.assertEqual(r["llm"]["rewritten"], r["llm"]["paragraphs"])

    def test_dropped_or_new_names_are_refused(self):
        import explain_llm, json, re
        r = explain_llm.polish_lesson(self.rec(), lambda s, u: json.dumps({k: re.sub(r"«[^»]+»", "هو", v) + " «القمر»" for k, v in json.loads(u).items()}, ensure_ascii=False))
        self.assertEqual(r["llm"]["rewritten"], 0)

    def test_broken_answer_changes_nothing(self):
        import explain_llm
        before = self.rec()["overview"]["paragraph"]
        r = explain_llm.polish_lesson(self.rec(), lambda s, u: "sorry")
        self.assertEqual(r["overview"]["paragraph"], before)


if __name__ == "__main__":
    unittest.main()
