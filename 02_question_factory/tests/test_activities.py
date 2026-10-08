"""🆕 The 5 new activities (batch 26): made from the graph only, true, said the way each age talks, and spread over the lessons."""
import os
import re
import unittest
from collections import Counter

import audience as A
import explain_activities as act
import explain_generator as eg
from graph_reader import Graph

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOKS = ["plants", "math", "arabic_g4", "history", "geo_g5", "phy_g6", "chem_g7", "sci_g8", "math_g9", "phy_g10", "chem_g11", "bio_g12"]
_ALL = {}


def book(name):
    if name not in _ALL:
        g = Graph.load(os.path.join(HERE, name + "_book_graph.json"))
        _ALL[name] = (g, [eg.explain_lesson(g, l) for l in g.lessons()])
    return _ALL[name]


def scenes(kind=None):
    for name in BOOKS:
        g, recs = book(name)
        for rec in recs:
            for c in rec["concepts"]:
                for s in c["scenes"]:
                    if kind is None or s["kind"] == kind:
                        yield name, g, rec, s


def strings(x):
    if isinstance(x, str):
        yield x
    elif isinstance(x, dict):
        for k, v in x.items():
            if k not in ("kind", "target", "id", "ref", "side", "type", "rel", "from", "to", "mode", "other", "nodes", "calm", "concepts", "edges", "levels", "verb", "traveller", "before", "with", "result", "parts", "needs_ids"):
                yield from strings(v)
    elif isinstance(x, list):
        for v in x:
            yield from strings(v)


class TestActivities(unittest.TestCase):
    def test_every_kind_appears_in_the_books(self):
        c = Counter(s["kind"] for _, _, _, s in scenes() if s["kind"] in act.KINDS)
        for k in act.KINDS:
            self.assertGreaterEqual(c[k], 8 if k != "recipe" else 10, (k, c))

    def test_every_new_scene_is_true_to_the_graph(self):
        for name, g, _, s in scenes():
            if s["kind"] in act.KINDS:
                self.assertEqual(act.check(g, s), [], (name, s["kind"], s.get("target")))

    def test_the_check_catches_a_lie(self):
        name, g, _, s = next(scenes("connect"))
        bad = dict(s, links=[dict(s["links"][0], **{"from": s["links"][0]["to"], "to": s["links"][0]["from"]})])
        self.assertTrue(act.check(g, bad))
        name, g, _, s = next(scenes("compare"))
        lie = [dict(f, side={"a": "b", "b": "a", "both": "a"}[f["side"]]) for f in s["facts"]]
        self.assertTrue(act.check(g, dict(s, facts=lie)))

    def test_one_new_activity_per_concept_and_mixed_in_each_lesson(self):
        for name in BOOKS:
            g, recs = book(name)
            for rec in recs:
                kinds = [[s["kind"] for s in c["scenes"] if s["kind"] in act.KINDS] for c in rec["concepts"]]
                self.assertTrue(all(len(k) <= 1 for k in kinds), (name, rec["lesson_id"], kinds))
                flat = [k[0] for k in kinds if k]
                if len(flat) >= 3:
                    self.assertGreaterEqual(len(set(flat)), 2, (name, rec["lesson_id"], flat))

    def test_recipe_only_when_two_things_or_more(self):
        for _, g, _, s in scenes("recipe"):
            self.assertGreaterEqual(len(s["needs"]), 2)
            self.assertTrue(all(g.is_prereq(n["id"], s["target"]) for n in s["needs"]))

    def test_connect_explains_the_reversed_arrow(self):
        for _, _, _, s in scenes("connect"):
            req = [l for l in s["links"] if l["required"]]
            self.assertGreaterEqual(len(req), 2)
            for l in req:
                self.assertTrue(l["rev_say"] and l["ok_say"])

    def test_compare_has_same_and_different(self):
        for _, _, _, s in scenes("compare"):
            sides = Counter(f["side"] for f in s["facts"])
            self.assertTrue(sides["a"] and sides["b"] and sides["both"], sides)
            self.assertLessEqual(len(s["facts"]), 6)

    def test_teach_has_one_right_answer_per_question(self):
        for _, _, _, s in scenes("teach"):
            self.assertGreaterEqual(len(s["rounds"]), 2)
            for r in s["rounds"]:
                self.assertEqual(sum(o["ok"] for o in r["options"]), 1)
                self.assertTrue(all(o["reply"] for o in r["options"]))

    def test_ladder_steps_follow_the_arrows(self):
        for _, g, _, s in scenes("ladder"):
            self.assertGreaterEqual(len(s["rungs"]), 2)
            self.assertTrue(s["end_say"])

    def test_grown_ups_hear_grown_up_words(self):
        for name, g, rec, s in scenes():
            st = rec["audience"]["stage"]
            for t in strings(s):
                if st in ("teen", "senior") and s["kind"] in act.KINDS:
                    self.assertNotRegex(t, r"(^|\s)(بيحتاج|بتحتاج|بيحتاجه|بيحتاجوا)(\s|$)", (name, s["kind"], t))
                if st == "senior":
                    self.assertNotRegex(t, "[‍️](?<![✅✔⚠]️)", (name, s["kind"], "a leftover emoji glue", t))

    def test_never_a_dangling_ala(self):
        """«بيعتمد على،» / «على للي» — the teen/senior wording must never leave «على» without its object (every scene, old and new)."""
        for name, g, rec, s in scenes():
            for t in strings(s):
                self.assertNotRegex(t, r"على\s*[،.؟!:]|على\s+للي|على\s*$", (name, s["kind"], t))
        self.assertEqual(A.voice("➜ السهم يعني «بيحتاج»: من اللي بيحتاج، للي بيحتاجه", "teen"), "➜ السهم يعني «بيعتمد على»: من اللي بيعتمد، للي بيعتمد عليه")

    def test_the_new_text_fields_are_voiced(self):
        for k in ("ready", "ok_say", "rev_say", "end_say", "fact", "ask", "opt", "reply", "learnt", "because", "short"):
            self.assertIn(k, A._TEXT_KEYS)


if __name__ == "__main__":
    unittest.main()
