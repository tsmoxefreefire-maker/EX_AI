# Interactive Explanation API · الشرح التفاعلي (FastAPI)

**أي جراف ← الشرح التفاعلي كامل.** السيرفر بيعطي **الصفحة نفسها** (بكل التفاعلات والأصوات)، والداتا JSON، ورسومات الشخصيات SVG. والمادة **الجديدة كلياً** بتاخد **هوية خاصة فيها** (صوت + شخصيات).

## التشغيل
```bash
pip install -r requirements.txt
uvicorn main:app --reload
# افتح http://127.0.0.1:8000/   (الكتب + «جراف جديد»)  ·  /explain (الصفحة)  ·  /docs (كل الطلبات)
```
أول مرة وما في كتب: **بيعمل الكتب الـ١٢ لحاله** (`EXPLAIN_SEED=0` بيوقّفها).

## الطلبات (Endpoints)
| الطلب | شو بيعمل |
|---|---|
| `GET /` | صفحة السيرفر: الكتب + صندوق «➕ جراف جديد» |
| `POST /explanations/generate` | `{"graph": {...}}` أو `{"graph_path": "x.json"}` (+ `"use_llm": true` اختياري: بيحسّن «ليش؟» و🆕 **بيختار هوية المادة الجديدة مرة وحدة**) ← **بيولّد** شرح كل الدروس **وبيحفظه** ← بيرجّع `page_url` و`identity` |
| `GET /explain` · `GET /explain/{book_id}` | **الصفحة التفاعلية** (كل الكتب · كتاب واحد) + 🆕 مشاهد الموديل اللي **وافق عليها المعلم** |
| `GET /explain-data?books=a,b` | نفس داتا الصفحة (JSON) |
| `GET /books` · `DELETE /books/{book_id}` · `POST /explanations/samples` | الكتب · احذف كتاب · اعمل الكتب الـ١٢ |
| `GET /books/{book_id}/lessons` | دروس كتاب |
| `GET /lessons/{lesson_id}/explanation` | **كل مشاهد الدرس** + الجمل + **روابط الرسومات** (`?include_llm=true` + مشاهد الموديل المقبولة) |
| `GET /concepts/{concept_id}/explanation` | مشاهد **مفهوم واحد** |
| 🧱 `GET /lego/parts` · `GET /lego/drawings` · `POST /lego/drawings/choose` | **ليغو الرسومات:** القطع · المكتبة اللي بتكبر (وخيارات الموديل) · المعلم بيختار رسمة ثانية أو بيرفض |
| `GET /art/{key}.svg?stage=kids` | **رسمة الشخصية** (وجهها حسب العمر) |
| `GET /scene-kinds` | **العقد**: كل نوع مشهد وشو حقوله |
| `/llm/…` | 🤖 مشاهد بيكتبها الموديل بأدوات قالبنا (فحص + مراجعة المعلم + صندوق معزول) |
| `GET /health` | السيرفر شغّال؟ |

## مثال للفرونت إند
```js
const r = await (await fetch("/explanations/generate", {method: "POST", headers: {"Content-Type": "application/json"},
                             body: JSON.stringify({graph})})).json();
location.href = r.page_url;                       // الصفحة كاملة لهالكتاب
// أو ارسم بنفسك: const data = await (await fetch("/explain-data?books=" + r.book_id)).json();
```

## الفحوصات
```bash
python -m unittest discover -s tests -v          # 51: الخدمة + الطلبات + الصفحة + المادة الجديدة + مشهد الموديل + 🧱 الليغو
python tests_browser/test_server_page.py         # 19: صفحة السيرفر بمتصفح حقيقي (بدها playwright)
python tests_browser/test_lego_page.py           # 10: 🧱 الليغو بالمتصفح
```
(ببيئتنا ما بنقدر ننزّل FastAPI، فشغّلنا الطلبات بنسخة تجريبية: `PYTHONPATH=tests/local_stub_only_for_sandbox` — **مش للإنتاج**.)

## إعدادات (متغيرات بيئة)
`EXPLAIN_DATA_DIR` (وين ينحفظ الشرح) · `EXPLAIN_FACTORY_DIR` (المصنع، افتراضياً `../02_question_factory`) · `EXPLAIN_SEED=0` · `EXPLAIN_CORS_ORIGINS` · مفاتيح الموديل: `GEMINI_API_KEY` / `OPENAI_API_KEY` / `ANTHROPIC_API_KEY` (أو `02_question_factory/api_key.txt`، **ما بينرفع على GitHub**).

## بعد ما تغيّر رسومات بالصفحة
```bash
python scripts/export_art.py      # الرسومات ← art/art.json (ملف واحد)
python scripts/refresh_doc.py     # الكود بملف الشرح EXPLANATION_API_AR.md
```

الشرح الكامل لكل ملف: **`EXPLANATION_API_AR.md`**.
