"""🤖 Scenes written by the model — the whole pipeline with a FAKE model (no keys needed):
generate → checks → one repair round → saved as pending_review → teacher approves → the lesson shows it (include_llm) → sandbox page."""
import json
import os
import shutil
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAMPLES = os.path.join(os.path.dirname(HERE), "02_question_factory")          # the sample books live in the factory (no copies here)
os.environ.setdefault("EXPLAIN_SEED", "0")                                   # tests make their own books
TMP = tempfile.mkdtemp()
os.environ["EXPLAIN_DATA_DIR"] = TMP
sys.path.insert(0, HERE)
from core import llm_scenes, service, settings  # noqa: E402
import scene_writer  # noqa: E402

GOOD = scene_writer.EXAMPLE
BAD = "function buildScene(SDK, data) { fetch('http://evil'); while (true) {} }"


class FakeModel:
    """Answers with the given codes in order (and counts the calls)."""
    def __init__(self, *codes):
        self.codes, self.calls, self.last_user = list(codes), 0, ""

    def __call__(self, system, user):
        self.calls += 1
        self.last_user = user
        return "```javascript\n" + self.codes[min(self.calls - 1, len(self.codes) - 1)] + "\n```"


class TestSceneWriter(unittest.TestCase):
    """The checks themselves (no server)."""
    def test_example_passes_every_check(self):
        self.assertEqual(scene_writer.check_code(GOOD), [])

    def test_dangerous_code_is_refused(self):
        for bad, why in [("function buildScene(SDK, data) { window.top.x = 1 }", "window"), ("function buildScene(SDK, data) { fetch('x') }", "fetch"),
                         ("function buildScene(SDK, data) { while (1) {} }", "while loop"), ("function buildScene(SDK, data) { eval('1') }", "eval"),
                         ("function buildScene(SDK, data) { SDK.caption(`${document.cookie}`) }", "document"),
                         ("function buildScene(SDK, data) { localStorage.x = 1 }", "storage"), ("function buildScene(SDK, data) { const a = {}.constructor }", "escape tricks")]:
            self.assertTrue(any(why in p for p in scene_writer.check_code(bad)), (bad, scene_writer.check_code(bad)))

    def test_arabic_words_inside_strings_are_not_code(self):
        self.assertEqual(scene_writer.check_code('function buildScene(SDK, data) { SDK.caption("while بالعربي ما بتضر"); for (let i = 0; i < 3; i++) {} }'), [])

    def test_missing_function_and_syntax_errors(self):
        self.assertIn("missing: function buildScene(SDK, data)", scene_writer.check_code("const x = 1;"))
        self.assertTrue(any(p.startswith("unbalanced") or p.startswith("syntax") for p in scene_writer.check_code("function buildScene(SDK, data) { SDK.caption('x' ")))

    def test_too_long_is_refused(self):
        self.assertTrue(any(p.startswith("too long") for p in scene_writer.check_code(GOOD + "\n//" + "x" * scene_writer.MAX_CODE)))

    def test_prompt_has_the_rules_the_facts_and_the_age(self):
        data = {"concept": {"id": "accel", "name": "التسارع", "meaning": "م", "ins": [], "outs": []}, "concepts": {}, "lesson": {"id": "l", "title": "t"},
                "subject": "Physics", "stage": "senior", "grade": 10, "needsWord": "بيعتمد على"}
        system, user = scene_writer.build_prompt(data, idea="سيارة بتسرّع")
        self.assertIn("function buildScene(SDK, data)", system); self.assertIn("No while loops", system)
        self.assertIn("calm expert", user); self.assertIn("التسارع", user); self.assertIn("سيارة بتسرّع", user)

    def test_runner_blocks_the_network_and_carries_the_code(self):
        data = {"concept": {"id": "a", "name": "أ"}, "stage": "teen"}
        html = scene_writer.runner_html("function buildScene(SDK, data) { SDK.caption('</script>') }", data, sdk_js="/*sdk*/")
        self.assertIn("default-src 'none'", html); self.assertIn('data-stage="teen"', html)
        self.assertNotIn("('</script>')", html)              # «</» is escaped: the code cannot close the script tag


