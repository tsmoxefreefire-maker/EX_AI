# Context for writing the explorer notes (read this first)

## The project in one paragraph
"الشرح التفاعلي" (Interactive Explanation): you send a **curriculum graph** (JSON: concepts + "needs" arrows = prerequisites + units/topics/lessons, with `book.grade` and `book.subject`) to a **FastAPI server** (`05_explanation_api`). The server hands it to **the factory** (`02_question_factory`, plain Python, no AI by default) which reads the graph and writes **scenes** for every lesson (19 scene kinds: overview, meet, interview, flip, play/film, slider, dialogue, lens, journey, what_if, before_after, world, assemble + 5 activities: recipe, connect, compare, teach, ladder). Each scene is checked against the graph (a sentence says "X needs Y" only if the arrow exists) and saved as `lessons/<id>/explanations.json`. Then the server builds **one HTML page**: the page code (`03_explain_player_src`, JavaScript + CSS, glued together by `build_explain_template.py` into `player/explain_template.html`) + the data. **The browser** draws everything (SVG), animates it, and makes the sounds (Web Audio, no sound files).

## The journey (the order things happen)
1. `05_explanation_api/main.py` starts the server → `api/routes.py` (the doors / endpoints) → `api/schemas.py` (the shape of requests and answers).
2. `core/service.py` = the manager: names the book, (optional, with a model) picks Lego drawings and the subject identity, then calls the factory.
3. Factory: `explain_main.run` → `graph_reader.Graph` (reads the graph) → `explain_generator.explain_lesson` (makes the scenes) → helpers: `offline_generator.icon_for` (which drawing for a concept), `lego.py` (built drawings from parts when we have no drawing), `identity.py` (a NEW subject gets its own sound, look, mascot), `audience.py` (the age stage from the grade: kids 1–4, junior 5–7, teen 8–9, senior 10–12, and the wording per age), `explain_activities.py` (the 5 activities) → `check_scene` → saved by `core/storage.py`.
4. The page: GET `/explain/{book}` → `service.page_html` → `player/build_explain_player.py` (`pack` = the data of a book, `page_html` = puts the data into the template) → the browser runs `part3_core.js` (drawings, sounds, helpers) + `explain.js` (the scenes player) + the other JS files.
5. Optional AI: `llm_gateway.py` (talks to Gemini/OpenAI with keys from environment variables), `explain_llm.py`, `core/llm_scenes.py` (a model may write a scene; a teacher approves it; `core/contract.py` = the safety rules for model scenes). The model only CHOOSES from our lists; it never draws.

## Words used in this project (use them the same way)
- الجراف = the curriculum graph. مفهوم = concept. السهم / «بيحتاج» = prerequisite arrow. درس، موضوع، وحدة = lesson, topic, unit.
- المصنع = the factory (`02_question_factory`). المشهد = a scene. خطوة = a step inside a scene.
- المرحلة العمرية = age stage (أطفال / إعدادي / متوسط / ثانوي). الهوية = a subject's identity (sound + look + mascot).
- الليغو = drawings built from parts: key `lego:<main>:<extras>:<color>:<motion>`.
- مفتاح الرسمة = a drawing key like `sec:slope` or `lego:drawers::3:bob`; the page turns the key into an SVG picture.
- السيرفر = the FastAPI server. الصفحة = the one HTML page. المتصفح = the browser.

## Who reads the notes
Hareth (a student on the team) and **anyone** who opens the project: they may be beginners. They want to understand **what each file and each function does and why**, not line by line.

## Style (strict)
- **Jordanian Arabic**, simple, short, **no filler**, no exaggeration. One idea per sentence.
- Explain like to a smart beginner: say **what it does, what it takes, what it gives**, and **why it exists** when that helps. Use a small everyday comparison only when it really helps.
- Keep code names (function, file, variable names) in English exactly as in the code; write them plainly (the page will style them).
- Be **accurate**: read the real code. Never invent features. If something is only for tests or old/compatibility code, say so.
- Do NOT explain line by line. Do NOT explain basic Python/JS (what `for` or `import` means).
- No emojis except where the code itself uses them as names.