class TestPipeline(unittest.TestCase):
    """generate → save → review → the lesson (with a fake model)."""
    @classmethod
    def setUpClass(cls):
        cls.keep = (settings.DATA_DIR, settings.GRAPHS_DIR, settings.BOOKS_DIR)     # its OWN data folder (other test files share the process)
        settings.DATA_DIR, settings.GRAPHS_DIR, settings.BOOKS_DIR = TMP, os.path.join(TMP, "graphs"), os.path.join(TMP, "books")
        os.makedirs(settings.GRAPHS_DIR, exist_ok=True)
        shutil.copy(os.path.join(SAMPLES, "phy_g10_book_graph.json"), settings.GRAPHS_DIR)
        service.generate(graph_path="phy_g10_book_graph.json")

    @classmethod
    def tearDownClass(cls):
        settings.DATA_DIR, settings.GRAPHS_DIR, settings.BOOKS_DIR = cls.keep
        shutil.rmtree(TMP, ignore_errors=True)

    def test_1_a_good_scene_waits_for_the_teacher(self):
        m = FakeModel(GOOD)
        r = llm_scenes.generate("phy_g10", "l_speed", concept_id="accel", llm=m)
        s = r["scenes"][0]
        self.assertEqual((s["status"], s["problems"], m.calls), ("pending_review", [], 1))
        self.assertIn("التسارع", m.last_user); self.assertIn("calm expert", m.last_user)     # the facts + the senior stage reached the model
        rec = llm_scenes.get_scene(s["scene_id"])
        self.assertEqual(rec["data"]["stage"], "senior"); self.assertTrue(rec["data"]["art"]["accel"].startswith("<svg"))

    def test_2_asking_again_costs_nothing(self):
        m = FakeModel(GOOD)
        r = llm_scenes.generate("phy_g10", "l_speed", concept_id="accel", llm=m)
        self.assertTrue(r["scenes"][0]["reused"]); self.assertEqual(m.calls, 0)

    def test_3_a_bad_answer_gets_one_repair_round(self):
        m = FakeModel(BAD, GOOD)
        r = llm_scenes.generate("phy_g10", "l_speed", concept_id="velocity", llm=m)
        self.assertEqual((r["scenes"][0]["status"], r["scenes"][0]["attempts"], m.calls), ("pending_review", 2, 2))
        self.assertIn("REJECTED", m.last_user)                # the model was told what was wrong

    def test_4_still_bad_is_rejected_and_never_approved(self):
        m = FakeModel(BAD, BAD)
        r = llm_scenes.generate("phy_g10", "l_speed", concept_id="freefall", llm=m)
        s = r["scenes"][0]
        self.assertEqual(s["status"], "rejected"); self.assertTrue(r["warnings"])
        with self.assertRaises(llm_scenes.BadInput):
            llm_scenes.review(s["scene_id"], approve=True)

    def test_5_approved_scenes_join_the_lesson(self):
        sid = llm_scenes.list_scenes("phy_g10", "l_speed", "pending_review")[0]["scene_id"]
        before = service.get_lesson("l_speed", "phy_g10", include_llm=True)
        llm_scenes.review(sid, approve=True, note="ممتاز")
        after = service.get_lesson("l_speed", "phy_g10", include_llm=True)
        n = lambda rec: sum(1 for c in rec["concepts"] for s in c["scenes"] if s["kind"] == "custom")
        self.assertEqual(n(after), n(before) + 1)
        self.assertEqual(n(service.get_lesson("l_speed", "phy_g10")), 0)        # without include_llm: the factory's scenes only
        custom = next(s for c in after["concepts"] for s in c["scenes"] if s["kind"] == "custom")
        self.assertTrue(custom["runner_url"].startswith("/llm/scenes/")); self.assertEqual(after["audience"]["stage"], "senior")

    def test_5b_approved_scene_is_inside_the_page(self):
        """🆕 batch 28: the scene a teacher approved shows INSIDE /explain (the page), not only in the lesson data."""
        page = service.page_data(["phy_g10"])["graphs"][0]
        custom = [s for l in page["lessons"] for c in l["concepts"] for s in c["scenes"] if s.get("source") == "llm"]
        self.assertEqual(len(custom), 1)
        self.assertEqual(custom[0]["kind"], "custom"); self.assertIn("function buildScene", custom[0]["runner_html"])
        self.assertIn("default-src 'none'", custom[0]["runner_html"])                # the same sandbox walls
        html = service.page_html(["phy_g10"])
        self.assertIn('"source": "llm"', html)

    def test_6_runner_and_browser_report(self):
        sid = llm_scenes.list_scenes("phy_g10")[0]["scene_id"]
        html = llm_scenes.runner(sid)
        self.assertIn("function buildScene", html); self.assertIn("default-src 'none'", html); self.assertIn("SCENE SDK", html)
        r = llm_scenes.report(sid, {"ok": True, "drawn": 12, "outside": 0, "errors": []})
        self.assertTrue(r["browser_check"]["ok"])

    def test_7_limits_and_wrong_input(self):
        with self.assertRaises(llm_scenes.BadInput):
            llm_scenes.generate("phy_g10", "l_speed", max_scenes=50, llm=FakeModel(GOOD))
        with self.assertRaises(llm_scenes.NotFound):
            llm_scenes.generate("phy_g10", "no_lesson", llm=FakeModel(GOOD))
        with self.assertRaises(llm_scenes.NotFound):
            llm_scenes.generate("no_book", "l_speed", llm=FakeModel(GOOD))

    def test_8_no_key_no_call(self):
        keep = llm_scenes.llm_gateway.api_key_from_anywhere
        llm_scenes.llm_gateway.api_key_from_anywhere = lambda: ""
        try:
            with self.assertRaises(llm_scenes.BadInput):
                llm_scenes.generate("phy_g10", "l_position", concept_id="time")
        finally:
            llm_scenes.llm_gateway.api_key_from_anywhere = keep

    def test_9_sdk_doc(self):
        d = llm_scenes.sdk_doc()
        self.assertIn("SDK.character", d["sdk_reference"]); self.assertIn("senior", d["stage_rules"]); self.assertIn("window", d["forbidden"])


try:
    from fastapi.testclient import TestClient
    from main import app
    HAVE_HTTP = True
except ImportError:
    HAVE_HTTP = False


@unittest.skipUnless(HAVE_HTTP, "pip install -r requirements.txt")
class TestHTTP(unittest.TestCase):
    """The endpoints (the model is a fake one, plugged into the gateway)."""
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp()
        cls.keep = (settings.DATA_DIR, settings.GRAPHS_DIR, settings.BOOKS_DIR, llm_scenes.llm_gateway.generate, llm_scenes.llm_gateway.api_key_from_anywhere)
        settings.DATA_DIR, settings.GRAPHS_DIR, settings.BOOKS_DIR = cls.tmp, os.path.join(cls.tmp, "graphs"), os.path.join(cls.tmp, "books")
        llm_scenes.llm_gateway.generate = FakeModel(GOOD); llm_scenes.llm_gateway.api_key_from_anywhere = lambda: "fake-key"
        cls.c = TestClient(app)
        with open(os.path.join(SAMPLES, "bio_g12_book_graph.json"), encoding="utf-8") as f:
            cls.c.post("/explanations/generate", json={"graph": json.load(f)})

    @classmethod
    def tearDownClass(cls):
        (settings.DATA_DIR, settings.GRAPHS_DIR, settings.BOOKS_DIR, llm_scenes.llm_gateway.generate, llm_scenes.llm_gateway.api_key_from_anywhere) = cls.keep
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_generate_review_lesson_runner(self):
        r = self.c.post("/llm/scenes/generate", json={"book_id": "bio_g12", "lesson_id": "l_traits", "concept_id": "genotype", "idea": "مربع بانيت بيتعبّى"})
        self.assertEqual(r.status_code, 200); s = r.json()["scenes"][0]; self.assertEqual(s["status"], "pending_review")
        self.assertEqual(self.c.get("/llm/scenes", params={"status": "pending_review"}).json()[0]["scene_id"], s["scene_id"])
        html = self.c.get(s["runner_url"])
        self.assertEqual(html.status_code, 200); self.assertIn("default-src 'none'", html.text)
        self.assertEqual(self.c.post(f"/llm/scenes/{s['scene_id']}/review", json={"approve": True}).json()["status"], "approved")
        lesson = self.c.get("/lessons/l_traits/explanation", params={"include_llm": "true"}).json()
        self.assertTrue(any(x["kind"] == "custom" for c in lesson["concepts"] for x in c["scenes"]))
        self.assertEqual(lesson["audience"]["stage"], "senior")
        self.assertEqual(self.c.post(f"/llm/scenes/{s['scene_id']}/report", json={"ok": True, "drawn": 9, "outside": 0, "errors": []}).status_code, 200)

    def test_errors_and_sdk(self):
        self.assertEqual(self.c.post("/llm/scenes/generate", json={"book_id": "nope", "lesson_id": "x"}).status_code, 404)
        self.assertEqual(self.c.get("/llm/scenes/nope").status_code, 404)
        self.assertIn("SDK.character", self.c.get("/llm/sdk").json()["sdk_reference"])


if __name__ == "__main__":
    unittest.main()
