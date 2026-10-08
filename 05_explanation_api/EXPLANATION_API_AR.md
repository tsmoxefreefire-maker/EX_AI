# شرح كود الـ API (الشرح التفاعلي) · ملف واحد كامل

> كل ملف: **كوده كامل** + **شرحه بالعربي** (كل دالة: شو بتاخد، كيف بتقرر، شو بترجّع، وشو بيصير بالحالات الغريبة).

## الفكرة كلها بجملة
**أي جراف يدخل ← المصنع بيعمل مشاهد الشرح ← بنحفظها ← الـ API بيعطي: الصفحة التفاعلية نفسها (`/explain`، بكل التفاعلات والأصوات) + الداتا JSON + الرسومات SVG.** والمادة **الجديدة كلياً** بتاخد **هوية خاصة فيها**: صوت وشخصيات.

## 🆕 الدفعة ٢٩: 🧱 «ليغو الرسومات» (💡 فكرة حارث)
- **مفهوم ما إله رسمة** ← رسمة **مركّبة من قطع** بأسلوبنا: قطعة أساسية (الاستعارة) + وجه + لحد شارتين، بلون المفهوم وحركة.
- **المفتاح فيه الوصفة:** `lego:drawers:binary:3:wobble`. الصفحة (`lego.js`) والسيرفر (`core/art.py → lego_svg`) بيرسموها **نفس الشي بالحرف**.
- **مين بيقرر:** المكتبة المحفوظة ← كلمات المفهوم (بلا AI) ← (مع `use_llm`) **الموديل بيختار** من القطع، مرة وحدة، بفحص وحفظ.
- **طلبات جديدة:** `GET /lego/parts` · `GET /lego/drawings` · `POST /lego/drawings/choose` (المعلم). و`generate` بيرجّع `lego: {library, built, subject_character}`.
- **التفاصيل:** `02_question_factory/CHANGES_AR.md` ← الدفعة ٢٩. والكود الكامل تحت: `lego.py` و`lego.js`.

## 🆕 الدفعة ٢٨ (طلب حارث): ٦ تعديلات
- **📱 ترتيب الهاتف:** رقم ١ على اليمين بكل سطر (الصفحة نفسها، فبيوصل للسيرفر والمنشورة مع بعض).
- **🔄 التدوير:** شغل الطالب بيضل.
- **➜ كلمة السهم:** رياضيات «مبني على»، تاريخ «بسبب».
- **🤖 مشاهد الموديل المقبولة جوا `/explain`:** `llm_scenes.approved_for_page(book)` ← `service.page_data` ← `player.pack(…, extra=…)`. بس المشاهد اللي **وافق عليها المعلم**، وبنفس الصندوق المعزول.
- **🎭 الهوية بالموديل:** `POST /explanations/generate` مع `use_llm: true` ومادة جديدة مش من العائلات ← **استدعاء واحد** بيختار من قوائمنا ← فحص ← حفظ بـ `data/subject_identities.json`. الجواب فيه `identity.by_model`.
- **🖼️ ١٨ رسمة جديدة:** `art/art.json` صار فيه ١٣٧ رسمة.
- **التفاصيل وشرح الكود:** `02_question_factory/CHANGES_AR.md` ← الدفعة ٢٨.

## 🆕 الدفعة ٢٧ (طلب حارث): كل الشغل من FastAPI + هوية للمادة الجديدة
| | قبل | هلأ |
|---|---|---|
| **الصفحة** | ملف HTML لحاله (`explain.html`) | **السيرفر بيعطيها:** `GET /explain` (كل الكتب) · `GET /explain/{book_id}` (كتاب واحد). **نفس الصفحة المنشورة بالبايت** للكتب الـ١٢ (في فحص بيتأكد) |
| **جراف جديد** | الـ API بيعطي JSON بس | `POST /explanations/generate` ← بيرجّع `page_url` ← **افتحه وبتلاقي الشرح كامل**: المشاهد، الفعاليات الخمس، الأفلام، والأصوات |
| **الصفحة الرئيسية** | `/` كانت بتحوّل لـ `/docs` | `/` = **صفحة السيرفر**: الكتب + صندوق «جراف جديد» (اسحب ملف JSON ← ولّد ← افتح) |
| **🎭 المادة الجديدة** | صوت الجرس العام، وكل الشخصيات **نفس الدورق** والاسم **مقصوص** («وحدات إدخا») | **هوية خاصة فيها** (`02_question_factory/identity.py`): **صوت خاص** (آلة + مقام) · **شخصيات بشكلها** (💻 للحاسوب، 🎵 للموسيقى…) و**لون لكل مفهوم** و**الاسم كامل على سطرين** · **شخصية بتسلّم** باسمها («بِتّو» للحاسوب) · بتكبس على الشخصية ← **نغمة من آلتها** |
| **مادة ما في إلها كلمة بنعرفها** | — | **هوية ثابتة من اسمها**: نفس المادة دايماً نفس الصوت والشكل، ومادتين مختلفات تقريباً ما بيتشابهوا |
| **المصنع** | **نسختين** (`02_question_factory/` و`05_explanation_api/engine/`) | **نسخة وحدة**: الـ API بيستعمل `02_question_factory` مباشرة (ما في نسخ تختلف) |
| **الرسومات** | ١٢٠ ملف بمجلد `art/` | **ملف واحد** `art/art.json` (عشان GitHub) |
| **🐞 وجه الشخصية بـ `<img>`** | كانت تطلع **٥ تمّات وحواجب فوق بعض** (الرسمة ما بتشوف CSS الصفحة) | كل SVG **جواه قواعد الوجه**، وحسب العمر: `/art/{key}.svg?stage=senior` |
| **الكتب الـ١٢** | لازم تبنيها بإيدك | أول مرة السيرفر بيشتغل وما في كتب ← **بيعملهم لحاله** (`EXPLAIN_SEED=0` بيوقّفها) |

### 🎭 الهوية: مين بياخد شو
| المادة (كلمات من `book.subject`) | الشكل | الشخصية | الصوت |
|---|---|---|---|
| حاسوب / برمجة / تكنولوجيا / روبوت / Computer | 💻 لابتوب | بِتّو | **chip** (8-bit ناعم) |
| موسيقى / Music | 🎵 طبلة | نغّوم | **harp** (قيثارة) |
| فنون / رسم / تصميم / Art | 🎨 لوحة ألوان | لوّون | **vibes** (فايبرافون) |
| اقتصاد / محاسبة / أعمال / Economics | 💹 عملة | قرّوش | **steel** (طبل معدني) |
| تربية إسلامية / Islamic | 📗 كتاب أخضر (**بلا وجه، احتراماً**) | نور | harp هادي |
| تربية بدنية / رياضة / Sport | ⚽ طابة | كوّور | steel |
| صحة / تغذية / Health | 🩺 شنطة إسعاف | صحّوح | vibes |
| وطنية / اجتماعيات / Social Studies | 🏛️ مبنى | وطّون | marimba بمقام مختلف |
| فلسفة / منطق / تفكير | 💡 لمبة | فكّور | glass |
| فلك / فضاء / Astronomy | 🪐 كوكب | كوكوب | glass بمقام مختلف |
| زراعة | 🌾 كيس قمح | سنبول | kalimba |
| **أي إشي ثاني** | واحد من ٦ أشكال لطيفة (سداسي، نجمة، غيمة، درع، نقطة، جوهرة) | اسم من ٦ | آلة + مقام **من اسم المادة** |
**المواد السبعة اللي عنا** (علوم، رياضيات، فيزياء، كيمياء، جغرافيا، تاريخ، لغة) **ما تغيّر عليها إشي.** والكلمات **كلمة كاملة بس**: «طب» مش جوا «تطبيقية»، و«art» مش جوا «Earth».

## خريطة الملفات
```
05_explanation_api/
├── main.py            ← الباب: بيعمل تطبيق FastAPI وبيشبك الطلبات
├── api/
│   ├── schemas.py     ← أشكال اللي بيدخل وبيطلع (Pydantic)
│   └── routes.py      ← الطلبات (رفيعة: بتنادي الخدمة بس)
├── core/
│   ├── settings.py    ← وين الملفات + النسخة
│   ├── storage.py     ← قراءة وحفظ الملفات
│   ├── art.py         ← رسومات الشخصيات SVG
│   ├── contract.py    ← «العقد» مع الفرونت: كل نوع مشهد وحقوله + المراحل العمرية
│   ├── service.py     ← المنطق كله (بايثون عادي): توليد + الصفحة + الكتب الـ١٢ + حذف
│   └── llm_scenes.py  ← 🤖 مشاهد بيكتبها الموديل: توليد، فحص، حفظ، مراجعة المعلم، صندوق معزول
├── static/home.html   ← 🆕 صفحة السيرفر الرئيسية (الكتب + جراف جديد)
├── scripts/           ← export_art.py (كل الرسومات من الصفحة ← art/art.json)
├── art/art.json       ← 🆕 كل الرسومات بملف واحد: 119 رسمة + 25 شكل «شخصية المادة»
├── data/              ← (بينعمل لحاله) الجرافات اللي وصلت + الشرح المحفوظ
├── tests/             ← فحوصات الخدمة والـ API
└── tests_browser/     ← 🆕 test_server_page.py: صفحة السيرفر بمتصفح حقيقي
02_question_factory/   ← المصنع (نفسه للصفحة وللـ API) + identity.py 🆕 + examples/ (مادة جديدة للتجربة)
```

## ⚙️ كيف بيشتغل وشو بيستعمل
| | بيستعمل |
|---|---|
| الطلبات | **FastAPI** (بايثون) + **Pydantic** للأشكال + **uvicorn** للتشغيل |
| صنع المشاهد | **المصنع (engine)**: بايثون عادي (قواعد)، **بلا AI** |
| الرسومات | **SVG من مكتبتنا** بملف واحد (`art/art.json`)، وكل رسمة جواها قواعد الوجه حسب العمر |
| 📖 الصفحة | **نفس صفحة الشرح** (`02_question_factory/player`): السيرفر بيحط فيها الكتب اللي عنده (`/explain`) |
| 🎭 هوية المادة الجديدة | `02_question_factory/identity.py`: **كلمات + حساب ثابت من اسم المادة**. **بلا AI** |
| 🤖 AI (اختياري) | `use_llm: true` ← **Gemini ← GPT ← Claude** بيحسّن فقرات «ليش؟» (بالمفاتيح اللي على السيرفر) |
| الحفظ | **ملفات JSON** بمجلد `data/` (بيتولّد **مرة** وبيرجع **فوراً** بعدين) |
| 👥 العمر | `engine/audience.py`: **صف الكتاب ← المرحلة** (kids/junior/teen/senior) و**الكلام حسب العمر**. **كود عادي، بلا AI** |
| 🤖 مشاهد الموديل | `core/llm_scenes.py` + `engine/scene_writer.py`: الموديل (**Gemini ← GPT ← Claude**) بيكتب `buildScene(SDK, data)` بأدوات قالبنا ← **فحص** (ممنوعات + حجم + `node --check`) ← **جولة تصليح وحدة** ← **بانتظار المعلم** ← **صندوق معزول** (iframe sandbox + CSP بلا إنترنت) |

## 🖼️ هل الـ API بيطلع نفس نتيجة الصفحة؟
**المحتوى نفسه ١٠٠٪، والشكل بيعتمد على مين بيرسم.**

### ✅ شو نفسه
**نفس المشاهد، نفس الجمل، نفس الرسومات، نفس البطاقات.** السبب: الصفحة والـ API بيستعملوا **نفس المصنع** (`explain_generator.py`). الصفحة بتحط الداتا **جواها**، والـ API بيبعتها **JSON**.

### ❓ شو ممكن يختلف
**الشكل والتفاعل** (وين الفقاعة، الكاميرا، العدسة…). هاد **شغل الفرونت إند**:
| الفرونت إند… | النتيجة |
|---|---|
| **بيستعمل مشغّلنا** (كود الصفحة: `03_explain_player_src`) | **نفس الصفحة بالضبط** |
| **بيرسم بطريقته** | نفس المحتوى، بس الشكل حسب شغلهم، و**ممكن يقعوا بنفس الأغلاط اللي صلّحناها** (تحت) |

### 🧭 كيف كل حقل بيطلع على الشاشة (أمثلة من `GET /lessons/{id}/explanation`)
| الحقل | كيف بيبين |
|---|---|
| `steps` | **سطر الراوي** تحت الصورة، جملة بكل خطوة |
| `paragraph` | **«💡 ليش؟»** فقرة أطول تحت المشهد |
| `art` | رابط **رسمة الشخصية** (`/art/{key}.svg`) |
| `flip.cards[].front` / `.back` | **الوجه = السؤال**، **الضهر = جملة كاملة**، والسؤال صغير فوقها لما تنقلب. **٢×٢** |
| `dialogue.lines[]` | كل سطر = **فقاعة فوق اللي بيحكي** (`who`) + سطر بالمحادثة |
| `interview.qa[]` | أزرار أسئلة (`q`)، والجواب (`a`) **فقاعة** + شات |
| `lens.facts[]` | معلومات **مخبّاية بالضباب**، بتطلع **كاملة** لما **الطالب** يحرّك العدسة عليها (ما بتتحرك لحالها) |
| `before_after.mode` | `becomes` ← «قبل/بعد» واللي قبل **بيختفي** بالجديد · `needs` ← «أول/وبعدين»: الأول **بيضل**، والثاني بيجي مع سهم «بيحتاج» و`why` |
| `meet.focus[]` | لكل خطوة **مين نضوّي** ونحرّك الكاميرا عليه |
| `edges [a, b]` | سهم **من b لـ a** وعليه «بيحتاج» (يعني b بيحتاج a) |

### ⚠️ قواعد الرسم اللي اتعلمناها (للفرونت إند)
1. **الفقاعة بطبقة فوق كل إشي** (فوق الضوء الغامق وفوق الشخصيات) ← ما بتعتم.
2. **الفقاعة دايماً جوا الإطار اللي بيشوفه الطالب** (حتى لو الكاميرا مقرّبة)، وإلها **ذيل** على اللي بيحكي.
3. **الكلام الطويل يتلف على سطور** (حوالي ٢٢ حرف بالسطر)، **وما ينقص بنص كلمة**.
4. **على التلفون الفقاعة أكبر** (الكلام ≥ ١٣px).
5. **الحركات بالوقت** (مش بعدد الإطارات) ← نفس السرعة على تلفون ضعيف.
6. **ولا حركة CSS على عنصر إله مكان (`transform`)** ← الحركة على عنصر جوّاه، وإلا بيقفز لزاوية الصورة.
7. **أسماء class خاصة** ← اسم مشترك مع مكوّن ثاني بيخرّب بصمت.

### 🔁 المصنع بمكان واحد (الدفعة ٢٧)
كان المصنع **بمكانين** (`02_question_factory/` ونسخة بـ `05_explanation_api/engine/`)، وكان لازم نتذكر ننسخ كل تعديل. **هلأ في نسخة وحدة:** الـ API بيستعمل `02_question_factory` مباشرة (`core/settings.py` ← `FACTORY_DIR`، وبيتغير بمتغير البيئة `EXPLAIN_FACTORY_DIR`). فالصفحة والـ API **ما بيختلفوا أبداً**.

### 🧪 تجربة كل واحد
| | كيف |
|---|---|
| **الصفحة** (الشكل) | بتفتح الرابط وبتشوف بعينك + فحوصات المتصفح (`tests_browser/`) |
| **الـ API** (كله) | `uvicorn main:app --reload` ← افتح `/` (الكتب + جراف جديد) · `/explain` (الصفحة) · `/docs` (كل الطلبات) |

---

## `main.py`

**الباب.** بيعمل تطبيق FastAPI باسم ونسخة ووصف (هدول بيطلعوا بصفحة `/docs`)، وبيسمح للفرونت إند يطلب من دومين ثاني (**CORS**، والمسموحين من متغير بيئة)، وبيشبك كل الطلبات من `api/routes.py`. (🆕 `/` صارت **صفحة السيرفر** بـ `routes.py`، مش تحويل لـ `/docs`.)

```python
"""The door of the service: creates the FastAPI app and plugs in the endpoints.
Run:  uvicorn main:app --reload  → open http://127.0.0.1:8000/  (the books + send a graph) · /explain (the page) · /docs (every endpoint)"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import router
from core import settings

app = FastAPI(title="Interactive Explanation API · الشرح التفاعلي", version=settings.API_VERSION,
              description="بياخد أي جراف وبيعمل الشرح التفاعلي كامل: الصفحة نفسها (/explain) بكل التفاعلات والأصوات، "
                          "والداتا (JSON) ورسومات الشخصيات (SVG) لأي فرونت إند. المادة الجديدة بتاخد هوية خاصة فيها (صوت وشخصيات).")
app.add_middleware(CORSMiddleware, allow_origins=settings.CORS_ORIGINS, allow_methods=["*"], allow_headers=["*"])
app.include_router(router)
```

---

## `api/schemas.py`

> 🆕 **الدفعة ٢٥:** أشكال طلبات «مشاهد الموديل»: `LLMSceneRequest` (الكتاب، الدرس، مفهوم اختياري، **فكرة المعلم** اختيارية، `max_scenes` من ١ لـ ١٠ = حد التكلفة، `force`) · `LLMSceneSummary` و`LLMSceneResponse` (الحالة: `pending_review`/`approved`/`rejected` + المشاكل + رابط الصندوق) · `ReviewRequest` (قرار المعلم) · `BrowserReport` (شو شاف المتصفح).

**أشكال الداتا.** FastAPI بيستعملها عشان: (١) **يفحص الطلب** (لو حدا بعت إشي غلط بيرد عليه بخطأ واضح)، (٢) **يكتب صفحة `/docs`** لحاله.
- `GenerateRequest`: **إما** الجراف نفسه (`graph`) **أو** اسم ملفه (`graph_path`)، و`use_llm` (هل نستعمل الموديل).
- `GenerateResponse`: ملخّص اللي انعمل: الكتاب، دروسه (كل درس: كم مفهوم وكم مشهد)، مجموع المشاهد، الوقت، الموديل اللي استُعمل، والتحذيرات.
- `BookSummary` و`LessonSummary` و`Health`: أشكال صغيرة للقوائم وفحص السيرفر.
- **ليش مشاهد الدرس `Dict` مش شكل مفصّل؟** لأنه في **١٣ نوع مشهد**، والعقد التفصيلي موجود بـ `/scene-kinds`، فبنخلي الشكل **مرن** وما بنكرر.

```python
"""The shapes of what goes IN and OUT of the API (Pydantic). FastAPI uses them to check requests and to write the /docs page."""
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class GenerateRequest(BaseModel):
    graph: Optional[Dict[str, Any]] = Field(None, description="الجراف نفسه (JSON): book + nodes + relationships + node_content")
    graph_path: Optional[str] = Field(None, description="أو اسم جراف محفوظ بمجلد data/graphs")
    use_llm: bool = Field(False, description="الموديل يحسّن فقرات «ليش؟» (إذا في مفتاح على السيرفر)")


class LessonSummary(BaseModel):
    lesson_id: str
    title: str
    concepts: int
    scenes: int


class Identity(BaseModel):
    """🎭 The subject's identity: a NEW subject gets its own sound and characters (identity.py)."""
    new: bool = False
    family: Optional[str] = Field(None, description="computer · music · art · economy · religion · sport · health · civics · thinking · space · farming · chosen (by the model) · new")
    by_model: bool = Field(False, description="True: the model chose it (use_llm, once per new subject)")
    label: str = ""
    emblem: Optional[str] = Field(None, description="the shape of its characters (💻 🎵 🎨 …)")
    mascot_name: Optional[str] = None
    sound: Optional[Dict[str, Any]] = Field(None, description="{instr, root, scale}: its own instrument (null = the known subject's own)")


class LegoSummary(BaseModel):
    """🧱 How the book's concepts got their pictures."""
    library: int = Field(0, description="من مكتبة الرسومات الجاهزة")
    built: int = Field(0, description="🧱 مركّبة من قطع (ليغو)")
    subject_character: int = Field(0, description="شخصية المادة مع اسم المفهوم (ما في رسمة)")


class LegoChoice(BaseModel):
    """The teacher's decision about a built drawing."""
    name: str = Field(..., description="اسم المفهوم زي ما هو بالجراف")
    pick: Optional[int] = Field(None, description="رقم الاقتراح: 0 أو 1 أو 2")
    reject: bool = Field(False, description="true = لا، رجّع شخصية المادة")


class GenerateResponse(BaseModel):
    book_id: str
    title: str
    subject: str = ""
    grade: Optional[int] = None
    stage: Optional[str] = Field(None, description="kids · junior · teen · senior (from the grade)")
    identity: Optional[Identity] = None
    lego: Optional[LegoSummary] = None
    lessons: List[LessonSummary]
    scenes: int
    generated_at: str
    llm: Optional[str] = None
    version: str
    page_url: Optional[str] = Field(None, description="افتح هالرابط: الصفحة التفاعلية لهالكتاب")
    warnings: List[str] = []


class BookSummary(BaseModel):
    book_id: str
    title: str
    subject: str = ""
    grade: Optional[int] = None
    stage: Optional[str] = None
    identity: Optional[Identity] = None
    scenes: int
    generated_at: str
    page_url: Optional[str] = None


class Health(BaseModel):
    status: str
    version: str


# ---------- 🤖 scenes written by the model (option «ج»: the model writes ONE scene with our toolkit) ----------
class LLMSceneRequest(BaseModel):
    book_id: str = Field(..., description="الكتاب (لازم يكون انعمله /explanations/generate قبل)")
    lesson_id: str = Field(..., description="الدرس")
    concept_id: Optional[str] = Field(None, description="مفهوم واحد (إذا فاضي: مفاهيم الدرس بالترتيب لحد max_scenes)")
    idea: Optional[str] = Field(None, description="فكرة من المعلم للفعالية (اختياري)، مثلاً: «الطالب يسحب الإلكترون من ذرة لذرة»")
    max_scenes: int = Field(1, ge=1, le=10, description="حد التكلفة: كم مشهد بهالطلب")
    force: bool = Field(False, description="اسأل الموديل من جديد حتى لو في مشهد محفوظ لنفس المفهوم والفكرة")


class LLMSceneSummary(BaseModel):
    scene_id: str
    concept_id: str
    concept: Optional[str] = None
    status: str                                   # pending_review · approved · rejected
    problems: List[str] = []
    attempts: Optional[int] = None
    provider: Optional[str] = None
    reused: bool = False
    runner_url: str


class LLMSceneResponse(BaseModel):
    book_id: str
    lesson_id: str
    scenes: List[LLMSceneSummary]
    warnings: List[str] = []


class ReviewRequest(BaseModel):
    approve: bool = Field(..., description="true = يوصل للطلاب · false = لا")
    note: Optional[str] = Field(None, description="ملاحظة المعلم")


class BrowserReport(BaseModel):
    ok: bool
    drawn: int = 0
    outside: int = 0
    errors: List[str] = []
    done: Optional[str] = None
```

---

## `api/routes.py`

> 🆕 **الدفعة ٢٥:** `GET /lessons/{id}/explanation?include_llm=true` (بيزيد مشاهد الموديل **المقبولة بس**) + ٧ طلبات جديدة تحت `/llm/…`: `POST /llm/scenes/generate` · `GET /llm/scenes` · `GET /llm/scenes/{id}` · `GET /llm/scenes/{id}/runner.html` (الصندوق، ومعه هيدر CSP بلا إنترنت) · `POST /llm/scenes/{id}/review` · `POST /llm/scenes/{id}/report` · `GET /llm/sdk`. وأخطاء `llm_scenes` كمان بتتحوّل لـ 404/400.

**الطلبات.** كل طلب **رفيع**: بينادي دالة من `core/service.py` وبس.
- `_call`: بتشغّل دالة الخدمة، ولو رمت `NotFound` بترجّع **404**، ولو `BadInput` بترجّع **400**. هيك كل الطلبات **بتتعامل مع الأخطاء بنفس الطريقة**.
- `/health`: «السيرفر شغّال» + النسخة.
- `/scene-kinds`: العقد (من `contract.py`).
- `POST /explanations/generate`: بياخد الطلب وبينادي `service.generate`.
- `/books`، `/books/{id}/lessons`، `/lessons/{id}/explanation`، `/concepts/{id}/explanation`: قراءة اللي انحفظ. `book_id` **اختياري** بالدرس والمفهوم (إذا ما انبعت، بندوّر بكل الكتب).
- `/art/{key}.svg`: بيرجّع **نص الـ SVG** بنوع `image/svg+xml`، ومعه **تخزين بالمتصفح يوم كامل** (الرسمة ما بتتغير).

```python
"""The endpoints. Each one is THIN: it calls the service and turns its errors into HTTP codes (NotFound → 404, BadInput → 400)."""
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import HTMLResponse, Response

from api.schemas import (BookSummary, BrowserReport, GenerateRequest, GenerateResponse, Health, LegoChoice, LessonSummary, LLMSceneRequest,
                         LLMSceneResponse, LLMSceneSummary, ReviewRequest)
from core import contract, llm_scenes, service, settings

router = APIRouter()


def _call(fn, *args, **kwargs):
    try:
        return fn(*args, **kwargs)
    except (service.NotFound, llm_scenes.NotFound) as e:
        raise HTTPException(status_code=404, detail=str(e))
    except (service.BadInput, llm_scenes.BadInput) as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/health", response_model=Health, tags=["system"])
def health():
    return {"status": "ok", "version": settings.API_VERSION}


# ---------- 📖 the PAGE: the same interactive page as the published one, for ANY graph on the server ----------
@router.get("/", response_class=HTMLResponse, include_in_schema=False)
def home():
    """The server's front page: the books, and a box to send a new graph."""
    service.ensure_samples()
    return HTMLResponse(content=_call(service.home_html))


@router.get("/explain", response_class=HTMLResponse, tags=["page"])
def explain_page(books: Optional[str] = Query(None, description="كتب معيّنة: b1,b2 (فاضي = كل الكتب)")):
    """The interactive page with every book on the server (scenes, the 5 activities, films, sounds per subject and age)."""
    service.ensure_samples()
    ids = [b.strip() for b in books.split(",")] if books else None
    return HTMLResponse(content=_call(service.page_html, ids))


@router.get("/explain/{book_id}", response_class=HTMLResponse, tags=["page"])
def explain_book_page(book_id: str):
    """The interactive page of ONE book (e.g. the one you just sent with /explanations/generate → its «page_url»)."""
    return HTMLResponse(content=_call(service.page_html, [book_id]))


@router.get("/explain-data", tags=["page"])
def explain_data(books: Optional[str] = Query(None, description="b1,b2 (فاضي = كل الكتب)")) -> Dict[str, Any]:
    """Exactly what the page receives (for a front end that wants to draw the page itself)."""
    service.ensure_samples()
    ids = [b.strip() for b in books.split(",")] if books else None
    return _call(service.page_data, ids)


@router.get("/scene-kinds", tags=["contract"])
def scene_kinds() -> Dict[str, Any]:
    """The contract: every scene kind, what it means and its fields (for the front end)."""
    return contract.describe()


@router.post("/explanations/generate", response_model=GenerateResponse, tags=["explanations"])
def generate(req: GenerateRequest):
    """Graph → explanations for every lesson (kept on the server; generated once, then served instantly)."""
    return _call(service.generate, graph=req.graph, graph_path=req.graph_path, use_llm=req.use_llm)


@router.post("/explanations/samples", response_model=List[GenerateResponse], tags=["explanations"])
def samples(force: bool = Query(False, description="true = اعملهم كلهم من جديد")):
    """Make the 12 sample books (grade 4 → 12) on the server."""
    return _call(service.seed_samples, force=force in (True, "true", "1", 1))


@router.get("/books", response_model=List[BookSummary], tags=["explanations"])
def books():
    service.ensure_samples()
    return service.list_books()


@router.delete("/books/{book_id}", tags=["explanations"])
def delete_book(book_id: str) -> Dict[str, Any]:
    """Remove a book from the server (its explanations and its graph)."""
    return _call(service.delete_book, book_id)


@router.get("/books/{book_id}/lessons", response_model=List[LessonSummary], tags=["explanations"])
def lessons(book_id: str):
    return _call(service.list_lessons, book_id)


@router.get("/lessons/{lesson_id}/explanation", tags=["explanations"])
def lesson_explanation(lesson_id: str, book_id: Optional[str] = Query(None),
                       include_llm: bool = Query(False, description="زيد المشاهد اللي كتبها الموديل وانقبلت من المعلم")) -> Dict[str, Any]:
    """All the scenes of one lesson + texts + picture URLs + «audience» (the age stage). See /scene-kinds for the fields."""
    return _call(service.get_lesson, lesson_id, book_id, include_llm=include_llm)


@router.get("/concepts/{concept_id}/explanation", tags=["explanations"])
def concept_explanation(concept_id: str, book_id: Optional[str] = Query(None)) -> Dict[str, Any]:
    return _call(service.get_concept, concept_id, book_id)


# ---------- 🧱 Lego drawings (batch 29): a concept with no drawing gets one BUILT from our parts ----------
@router.get("/lego/parts", tags=["lego"])
def lego_parts() -> Dict[str, Any]:
    """The parts (main + badges + motions) and what each can mean — the same list the model chooses from."""
    return service.lego_parts()


@router.get("/lego/drawings", tags=["lego"])
def lego_drawings() -> List[Dict[str, Any]]:
    """Every drawing built so far (the library that grows): its picture, the model's other suggestions, and its status
    (auto = the model's first choice, used now · approved = a teacher picked it · rejected = back to the subject character)."""
    return service.lego_library()


@router.post("/lego/drawings/choose", tags=["lego"])
def lego_choose(req: LegoChoice) -> Dict[str, Any]:
    """The teacher picks another suggestion (pick) or says no (reject). The saved books show the change at once."""
    return _call(service.lego_choose, req.name, req.pick, req.reject)


@router.get("/art/{key}.svg", tags=["art"])
def art_svg(key: str, stage: str = Query("kids", description="kids · junior · teen · senior (the face changes with the age)")):
    """A character as SVG (the key comes from «icons»/«art» in the lesson; URL-encoded). It carries its own face rules."""
    svg = _call(service.get_art, key, stage)
    return Response(content=svg, media_type="image/svg+xml", headers={"Cache-Control": "public, max-age=86400"})


# ---------- 🤖 scenes written by the model (with our template's toolkit) ----------
@router.post("/llm/scenes/generate", response_model=LLMSceneResponse, tags=["llm scenes"])
def llm_generate(req: LLMSceneRequest):
    """The model writes a NEW scene for a concept, with our toolkit (SDK). Checked automatically; waits for a teacher (pending_review)."""
    return _call(llm_scenes.generate, req.book_id, req.lesson_id, concept_id=req.concept_id, idea=req.idea,
                 max_scenes=req.max_scenes, force=req.force)


@router.get("/llm/scenes", response_model=List[LLMSceneSummary], tags=["llm scenes"])
def llm_list(book_id: Optional[str] = Query(None), lesson_id: Optional[str] = Query(None), status: Optional[str] = Query(None)):
    return _call(llm_scenes.list_scenes, book_id, lesson_id, status)


@router.get("/llm/scenes/{scene_id}", tags=["llm scenes"])
def llm_get(scene_id: str, book_id: Optional[str] = Query(None)) -> Dict[str, Any]:
    """Everything about one scene: the code, the checks, the data the model got, the review."""
    return _call(llm_scenes.get_scene, scene_id, book_id)


@router.get("/llm/scenes/{scene_id}/runner.html", response_class=HTMLResponse, tags=["llm scenes"])
def llm_runner(scene_id: str, book_id: Optional[str] = Query(None)):
    """The sandbox page. Use it ONLY inside <iframe sandbox="allow-scripts"> (its CSP blocks every network request)."""
    html = _call(llm_scenes.runner, scene_id, book_id)
    return HTMLResponse(content=html, headers={"Content-Security-Policy": "default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; img-src data:; sandbox allow-scripts"})


@router.post("/llm/scenes/{scene_id}/review", response_model=LLMSceneSummary, tags=["llm scenes"])
def llm_review(scene_id: str, req: ReviewRequest, book_id: Optional[str] = Query(None)):
    """The teacher approves (students will see it) or rejects."""
    return _call(llm_scenes.review, scene_id, req.approve, req.note, book_id)


@router.post("/llm/scenes/{scene_id}/report", tags=["llm scenes"])
def llm_report(scene_id: str, req: BrowserReport, book_id: Optional[str] = Query(None)) -> Dict[str, Any]:
    """What the browser saw when the scene ran (sent by the preview page): drew? everything inside? errors?"""
    return _call(llm_scenes.report, scene_id, req.model_dump(), book_id)


@router.get("/llm/sdk", tags=["llm scenes"])
def llm_sdk() -> Dict[str, Any]:
    """What the model may use (the toolkit), the rules per age, what is forbidden, an example, and how to embed the sandbox."""
    return llm_scenes.sdk_doc()
```

---

## `core/settings.py`

**وين كل إشي.** مسارات المجلدات، النسخة، ومين مسموح يطلب (CORS). بيتغيروا **بمتغيرات بيئة** بلا ما نلمس الكود.
- 🆕 `FACTORY_DIR` = `../02_question_factory` (**المصنع نفسه**، مش نسخة) · `PAGE_TEMPLATE` (قالب الصفحة) · `SAMPLES_DIR` (الكتب الـ١٢) · `ART_FILE` (الرسومات بملف واحد) · `SEED_SAMPLES` (أول مرة بلا كتب ← بيعمل الـ١٢؛ `EXPLAIN_SEED=0` بيوقّفها) · النسخة صارت `2.0.0`.

```python
"""Where everything lives (paths) and the service's version. Change folders with environment variables, no code changes."""
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))          # 05_explanation_api/
# the explanation FACTORY (plain Python): the SAME code that builds the published page — no copy of it here any more
FACTORY_DIR = os.environ.get("EXPLAIN_FACTORY_DIR", os.path.join(os.path.dirname(BASE_DIR), "02_question_factory"))
ENGINE_DIR = FACTORY_DIR                                                        # (old name, kept for older code)
PLAYER_DIR = os.path.join(FACTORY_DIR, "player")                                # the page's builder + its template
PAGE_TEMPLATE = os.path.join(PLAYER_DIR, "explain_template.html")               # built from 03_explain_player_src (build_explain_template.py)
SAMPLES_DIR = FACTORY_DIR                                                       # the 12 sample books (*_book_graph.json)
ART_FILE = os.path.join(BASE_DIR, "art", "art.json")                            # every character drawing, in ONE file
DATA_DIR = os.environ.get("EXPLAIN_DATA_DIR", os.path.join(BASE_DIR, "data"))   # generated explanations are kept here
GRAPHS_DIR = os.path.join(DATA_DIR, "graphs")                                   # the graphs we received
BOOKS_DIR = os.path.join(DATA_DIR, "books")                                     # one folder per book: lessons/<id>/explanations.json
SEED_SAMPLES = os.environ.get("EXPLAIN_SEED", "1") != "0"                      # first start with no books: make the 12 sample books
API_VERSION = "2.0.0"
CORS_ORIGINS = [o.strip() for o in os.environ.get("EXPLAIN_CORS_ORIGINS", "*").split(",") if o.strip()]
```

---

## `core/storage.py`

**القراءة والحفظ (بس).** ما فيه منطق عن «كيف نشرح»، بس «وين الملفات».
- `book_dir`: مجلد كل كتاب.
- `save_meta`: بيحفظ **ملخّص الكتاب** (`meta.json`).
- `list_books`: كل الكتب اللي إلها ملخّص.
- `book_meta` / `lesson_ids` / `load_lesson`: قراءة ملخّص، أرقام الدروس، ودرس كامل. **لو الملف مش موجود بترجّع `None`** (والخدمة بتحوّلها لـ 404).
- `find_lesson`: بتدوّر على الدرس **بكتاب معيّن أو بكل الكتب**.

```python
"""Reading what the factory saved: books, lessons, concepts (JSON files on disk). No logic about HOW to explain — only WHERE things are."""
import json
import os
import shutil

from core import settings


def _read(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def book_dir(book_id: str) -> str:
    return os.path.join(settings.BOOKS_DIR, book_id)


def save_meta(book_id: str, meta: dict) -> None:
    os.makedirs(book_dir(book_id), exist_ok=True)
    with open(os.path.join(book_dir(book_id), "meta.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)


def list_books() -> list:
    if not os.path.isdir(settings.BOOKS_DIR):
        return []
    out = []
    for b in sorted(os.listdir(settings.BOOKS_DIR)):
        p = os.path.join(settings.BOOKS_DIR, b, "meta.json")
        if os.path.exists(p):
            out.append(_read(p))
    return out


def book_meta(book_id: str):
    p = os.path.join(book_dir(book_id), "meta.json")
    return _read(p) if os.path.exists(p) else None


def lesson_ids(book_id: str) -> list:
    p = os.path.join(book_dir(book_id), "explain_index.json")
    return _read(p)["lessons"] if os.path.exists(p) else []


def load_lesson(book_id: str, lesson_id: str):
    p = os.path.join(book_dir(book_id), "lessons", lesson_id, "explanations.json")
    return _read(p) if os.path.exists(p) else None


def save_lesson(book_id: str, lesson_id: str, rec: dict) -> None:
    """Write a lesson back (used when a teacher picks another Lego drawing: only its picture keys change)."""
    p = os.path.join(book_dir(book_id), "lessons", lesson_id, "explanations.json")
    with open(p, "w", encoding="utf-8") as f:
        json.dump(rec, f, ensure_ascii=False, indent=2)


def find_lesson(lesson_id: str, book_id: str = None):
    """The lesson in a given book, or in any book (lesson ids are unique inside the platform's graph)."""
    books = [book_id] if book_id else [m["book_id"] for m in list_books()]
    for b in books:
        rec = load_lesson(b, lesson_id)
        if rec is not None:
            return b, rec
    return None, None


def delete_book(book_id: str) -> None:
    """Remove a book's explanations (its folder)."""
    shutil.rmtree(book_dir(book_id), ignore_errors=True)
```

---

## `core/art.py`

**الرسومات** (🆕 الدفعة ٢٧: ملف واحد + شخصيات المادة الجديدة + قواعد الوجه).
- `_art`: بيقرأ `art/art.json` **مرة وحدة**: `files` (مفتاح ← نص الـ SVG) + `subject_templates` (لكل شكل مادة: الرسمة **بفراغات** للون والاسم).
- `art_url`: بيحوّل مفتاح الرسمة (مثلاً 🫚) لرابط جاهز `/art/%F0%9F%AB%9A.svg`.
- `subj_label`: **الاسم كامل** على سطر أو سطرين (بيقسم عند المسافة اللي بتخلّي السطرين أقرب لبعض)، وحجم الخط حسب الطول (الحرف العربي ≈ نص حجم الخط: قسناها بالمتصفح)، ولو لسا طويل بيتضغط ليدخل (**ما بينقص أبداً**). سطرين ← الخط **١٢ بالأكثر** عشان الوجه يضل فاضي.
- `subj_color`: **لون لكل مفهوم** من اسمه (نفس قائمة الصفحة).
- `name_block`: مربع الاسم الأبيض والسطور، **بنفس أرقام الصفحة بالزبط** (`_r1` و`_num` بيكتبوا الأرقام زي JavaScript، عشان الـ SVG يطلع **نفسه حرف بحرف**).
- `subject_svg`: قالب الشكل + اللون + الاسم ← شخصية جاهزة.
- `with_face_rules`: 🐞 **التصليح:** الرسمة اللي بتنحط بـ `<img>` ما بتشوف CSS الصفحة، فكان الوجه يطلع **بالـ٥ تمّات والحواجب مع بعض**. هلأ بنحط **قواعد الوجه جوا الرسمة** حسب العمر (الصغار وجه كامل ← الثانوي بلا وجه).
- `art_svg(key, stage)`: (١) رسمة إلها ملف ← هي. (٢) `subj:💻:الذاكرة` ← **شخصية المادة** باسمها ولونها. (٣) غير هيك ← `None` (404). `stage` ← مع قواعد الوجه؛ بدونه ← الرسمة **عارية** (لصندوق مشهد الموديل اللي بيحط CSS تبعه).
- **فحص بالمتصفح** (`tests_browser/test_server_page.py`) بيتأكد إنه الـ API بيرسم **نفس شخصيات الصفحة بالزبط** (٢٥ شكل × ٧ أسماء).

```python
"""The characters as SVG for any front end: /art/<key>.svg  (the SAME drawings the page draws).

   · All drawings live in ONE file: art/art.json  ({"files": {key: svg}, "subject_templates": {emblem: svg with holes}})
     — one file instead of 120, so the folder goes up to GitHub in one go. Made by scripts/export_art.py from the built page.
   · «subj:<emblem>:<name>» keys (a concept with no drawing of its own, or a NEW subject's character): the emblem's
     template + the concept's own colour + its WHOLE name on 1–2 lines. This mirrors ARTS.subject in the page
     (03_explain_player_src/part3_core.js) line by line, and a browser test checks both give the SAME SVG.
   · 🐞 fixed (batch 27): a drawing given to an <img> cannot see the page's CSS, so the face showed its 5 mouths, the brows
     and the joy eyes all at once. Every SVG now carries its own face rules (the same ones as the page), per age stage."""
import json
import math
import re

from core import settings

_ART = None

# the face rules of each age stage (the same as the page's stage.css and the lab's drawing.js)
FACE_CSS = {"base": ".m,.ejoy,.brows{display:none}.m-happy{display:inline}",
            "junior": ".scheek{display:none}",
            "teen": ".scheek,.brows,.m{display:none!important}",
            "senior": ".sface{display:none!important}[stroke=\"#3b2a1a\"]{stroke-width:1.6px}"}
STAGES = ("kids", "junior", "teen", "senior")

# the colours of a new subject's characters: (fill, ink) — the same list as SUBJ_COLORS in the page
SUBJ_COLORS = (("#7CC6F2", "#2F6FA8"), ("#F6C177", "#9A6416"), ("#A3D9A5", "#2E7D3A"), ("#C4A7E7", "#6A45A8"),
               ("#F5A97F", "#B5532A"), ("#9CCFD8", "#2E7A86"), ("#EBBCBA", "#A8505A"), ("#F2D479", "#8A6D0B"))


def _art():
    global _ART
    if _ART is None:
        with open(settings.ART_FILE, encoding="utf-8") as f:
            _ART = json.load(f)
    return _ART


def art_url(icon: str) -> str:
    """The URL the front end puts in <img src>: /art/<the picture key, URL-encoded>.svg"""
    import urllib.parse
    return "/art/" + urllib.parse.quote(icon or "🔹", safe="") + ".svg"


# ---------- the same little maths as the page (JavaScript numbers → the same text) ----------
def _r1(v: float) -> float:
    """JavaScript Math.round(v*10)/10 (rounds .5 up, like the page)."""
    return math.floor(v * 10 + 0.5) / 10


def _num(v) -> str:
    """A number written the way JavaScript writes it: 14 (not 14.0), 24.3."""
    v = float(v)
    return str(int(v)) if v.is_integer() else repr(v)


def _jslen(s: str) -> int:
    """String length the way JavaScript counts it (UTF-16 units)."""
    return len(s.encode("utf-16-le")) // 2


def subj_color(label: str) -> tuple:
    n = sum(int.from_bytes(label.encode("utf-16-le")[i:i + 2], "little") for i in range(0, len(label.encode("utf-16-le")), 2))
    return SUBJ_COLORS[n % len(SUBJ_COLORS)]


def subj_label(label: str) -> tuple:
    """(lines, font size): the WHOLE name on 1 or 2 lines (split where the two halves are most equal), never cut."""
    t = re.sub(r"\s+", " ", re.sub(r'[<&>"]', "", str(label or ""))).strip()
    if not t:
        return [], 0
    lines, w = [t], t.split(" ")
    if _jslen(t) > 9 and len(w) > 1:
        best = None
        for i in range(1, len(w)):
            a, b = " ".join(w[:i]), " ".join(w[i:])
            m = max(_jslen(a), _jslen(b))
            if best is None or m < best[0]:
                best = (m, [a, b])
        lines = best[1]
    n = max(_jslen(x) for x in lines)
    return lines, max(7, min(12 if len(lines) > 1 else 15, math.floor(128 / n)))


def name_block(x: float, y: float, ink: str, lines: list, fs: int) -> str:
    if not lines:
        return ""
    lh = _r1(fs * 1.2)
    h = _r1(len(lines) * lh + 6)
    top = _r1(y - 4 - h / 2)
    out = f'<rect x="{_num(x - 36)}" y="{_num(top)}" width="72" height="{_num(h)}" rx="{_num(min(10, _r1(h / 2)))}" fill="#fff" stroke="{ink}" stroke-width="2"/>'
    for i, t in enumerate(lines):
        fit = ' textLength="66" lengthAdjust="spacingAndGlyphs"' if _jslen(t) * fs * .5 > 66 else ""
        out += (f'<text x="{_num(x)}" y="{_num(_r1(top + 3 + lh * (i + .8)))}" text-anchor="middle" font-size="{fs}" font-weight="800" '
                f'fill="{ink}" font-family="sans-serif"{fit}>{t}</text>')
    return out


_NB = re.compile(r"\{\{NB\|([^|]+)\|([^|]+)\|(\{\{INK\}\}|[^}]+)\}\}")


def subject_svg(emblem: str, label: str):
    """A subject character: the emblem's template + the concept's colour + its name (None if no template at all)."""
    tpls = _art().get("subject_templates", {})
    tpl = tpls.get(emblem) or tpls.get("🔹")
    if not tpl:
        return None
    fill, ink = subj_color(label)
    lines, fs = subj_label(label)
    svg = _NB.sub(lambda m: name_block(float(m.group(1)), float(m.group(2)), m.group(3), lines, fs), tpl)
    return svg.replace("{{FILL}}", fill).replace("{{INK}}", ink)


def subj_parts(icon: str):
    """«subj:💻:وحدة المعالجة» → ("💻", "وحدة المعالجة")"""
    rest = icon[5:]
    i = rest.find(":")
    return (rest, "") if i < 0 else (rest[:i], rest[i + 1:])


# ---------- 🧱 Lego drawings (batch 29): «lego:<main>:<extra>+<extra>:<colour>:<motion>» ----------
_LEGO_NUM = re.compile(r"-?\d+")


def lego_svg(key: str):
    """A drawing BUILT from parts: the main part + up to 2 badges, in the concept's colour — put together exactly like
    legoSVG in the page (03_explain_player_src/lego.js); a browser test checks both give the same SVG. None if not a Lego key."""
    parts = _art().get("lego") or {}
    mains, extras, badges = parts.get("main", {}), parts.get("extra", {}), parts.get("badge", [])
    p = (key or "").split(":") + ["", "", "", ""]
    if not key.startswith("lego:") or p[1] not in mains:
        return None
    xs = [x for x in p[2].split("+") if x in extras][:2]
    m = _LEGO_NUM.match(p[3] or "")
    fill, ink = SUBJ_COLORS[abs(int(m.group())) % len(SUBJ_COLORS) if m else 0]
    s = mains[p[1]] + "".join(badges[i] + extras[x] + "</g>" for i, x in enumerate(xs))
    return s.replace("{{FILL}}", fill).replace("{{INK}}", ink)


def lego_parts() -> dict:
    """What the Lego drawings are built from (names only; the drawings are in art.json → lego)."""
    parts = _art().get("lego") or {}
    return {"main": sorted(parts.get("main", {})), "extra": sorted(parts.get("extra", {})), "motions": parts.get("motions", [])}


def with_face_rules(svg: str, stage: str = "kids") -> str:
    """Put the face rules INSIDE the picture (one face, the right one for the age stage)."""
    st = stage if stage in STAGES else "kids"
    css = FACE_CSS["base"] + FACE_CSS.get(st, "")
    i = svg.find(">")
    return svg[:i + 1] + f"<style>{css}</style>" + svg[i + 1:] if i > 0 else svg


def art_svg(icon: str, stage: str = None):
    """The SVG text of a picture key, or None if we have no drawing for it.
    stage=None → the bare drawing (for code that adds its own CSS, like the model's sandbox) · a stage → with its face rules."""
    a = _art()
    svg = None
    if icon in a["files"]:
        svg = a["files"][icon]
    elif icon.startswith("lego:"):                                    # 🧱 «lego:drawers:binary:3:wobble» → built from parts
        body = lego_svg(icon)
        svg = None if body is None else f'<svg xmlns="http://www.w3.org/2000/svg" width="240" height="240" viewBox="0 0 100 100">{body}</svg>'
    elif icon.startswith("subj:"):                                    # «subj:💻:الذاكرة» → the computer with «الذاكرة» on it
        e, name = subj_parts(icon)
        body = subject_svg(e, name)
        svg = body if body is None or body.startswith("<svg") else f'<svg xmlns="http://www.w3.org/2000/svg" width="240" height="240" viewBox="0 0 100 100">{body}</svg>'
    if svg is None:
        return None
    return with_face_rules(svg, stage) if stage else svg
```

---

## `core/contract.py`

> 🆕 **الدفعة ٢٦:** ٥ أنواع جديدة **`recipe` · `connect` · `compare` · `teach` · `ladder`** (فعالية وحدة لكل مفهوم، شرحها تحت بـ `engine/explain_activities.py`) + **`SOUNDS`** (آلة كل مادة) + وصف **الفارة على الشخصية** بكل مرحلة (`STAGES`).

> 🆕 **الدفعة ٢٥:** نوع مشهد جديد **`custom`** (مشهد الموديل)، حقل **`audience`** بكل درس (الصف والمرحلة)، **`STAGES`** (وصف كل مرحلة للفرونت)، وأوضاع الشريط الجديدة `line/motion/accel` (من الصف الثامن)، و`before_after.mode/why`.

**العقد مع الفرونت إند.** لكل نوع مشهد من الـ ١٣: **شو هو** (جملة عربية) و**حقوله**. وكمان **حقول الدرس** و**معنى السهم** (`[a, b]` = «b بيحتاج a»). الفرونت إند بيقرأ هاد من `/scene-kinds` وبيعرف **كيف يرسم كل نوع** بلا ما يسألنا.

```python
"""The CONTRACT with the front end: what each scene kind means and which fields it carries. Served at GET /scene-kinds.
Relations everywhere: an edge [a, b] means «b needs a» (a comes before b). Every text is Arabic and ready to show."""

COMMON = {"kind": "نوع المشهد", "steps": "جمل قصيرة بالترتيب (سطر الراوي)", "paragraph": "فقرة «ليش؟» (شرح أطول وبسيط)"}

SCENE_KINDS = {
    "overview": {"what": "🗺️ الصورة الكبيرة للدرس: كل المفاهيم مرقّمة بترتيب التعلّم وأسهم «بيحتاج».",
                 "fields": {"concepts": "ids المفاهيم", "edges": "[[a,b]] يعني b بيحتاج a", "levels": "{id: رقم العمود بترتيب التعلّم}"}},
    "world": {"what": "🌱 عالم حقيقي (طقم النبتة): مي وشمس وهوا، والطالب بيجرّب بإيده.",
              "fields": {"kit": "اسم الطقم (plant)", "parts": "{دور: concept_id}", "needs": "شو بتحتاج (water/sun/air)", "info": "{دور: معنى من الجراف}"}},
    "assemble": {"what": "🧩 ركّب المشهد: كل شخصية لظلّها (بازل)، ولما توصل بتحكي مين هي.",
                 "fields": {"concepts": "ids", "edges": "[[a,b]]", "levels": "{id: عمود}", "says": "{id: جملة تعريف}"}},
    "meet": {"what": "👋 تعرّف عليّ: المفهوم بالنص، واللي بيحتاجهم من جهة، واللي بيحتاجوه من الجهة الثانية.",
             "fields": {"target": "id", "ins": "اللي بيحتاجهم", "outs": "اللي بيحتاجوه", "roles": "{id: ليش}", "focus": "لكل خطوة: target / ins / out:<id> (مين نضوّي ونركّز الكاميرا عليه)"}},
    "interview": {"what": "🎤 مقابلة: الطالب بيكبس سؤال والشخصية بتجاوب.", "fields": {"target": "id", "qa": "[{q, a}]"}},
    "flip": {"what": "🎴 بطاقات بتتقلب: على الوجه سؤال، وورا كل بطاقة جملة كاملة بتنفهم لحالها.",
             "fields": {"target": "id", "cards": "[{front: السؤال, back: جملة كاملة}] (اعرضوا السؤال صغير فوق الجملة لما تنقلب)"}},
    "journey": {"what": "🚶 الرحلة: سلسلة «بيحتاج». إذا traveller = id بيمشي فعلاً (مي/هوا/ضوء)، وإذا spark المراحل بتضوّي بالكبس.",
                "fields": {"target": "id", "route": "ids بالترتيب", "traveller": "id أو spark", "stops": "[{id, say}]"}},
    "what_if": {"what": "🔮 شو بيصير لو: مفتاح بيطفي المفهوم، واللي بيحتاجوه بيتعبوا ورا بعض.",
                "fields": {"target": "id", "affected": "ids بالترتيب", "calm": "ids ما بتتأثر", "edges": "[[a,b]]"}},
    "before_after": {"what": "⏳ شريط بين مفهومين. mode=becomes: «قبل/بعد» واللي قبل بيتحوّل فعلاً للي بعد (البذرة ← الإنبات). mode=needs: «أول/وبعدين»: الأول بيضل موجود، والثاني بيجي بعده لأنه بيحتاجه (الساق بيحتاج الجذر).",
                     "fields": {"target": "id (بعد / وبعدين)", "before": "id (قبل / أول)", "mode": "becomes أو needs",
                                "why": "ليش (من معنى المفهوم بالجراف) أو فاضي إذا الجراف ما بيحكي"}},
    "play": {"what": "🎞️ فيلم عملية حقيقية (سينما وبعدين الطالب بيعملها).",
             "fields": {"verb": "visit/carry/transform/combine/take_away/groups/share/cut/equivalent/compare/build/exchange/flow_river/write",
                        "target": "id", "actor": "مين بيعمل الحركة (مثلاً النحلة)", "with": "id اللي بيزوره/بيحمله", "result": "id النتيجة",
                        "example": "أرقام المثال (للرياضيات)", "drive": "جملة «دورك»"}},
    "slider": {"what": "🎚️ الشريط السحري: الأرقام بتتغير والصورة معها فوراً. من الصف الثامن: line (y = mx + b) · motion (d = v × t) · accel (v = a × t).",
               "fields": {"target": "id", "mode": "add/sub/mul/div/frac · line/motion/accel (صف ٨+)"}},
    "dialogue": {"what": "🗣️ حوار شخصيتين عن ليش وحدة بتحتاج الثانية.", "fields": {"target": "id", "with": "id", "lines": "[{who: id, say}]"}},
    "lens": {"what": "🔍 العدسة: المعلومات مخبّاية، والطالب بيكشفها بالماوس/الإصبع.", "fields": {"target": "id", "facts": "[نص]"}},
    # 🆕 batch 26: five more activities (one per concept). No points, no failing: a wrong move gets an explanation.
    "recipe": {"what": "🧪 الشروط: الأشياء اللي بيحتاجها المفهوم كمفاتيح. بيبلش فاضي، والمفهوم بيكتمل بس لما يشتغلوا كلهم. طفّي واحد ← بيقول شو ناقص وليش.",
               "fields": {"target": "id", "needs": "[{id, why}] (٢ أو أكثر)", "ready": "جملة لما يكتملوا كلهم"}},
    "connect": {"what": "✏️ ارسم الأسهم: الطالب بيرسم أسهم «بيحتاج» بنفسه (سحب، أو كبسة على الاثنين بالترتيب). الصح بيضل مع السبب، والمقلوب بينشرح ليش.",
                "fields": {"target": "id", "nodes": "ids (المفهوم أول واحد)", "links": "[{from: اللي بيحتاج, to: اللي بيحتاجه, required, ok_say, rev_say}] (required=false: سهم صح زيادة بين الباقيين، بينقبل)",
                           "calm": "ids ما إلهم سهم مع المفهوم (ولا من خلال سلسلة)", "end_say": "جملة النهاية"}},
    "compare": {"what": "⚖️ قارن: مفهومين قريبين. كل بطاقة بتروح عند الأول، عند الثاني، أو «الاثنين». الغلط: «جرّب مكان ثاني»، وثاني غلطة البطاقة بتروح لمكانها مع السبب.",
                "fields": {"target": "id (a)", "other": "id (b)", "facts": "[{fact: نص البطاقة, side: a/b/both, type: def/need/feed, ref: id, why: الشرح}]", "end_say": "جملة النهاية"}},
    "teach": {"what": "🧑‍🏫 اشرح لزميلك: زميل مش فاهم بيسأل ٢–٣ أسئلة، والطالب بيختار الجواب. الغلط بيترد عليه بالسبب (هاد تعريف مفهوم ثاني · السهم بالعكس). بالآخر: الشرح اللي بناه.",
              "fields": {"target": "id", "rounds": "[{ask, rel: def/needs/needed_by, options:[{opt, id, ok, reply}]}]", "learnt": "الشرح كامل بالآخر"}},
    "ladder": {"what": "🪜 السلّم: «ليش؟» ورا «ليش؟»: كل جواب درجة أعمق لحد الأساس (mode=why). أو «وبعدين؟» للي بيجي بعده (mode=then). الأسهم دايماً من اللي بيحتاج.",
               "fields": {"target": "id", "mode": "why أو then", "rungs": "[{id, because: الجملة الكاملة, short: جملة قصيرة للفقاعة}]", "end_say": "جملة النهاية"}},
    "custom": {"what": "🤖 مشهد كتبه الموديل بأدوات القالب (SDK) وانقبل من المعلم. بيشتغل بس جوا <iframe sandbox=\"allow-scripts\">. بيوصل بس مع include_llm=true.",
               "fields": {"target": "id", "scene_id": "id المشهد", "runner_url": "رابط صفحة الصندوق المعزول", "source": "llm", "provider": "مين كتبه (gemini/openai/claude)"}},
}

LESSON_FIELDS = {
    "lesson_id": "id الدرس", "lesson_title": "اسم الدرس", "overview": "مشهد الصورة الكبيرة", "world": "مشهد العالم (أو null)",
    "assemble": "مشهد ركّب (أو null)", "concepts": "[{concept_id, title, scenes:[...], teach:{hook, answer, summary, recap}}]",
    "icons": "{concept_id: مفتاح الرسمة}", "art": "{concept_id: رابط الرسمة SVG}", "status": "needs_review = بانتظار مراجعة المعلم",
    "warnings": "مشاكل انكشفت (المشهد الغلط ما بيوصل)",
    "audience": "{grade, stage, label, persona} — المرحلة العمرية: kids (١–٤) · junior (٥–٧) · teen (٨–٩) · senior (١٠–١٢). الفرونت بيختار الشكل والأصوات منها، والكلام جاي جاهز للعمر",
}

STAGES = {"kids": "🌈 رفيق مرح: وجوه كاملة، ضحك، إيموجي، ألحان صغيرة · الفارة على الشخصية: بتضحك بصوتها هي",
          "junior": "🧭 مستكشف فضولي: وجوه بلا خدود، بلا ضحك، أصوات ناعمة · الفارة: بتميل وبتقول «همم؟»",
          "teen": "🔬 زميل واثق: عيون بس، «بيعتمد على»، نوتات قصيرة نظيفة، شكل دفتر مختبر · الفارة: بتضوي + اسمها ومعناها",
          "senior": "📐 خبير هادي: بلا وجوه، رسومات علمية رفيعة، بلا إيموجي، «نقاش»، شبه صامت · الفارة: اسمها ومعناها بلا صوت"}

SOUNDS = {"what": "🎵 الأصوات بتنعمل بالمتصفح (Web Audio)، بلا ملفات. المرحلة بتقرر قديش وكم عالي، والمادة بتقرر الآلة والسلّم الموسيقي، وما في نفس النوتة مرتين ورا بعض.",
          "subject_instrument": {"science": "ماريمبا", "math": "وتر مقروص", "physics": "بيانو كهربائي", "chemistry": "أجراس زجاج",
                                 "geography": "كاليمبا", "history": "خشب", "language": "ناي ناعم", "general": "جرس صغير"},
          "where": "03_explain_player_src/sound.js (الفرونت بقدر ياخذه زي ما هو)"}


def describe() -> dict:
    return {"relation": "edge [a, b] = «b بيحتاج a»", "common_fields": COMMON, "lesson_fields": LESSON_FIELDS, "scene_kinds": SCENE_KINDS, "stages": STAGES, "sounds": SOUNDS}
```

---

## `core/service.py`

> 🆕 **الدفعة ٢٥:** `get_lesson(..., include_llm=False)`: إذا `True` بيجيب من `llm_scenes.approved_for_lesson` المشاهد **المقبولة** وبيزيدها لمشاهد كل مفهوم (بنفس الشكل، `kind: custom`). بدونها: **مشاهد المصنع بس** (زي قبل).

> 🆕 **الدفعة ٢٧:** المصنع من `02_question_factory` مباشرة · `generate` بيرجّع كمان `grade` و`stage` و**`identity`** (هوية المادة) و**`page_url`** · `_book_id_of` بيرفض أي رقم كتاب فيه `/` أو `..` (لأنه بيصير اسم مجلد) · جراف بلا دروس أو خربان ← `BadInput` **مع السبب** (مش ٥٠٠) · `seed_samples` / `ensure_samples` (الكتب الـ١٢) · `delete_book` · **`page_data` / `page_html`** (الصفحة من داتا السيرفر، بنفس `pack` و`page_html` تبع باني الصفحة) · `home_html` (صفحة السيرفر) · `_order` (صف ٤ ← ١٢، والكتب الـ١٢ بنفس ترتيب الصفحة المنشورة، فالصفحة بتطلع **نفسها بالبايت**).

**المنطق كله** (بايثون عادي، فسهل نفحصه ونستعمله بأي مكان).
- `NotFound` و`BadInput`: نوعين أخطاء واضحين.
- `_book_id_of`: بياخد رقم الكتاب من `book.id` أو من أول node مستواه `book`. **لو ما لقى** ← `BadInput`.
- `generate`: 
  ١. **لازم** يجي جراف أو اسم ملف، وإلا `BadInput`.
  ٢. إذا جراف: بيتأكد إنه JSON فيه `nodes`، وبيحفظه بـ `data/graphs/<book>.json`. إذا اسم ملف: لازم يكون موجود وإلا `NotFound`.
  ٣. **الموديل:** إذا `use_llm` وفي مفتاح ← بيستعمل البوابة (Gemini ← GPT ← Claude). **ما في مفتاح؟** بيكمّل **بدون AI** وبيكتب تحذير (ما بيوقف).
  ٤. **بينادي المصنع** (`explain_main.run`) ← شرح **كل درس** بينحفظ.
  ٥. بيعمل **ملخّص الكتاب** (الدروس، المشاهد، الوقت، الموديل) وبيحفظه وبيرجّعه **مع التحذيرات**.
- `list_books` / `list_lessons`: قوائم (الكتاب مش موجود ← `NotFound`).
- `_with_art`: بيضيف لكل درس حقل `art`: **رابط رسمة كل مفهوم**.
- `get_lesson`: الدرس كامل **+ روابط الرسومات + رقم الكتاب**.
- `get_concept`: بيدوّر على المفهوم بالدروس، وبيرجّع **مشاهده + رسمته + رسومات المفاهيم الثانية** (اللي بتظهر بمشاهده).
- `get_art`: نص الـ SVG أو `NotFound`.

```python
"""The service: everything the API can do, as plain Python (no web code here, so it is easy to test and reuse).

   graph → the factory makes the explanation of EVERY lesson and keeps it → then:
     · the PAGE itself (/explain): the same interactive page as the published one (scenes, the 5 activities, films,
       sounds per subject and per age stage), built from what is kept on the server — for any graph;
     · the DATA (books / lessons / concepts / pictures) for any other front end.
   A NEW subject gets its own identity (identity.py in the factory): its own sound and its own characters.
   No AI unless asked (use_llm), and then only to polish the «ليش؟» paragraphs."""
import datetime
import json
import os
import re
import sys

from core import art, settings, storage

sys.path.insert(0, settings.FACTORY_DIR)          # the explanation factory (plain Python) — the SAME code that built the published page
sys.path.insert(0, settings.PLAYER_DIR)           # the page builder (pack + the template)
import audience  # noqa: E402
import build_all_books  # noqa: E402
import build_explain_player as player  # noqa: E402
import explain_main  # noqa: E402
import identity  # noqa: E402
import lego  # noqa: E402
import offline_generator as og  # noqa: E402
import llm_gateway  # noqa: E402
from graph_reader import Graph  # noqa: E402

identity.set_store(os.path.join(settings.DATA_DIR, "subject_identities.json"))   # 🤖 identities the model chose (one per new subject)
lego.set_store(os.path.join(settings.DATA_DIR, "lego_library.json"))              # 🧱 drawings BUILT from parts (the library grows)


class NotFound(Exception):
    """Asked for something that does not exist (→ 404)."""


class BadInput(Exception):
    """The request itself is wrong (→ 400)."""


_SAFE_ID = re.compile(r"^[\w\-؀-ۿ]{1,80}$")


def _book_id_of(graph: dict) -> str:
    bid = (graph.get("book") or {}).get("id")
    if not bid:
        bid = next((n.get("id") for n in graph.get("nodes", []) if n.get("level") == "book"), None)
    if not bid:
        raise BadInput("الجراف ما فيه كتاب (book.id أو node level=book)")
    bid = str(bid)
    if not _SAFE_ID.match(bid):                       # it becomes a folder name: letters, digits, _ and - only (never «../»)
        raise BadInput("رقم الكتاب (book.id) لازم يكون حروف وأرقام و _ - بس")
    return bid


def _graph_file(book_id: str) -> str:
    return os.path.join(settings.GRAPHS_DIR, f"{book_id}.json")


def _find_graph(name: str) -> str:
    """A graph by name: a saved one (data/graphs) or one of the sample books (02_question_factory)."""
    if os.path.isabs(name):
        return name
    for base in (settings.GRAPHS_DIR, settings.SAMPLES_DIR):
        p = os.path.join(base, os.path.basename(name))
        if os.path.exists(p):
            return p
    raise NotFound(f"ما في جراف اسمه {name}")


def generate(graph: dict = None, graph_path: str = None, use_llm: bool = False, llm=None, _sample: str = None) -> dict:
    """Turn a graph into explanations for EVERY lesson and keep them. Give the graph itself (JSON) or the name of a saved graph."""
    if graph is None and not graph_path:
        raise BadInput("ابعت الجراف (graph) أو اسم ملفه (graph_path)")
    if graph is None:
        with open(_find_graph(graph_path), encoding="utf-8") as f:
            graph = json.load(f)
    if not isinstance(graph, dict) or not isinstance(graph.get("nodes"), list):
        raise BadInput("الجراف لازم يكون JSON فيه nodes")
    book_id = _book_id_of(graph)
    os.makedirs(settings.GRAPHS_DIR, exist_ok=True)
    path = _graph_file(book_id)
    with open(path, "w", encoding="utf-8") as f:                     # a copy of the graph is kept: the page is built from it later
        json.dump(graph, f, ensure_ascii=False)
    warnings = []
    if llm is None and use_llm:
        if llm_gateway.api_key_from_anywhere():
            llm = llm_gateway.generate
        else:
            warnings.append("ما في مفتاح موديل على السيرفر: انعمل الشرح بدون AI")
    try:
        g = Graph.load(path)
        if not g.lessons():
            raise BadInput("الجراف ما فيه ولا درس (node level=lesson فيه مفاهيم)")
        if llm and identity.needs_model(g.book.get("subject")):          # 🤖 a new subject: ONE call → an identity that fits its meaning (saved)
            if identity.ask_model(g.book.get("subject"), llm) is None:
                warnings.append("الموديل ما أعطى هوية صالحة للمادة: أخذت هوية ثابتة من اسمها")
        lego_new = _lego_for_book(g, llm) if llm else {}                 # 🧱 concepts with no drawing: the model picks parts (ONE call)
        recs = explain_main.run(path, storage.book_dir(book_id), llm)
    except BadInput:
        raise
    except Exception as e:                                           # a broken graph says WHY, not «500»
        raise BadInput(f"ما قدرت أقرأ الجراف: {e}")
    lessons = [{"lesson_id": r["lesson_id"], "title": r["lesson_title"], "concepts": len(r["concepts"]),
                "scenes": 1 + bool(r.get("world")) + bool(r.get("assemble")) + sum(len(c["scenes"]) for c in r["concepts"])} for r in recs]
    for r in recs:
        warnings += [w for w in r.get("warnings", [])]
    idn = identity.of_book(g.book)
    meta = {"book_id": book_id, "title": g.book.get("title", book_id), "subject": g.book.get("subject", ""),
            "grade": g.book.get("grade"), "stage": audience.audience(g)["stage"],
            "lego": _lego_summary(g),
            "identity": {"new": idn["new"], "family": idn["family"], "by_model": idn["family"] == "chosen", "label": idn["label"], "emblem": idn["emblem"],
                         "mascot_name": idn["mascot_name"], "sound": idn["sound"]},
            "lessons": lessons, "scenes": sum(x["scenes"] for x in lessons),
            "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
            "llm": (llm_gateway.LAST_PROVIDER if llm is llm_gateway.generate else ("custom" if llm else None)),
            "version": settings.API_VERSION, "page_url": f"/explain/{book_id}"}
    if _sample:
        meta["sample"] = _sample                                     # (only for the order on the page)
    storage.save_meta(book_id, meta)
    return dict(meta, warnings=warnings)


# ---------- 🧱 Lego drawings (batch 29 · 💡 Hareth's idea) ----------
def _entities(g) -> list:
    return [c for c in g.concepts.values() if og.is_entity(g, c.id)]


def _lego_for_book(g, llm) -> dict:
    """The concepts that would get only the subject's character (no drawing in the library, no word that fits a part):
    ONE model call for all of them → the model CHOOSES parts → saved in the library. Nothing to ask → no call, no cost."""
    subject = str(g.book.get("subject", ""))
    todo = [c for c in _entities(g) if og.icon_for(c.text, c.description, subject).startswith("subj:")]
    if not todo:
        return {}
    return lego.ask_model([c.text for c in todo], llm, subject, {c.text: c.description for c in todo})


def _lego_summary(g) -> dict:
    """How the book's concepts got their pictures: from the library · built (Lego) · the subject's character."""
    subject = str(g.book.get("subject", ""))
    keys = [og.icon_for(c.text, c.description, subject) for c in _entities(g)]
    return {"library": sum(1 for k in keys if not k.startswith(("lego:", "subj:"))), "built": sum(1 for k in keys if k.startswith("lego:")),
            "subject_character": sum(1 for k in keys if k.startswith("subj:"))}


def lego_parts() -> dict:
    """The parts a Lego drawing is built from: their names, what they can mean, and the motions (the model sees the same)."""
    return {"main": {k: v[0] for k, v in lego.MAINS.items()}, "extra": dict(lego.EXTRAS), "motions": list(lego.MOTIONS),
            "key": "lego:<main>:<extra>+<extra>:<colour 0-7>:<motion>", "example": art.art_url("lego:drawers:binary:3:wobble")}


def lego_library() -> list:
    """Every drawing BUILT so far (the library that grows), with its suggestions for the teacher and a picture URL for each."""
    out = []
    for e in lego.library().values():
        out.append(dict(e, art=art.art_url(e["key"]), suggestion_art=[art.art_url(k) for k in e.get("suggestions", [])]))
    return sorted(out, key=lambda e: (e.get("status") != "auto", e.get("name", "")))


def lego_choose(name: str, pick: int = None, reject: bool = False) -> dict:
    """The teacher's choice (one of the model's suggestions, or «no» → the subject character). Every saved book that shows
    this concept gets the new picture at once (only the picture key changes in its lessons, nothing else)."""
    try:
        r = lego.choose(name, pick, reject)
    except KeyError:
        raise NotFound(f"ما في رسمة ليغو محفوظة لـ «{name}»")
    except ValueError as e:
        raise BadInput(str(e))
    updated = []
    for m in storage.list_books():
        b = m["book_id"]
        if not os.path.exists(_graph_file(b)):
            continue
        g = Graph.load(_graph_file(b))
        subject = str(g.book.get("subject", ""))
        for lid in storage.lesson_ids(b):
            rec = storage.load_lesson(b, lid)
            icons, changed = (rec or {}).get("icons", {}), False
            for cid, old in list(icons.items()):                       # a lesson keeps the picture key of every concept it shows
                if cid in g.concepts and lego._key_of(g.concepts[cid].text) == lego._key_of(name):
                    new = og.icon_for(g.concepts[cid].text, g.concepts[cid].description, subject)
                    if new != old:
                        icons[cid], changed = new, True                # only THIS concept (another one may share the same key)
            if changed:
                storage.save_lesson(b, lid, rec)
                updated.append(f"{b}/{lid}")
    return dict(r, art=art.art_url(r["new"]) if r["new"] else None, updated_lessons=updated)


# ---------- the 12 sample books ----------
def sample_files() -> list:
    return sorted(f for f in os.listdir(settings.SAMPLES_DIR) if f.endswith("_book_graph.json"))


def seed_samples(force: bool = False) -> list:
    """Make the sample books (grade 4 → 12). force=False: only the ones not made yet."""
    have = {m["book_id"] for m in storage.list_books()}
    out = []
    for name in sample_files():
        with open(os.path.join(settings.SAMPLES_DIR, name), encoding="utf-8") as f:
            graph = json.load(f)
        if force or _book_id_of(graph) not in have:
            out.append(generate(graph=graph, _sample=name.replace("_book_graph.json", "")))
    return out


def ensure_samples() -> None:
    """The first time the server has no book at all: make the samples, so the page is never empty (EXPLAIN_SEED=0 turns it off)."""
    if settings.SEED_SAMPLES and not storage.list_books():
        seed_samples()


def delete_book(book_id: str) -> dict:
    if not _SAFE_ID.match(book_id or "") or storage.book_meta(book_id) is None:
        raise NotFound(f"ما في كتاب {book_id}")
    storage.delete_book(book_id)
    if os.path.exists(_graph_file(book_id)):
        os.remove(_graph_file(book_id))
    return {"deleted": book_id}


# ---------- books / lessons / concepts / pictures (the data) ----------
def _order(m: dict) -> tuple:
    """Grade 4 → 12 (like the published page); in one grade, the samples in the page's own order, then the new books by title."""
    try:
        grade = int(m.get("grade") or 99)
    except (TypeError, ValueError):
        grade = 99
    first = {f.replace("_book_graph.json", ""): i for i, f in enumerate(build_all_books.BOOKS)}
    return (grade, first.get(m.get("sample") or "", 99), m.get("title") or "")


def list_books() -> list:
    keys = ("book_id", "title", "subject", "grade", "stage", "identity", "scenes", "generated_at", "page_url")
    return [{k: m.get(k) for k in keys} for m in sorted(storage.list_books(), key=_order)]


def list_lessons(book_id: str) -> list:
    meta = storage.book_meta(book_id)
    if meta is None:
        raise NotFound(f"ما في كتاب {book_id}")
    return meta["lessons"]


def _with_art(rec: dict) -> dict:
    rec = dict(rec)
    rec["art"] = {cid: art.art_url(icon) for cid, icon in rec.get("icons", {}).items()}
    return rec


def get_lesson(lesson_id: str, book_id: str = None, include_llm: bool = False) -> dict:
    """Everything the front end needs to show one lesson (scenes + texts + picture URLs + «audience» = the age stage).
    include_llm=True adds the scenes the model wrote AND a teacher approved ({"kind": "custom", "runner_url": …})."""
    b, rec = storage.find_lesson(lesson_id, book_id)
    if rec is None:
        raise NotFound(f"ما في درس {lesson_id}")
    rec = _with_art(rec)
    if include_llm:
        from core import llm_scenes                                   # (imported here: the model part is optional)
        extra = llm_scenes.approved_for_lesson(b, lesson_id)
        rec["concepts"] = [dict(c, scenes=c["scenes"] + extra.get(c["concept_id"], [])) for c in rec["concepts"]]
    return dict(rec, book_id=b)


def get_concept(concept_id: str, book_id: str = None) -> dict:
    """The scenes of ONE concept (and the lesson it belongs to)."""
    books = [book_id] if book_id else [m["book_id"] for m in storage.list_books()]
    for b in books:
        for lid in storage.lesson_ids(b):
            rec = storage.load_lesson(b, lid)
            for c in (rec or {}).get("concepts", []):
                if c["concept_id"] == concept_id:
                    icon = rec.get("icons", {}).get(concept_id)
                    return dict(c, book_id=b, lesson_id=lid, lesson_title=rec["lesson_title"], icon=icon, art=art.art_url(icon),
                                art_of_others={k: art.art_url(v) for k, v in rec.get("icons", {}).items()})
    raise NotFound(f"ما في مفهوم {concept_id}")


def get_art(key: str, stage: str = "kids") -> str:
    svg = art.art_svg(key, stage or "kids")
    if svg is None:
        raise NotFound(f"ما في رسمة للمفتاح {key}")
    return svg


# ---------- 📖 the PAGE (the same interactive page as the published one) ----------
def _books_for_page(book_ids=None) -> list:
    metas = sorted(storage.list_books(), key=_order)
    if book_ids:
        want = [b for b in book_ids if b]
        missing = [b for b in want if b not in {m["book_id"] for m in metas}]
        if missing:
            raise NotFound("ما في كتاب: " + "، ".join(missing))
        metas = [m for m in metas if m["book_id"] in want]
    return metas


def _approved_llm(book_id: str) -> dict:
    """The model scenes a teacher approved for this book (empty if none, or if the model part is not there)."""
    try:
        from core import llm_scenes
        return llm_scenes.approved_for_page(book_id)
    except Exception:                                                # the model part is optional: the page never breaks because of it
        return {}


def page_data(book_ids=None) -> dict:
    """What the page gets: every chosen book with its lessons, scenes, stage, subject and (for a new subject) its identity."""
    graphs = []
    for m in _books_for_page(book_ids):
        if os.path.exists(_graph_file(m["book_id"])):
            graphs.append(player.pack(_graph_file(m["book_id"]), storage.book_dir(m["book_id"]), extra=_approved_llm(m["book_id"])))
    if not graphs:
        raise NotFound("لسا ما في ولا كتاب: ابعت جراف لـ POST /explanations/generate")
    return {"graphs": graphs}


def page_html(book_ids=None) -> str:
    """The whole interactive page with the chosen books (all of them if none chosen), built from the server's data."""
    if not os.path.exists(settings.PAGE_TEMPLATE):
        raise NotFound("قالب الصفحة مش موجود: شغّل python 03_explain_player_src/build_explain_template.py")
    return player.page_html(page_data(book_ids)["graphs"])


def home_html() -> str:
    """The server's front page: the books + a box to send a NEW graph (then open its page)."""
    with open(os.path.join(settings.BASE_DIR, "static", "home.html"), encoding="utf-8") as f:
        return f.read()
```

---

---

## `core/llm_scenes.py` 🆕 (الدفعة ٢٥)
**🤖 مشاهد بيكتبها الموديل بأدوات قالبنا.** هي **زيادة** على مشاهد المصنع (اللي ما بتتغير أبداً)، و**ما بتوصل لطالب إلا بعد موافقة المعلم**.

| الدالة | شو بتاخد | كيف بتقرر | شو بترجع |
|---|---|---|---|
| `generate` | الكتاب، الدرس، (مفهوم)، (فكرة المعلم)، `max_scenes`، `force`، (`llm`) | `max_scenes` لازم ١–١٠ (**حد تكلفة**). إذا ما عطيناها `llm` بتستعمل البوابة، و**إذا ما في مفتاح ← خطأ 400 واضح** (ما بتنادي إشي). لكل مفهوم: إذا في مشهد محفوظ **لنفس المفهوم ونفس الفكرة** ← بترجعه **بلا ما تسأل** (`reused`، ببلاش). غير هيك: بتجهّز الحقائق (`scene_data`) وبتسأل (`write_scene`) وبتحفظ: **`pending_review`** إذا الفحص نجح، **`rejected`** إذا لأ (ومعه الأسباب) | ملخص لكل مشهد + **تحذيرات** («الكود انرفض… المشهد العادي بيضل») |
| `_scene_id` | الكتاب، الدرس، المفهوم، الفكرة | **بصمة** (sha1) منهم ومن نسخة البرومبت ← نفس الطلب = نفس الـ id | `accel-3f9c…` |
| `_graph` | الكتاب | بيدوّر على `data/graphs/<book>.json`، وإذا الجراف انحفظ باسم ملف ثاني بيدوّر على **`book.id` جواه** | الجراف (أو 404) |
| `list_scenes` / `get_scene` | فلاتر (كتاب، درس، حالة) / id | — | الملخصات / كل إشي عن المشهد (الكود، الفحص، الحقائق اللي شافها الموديل، المراجعة) |
| `review` | id، موافق؟، ملاحظة | **مشهد فشل بالفحص ما بينفع ينقبل** (400) | الملخص بحالته الجديدة |
| `report` | id، `{ok, drawn, outside, errors}` | بيحفظ شو شاف المتصفح لما المشهد اشتغل (من شاشة المعلم) | النتيجة المحفوظة |
| `runner` | id | — | **صفحة الصندوق المعزول** (HTML) |
| `approved_for_lesson` | الكتاب، الدرس | **المقبولة بس** | `{concept_id: [{kind: "custom", runner_url, steps, paragraph…}]}` |
| `sdk_doc` | — | — | توثيق للفرونت والفريق: الأدوات، قواعد كل عمر، الممنوعات، مثال، وكيف نحط الصندوق |

**⚙️ شو بيستعمل:** بايثون عادي + **الموديل** عن طريق `llm_gateway` (**Gemini ← GPT ← Claude**). كل مشهد بينحفظ ملف JSON بـ `data/llm_scenes/<book>/<scene_id>.json`.

```python
"""🤖 Scenes WRITTEN BY THE MODEL (with our template's toolkit) — generate, check, keep, review, run in a sandbox.

The factory's own scenes never change; a model scene is an EXTRA, and a student sees it only after a teacher approves it.
  generate(book_id, lesson_id, concept_id=None, idea=None, max_scenes=1, force=False, llm=None)
      → for each concept: scene_writer.write_scene (model + checks + one repair round) → saved as data/llm_scenes/<book>/<scene_id>.json
  list_scenes / get_scene / review (approve | reject) / report (what the browser saw: drew? inside? errors?)
  runner(scene_id) → the sandbox HTML (CSP: no network) for <iframe sandbox="allow-scripts">
  approved_for_lesson(book, lesson) → the approved scenes as {"kind": "custom", ...} for /lessons/{id}/explanation?include_llm=true
Cost guard: max_scenes ≤ 10 per call, and an existing scene for the same concept + idea is returned instead of asking again (unless force)."""
import datetime
import hashlib
import json
import os
import sys

from core import art, settings, storage

sys.path.insert(0, settings.ENGINE_DIR)          # the factory + the scene writer (engine/) are plain Python modules
import llm_gateway  # noqa: E402
import scene_writer  # noqa: E402
from graph_reader import Graph  # noqa: E402

STATUSES = ("pending_review", "approved", "rejected")


class NotFound(Exception):
    pass


class BadInput(Exception):
    pass


def _dir(book_id: str) -> str:
    return os.path.join(settings.DATA_DIR, "llm_scenes", book_id)


def _now() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")


def _save(rec: dict) -> None:
    os.makedirs(_dir(rec["book_id"]), exist_ok=True)
    with open(os.path.join(_dir(rec["book_id"]), rec["scene_id"] + ".json"), "w", encoding="utf-8") as f:
        json.dump(rec, f, ensure_ascii=False, indent=1)


def _all(book_id: str = None) -> list:
    root = os.path.join(settings.DATA_DIR, "llm_scenes")
    books = [book_id] if book_id else (sorted(os.listdir(root)) if os.path.isdir(root) else [])
    out = []
    for b in books:
        d = _dir(b)
        if os.path.isdir(d):
            for name in sorted(os.listdir(d)):
                if name.endswith(".json"):
                    with open(os.path.join(d, name), encoding="utf-8") as f:
                        out.append(json.load(f))
    return out


def _graph(book_id: str):
    path = os.path.join(settings.GRAPHS_DIR, f"{book_id}.json")
    if not os.path.exists(path):                                 # graphs sent by name keep their file name: look them up by book id
        for name in (os.listdir(settings.GRAPHS_DIR) if os.path.isdir(settings.GRAPHS_DIR) else []):
            p = os.path.join(settings.GRAPHS_DIR, name)
            try:
                with open(p, encoding="utf-8") as f:
                    if (json.load(f).get("book") or {}).get("id") == book_id:
                        path = p
                        break
            except (OSError, ValueError):
                continue
    if not os.path.exists(path):
        raise NotFound(f"ما في جراف للكتاب {book_id} (اعمل /explanations/generate أول)")
    return Graph.load(path)


def _scene_id(book_id, lesson_id, cid, idea) -> str:
    h = hashlib.sha1(f"{book_id}|{lesson_id}|{cid}|{idea or ''}|{scene_writer.PROMPT_VERSION}".encode("utf-8")).hexdigest()[:10]
    return f"{cid}-{h}"


def generate(book_id: str, lesson_id: str, concept_id: str = None, idea: str = None, max_scenes: int = 1, force: bool = False, llm=None) -> dict:
    """Ask the model for new scenes (one per concept, at most max_scenes). Nothing is shown to students until approved."""
    if not (1 <= int(max_scenes) <= 10):
        raise BadInput("max_scenes لازم بين 1 و 10 (حد للتكلفة)")
    g = _graph(book_id)
    lesson = next((l for l in g.lessons() if l.id == lesson_id), None)
    if lesson is None:
        raise NotFound(f"ما في درس {lesson_id} بالكتاب {book_id}")
    ids = [c.id for c in lesson.concepts]
    if concept_id:
        if concept_id not in ids:
            raise NotFound(f"المفهوم {concept_id} مش بالدرس {lesson_id}")
        ids = [concept_id]
    warnings = []
    if llm is None:
        if not llm_gateway.api_key_from_anywhere():
            raise BadInput("ما في مفتاح موديل على السيرفر (api_key.txt أو GEMINI_API_KEY / OPENAI_API_KEY / ANTHROPIC_API_KEY)")
        llm = llm_gateway.generate
    out = []
    for cid in ids[:int(max_scenes)]:
        sid = _scene_id(book_id, lesson_id, cid, idea)
        old = next((r for r in _all(book_id) if r["scene_id"] == sid), None)
        if old and not force:                                    # already asked: no new cost
            out.append(_summary(old, reused=True))
            continue
        data = scene_writer.scene_data(g, lesson, cid, art_svg=art.art_svg)
        res = scene_writer.write_scene(data, llm, idea=idea)
        rec = {"scene_id": sid, "book_id": book_id, "lesson_id": lesson_id, "concept_id": cid, "concept": data["concept"]["name"],
               "idea": idea, "stage": data["stage"], "status": "pending_review" if res["ok"] else "rejected",
               "problems": res["problems"], "attempts": res["attempts"], "code": res["code"], "data": data,
               "provider": (llm_gateway.LAST_PROVIDER if llm is llm_gateway.generate else "custom"),
               "prompt_version": scene_writer.PROMPT_VERSION, "created_at": _now(), "review": None, "browser_check": None}
        _save(rec)
        out.append(_summary(rec))
        if not res["ok"]:
            warnings.append(f"«{data['concept']['name']}»: الكود انرفض ({'; '.join(res['problems'][:3])}) — المشهد العادي بيضل")
    return {"book_id": book_id, "lesson_id": lesson_id, "scenes": out, "warnings": warnings}


def _summary(rec: dict, reused: bool = False) -> dict:
    return {"scene_id": rec["scene_id"], "concept_id": rec["concept_id"], "concept": rec.get("concept"), "status": rec["status"],
            "problems": rec.get("problems", []), "attempts": rec.get("attempts"), "provider": rec.get("provider"), "reused": reused,
            "runner_url": f"/llm/scenes/{rec['scene_id']}/runner.html?book_id={rec['book_id']}"}


def list_scenes(book_id: str = None, lesson_id: str = None, status: str = None) -> list:
    if status and status not in STATUSES:
        raise BadInput(f"status لازم وحدة من {STATUSES}")
    return [_summary(r) for r in _all(book_id) if (not lesson_id or r["lesson_id"] == lesson_id) and (not status or r["status"] == status)]


def get_scene(scene_id: str, book_id: str = None) -> dict:
    rec = next((r for r in _all(book_id) if r["scene_id"] == scene_id), None)
    if rec is None:
        raise NotFound(f"ما في مشهد {scene_id}")
    return rec


def review(scene_id: str, approve: bool, note: str = None, book_id: str = None) -> dict:
    """The teacher's decision. A rejected-by-checks scene can never be approved (its code did not pass)."""
    rec = get_scene(scene_id, book_id)
    if approve and rec.get("problems"):
        raise BadInput("هالمشهد ما نجح بالفحص، فما بينفع ينقبل: " + "; ".join(rec["problems"][:3]))
    rec["status"] = "approved" if approve else "rejected"
    rec["review"] = {"approved": bool(approve), "note": note, "at": _now()}
    _save(rec)
    return _summary(rec)


def report(scene_id: str, result: dict, book_id: str = None) -> dict:
    """What the browser saw when the scene ran (from the teacher's preview): {ok, drawn, outside, errors}."""
    rec = get_scene(scene_id, book_id)
    keep = {k: result.get(k) for k in ("ok", "drawn", "outside", "errors", "done")}
    rec["browser_check"] = dict(keep, at=_now())
    _save(rec)
    return {"scene_id": scene_id, "browser_check": rec["browser_check"]}


def runner(scene_id: str, book_id: str = None) -> str:
    """The sandbox page (put it in <iframe sandbox="allow-scripts">). Pending scenes can be previewed; rejected ones too, to see why."""
    rec = get_scene(scene_id, book_id)
    return scene_writer.runner_html(rec["code"], rec["data"])


def approved_for_lesson(book_id: str, lesson_id: str) -> dict:
    """{concept_id: [custom scene, …]} — only APPROVED scenes, in the shape of the other scenes (+ where to run them)."""
    out = {}
    for r in _all(book_id):
        if r["lesson_id"] == lesson_id and r["status"] == "approved":
            out.setdefault(r["concept_id"], []).append({
                "kind": "custom", "scene_id": r["scene_id"], "target": r["concept_id"], "source": "llm", "provider": r.get("provider"),
                "runner_url": f"/llm/scenes/{r['scene_id']}/runner.html?book_id={book_id}",
                "steps": [f"🤖 مشهد جديد عن «{r['concept']}»"], "paragraph": r["data"]["concept"]["meaning"]})
    return out


def approved_for_page(book_id: str) -> dict:
    """{(lesson_id, concept_id): [scene, …]} — the APPROVED scenes of a book, ready to go INSIDE the page (/explain):
    the sandbox page is carried in the scene itself (runner_html), the same way the page shows its example scene."""
    out = {}
    for r in _all(book_id):
        if r["status"] == "approved":
            out.setdefault((r["lesson_id"], r["concept_id"]), []).append({
                "kind": "custom", "scene_id": r["scene_id"], "target": r["concept_id"], "source": "llm", "label": "🤖 مشهد من الموديل (وافق عليه المعلم)",
                "runner_html": scene_writer.runner_html(r["code"], r["data"]),
                "steps": [f"🤖 مشهد جديد عن «{r['concept']}»"], "paragraph": r["data"]["concept"]["meaning"]})
    return out


def sdk_doc() -> dict:
    """For the front end and the team: what the model may use, the rules it gets, and the version."""
    return {"prompt_version": scene_writer.PROMPT_VERSION, "max_code_chars": scene_writer.MAX_CODE,
            "sdk_reference": scene_writer.SDK_REFERENCE, "stage_rules": scene_writer.STAGE_RULES,
            "forbidden": [label for _, label in scene_writer.FORBIDDEN], "example": scene_writer.EXAMPLE,
            "sandbox": "<iframe sandbox=\"allow-scripts\" src=\"/llm/scenes/{scene_id}/runner.html\"> — CSP: default-src 'none' (no network)",
            "messages": {"llm-scene": "{ok, drawn, outside, errors, done} — POST it to /llm/scenes/{id}/report",
                         "llm-caption": "{text} — the narrator line (show it under the scene)"}}
```

---

## `02_question_factory/scene_writer.py` 🆕 (الدفعة ٢٥)
**الكاتب:** بيجهّز الحقائق، بيكتب البرومبت، بيفحص الكود، وبيعمل صفحة الصندوق. **بايثون عادي**، والموديل بينادى من برا (أي دالة `llm(system, user) → نص`)، فالفحوصات بتستعمل **موديل وهمي**.

| الدالة | شو بتعمل |
|---|---|
| `scene_data(g, lesson, cid, art_svg)` | **الحقائق من الجراف بس**: اسم المفهوم ومعناه، **شو بيحتاج** (لأول ٢) ومعه **«ليش»** (الجزء من المعنى اللي بيذكره)، **مين بيحتاجه**، **المرحلة العمرية**، كلمة «بيحتاج/بيعتمد على»، و**رسوماتنا** (SVG) للمفهوم وجيرانه |
| `build_prompt(data, idea)` | `system`: الهدف (الطالب **يعمل** إشي ويشوف شو بيتغير، بلا صح وغلط) + **الأدوات المسموحة** (`SDK_REFERENCE`) + **القواعد الصارمة** + **مثال كامل**. `user`: **قاعدة العمر** (`STAGE_RULES`) + الحقائق JSON + **فكرة المعلم** إذا في |
| `extract_code(text)` | الكود من أول بلوك ```javascript (أو النص كله) |
| `_strip_strings(code)` | الكود **بلا نصوص وتعليقات** (عشان «while» جوا جملة عربية ما تنحسب)، **بس جوا** `` `…${هون}…` `` الجزء `${…}` **كود** فبيضل |
| `check_code(code)` | **فحص بخطوات**: الحجم (≤ ٩٠٠٠ حرف) · `function buildScene(SDK, data)` موجودة · **الممنوعات** (`window`، `document`، `fetch`، `eval`، `innerHTML`، التخزين، `parent`، حيل `constructor`، `while`…) · **الأقواس متوازنة** · **`node --check`** (فحص JavaScript حقيقي، إذا Node موجود) ← **قائمة المشاكل** (فاضية = تمام) |
| `write_scene(data, llm, idea)` | بيسأل ← بيفحص ← **إذا في مشاكل: جولة تصليح وحدة** (بنبعتله الأخطاء والكود القديم) ← بيرجّع `{code, problems, ok, attempts}`. **ما بيرمي خطأ أبداً** (حتى لو الموديل وقع: بيرجع المشكلة) |
| `runner_html(code, data)` | **صفحة الصندوق كاملة**: CSP `default-src 'none'` (**ولا طلب إنترنت**) · المرحلة العمرية (`data-stage`) · `DATA` · الـ SDK · كود الموديل · التشغيل. وكل `</` بيصير `<\/` عشان الكود **ما يقدر يسكّر الـ script** |

**🧱 جدارين، مش واحد:** الفحص الثابت **ما بيمسك كل الحيل** (مثلاً كلمة ممنوعة مقسومة لقطعتين بنص). عشان هيك في **جدار ثاني**: الصندوق المعزول (`sandbox="allow-scripts"` بلا `allow-same-origin` + CSP بلا إنترنت) ما بيقدر يوصل **للصفحة ولا للكوكيز ولا للشبكة** حتى لو عدّى الفحص. و**الجدار الثالث**: مراجعة المعلم.

```python
"""🤖 The model writes a NEW scene with our template's toolkit (option «ج» — hybrid).

What the model writes:   function buildScene(SDK, data) { … }    (≈ 30–120 lines, only the SDK, see sdk/scene_sdk.js)
What it can NOT do:      the network, the page around it, cookies/storage, eval… (checked here, and blocked again by the sandbox)
The flow:
  1. scene_data(...)   → what the model knows: the concept, its meaning, what it needs / who needs it (+ why), the age stage
  2. build_prompt(...) → system + user messages (toolkit reference, rules for the age, one worked example)
  3. llm(system, user) → the gateway (Gemini → GPT → Claude); any function(system, user) -> text works (tests use a fake one)
  4. check_code(...)   → safety + size + structure + a real JavaScript syntax check (node --check, if Node is installed)
  5. one repair round  → if the checks fail, the model gets the list of problems once and tries again
  6. runner_html(...)  → the sandbox page (CSP: no network) that runs the scene and reports back {ok, drawn, outside, errors}
Nothing reaches a student before a teacher approves it (status «pending_review»), and the factory's own scenes always stay.
Plain Python (standard library)."""
import json
import os
import re
import shutil
import subprocess
import tempfile

import audience as A
import offline_generator as og

HERE = os.path.dirname(os.path.abspath(__file__))
SDK_PATH = os.path.join(HERE, "sdk", "scene_sdk.js")
PROMPT_VERSION = "scene-v1"
MAX_CODE = 9000

# ---------- 1. what the model knows ----------
def scene_data(g, lesson, cid: str, art_svg=None) -> dict:
    """The facts for ONE concept (only from the graph) + the age stage + our drawings of it and its neighbours."""
    name = lambda x: g.concepts[x].text
    ins = [p for p in sorted(g.prereq_in.get(cid, [])) if og.is_entity(g, p)][:2]
    outs = [x for x in sorted(g.prereq_out.get(cid, [])) if og.is_entity(g, x)][:2]
    st = A.stage(g)
    ids = [cid] + ins + outs
    subject = str(g.book.get("subject", ""))
    icons = {x: og.icon_for(name(x), g.concepts[x].description, subject) for x in ids}
    why = {}
    for p in ins:
        w = p and name(p).replace("ال", "", 1).split()[0]
        why[p] = next((f.strip(" .") for f in (og.fragments(g.concepts[cid].description) or []) if w and w in f), "")
    return {"concept": {"id": cid, "name": name(cid), "meaning": g.concepts[cid].description or "",
                        "ins": [{"id": p, "name": name(p), "why": why.get(p, "")} for p in ins],
                        "outs": [{"id": x, "name": name(x)} for x in outs]},
            "concepts": {x: {"name": name(x), "meaning": g.concepts[x].description or ""} for x in ids},
            "lesson": {"id": lesson.id, "title": lesson.title}, "subject": subject, "stage": st,
            "grade": A.grade_of(g.book), "needsWord": "بيحتاج" if st in ("kids", "junior") else "بيعتمد على",
            "icons": icons, "art": {x: (art_svg(icons[x]) if art_svg else None) for x in ids}}


# ---------- 2. the prompt ----------
SDK_REFERENCE = """SDK (the ONLY things you may use). Stage: 640×340 units, (0,0) top-left. Right-to-left Arabic page.
- SDK.character(id, {x, y, size=90, label=true}) → h   draws OUR picture of a concept (ids from data.concepts)
    h.moveTo(x, y, ms) → Promise · h.say(text) (speech bubble, auto-wrapped, stays inside) · h.dim(bool) · h.glow(bool)
    h.onTap(fn) · h.draggable({onMove(h), onDrop(h)}) · h.near(otherHandle, dist=80) → bool · h.x, h.y, h.size
- SDK.arrow(fromH, toH, {label, hidden}) → a   the «needs» arrow FROM the one who needs TO what it needs; a.show(bool), a.redraw()
- SDK.text(x, y, str, {size=16, weight=700, color, ltr=false, anchor="middle"})   (formulas: ltr:true, e.g. "v = a × t")
- SDK.shape("circle"|"rect"|"line"|"path"|"ellipse"|"polygon"|"polyline", attrs)   (simple SVG shapes; colours: "var(--brand)", "var(--good)", "var(--warn)", "var(--ink)", "var(--muted)")
- SDK.slider({label, min, max, step, value}, onChange(value)) → {set(v), value}   ·   SDK.button(label, onClick)
- SDK.caption(text)   the narrator line under the picture (one sentence at a time)
- SDK.tween(ms, fn(t from 0 to 1)) → Promise   ·   SDK.wait(ms) → Promise   ·   SDK.done(note)   call when the student finished the activity"""

STAGE_RULES = {
    "kids": "Grade 1–4. A playful friend: simple Jordanian Arabic, characters may talk in the first person, at most one emoji per sentence.",
    "junior": "Grade 5–7. A curious explorer: friendly Jordanian Arabic, few emoji, short sentences.",
    "teen": "Grade 8–9. A confident classmate: clear Jordanian Arabic, NO face emoji, say «بيعتمد على» (not «بيحتاج»), no baby talk.",
    "senior": "Grade 10–12. A calm expert: precise and simple Arabic with the correct scientific terms, NO emoji, third person "
              "(««التسارع» بيعتمد على …»), formulas written left-to-right with SDK.text(..., {ltr:true}).",
}

EXAMPLE = r"""function buildScene(SDK, data) {
  const c = data.concept, need = c.ins[0];
  const me = SDK.character(c.id, { x: 470, y: 170, size: 110 });
  if (!need) { me.say(c.meaning); SDK.caption("«" + c.name + "»: " + c.meaning); SDK.done(); return; }
  const it = SDK.character(need.id, { x: 150, y: 170, size: 90 });
  const arrow = SDK.arrow(me, it, { hidden: true });
  SDK.caption("اسحب «" + c.name + "» لـ«" + need.name + "» وشوف شو العلاقة.");
  me.draggable({
    onMove: () => arrow.redraw(),
    onDrop: () => {
      if (!me.near(it, 140)) { me.moveTo(470, 170, 400).then(() => arrow.redraw()); return; }
      me.moveTo(330, 170, 300).then(() => {
        arrow.redraw(); arrow.show(true);
        me.say("«" + c.name + "» " + data.needsWord + " «" + need.name + "»" + (need.why ? ": " + need.why : "") + ".");
        SDK.caption(need.why ? "لأنه " + need.why + "." : "ما بيصير بدونه.");
        SDK.done("connected");
      });
    }
  });
}"""

SYSTEM = f"""You write ONE interactive explanation scene for an Arabic learning platform, as plain JavaScript.
Output ONLY one ```javascript code block containing exactly: function buildScene(SDK, data) {{ ... }}

Goal: the student UNDERSTANDS the concept by DOING something (drag, slide, tap) and SEEING what changes. No quiz, no right/wrong score.
Use ONLY the facts in `data` (data.concept.meaning, data.concept.ins[].why, names). Never invent facts, numbers or relations.

{SDK_REFERENCE}

Hard rules (the code is checked automatically and rejected otherwise):
- Use only SDK.* and plain JS (const/let, arrays, Math, arrow functions, if, for with a fixed bound). No while loops, no for(;;).
- Never use: window, document, fetch, XMLHttpRequest, import, eval, Function, setInterval, innerHTML, localStorage, parent, top, location, navigator, constructor, prototype.
- Everything stays inside 640×340. At most 4 characters. Under {MAX_CODE} characters, ideally 30–120 lines.
- Every text shown to the student is Arabic (formulas may be Latin), short, and correct.
- Call SDK.caption(...) at the start (what to do) and SDK.done() when the activity is complete.

Worked example (one possible scene; invent a DIFFERENT activity that fits the concept):
```javascript
{EXAMPLE}
```"""


def build_prompt(data: dict, idea: str = None) -> tuple:
    """(system, user): the rules + the facts for this concept + the age stage + an optional idea from the teacher."""
    facts = {k: data[k] for k in ("concept", "concepts", "lesson", "subject", "stage", "grade", "needsWord")}
    user = (f"Age stage: {STAGE_RULES.get(data['stage'], STAGE_RULES['kids'])}\n"
            f"Concept data (JSON):\n{json.dumps(facts, ensure_ascii=False, indent=1)}\n"
            + (f"Teacher's idea for the activity: {idea}\n" if idea else "Choose the activity that best shows this concept and its relations.\n")
            + "Return only the code block.")
    return SYSTEM, user


# ---------- 4. the checks ----------
FORBIDDEN = [(r"\bwindow\b", "window"), (r"\bdocument\b", "document"), (r"\bfetch\s*\(", "fetch"), (r"XMLHttpRequest|WebSocket|EventSource", "network"),
             (r"\bimport\b", "import"), (r"\beval\s*\(", "eval"), (r"\bFunction\s*\(", "Function()"), (r"\bsetInterval\b", "setInterval"),
             (r"innerHTML|outerHTML|insertAdjacentHTML", "innerHTML"), (r"localStorage|sessionStorage|indexedDB|cookie", "storage"),
             (r"\bparent\b|\btop\b\s*\.|\bopener\b|postMessage", "parent page"), (r"\blocation\b|\bnavigator\b", "location/navigator"),
             (r"constructor|prototype|__proto__|globalThis|\bself\b", "escape tricks"), (r"<\s*/?\s*script|</", "html tags"),
             (r"\bwhile\b", "while loop"), (r"for\s*\(\s*;\s*;", "endless for")]


def extract_code(text: str) -> str:
    """The code inside the first ```javascript block (or the whole text if there is no block)."""
    m = re.search(r"```(?:javascript|js)?\s*\n([\s\S]*?)```", text or "")
    return (m.group(1) if m else (text or "")).strip()


def _strip_strings(code: str) -> str:
    """The code without strings and comments (so «while» inside an Arabic sentence is not a while loop).
    Inside `template ${strings}` the ${…} parts ARE code, so they are kept."""
    code = re.sub(r"/\*[\s\S]*?\*/|//[^\n]*", " ", code)
    code = re.sub(r"`(?:\\.|[^`\\])*`", lambda m: " ".join(re.findall(r"\$\{([^}]*)\}", m.group())) or "''", code)
    return re.sub(r"'(?:\\.|[^'\\\n])*'|\"(?:\\.|[^\"\\\n])*\"", "''", code)


def check_code(code: str, node_check: bool = True) -> list:
    """Every problem found (empty list = OK): structure, size, forbidden things, brackets, and JavaScript syntax (node --check)."""
    problems = []
    if not code:
        return ["empty: no code"]
    if len(code) > MAX_CODE:
        problems.append(f"too long: {len(code)} > {MAX_CODE} characters")
    if not re.search(r"function\s+buildScene\s*\(\s*SDK\s*,\s*data\s*\)", code):
        problems.append("missing: function buildScene(SDK, data)")
    bare = _strip_strings(code)
    for pat, label in FORBIDDEN:                           # loops: only real code counts · everything else: also inside strings
        if re.search(pat, bare) or (label not in ("while loop", "endless for") and re.search(pat, code)):
            problems.append(f"forbidden: {label}")
    for o, c in ("()", "[]", "{}"):
        if bare.count(o) != bare.count(c):
            problems.append(f"unbalanced: {o}{c}")
    if node_check and shutil.which("node") and not any(p.startswith("forbidden") for p in problems):
        with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as f:
            f.write(code + "\n")
            path = f.name
        try:
            r = subprocess.run(["node", "--check", path], capture_output=True, text=True, timeout=10)
            if r.returncode != 0:
                err = [ln for ln in (r.stderr or "").splitlines() if "Error" in ln]
                problems.append("syntax: " + (err[0] if err else "invalid JavaScript")[:200])
        except Exception:                                    # no node / timeout → the browser check (runner) still runs
            pass
        finally:
            os.unlink(path)
    return problems


# ---------- 3 + 5. ask the model (with one repair round) ----------
def write_scene(data: dict, llm, idea: str = None, repair: bool = True) -> dict:
    """Ask the model for a scene and check it. Returns {code, problems, ok, attempts}. Never raises for a bad answer."""
    system, user = build_prompt(data, idea)
    attempts, code, problems = 0, "", ["not asked"]
    for round_ in range(2 if repair else 1):
        attempts += 1
        msg = user if round_ == 0 else (user + "\n\nYour previous code was REJECTED for these problems:\n- " + "\n- ".join(problems)
                                         + "\nFix them and return the whole function again.\nPrevious code:\n```javascript\n" + code[:MAX_CODE] + "\n```")
        try:
            text = llm(system, msg)
        except Exception as e:                               # no key / no credit / busy → reported, nothing breaks
            return {"code": code, "problems": [f"model: {e}"], "ok": False, "attempts": attempts}
        code = extract_code(text)
        problems = check_code(code)
        if not problems:
            break
    return {"code": code, "problems": problems, "ok": not problems, "attempts": attempts}


# ---------- 6. the sandbox page ----------
STAGE_CSS = """:root{--bg:#fff;--panel:#fff;--ink:#17222D;--muted:#5C6A77;--line:#D6DEE6;--chip:#EDF1F5;--brand:#1F6F78;--good:#2E8B57;--warn:#B9770E}
@media (prefers-color-scheme:dark){:root{--bg:#151F28;--panel:#151F28;--ink:#E4ECF2;--muted:#9AAAB8;--line:#283643;--chip:#1C2834;--brand:#4FB3BD;--good:#4CB36E;--warn:#E3B44F}}
body[data-stage=teen]{--brand:#2F6FA8}body[data-stage=senior]{--brand:#0F766E}
html,body{margin:0;background:var(--bg);color:var(--ink);font-family:"IBM Plex Sans Arabic",Tahoma,system-ui,sans-serif}
#stage{display:block;width:100%;height:auto;touch-action:none}#cap{min-height:1.8em;padding:6px 12px;font-weight:700;text-align:center}
#ui{display:flex;flex-wrap:wrap;gap:10px;justify-content:center;padding:4px 10px 10px}
.sdk-sl{display:flex;gap:8px;align-items:center;font-weight:700}.sdk-sl b{min-width:2.2em;text-align:center}
.sdk-btn{font:inherit;font-weight:700;border:0;border-radius:10px;padding:7px 14px;background:var(--brand);color:#fff;cursor:pointer}
.sdk-name{font-weight:800;font-size:14px;fill:var(--ink)}.sdk-text{fill:var(--ink)}.sdk-shape:not([fill]){fill:var(--chip)}.sdk-shape:not([stroke]){stroke:var(--ink);stroke-width:1.5}
.sdk-line{fill:none;stroke:var(--muted);stroke-width:3}.sdk-tag{fill:var(--panel);stroke:var(--line)}.sdk-tagt{font-size:11px;font-weight:800;fill:var(--muted)}
.sdk-bub rect{fill:var(--panel);stroke:var(--brand);stroke-width:2}.sdk-tail{fill:var(--panel);stroke:var(--brand);stroke-width:2}.sdk-bub text{font-size:13.5px;font-weight:800;fill:var(--ink)}
.sdk-glow .sdk-body{filter:drop-shadow(0 0 6px var(--brand))}.sdk-blob{fill:var(--brand);opacity:.5}
body[data-stage=senior] .sface{display:none}body[data-stage=teen] .sface .scheek,body[data-stage=teen] .sface .brows,body[data-stage=teen] .sface .m{display:none}
.sface .m{display:none}.sface .m-happy{display:inline}"""


def runner_html(code: str, data: dict, sdk_js: str = None) -> str:
    """The sandbox page for one scene. Put it in <iframe sandbox="allow-scripts">: the CSP blocks every network request."""
    sdk_js = sdk_js if sdk_js is not None else open(SDK_PATH, encoding="utf-8").read()
    safe = lambda s: s.replace("</", "<\\/")
    return ("<!doctype html><html lang=\"ar\" dir=\"rtl\"><head><meta charset=\"utf-8\">"
            "<meta http-equiv=\"Content-Security-Policy\" content=\"default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; img-src data:\">"
            f"<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\"><style>{STAGE_CSS}</style></head>"
            f"<body data-stage=\"{data.get('stage', 'kids')}\"><svg id=\"stage\" viewBox=\"0 0 640 340\" role=\"img\" aria-label=\"{data['concept']['name']}\">"
            "<defs><marker id=\"sdkhead\" viewBox=\"0 0 10 10\" refX=\"8\" refY=\"5\" markerWidth=\"7\" markerHeight=\"7\" orient=\"auto-start-reverse\">"
            "<path d=\"M1 1 L9 5 L1 9\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"1.8\"/></marker></defs></svg>"
            "<div id=\"cap\" aria-live=\"polite\"></div><div id=\"ui\"></div>"
            f"<script>window.DATA={safe(json.dumps(data, ensure_ascii=False))};</script>"
            f"<script>{safe(sdk_js)}</script><script>{safe(code)}\n;window.buildScene=typeof buildScene==='function'?buildScene:undefined;</script>"
            "<script>window.__bootScene();</script></body></html>")
```

---

## `02_question_factory/audience.py` 🆕 (الدفعة ٢٥)
**👥 الصف ← المرحلة ← طريقة الحكي.** بايثون عادي، **بلا AI**.

| الدالة | شو بتعمل |
|---|---|
| `grade_of(book)` | الصف من حقل `grade` (رقم أو `"g10"`)، أو من **العنوان** («الصف الحادي عشر» ← ١١؛ الأسماء الطويلة أول عشان «الثاني عشر» ما ينقرا «الثاني»)، أو من الـ id (`…_g10`). إذا ما عرف ← `None` |
| `stage_of_grade(n)` | ١–٤ `kids` · ٥–٧ `junior` · ٨–٩ `teen` · ١٠–١٢ `senior` (مش معروف ← `kids`، الشكل الأصلي) |
| `audience(g)` | `{grade, stage, label, persona}` ← بينحط **بكل درس** |
| `voice(text, stage)` | **نفس الجملة بحكي العمر**: الصغار زي ما هي · ابتدائي عليا بلا وجوه إيموجي · إعدادي وثانوي: «بيحتاج» ← «**بيعتمد على**»، «بيتعب» ← «**بيتأثر**»، «بتصحى» ← «**بتتفعّل**»، «الشريط السحري» ← «**جرّب المتغيّرات**»… · ثانوي كمان **بلا إيموجي** بالكلام (إلا ✅ ⚠️). **مرتين = مرة** (ثابتة) |
| `voice_record(rec, stage)` | بتمشي على الدرس كله وبتغيّر **حقول الكلام بس** (`steps`، `paragraph`، `say`، `q`، `a`، `front`، `back`، `facts`…)، **ولا id ولا رقم بيتغير** |

**نفس القواعد بالصفحة** (`VOICE` بـ `stage.js`)، عشان لو حدا جرّب مرحلة ثانية بالمفتاح، الكلام بيطلع صح.

```python
"""👥 Who is the lesson for? The book's GRADE decides the STAGE, and the stage decides how the explanation TALKS.

Stages (the same four the page uses, stage.js):
  kids   (grades 1–4)   a playful friend      — the original words (nothing changes)
  junior (grades 5–7)   a curious explorer    — the same words, a few emoji less
  teen   (grades 8–9)   a confident classmate — «بيعتمد على» instead of «بيحتاج», «بيتأثر» instead of «بيتعب», no face emoji
  senior (grades 10–12) a calm expert         — like teen, and no emoji inside the words at all

Plain Python, no AI: a grade lookup + word replacements. The page applies the same rules (VOICE in stage.js),
so a lesson looks right even when someone tries another stage with the switcher."""
import re

STAGES = {
    "kids": {"label": "الصغار", "grades": (1, 4), "persona": "رفيق مرح"},
    "junior": {"label": "ابتدائي عليا", "grades": (5, 7), "persona": "مستكشف فضولي"},
    "teen": {"label": "إعدادي", "grades": (8, 9), "persona": "زميل واثق"},
    "senior": {"label": "ثانوي", "grades": (10, 12), "persona": "خبير هادي"},
}

# «الصف العاشر» → 10 (the longer names first: «الحادي عشر» before «الأول», «الثاني عشر» before «الثاني»)
_ORDINALS = (("الحادي عشر", 11), ("الثاني عشر", 12), ("العاشر", 10), ("التاسع", 9), ("الثامن", 8), ("السابع", 7), ("السادس", 6),
             ("الخامس", 5), ("الرابع", 4), ("الثالث", 3), ("الثاني", 2), ("الأول", 1))


def grade_of(book: dict):
    """The book's grade (1–12) from its «grade» field, or its title («الصف العاشر»), or its id («…_g10»). None if unknown."""
    book = book or {}
    g = book.get("grade")
    if isinstance(g, int) and 1 <= g <= 12:
        return g
    if isinstance(g, str):
        m = re.search(r"\d+", g)
        if m and 1 <= int(m.group()) <= 12:
            return int(m.group())
    title = str(book.get("title", ""))
    for word, n in _ORDINALS:
        if word in title:
            return n
    m = re.search(r"g(\d{1,2})\b", str(book.get("id", "")))
    return int(m.group(1)) if m and 1 <= int(m.group(1)) <= 12 else None


def stage_of_grade(grade) -> str:
    """1–4 kids · 5–7 junior · 8–9 teen · 10–12 senior (unknown → kids, the original look)."""
    if not grade:
        return "kids"
    return next((k for k, v in STAGES.items() if v["grades"][0] <= grade <= v["grades"][1]), "kids")


def stage(g) -> str:
    return stage_of_grade(grade_of(getattr(g, "book", {}) or {}))


def audience(g) -> dict:
    """What the lesson carries for the page / the front end: {grade, stage, label, persona}."""
    grade = grade_of(getattr(g, "book", {}) or {})
    st = stage_of_grade(grade)
    return {"grade": grade, "stage": st, "label": STAGES[st]["label"], "persona": STAGES[st]["persona"]}


# ---- the VOICE: the same sentence the way that age talks (same lists as stage.js) ----
VOICE_WORDS = (("من اللي بيحتاج، للي بيحتاجه", "من اللي بيعتمد، للي بيعتمد عليه"),   # (the legend: never a dangling «على،»)
               ("شو بتحتاجي؟", "على شو بتعتمدي؟"), ("شو بتحتاج؟", "على شو بتعتمد؟"), ("شو بيحتاج", "على شو بيعتمد"), ("بيحتاجك", "بيعتمد عليك"),
               ("بتحتاجي", "بتعتمدي على"), ("خلص الحوار!", "خلص النقاش."), ("«يلا ←»", "«التالي ←»"), ("الشريط السحري", "جرّب المتغيّرات"),
               ("بيحتاجوه", "بيعتمدوا عليه"), ("بيحتاجوها", "بيعتمدوا عليها"), ("بيحتاجوا", "بيعتمدوا على"), ("بيحتاجه", "بيعتمد عليه"), ("بيحتاجها", "بيعتمد عليها"),
               ("بتحتاجه", "بتعتمد عليه"), ("بتحتاجها", "بتعتمد عليها"), ("بتحتاجيني", "بتعتمدي عليّ"), ("بتحتاجني", "بتعتمد عليّ"), ("بيحتاجني", "بيعتمد عليّ"), ("بحتاجك", "بعتمد عليك"),
               ("بيحتاج", "بيعتمد على"), ("بتحتاج", "بتعتمد على"), ("بيتعبوا", "بيتأثروا"), ("بيتعب", "بيتأثر"), ("بتتعب", "بتتأثر"), ("بيضل مبسوط", "ما بيتأثر"),
               ("بترجع مبسوطة", "بترجع طبيعية"), ("بتصحى", "بتتفعّل"), ("بيصحى", "بيتفعّل"), ("صحيت", "تفعّلت"), ("برافو!", "ممتاز."), ("يلا نشوف", "خلينا نشوف"))
_FACES = re.compile("[\U0001F600-\U0001F64F\U0001F917-\U0001F92F\U0001F970-\U0001F97A\U0001F60E\U0001F44B\U0001F463\U0001F446\U0001F642]")
_ANY_EMOJI = re.compile("[\U0001F000-\U0001FAFF⌀-⏿☀-➿⬀-⯿\U0001F1E6-\U0001F1FF]️?")
_KEEP = {"✅", "✔", "✔️", "⚠", "⚠️"}


def voice(text, st: str):
    """One sentence, said for this stage. kids: unchanged. junior: a few face emoji less. teen/senior: the grown-up words."""
    if not isinstance(text, str) or st == "kids":
        return text
    if st == "junior":
        return re.sub(r"\s{2,}", " ", re.sub(r"\s*[😄😢😟😎]+", "", text)).strip()
    s = re.sub(r"^أهلاً! أنا «([^»]+)»\.?$", lambda m: (f"تعريف «{m.group(1)}»." if st == "senior" else f"هاد «{m.group(1)}»."), text)
    s = re.sub(r"^📌\s*", "• ", s)                                       # the first line + the captions of «تعرّف عليّ»
    for a, b in VOICE_WORDS:
        s = s.replace(a, b)
    s = _FACES.sub("", s)
    if st == "senior":
        s = _ANY_EMOJI.sub(lambda m: m.group() if m.group() in _KEEP else "", s)
        s = re.sub("(?<![✅✔⚠])[\u200d\ufe0f]", "", s)                   # the glue of a removed emoji (🧑‍🏫) must not stay as an invisible mark
    s = re.sub(r"\s+([.،!؟:])", r"\1", s)
    return re.sub(r"\s{2,}", " ", s).strip()


# the human words inside a lesson record (ids, kinds and numbers are never touched)
_TEXT_KEYS = {"steps", "paragraph", "say", "says", "q", "a", "front", "back", "facts", "hook", "answer", "summary", "recap", "why", "drive", "info",
              "ready", "ok_say", "rev_say", "end_say", "fact", "ask", "opt", "reply", "learnt", "because", "short"}   # + the 5 new activities


def voice_record(rec, st: str):
    """The whole lesson, said for this stage (walks the record; only the text fields change)."""
    if st == "kids":
        return rec
    if isinstance(rec, list):
        return [voice_record(x, st) for x in rec]
    if not isinstance(rec, dict):
        return rec
    out = {}
    for k, v in rec.items():
        if k in _TEXT_KEYS:
            if isinstance(v, str):
                out[k] = voice(v, st)
            elif isinstance(v, list):
                out[k] = [voice(x, st) if isinstance(x, str) else voice_record(x, st) for x in v]
            elif isinstance(v, dict):
                out[k] = {kk: voice(vv, st) if isinstance(vv, str) else voice_record(vv, st) for kk, vv in v.items()}
            else:
                out[k] = v
        else:
            out[k] = voice_record(v, st)
    return out
```

---

## `02_question_factory/explain_activities.py` 🆕 (الدفعة ٢٦)
**🆕 ٥ فعاليات جديدة**، كلها **من الجراف بس**، وكل حركة بتنشرح. بايثون عادي، **بلا AI**. `explain_generator.explain_lesson` بيحط **فعالية وحدة لكل مفهوم** (`pick`)، و`check_scene` بيبعت هالأنواع لـ `check` هون.

| الدالة | بتاخذ | بتقرر | بترجع |
|---|---|---|---|
| `scene_recipe` 🧪 | المفهوم | إذا بيحتاج **٢ أو أكثر** (`_ins`)، ولكل واحد **ليش** (`eg._why` من معنى المفهوم بالجراف) | `{needs:[{id, why}], ready, steps, paragraph}` أو `None` |
| `scene_connect` ✏️ | المفهوم | جيرانه (٢ قبل + ٢ بعد) + **واحد ما إله أي علاقة** (`calm`، ولا من خلال سلسلة)، ولكل سهم جملة **الصح** و**المقلوب** | `{nodes, links:[{from, to, required, ok_say, rev_say}], calm, end_say}` |
| `_sibling` + `scene_compare` ⚖️ | المفهوم | مفهوم **قريب** (بيشتركوا بإشي بيحتاجوه أو إشي بيحتاجهم، ومش قبل/بعد بعض)، وبطاقات: التعريفين + **الشبه** + **الفرق** («و«ب» لأ» بس إذا **فعلاً** لأ، ولا من خلال سلسلة) | `{other, facts:[{fact, side: a/b/both, type, ref, why}], end_say}` |
| `scene_teach` 🧑‍🏫 | المفهوم | ٢–٣ أسئلة من زميل: التعريف (الغلط = **تعريف مفهوم ثاني**) · شو بيحتاج (الغلط = **السهم بالعكس** أو مفهوم مش قبله) · مين بيحتاجه | `{rounds:[{ask, rel, options:[{opt, id, ok, reply}]}], learnt}` |
| `scene_ladder` 🪜 | المفهوم | «ليش؟» ورا «ليش؟» (لورا لحد الأساس)، وإذا ما في ← «وبعدين؟» (لقدّام). بيختار الدرجة اللي **الجراف بيشرحها** أول | `{mode: why/then, rungs:[{id, because, short}], end_say}` |
| `pick` | المفهوم + رقمه | 🧪 **أول** إذا بيحتاج ٢+، وإلا **بالدور** (وكل درس بيبلش من مكان ثاني)، وإذا ما في داتا ← اللي بعدها | مشهد وحدة أو `None` |
| `check` | المشهد | كل جملة «بيحتاج» **سهم حقيقي**، وكل «لأ» **فعلاً لأ** | قائمة أغلاط (فاضية = تمام) |

**قاعدة الصدق:** «س بيحتاج ص» بس إذا في سهم بالجراف، و«س ما بيحتاج ص» بس إذا ص **مش قبل** س أبداً (ولا من خلال سلسلة). أي مشهد بيغلط **ما بيوصل للطالب** (`explain_main.py` بيشيله).

```python
"""🆕 Five more ways to UNDERSTAND a concept (batch 26). Everything comes from the graph only, and every move is explained.

  recipe   🧪 الشروط        the things a concept needs, as switches: it is complete only when ALL of them are there
  connect  ✏️ ارسم الأسهم   the student draws the «needs» arrows himself; a reversed arrow is explained (the most common mistake)
  compare  ⚖️ قارن          two close concepts; each fact goes to one of them or to «الاثنين» (the same / the different)
  teach    🧑‍🏫 اشرح لزميلك  a classmate does not get it; the student picks the right explanation (a wrong pick is explained)
  ladder   🪜 سلّم «ليش؟»   ask «ليش؟» again and again: each answer is the reason one step deeper, down to the base

No points and no failing: a wrong move = an explanation. Plain Python, no AI.
Truth rule (like the other scenes): a sentence says «X needs Y» only if the graph has that arrow, and «X does NOT need Y»
only if Y is not before X at all (not even through a chain). check() re-checks every scene against the graph."""
import random

import audience as A
import explain_generator as eg
import offline_generator as og

N = eg._name
V = eg._v


def _ins(g, x):
    return [p for p in sorted(g.prereq_in.get(x, [])) if og.is_entity(g, p)]


def _outs(g, x):
    return [n for n in sorted(g.prereq_out.get(x, [])) if og.is_entity(g, n)]


def _pieces(g, x):
    d = g.concepts[x].description
    return og.fragments(d) or ([d.strip(" .")] if d else [])


def _needs(g, x):
    """«بيحتاج» / «بتحتاج» — agrees with the concept (the page says «بيعتمد على» for the bigger grades)."""
    return V(N(g, x), "بيحتاج", "بتحتاج")


def _because(g, x):
    return V(N(g, x), "لأنه", "لأنها")


def _short_def(g, x):
    """The first piece of the meaning, not too long for a card (a shorter whole piece if the first one is very long)."""
    p = _pieces(g, x)
    if not p:
        return ""
    return p[0] if len(p[0].split()) <= 16 else og.tiny(g.concepts[x].description, 8)


def _rng(*key):
    return random.Random("act:" + ":".join(key))


# ---------------------------------------------------------------- 🧪 recipe
def scene_recipe(g, lesson, cid, used=None):
    """🧪 The things «X» needs, as switches. Starts empty; X is complete only when ALL are on (turn one off → you see why)."""
    ins = _ins(g, cid)
    if len(ins) < 2:                                       # one thing only is not a recipe (meet / dialogue already say it)
        return None
    ins = ins[:4]
    me, st = N(g, cid), A.stage(g)
    needs = []
    for a in ins:
        why = eg._why(g, a, cid)
        needs.append({"id": a, "why": f"«{me}» {_needs(g, cid)} «{N(g, a)}»" + (f": {why}." if why else ".")})
    done = V(me, "جاهز", "جاهزة") if st in ("kids", "junior") else V(me, "مكتمل", "مكتملة")
    has_all = V(me, "بيحتاجه", "بتحتاجه")
    ready = {"kids": f"✅ كل اللي {has_all} «{me}» موجود، فـ«{me}» {done}! 🎉",
             "junior": f"✅ كل اللي {has_all} «{me}» موجود، فـ«{me}» {done}!",
             "teen": f"✅ كل الشروط موجودة، فـ«{me}» {done}.",
             "senior": f"✅ الشروط كلها متحققة، فـ«{me}» {done}."}[st]
    names = eg._join([N(g, a) for a in ins])
    return {"kind": "recipe", "target": cid, "needs": needs, "ready": ready,
            "steps": [f"🧪 «{me}» شو {_needs(g, cid)}؟",
                      f"شغّل اللي تحت واحد واحد، وشوف إمتى «{me}» {V(me, 'بيصير', 'بتصير')} {done}.",
                      "وجرّب تطفي واحد منهم: شو بيصير؟"],
            "paragraph": f"«{me}» {_needs(g, cid)} {names} مع بعض، مش واحد بس. إذا غاب واحد منهم، «{me}» {V(me, 'بيضل', 'بتضل')} {V(me, 'ناقصه', 'ناقصها')} إشي."}


# ---------------------------------------------------------------- ✏️ connect
def _link(g, needer, needed, required=True):
    hn, dn = N(g, needer), N(g, needed)
    why = eg._why(g, needed, needer)
    return {"from": needer, "to": needed, "required": required,
            "ok_say": f"✅ «{hn}» {_needs(g, needer)} «{dn}»" + (f": {why}." if why else "."),
            "rev_say": f"↩️ السهم بالعكس: «{hn}» {V(hn, 'هو', 'هي')} اللي {_needs(g, needer)} «{dn}»، مش العكس."}


def scene_connect(g, lesson, cid, used=None):
    """✏️ The student draws the arrows around «X» (drag, or tap one then the other). Right → the reason. Reversed → why it is the other way."""
    ins, outs = _ins(g, cid)[:2], _outs(g, cid)[:2]
    if len(ins) + len(outs) < 2:
        return None
    me, st = N(g, cid), A.stage(g)
    near = set(ins + outs) | g.ancestors(cid) | g.descendants(cid) | {cid}
    calm = [x for x in og.tiered(g, lesson, _rng("connect", cid), exclude=near)][:1]   # one with NO arrow to «X» (not even through a chain)
    nodes = [cid] + ins + outs + calm
    links = [_link(g, cid, a) for a in ins] + [_link(g, x, cid) for x in outs]
    have = {(l["from"], l["to"]) for l in links}
    for a in nodes:                                        # a real arrow between two of the others is accepted too (never called wrong)
        for b in nodes:
            if a != b and g.is_prereq(a, b) and (b, a) not in have:
                links.append(_link(g, b, a, required=False)); have.add((b, a))
    how = ("اسحب من اللي بيحتاج، للي بيحتاجه (أو اكبس على الاثنين بالترتيب)." if st in ("kids", "junior")
           else "اسحب السهم من المفهوم اللي بيعتمد، للمفهوم اللي بيعتمد عليه (أو اكبس عليهم بالترتيب).")
    req = [l for l in links if l["required"]]
    end = "🎉 رسمت كل الأسهم! " + " ".join(l["ok_say"].removeprefix("✅ ") for l in req)
    return {"kind": "connect", "target": cid, "nodes": nodes, "links": links, "calm": calm, "end_say": end,
            "steps": [f"✏️ ارسم الأسهم حول «{me}».", how, "كل سهم صح بيحكيلك ليش، والسهم المقلوب بيحكيلك كمان ليش."],
            "paragraph": " ".join(l["ok_say"].removeprefix("✅ ") for l in req)
                         + (f" أما «{N(g, calm[0])}» فما في سهم مباشر {V(N(g, calm[0]), 'بينه', 'بينها')} وبين «{me}»." if calm else "")}


# ---------------------------------------------------------------- ⚖️ compare
def _sibling(g, lesson, cid, used):
    """A close concept to compare with: shares something it needs or something that needs it, and is not before/after it."""
    me_in, me_out = set(_ins(g, cid)), set(_outs(g, cid))
    anc, desc = g.ancestors(cid), g.descendants(cid)
    here = [c.id for c in lesson.concepts]
    cands = []
    for x in sorted(g.concepts):
        if x == cid or not og.is_entity(g, x) or x in anc or x in desc or not _pieces(g, x):
            continue
        shared = (me_in & set(_ins(g, x))) | (me_out & set(_outs(g, x)))
        if shared and frozenset((cid, x)) not in used:
            cands.append((x not in here, -len(shared), x))
    return sorted(cands)[0][2] if cands else None


def scene_compare(g, lesson, cid, used=None):
    """⚖️ «X» and a close concept «Y»: each fact card goes to «X», to «Y», or to «الاثنين». The same + the different."""
    used = used if used is not None else set()
    o = _sibling(g, lesson, cid, used)
    if not o or not _pieces(g, cid) or _short_def(g, o) == _short_def(g, cid):
        return None
    me, on = N(g, cid), N(g, o)
    facts = [{"fact": _short_def(g, cid), "side": "a", "ref": cid, "type": "def", "why": f"هاد تعريف «{me}»."},
             {"fact": _short_def(g, o), "side": "b", "ref": o, "type": "def", "why": f"هاد تعريف «{on}»."}]
    for s in sorted(set(_ins(g, cid)) & set(_ins(g, o)))[:1]:
        facts.append({"fact": f"بحاجة لـ«{N(g, s)}»", "side": "both", "ref": s, "type": "need",
                      "why": f"«{me}» و«{on}» الاثنين بيحتاجوا «{N(g, s)}»."})
    for x in sorted(set(_outs(g, cid)) & set(_outs(g, o)))[:1]:
        facts.append({"fact": f"شرط لـ«{N(g, x)}»", "side": "both", "ref": x, "type": "feed",
                      "why": f"«{N(g, x)}» {_needs(g, x)} «{me}» و«{on}» الاثنين."})
    for side, a, b in (("a", cid, o), ("b", o, cid)):          # different: true for one, and NOT true for the other (not even through a chain)
        an, bn = N(g, a), N(g, b)
        for i in [i for i in _ins(g, a) if i != b and i not in g.ancestors(b)][:1]:
            facts.append({"fact": f"بحاجة لـ«{N(g, i)}»", "side": side, "ref": i, "type": "need",
                          "why": f"«{an}» {_needs(g, a)} «{N(g, i)}»، و«{bn}» لأ."})
        for x in [x for x in _outs(g, a) if x != b and x not in g.descendants(b)][:1]:
            facts.append({"fact": f"شرط لـ«{N(g, x)}»", "side": side, "ref": x, "type": "feed",
                          "why": f"«{N(g, x)}» {_needs(g, x)} «{an}»، مش «{bn}»."})
    if not any(f["side"] == "both" for f in facts):
        return None
    keep = facts[:2] + [f for f in facts[2:] if f["side"] == "both"][:1]
    keep += [f for f in facts[2:] if f not in keep][:6 - len(keep)]
    used.add(frozenset((cid, o)))
    order = keep[:]
    _rng("compare", cid).shuffle(order)                          # the tray is mixed (the same mix every time)
    same = next(f for f in keep if f["side"] == "both")["why"]
    return {"kind": "compare", "target": cid, "other": o, "facts": order,
            "end_say": f"🎉 رتّبت كل البطاقات! الشبه: {same} والفرق بالتعريف: «{me}»: {_short_def(g, cid)}، و«{on}»: {_short_def(g, o)}.",
            "steps": [f"⚖️ «{me}» و«{on}»: شو الشبه وشو الفرق؟",
                      f"اكبس على بطاقة، وبعدين اكبس على مكانها: عند «{me}»، عند «{on}»، ولا عند الاثنين.",
                      "الشبه بيربطهم ببعض، والفرق بيخليك ما تخلط بينهم."],
            "paragraph": f"«{me}» و«{on}» قريبين من بعض: {same} بس كل واحد إله تعريفه: «{me}»: {_short_def(g, cid)}. و«{on}»: {_short_def(g, o)}."}


# ---------------------------------------------------------------- 🧑‍🏫 teach
def scene_teach(g, lesson, cid, used=None):
    """🧑‍🏫 A classmate does not get «X». Three questions; the student picks the right answer. A wrong pick is explained
    (the other definition belongs to «Y» · the arrow is the other way) — the classic mistakes, said out loud."""
    pa = _pieces(g, cid)
    if not pa:
        return None
    me, st = N(g, cid), A.stage(g)
    ins, outs = _ins(g, cid), _outs(g, cid)
    anc, desc = g.ancestors(cid), g.descendants(cid)
    rng = _rng("teach", cid)
    others = [x for x in og.tiered(g, lesson, rng, exclude={cid}) if _pieces(g, x) and _short_def(g, x) != _short_def(g, cid)]
    if not others:
        return None
    o = others[0]
    rounds = [{"ask": f"شو يعني «{me}»؟", "rel": "def",
               "options": [{"opt": _short_def(g, cid), "id": cid, "ok": True, "reply": f"آها! يعني «{me}»: {_short_def(g, cid)}."},
                           {"opt": _short_def(g, o), "id": o, "ok": False, "reply": f"لأ، هاد تعريف «{N(g, o)}»، مش «{me}»."}]}]
    if ins:
        a = ins[0]
        why = eg._why(g, a, cid)
        wrong = outs[0] if outs else next((x for x in others if x not in anc), None)
        if wrong:
            wn = N(g, wrong)
            wr = (f"لأ، بالعكس: «{wn}» {V(wn, 'هو', 'هي')} اللي {_needs(g, wrong)} «{me}»." if wrong in outs
                  else f"لأ، «{me}» ما {_needs(g, cid)} «{wn}».")
            rounds.append({"ask": f"طيب، «{me}» شو {_needs(g, cid)}؟", "rel": "needs",
                           "options": [{"opt": f"«{N(g, a)}»", "id": a, "ok": True,
                                        "reply": f"آها! «{me}» {_needs(g, cid)} «{N(g, a)}»" + (f"، {_because(g, cid)} {why}." if why else ".")},
                                       {"opt": f"«{wn}»", "id": wrong, "ok": False, "reply": wr}]})
    if outs:
        x = outs[0]
        why = eg._why(g, cid, x)
        wrong = ins[0] if ins else next((y for y in others if y not in desc and y not in anc), None)
        if wrong:
            wn = N(g, wrong)
            wr = (f"لأ، بالعكس: «{me}» {V(me, 'هو', 'هي')} اللي {_needs(g, cid)} «{wn}»." if wrong in ins
                  else f"لأ، «{wn}» ما {_needs(g, wrong)} «{me}».")
            rounds.append({"ask": f"وليش «{me}» {V(me, 'مهم', 'مهمة')}؟ مين {V(me, 'بيحتاجه', 'بيحتاجها')}؟", "rel": "needed_by",
                           "options": [{"opt": f"«{N(g, x)}»", "id": x, "ok": True,
                                        "reply": f"آها! «{N(g, x)}» {_needs(g, x)} «{me}»" + (f"، {_because(g, x)} {why}." if why else ".")},
                                       {"opt": f"«{wn}»", "id": wrong, "ok": False, "reply": wr}]})
    if len(rounds) < 2:
        return None
    for r in rounds:
        rng.shuffle(r["options"])
    said = [next(op["reply"] for op in r["options"] if op["ok"]).removeprefix("آها! ").removeprefix("يعني ") for r in rounds]
    kid = st in ("kids", "junior")
    return {"kind": "teach", "target": cid, "rounds": rounds, "learnt": "📝 هيك شرحتها: " + " ".join(said),
            "steps": ([f"🧑‍🏫 صاحبك مش فاهم «{me}»… ساعده!", "اختار الجواب الصح لكل سؤال. ولو غلطت، رح تعرف ليش.", "لما تشرح لغيرك، إنت بتفهم أكثر 💡"] if kid else
                      [f"🧑‍🏫 زميلك مش فاهم «{me}»، اشرحله.", "اختار الجواب الصح لكل سؤال، وأي غلط رح ينشرح.", "الشرح لغيرك بيثبّت الفكرة عندك."]),
            "paragraph": " ".join(said)}


# ---------------------------------------------------------------- 🪜 ladder
def scene_ladder(g, lesson, cid, used=None):
    """🪜 «ليش؟» again and again: «X» needs «A» because…, «A» needs «B» because… — down to the base (or «وبعدين؟» forward)."""
    me = N(g, cid)

    def climb(nexts, sentence):
        rungs, cur, seen = [], cid, {cid}
        while len(rungs) < 3:
            cands = [x for x in nexts(cur) if x not in seen]
            if not cands:
                break
            x = next((c for c in cands if sentence(cur, c)[1]), cands[0])   # prefer a step the graph explains
            text, _ = sentence(cur, x)
            rungs.append({"id": x, "because": text[0], "short": text[1]})
            seen.add(x); cur = x
        return rungs

    def why_step(cur, a):          # «cur» needs «a» (going down to the base)
        why = eg._why(g, a, cur)
        short = f"«{N(g, cur)}» {_needs(g, cur)} «{N(g, a)}»"
        return (short + (f"، {_because(g, cur)} {why}." if why else "."), short), why

    def then_step(cur, x):         # «x» needs «cur» (going on to what comes after)
        why = eg._why(g, cur, x)
        short = f"«{N(g, x)}» {_needs(g, x)} «{N(g, cur)}»"
        return (short + (f"، {_because(g, x)} {why}." if why else "."), short), why

    rungs, mode = climb(lambda c: _ins(g, c), why_step), "why"
    if len(rungs) < 2:
        rungs, mode = climb(lambda c: _outs(g, c), then_step), "then"
    if len(rungs) < 2:
        return None
    last = rungs[-1]["id"]
    ln = N(g, last)
    if mode == "why":
        end = (f"🏁 وصلنا للأساس: «{ln}» ما {_needs(g, last)} إشي {V(ln, 'قبله', 'قبلها')}." if not _ins(g, last)
               else f"🏁 وصلنا لـ«{ln}»، والسلسلة بتكمّل {V(ln, 'قبله', 'قبلها')} كمان.")
        steps = [f"🪜 شو ورا «{me}»؟ اكبس «ليش؟» وانزل درجة درجة.", "كل درجة بتحكيلك السبب: مين بيحتاج مين، وليش.", "لما توصل للأساس، بتشوف السلسلة كاملة."]
    else:
        end = (f"🏁 «{ln}» آخر وحدة بهالسلسلة." if not _outs(g, last)
               else f"🏁 وصلنا لـ«{ln}»، والسلسلة بتكمّل {V(ln, 'بعده', 'بعدها')} كمان.")
        steps = [f"🪜 شو بيجي بعد «{me}»؟ اكبس «وبعدين؟» وانزل درجة درجة.", "كل درجة بتحكيلك مين بيحتاج اللي قبله، وليش.", "لما توصل للآخر، بتشوف السلسلة كاملة."]
    return {"kind": "ladder", "target": cid, "mode": mode, "rungs": rungs, "end_say": end, "steps": steps,
            "paragraph": " ".join(r["because"] for r in rungs) + " " + end.removeprefix("🏁 ")}


MAKERS = [scene_recipe, scene_connect, scene_compare, scene_teach, scene_ladder]
KINDS = ("recipe", "connect", "compare", "teach", "ladder")


def pick(g, lesson, cid, i, used):
    """ONE new activity per concept: 🧪 the recipe when the concept needs 2+ things; otherwise a different one for each concept
    (each lesson starts somewhere else), the next one if the graph has not enough for it."""
    s = scene_recipe(g, lesson, cid, used)                 # needs 2+ things at once (the leaf: light + air + the stem): the recipe fits best
    if s:
        return s
    rest = MAKERS[1:]
    ids = [l.id for l in g.lessons()]
    start = (i + 2 * (ids.index(lesson.id) if lesson.id in ids else 0)) % len(rest)
    for maker in rest[start:] + rest[:start]:
        s = maker(g, lesson, cid, used)
        if s:
            return s
    return None


# ---------------------------------------------------------------- the check (the picture must never teach something wrong)
def check(g, s) -> list:
    k, t, errors = s["kind"], s.get("target"), []
    if k == "recipe":
        errors += [f"recipe: {t} does not need {n['id']}" for n in s["needs"] if not g.is_prereq(n["id"], t)]
        if len(s["needs"]) < 2:
            errors.append("recipe: fewer than 2 things")
    elif k == "connect":
        for l in s["links"]:
            if not g.is_prereq(l["to"], l["from"]):
                errors.append(f"connect: {l['from']} does not need {l['to']}")
        for c in s.get("calm", []):
            if c in g.ancestors(t) or c in g.descendants(t):
                errors.append(f"connect: {c} is linked to {t}")
        if not any(l["required"] for l in s["links"]):
            errors.append("connect: nothing to draw")
    elif k == "compare":
        o = s["other"]
        if o in g.ancestors(t) or o in g.descendants(t):
            errors.append("compare: the two are before/after each other")
        for f in s["facts"]:
            r, side = f["ref"], f["side"]
            if f["type"] == "def":
                ok = r == (t if side == "a" else o)
            elif f["type"] == "need":
                ok = (g.is_prereq(r, t) and g.is_prereq(r, o)) if side == "both" else (
                    g.is_prereq(r, t) and r not in g.ancestors(o) if side == "a" else g.is_prereq(r, o) and r not in g.ancestors(t))
            else:
                ok = (g.is_prereq(t, r) and g.is_prereq(o, r)) if side == "both" else (
                    g.is_prereq(t, r) and r not in g.descendants(o) if side == "a" else g.is_prereq(o, r) and r not in g.descendants(t))
            if not ok:
                errors.append(f"compare: «{f['fact']}» is not on side {side}")
    elif k == "teach":
        for r in s["rounds"]:
            for op in r["options"]:
                x = op["id"]
                if r["rel"] == "needs":
                    ok = g.is_prereq(x, t) if op["ok"] else (x not in g.ancestors(t))
                elif r["rel"] == "needed_by":
                    ok = g.is_prereq(t, x) if op["ok"] else (x not in g.descendants(t))
                else:
                    ok = (x == t) == op["ok"]
                if not ok:
                    errors.append(f"teach: option {x} ({r['rel']}) is not true")
    elif k == "ladder":
        prev = t
        for r in s["rungs"]:
            if not (g.is_prereq(r["id"], prev) if s["mode"] == "why" else g.is_prereq(prev, r["id"])):
                errors.append(f"ladder: {prev} → {r['id']} is not a link")
            prev = r["id"]
    ids = s.get("nodes", []) + [n["id"] for n in s.get("needs", [])] + [r["id"] for r in s.get("rungs", [])] + ([s["other"]] if s.get("other") else [])
    errors += [f"{k}: unknown concept {x}" for x in ids if x not in g.concepts or not og.is_entity(g, x)]
    return errors
```

---

## `02_question_factory/sdk/scene_sdk.js` 🆕 (الدفعة ٢٥)
**🧰 أدوات القالب للموديل.** الموديل بيكتب `buildScene(SDK, data)` بس، وكل الرسم بيمر من هون، فالمشهد **بيضل بشكل المنصة**: شخصياتنا، فقاعاتنا (ما بتنقص وبتلف الكلام)، أسهمنا، والمرحلة العمرية.

| الأداة | شو بتعمل |
|---|---|
| `SDK.character(id, {x, y, size, label})` | **شخصية من مكتبتنا** (الرسمة جاية بـ `data.art`)، وبترجع مقبض: `moveTo` (حركة بالوقت) · `say` (فقاعة جوا الصورة) · `dim` · `glow` · `onTap` · `draggable` (سحب بالماوس والإصبع، محصور جوا الصورة) · `near` |
| `SDK.arrow(a, b, {label, hidden})` | سهم «بيحتاج» **من اللي بيحتاج للي بيحتاجه**، والكلمة حسب العمر |
| `SDK.text` · `SDK.shape` | نص (المعادلات `ltr`) وأشكال بسيطة (بس دائرة، مستطيل، خط، مسار…) |
| `SDK.slider` · `SDK.button` | شريط وزر **تحت** الصورة |
| `SDK.caption` | سطر الراوي (بيوصل للصفحة كمان) |
| `SDK.tween` · `SDK.wait` | حركة **بالوقت** · استنا (أكثر إشي ١٠ ثواني) |
| `SDK.done(note)` | الطالب خلّص الفعالية |
| **التقرير** | بعد ١٫٢ ثانية (ومع `done`): `{ok, drawn, outside, errors}` ← `postMessage` للصفحة. وكمان `llm-size` (طول الصفحة) و`llm-caption` |

```javascript
/* ======================= 🧰 SCENE SDK v1 — the toolkit a model-written scene may use =======================
   The model writes ONLY:   function buildScene(SDK, data) { ... }
   It runs inside a sandboxed iframe (no network, no cookies, no parent page). Everything it draws goes through this SDK,
   so the scene keeps the platform's look: our characters, our speech bubbles (never cut, wrapped), our arrows, the age stage.
   data = {concept:{id,name,meaning,ins:[{id,name,why}],outs:[{id,name}]}, stage, subject, art:{id: "<svg…>"}, lesson}
   The runner reports back to the page: {type:"llm-scene", ok, drawn, outside, errors, done}. */
(function(){
  const NS="http://www.w3.org/2000/svg",W=640,H=340;
  const stage=document.getElementById("stage"),capEl=document.getElementById("cap"),ui=document.getElementById("ui");
  const errors=[];let drawn=0,doneNote=null;const handles=[];
  const node=(tag,attrs,parent)=>{const e=document.createElementNS(NS,tag);Object.entries(attrs||{}).forEach(([k,v])=>{if(v!==undefined&&v!==null)e.setAttribute(k,String(v));});(parent||stage).appendChild(e);drawn++;return e;};
  const clamp=(v,a,b)=>Math.max(a,Math.min(b,v));
  const layer=node("g",{id:"scene"}),bubbles=node("g",{id:"bubbles","pointer-events":"none"});drawn-=2;
  /* split a sentence into short lines (≈22 letters), never cutting a word; at most 4 lines */
  function lines(t){const w=String(t||"").split(/\s+/).filter(Boolean),out=[""];let cut=false;for(const x of w){const c=out[out.length-1];if(!c||(c+" "+x).length<=22)out[out.length-1]=(c+" "+x).trim();else if(out.length<4)out.push(x);else{cut=true;break;}}if(cut)out[out.length-1]+=" …";return out;}
  function bubbleFor(h,text){bubbles.innerHTML="";if(!text)return;const ls=lines(text),LH=19,bh=14+ls.length*LH;
    const g=node("g",{class:"sdk-bub"},bubbles);const r=node("rect",{rx:12,height:bh},g);const ts=ls.map((l,i)=>node("text",{y:22+i*LH,"text-anchor":"middle"},g));ts.forEach((t,i)=>t.textContent=ls[i]);
    let tw=0;ts.forEach(t=>{try{tw=Math.max(tw,t.getComputedTextLength());}catch(e){}});const bw=Math.max(70,Math.ceil(tw||ls.join("").length*8)+28);r.setAttribute("width",bw);ts.forEach(t=>t.setAttribute("x",bw/2));
    let top=h.y-h.size/2-bh-12;const down=top<6;if(down)top=Math.min(H-bh-6,h.y+h.size/2+26);const left=clamp(h.x-bw/2,6,W-6-bw);const tx=clamp(h.x-left,16,bw-16);
    node("path",{class:"sdk-tail",d:down?`M${tx-8} 2 L${tx} -10 L${tx+8} 2`:`M${tx-8} ${bh-2} L${tx} ${bh+10} L${tx+8} ${bh-2}`},g);g.setAttribute("transform",`translate(${left} ${top})`);drawn-=ls.length+3;}
  function art(id,size){const s=(window.DATA.art||{})[id];if(!s)return `<circle cx="50" cy="50" r="40" class="sdk-blob"/>`;return s.replace(/^[\s\S]*?<svg[^>]*>/,"").replace(/<\/svg>\s*$/,"");}
  const SDK={
    W,H,
    data:null,
    /* a character from our art library: SDK.character("root", {x, y, size, label}) */
    character(id,o){o=o||{};const size=o.size||90,c=(window.DATA.concepts||{})[id]||{name:o.name||id};
      const g=node("g",{class:"sdk-char",transform:`translate(${o.x||W/2} ${o.y||H/2})`,"data-id":id},layer);
      const body=node("g",{class:"sdk-body"},g);body.innerHTML=`<svg x="${-size/2}" y="${-size/2}" width="${size}" height="${size}" viewBox="0 0 100 100" overflow="visible">${art(id,size)}</svg>`;
      if(o.label!==false){const t=node("text",{y:size/2+18,"text-anchor":"middle",class:"sdk-name"},g);t.textContent=o.name||c.name;}
      const h={id,g,size,x:o.x||W/2,y:o.y||H/2,
        moveTo(x,y,ms){const fx=h.x,fy=h.y;x=clamp(x,size/2,W-size/2);y=clamp(y,size/2,H-size/2-18);return SDK.tween(ms||600,t=>{h.x=fx+(x-fx)*t;h.y=fy+(y-fy)*t;g.setAttribute("transform",`translate(${h.x} ${h.y})`);});},
        say(text){bubbleFor(h,text);return h;},
        dim(on){g.style.opacity=on?.3:1;return h;},glow(on){g.classList.toggle("sdk-glow",!!on);return h;},
        onTap(fn){g.style.cursor="pointer";g.addEventListener("click",e=>{try{fn(h,e);}catch(err){errors.push(String(err));}});return h;},
        draggable(opts){opts=opts||{};g.style.cursor="grab";g.style.touchAction="none";
          g.addEventListener("pointerdown",ev=>{ev.preventDefault();const R=stage.getBoundingClientRect(),k=W/R.width;g.setPointerCapture&&g.setPointerCapture(ev.pointerId);
            const mv=e=>{h.x=clamp((e.clientX-R.left)*k,size/2,W-size/2);h.y=clamp((e.clientY-R.top)*k,size/2,H-size/2-18);g.setAttribute("transform",`translate(${h.x} ${h.y})`);try{opts.onMove&&opts.onMove(h);}catch(err){errors.push(String(err));}};
            const up=()=>{window.removeEventListener("pointermove",mv);window.removeEventListener("pointerup",up);try{opts.onDrop&&opts.onDrop(h);}catch(err){errors.push(String(err));}};
            window.addEventListener("pointermove",mv);window.addEventListener("pointerup",up);});return h;},
        near(other,dist){return Math.hypot(h.x-other.x,h.y-other.y)<(dist||80);}};
      handles.push(h);return h;},
    /* the platform's «needs» arrow: from the one who needs → to what it needs, with the age's word on it */
    arrow(from,to,o){o=o||{};const g=node("g",{class:"sdk-arrow",opacity:o.hidden?0:1},layer);
      const draw=()=>{const dx=to.x-from.x,dy=to.y-from.y,d=Math.hypot(dx,dy)||1,r1=from.size/2+6,r2=to.size/2+10;
        const a=[from.x+dx/d*r1,from.y+dy/d*r1],b=[to.x-dx/d*r2,to.y-dy/d*r2],m=[(a[0]+b[0])/2,(a[1]+b[1])/2-18];
        g.innerHTML=`<path d="M${a[0]} ${a[1]} Q${m[0]} ${m[1]} ${b[0]} ${b[1]}" class="sdk-line" marker-end="url(#sdkhead)"/>`+(o.label===false?"":`<g transform="translate(${(a[0]+2*m[0]+b[0])/4} ${(a[1]+2*m[1]+b[1])/4})"><rect class="sdk-tag" x="-34" y="-11" width="68" height="20" rx="10"/><text y="4" text-anchor="middle" class="sdk-tagt">${o.label||window.DATA.needsWord}</text></g>`);};
      draw();return {g,redraw:draw,show(on){g.setAttribute("opacity",on?1:0);}};},
    text(x,y,str,o){o=o||{};const t=node("text",{x,y,"text-anchor":o.anchor||"middle",class:"sdk-text","font-size":o.size||16,"font-weight":o.weight||700,fill:o.color,direction:o.ltr?"ltr":null,"unicode-bidi":o.ltr?"embed":null},layer);t.textContent=String(str);return t;},
    shape(kind,attrs){if(!["circle","rect","line","path","ellipse","polygon","polyline"].includes(kind))throw new Error("shape: "+kind);return node(kind,Object.assign({class:"sdk-shape"},attrs||{}),layer);},
    slider(o,onChange){o=o||{};const lab=document.createElement("label");lab.className="sdk-sl";const sp=document.createElement("span");sp.textContent=o.label||"";
      const r=document.createElement("input");r.type="range";r.min=o.min??0;r.max=o.max??10;r.step=o.step??1;r.value=o.value??o.min??0;const b=document.createElement("b");b.textContent=r.value;
      lab.append(sp,r,b);ui.appendChild(lab);const fire=()=>{b.textContent=r.value;try{onChange&&onChange(parseFloat(r.value));}catch(err){errors.push(String(err));}};r.addEventListener("input",fire);setTimeout(fire,0);
      return {set(v){r.value=v;fire();},get value(){return parseFloat(r.value);}};},
    button(label,onClick){const bt=document.createElement("button");bt.className="sdk-btn";bt.textContent=label;bt.addEventListener("click",()=>{try{onClick&&onClick();}catch(err){errors.push(String(err));}});ui.appendChild(bt);return bt;},
    caption(t){capEl.textContent=String(t||"");parent.postMessage({type:"llm-caption",text:String(t||"")},"*");},
    tween(ms,fn){return new Promise(res=>{const t0=performance.now();const go=()=>{const t=Math.min(1,(performance.now()-t0)/(ms||1));try{fn(t<.5?2*t*t:1-Math.pow(-2*t+2,2)/2);}catch(err){errors.push(String(err));}if(t<1)requestAnimationFrame(go);else res();};go();});},
    wait(ms){return new Promise(r=>setTimeout(r,Math.min(ms||0,10000)));},
    done(note){doneNote=String(note||"تم");report();}};
  /* the report the page/teacher screen receives: did it draw, is everything inside the picture, any errors? */
  function report(){const R=stage.getBoundingClientRect(),k=W/(R.width||W);let outside=0;
    stage.querySelectorAll(".sdk-char,.sdk-text,.sdk-bub rect").forEach(e=>{const r=e.getBoundingClientRect();if(!r.width)return;const x0=(r.left-R.left)*k,x1=(r.right-R.left)*k,y0=(r.top-R.top)*k,y1=(r.bottom-R.top)*k;if(x0<-2||y0<-2||x1>W+2||y1>H+2)outside++;});
    const msg={type:"llm-scene",ok:!errors.length&&drawn>0,drawn,outside,errors:errors.slice(0,5),done:doneNote};window.__REPORT=msg;try{parent.postMessage(msg,"*");}catch(e){}}
  window.addEventListener("error",e=>{errors.push(String(e.message||e));});
  const size=()=>{try{parent.postMessage({type:"llm-size",h:document.documentElement.scrollHeight},"*");}catch(e){}};   /* the page sizes the iframe to fit */
  window.addEventListener("resize",size);setTimeout(size,50);setTimeout(size,600);
  window.__bootScene=function(){SDK.data=window.DATA;
    if(typeof window.buildScene!=="function"){errors.push("buildScene is missing");report();return;}
    try{const r=window.buildScene(SDK,window.DATA);if(r&&r.then)r.catch(err=>errors.push(String(err)));}catch(err){errors.push(String(err&&err.message||err));}
    setTimeout(report,1200);};
})();
```

---

## `scripts/export_art.py` 🆕 (الدفعة ٢٥)
**تصدير الرسومات من الصفحة ← `art/art.json` (ملف واحد).** بنشغّله **بعد ما نغيّر رسومات** بالمشغّل. بيفتح الصفحة المبنية بمتصفح (Playwright)، بياخد كل رسمة من مكتبة المشغّل (`window.__ART`) و**قالب كل شكل مادة** (`ARTS.subjectTemplate`: الرسمة بفراغات `{{FILL}}` `{{INK}}` `{{NB|x|y|لون}}`). **آخر مرة: ١١٩ رسمة + ٢٥ شكل.** (كان بيكتب ١٢٠ ملف؛ GitHub بياخد ١٠٠ ملف بالرفعة.)

```python
"""Export EVERY drawing of the page's library for the API, into ONE file: art/art.json
    {"files": {key: "<svg…>"}, "subject_templates": {emblem: "<the subject character with holes for colour + name>"},
     "lego": {"main": {part: "<svg with holes>"}, "extra": {badge: "…"}, "badge": ["<g …>" per spot], "motions": […]}}   (🧱 batch 29)
Run after changing drawings in the page (needs playwright + the built page):
    python scripts/export_art.py ../02_question_factory/player/explain.html
One file instead of 120 (GitHub's web upload takes 100 files at a time). core/art.py reads it."""
import json
import os
import sys

from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(HERE, "art", "art.json")
HEAD = '<svg xmlns="http://www.w3.org/2000/svg" width="240" height="240" viewBox="0 0 100 100">'

if __name__ == "__main__":
    page = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "02_question_factory", "player", "explain.html"))
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(); pg.goto("file://" + page); pg.wait_for_timeout(300)
        got = pg.evaluate("""()=>{const A=window.__ART;if(!A)return null;const files={};
            Object.keys(A.ART_OF).forEach(k=>{const s=A.artSVG(k,"");if(s)files[k]=s;});
            const tpl={};Object.keys(A.SUBJ_ART||{}).forEach(e=>{tpl[e]=A.ARTS.subjectTemplate(e);});
            const lego={main:{},extra:{},badge:[],motions:(A.LEGO_MOTIONS||[]).slice()};
            Object.keys(A.LEGO_MAIN||{}).forEach(k=>{lego.main[k]=A.legoMainTemplate(k);});
            Object.keys(A.LEGO_EXTRA||{}).forEach(k=>{lego.extra[k]=A.legoExtraTemplate(k);});
            (A.LEGO_SPOTS||[]).forEach((_,i)=>lego.badge.push(A.LEGO_BADGE(i)));return {files,tpl,lego};}""")
        b.close()
    if not got:
        sys.exit("the page has no window.__ART (build it first: build_explain_template.py + build_all_books.py)")
    files = {k: s.replace('<svg class="ch " viewBox="0 0 100 100" aria-hidden="true">', HEAD, 1) for k, s in got["files"].items()}
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump({"files": files, "subject_templates": got["tpl"], "lego": got["lego"]}, f, ensure_ascii=False)
    print(f"exported {len(files)} drawings + {len(got['tpl'])} subject characters + 🧱 {len(got['lego']['main'])} Lego parts "
          f"and {len(got['lego']['extra'])} badges → {OUT}")
```

---

## `tests/test_llm_scenes.py` 🆕 (الدفعة ٢٥)
**المسار كامل بموديل وهمي** (بلا مفاتيح): الفحوصات نفسها (الكود الخطير بينرفض، العربي جوا النصوص ما بينحسب كود، الطول، الأقواس) · البرومبت فيه القواعد والحقائق والعمر · الصندوق بلا إنترنت · **مشهد منيح ← بانتظار المعلم** · **نفس الطلب ثاني مرة ← ببلاش** · **جواب غلط ← جولة تصليح** · **غلط مرتين ← مرفوض وما بينفع ينقبل** · **المقبول بيطلع بالدرس مع `include_llm`** · الحدود (١–١٠، درس/كتاب مش موجود، بلا مفتاح ← 400) · وطلبات HTTP نفسها.

```python
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
```

---

## `tests/test_service.py`

**فحوصات الخدمة** (بمجلد داتا مؤقت، ما بتلمس الحقيقي): بيولّد العلوم (من ملف) والرياضيات (من JSON مباشرة) وبيتأكد: **كل الدروس انعملت**، القوائم صح، **كل درس فيه مشاهد وروابط رسومات**، **كل نوع مشهد موجود بالعقد** (عشان الفرونت ما يتفاجأ بنوع ما بيعرفه)، **كل رسمة بكل درس موجودة فعلاً**، احتياط المادة عليه الاسم، **الأخطاء** (٤٠٠/٤٠٤)، و**الموديل اختياري**: موديل تجريبي بيعيد كتابة الفقرات والنتيجة بتنحفظ.

```python
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
```

---

## `tests/test_api.py`

**فحوصات الـ API** بـ `TestClient` تبع FastAPI: الصحة، التوليد (٤ دروس)، الطلبات الغلط (٤٠٠ و٤٠٤)، **الرحلة كاملة**: كتب ← دروس ← درس ← مفهوم ← **رسمة SVG حقيقية**، و«غير موجود» (٤٠٤)، والعقد. **إذا FastAPI مش منصّب** بتتخطى (وفحوصات الخدمة بتضل تشتغل).

```python
"""The HTTP API (FastAPI). Runs with the real FastAPI: pip install -r requirements.txt"""
import json
import os
import shutil
import tempfile
import unittest

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAMPLES = os.path.join(os.path.dirname(HERE), "02_question_factory")          # the sample books live in the factory (no copies here)
os.environ.setdefault("EXPLAIN_SEED", "0")                                   # tests make their own books
TMP = tempfile.mkdtemp()
os.environ["EXPLAIN_DATA_DIR"] = TMP
import sys  # noqa: E402
sys.path.insert(0, HERE)
try:
    from fastapi.testclient import TestClient
    from main import app
    HAVE = True
except ImportError:                                       # FastAPI not installed → these tests are skipped (the service tests still run)
    HAVE = False


@unittest.skipUnless(HAVE, "pip install -r requirements.txt")
class TestAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.c = TestClient(app)
        with open(os.path.join(SAMPLES, "math_book_graph.json"), encoding="utf-8") as f:
            cls.g = json.load(f)
        cls.r = cls.c.post("/explanations/generate", json={"graph": cls.g})

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(TMP, ignore_errors=True)

    def test_health(self):
        r = self.c.get("/health"); self.assertEqual(r.status_code, 200); self.assertEqual(r.json()["status"], "ok")

    def test_generate(self):
        self.assertEqual(self.r.status_code, 200); body = self.r.json()
        self.assertEqual(len(body["lessons"]), 4); self.assertGreater(body["scenes"], 30)

    def test_generate_bad_requests(self):
        self.assertEqual(self.c.post("/explanations/generate", json={}).status_code, 400)
        self.assertEqual(self.c.post("/explanations/generate", json={"graph_path": "nope.json"}).status_code, 404)

    def test_books_lessons_lesson_concept_picture(self):
        book = self.r.json()["book_id"]
        self.assertIn(book, [b["book_id"] for b in self.c.get("/books").json()])
        lessons = self.c.get(f"/books/{book}/lessons").json(); self.assertEqual(len(lessons), 4)
        lid = lessons[0]["lesson_id"]
        l = self.c.get(f"/lessons/{lid}/explanation", params={"book_id": book}).json()
        self.assertEqual(l["lesson_id"], lid); self.assertTrue(l["concepts"])
        cid = l["concepts"][0]["concept_id"]
        c = self.c.get(f"/concepts/{cid}/explanation").json(); self.assertEqual(c["concept_id"], cid)
        pic = self.c.get(l["art"][cid]); self.assertEqual(pic.status_code, 200)
        self.assertIn("svg", pic.headers.get("content-type", "")); self.assertTrue(pic.text.startswith("<svg"))

    def test_not_found(self):
        self.assertEqual(self.c.get("/lessons/nope/explanation").status_code, 404)
        self.assertEqual(self.c.get("/books/nope/lessons").status_code, 404)
        self.assertEqual(self.c.get("/art/nope.svg").status_code, 404)

    def test_home_page(self):
        r = self.c.get("/"); self.assertEqual(r.status_code, 200)
        self.assertIn("text/html", r.headers.get("content-type", "")); self.assertIn("سيرفر الشرح التفاعلي", r.text)

    def test_the_interactive_page_from_the_server(self):
        book = self.r.json()["book_id"]
        r = self.c.get(f"/explain/{book}"); self.assertEqual(r.status_code, 200)
        self.assertIn("text/html", r.headers.get("content-type", "")); self.assertIn("const DATA = ", r.text)
        self.assertEqual(self.c.get("/explain").status_code, 200)
        self.assertEqual(self.c.get("/explain/nope").status_code, 404)
        d = self.c.get("/explain-data", params={"books": book}).json(); self.assertEqual(len(d["graphs"]), 1)
        self.assertEqual(self.r.json()["page_url"], f"/explain/{book}")

    def test_a_new_subject_through_the_api(self):
        with open(os.path.join(SAMPLES, "examples", "new_subject_computer_g7.json"), encoding="utf-8") as f:
            r = self.c.post("/explanations/generate", json={"graph": json.load(f)}).json()
        self.assertEqual(r["identity"]["family"], "computer"); self.assertEqual(r["identity"]["sound"]["instr"], "chip")
        self.assertIn('"instr": "chip"', self.c.get(r["page_url"]).text)
        b = [x for x in self.c.get("/books").json() if x["book_id"] == r["book_id"]][0]
        self.assertTrue(b["identity"]["new"])
        self.assertEqual(self.c.delete(f"/books/{r['book_id']}").status_code, 200)
        self.assertEqual(self.c.get(r["page_url"]).status_code, 404)

    def test_picture_per_age_stage(self):
        r = self.c.get("/art/%F0%9F%90%9D.svg", params={"stage": "senior"}); self.assertEqual(r.status_code, 200)
        self.assertIn(".sface{display:none!important}", r.text)

    def test_contract(self):
        k = self.c.get("/scene-kinds").json(); self.assertIn("meet", k["scene_kinds"]); self.assertIn("relation", k)


if __name__ == "__main__":
    unittest.main()
```

---

## `02_question_factory/lego.py` 🆕 (الدفعة ٢٩)
**🧱 مين بيقرر وصفة رسمة الليغو.** القطع ومعانيها وكلماتها · المفتاح · الوصفة من كلمات الاسم (بلا AI) · المكتبة اللي بتكبر · الموديل بيختار (استدعاء واحد للكتاب، فحص، حفظ) · المعلم بيختار أو بيرفض.
```python
"""🧱 LEGO DRAWINGS (batch 29 · 💡 Hareth's idea «ليغو الرسومات + الاستعارة»).

A concept that has NO drawing in our library gets one BUILT from ready parts (drawn in our style in the page, lego.js):
    ONE main part = the metaphor (memory → drawers, processor → chip, error → bug…) + a face + up to 2 small badges.
The picture key carries the whole recipe:   lego:<main>:<extra>+<extra>:<colour 0-7>:<motion>
    e.g.  lego:drawers:binary:3:wobble

Where a recipe comes from (in this order):
    1) the LIBRARY of built drawings (saved): the model chose it once, or a teacher picked it → reused by every book, no cost;
    2) the concept's own WORDS (no AI): «الذاكرة» → drawers, «وحدة المعالجة» → chip, «الخطأ البرمجي» → bug …;
    3) nothing → None (the page then shows the subject's character with the name on it, as before).
The MODEL (optional, use_llm): ONE call for all the new concepts of a book. It only CHOOSES from the lists below
(it never draws); every answer is checked; the first good option is used at once, the others are kept for the teacher.
Plain Python (standard library only)."""
import json
import os
import re

# ---------- the parts (the SAME names as LEGO_MAIN / LEGO_EXTRA in 03_explain_player_src/lego.js — a test checks) ----------
# name: (what it can mean — told to the model, its usual motion, the words that pick it without AI)
MAINS = {
    "drawers":   ("رف أدراج: تخزين، حفظ، ذاكرة، أرشيف", "wobble", ("ذاكرة", "تخزين", "أرشيف", "memory", "storage", "archive")),
    "chip":      ("شريحة إلكترونية: معالج، عقل الجهاز، تحكم", "buzz", ("معالجة", "معالج", "شريحة", "processor", "cpu", "chip")),
    "screen":    ("شاشة: حاسوب، عرض، إخراج، تطبيق ظاهر", "bob", ("حاسوب", "حاسب", "شاشة", "إخراج", "عرض", "computer", "screen", "output", "display")),
    "keyboard":  ("لوحة مفاتيح: إدخال، كتابة، طباعة", "bounce", ("إدخال", "لوحة المفاتيح", "كتابة", "input", "keyboard", "typing")),
    "page":      ("ورقة مكتوبة: ملف، مستند، نص، برنامج مكتوب، تعليمات", "wiggle", ("ملف", "ملفات", "مستند", "برنامج", "برامج", "تعليمات", "file", "document", "program")),
    "code":      ("بطاقة كود </>: برمجة، لغة برمجة، شيفرة", "wobble", ("برمجة", "البرمجة", "كود", "شيفرة", "code", "coding", "programming")),
    "bug":       ("خنفسة: خطأ، علة، مشكلة بالبرنامج، حشرة", "wiggle", ("خطأ", "أخطاء", "علة", "حشرة", "حشرات", "bug", "error", "insect")),
    "stairs":    ("درج بخطوات ١-٢-٣: خطوات، مراحل، خوارزمية، تقدّم، ترتيب", "bounce", ("خوارزمية", "خوارزميات", "خطوات", "مراحل", "algorithm", "steps", "stages")),
    "gear":      ("ترس: آلة، نظام، عملية، تقنية، محرك", "sun", ("آلة", "آلات", "نظام", "أنظمة", "عملية", "تقنية", "ترس", "machine", "system", "process")),
    "lock":      ("قفل: أمان، حماية، خصوصية، سرية", "wobble", ("أمان", "حماية", "خصوصية", "قفل", "security", "privacy", "protection")),
    "key":       ("مفتاح: حل، وصول، كلمة سر، فتح", "sway", ("مفتاح", "كلمة السر", "كلمة المرور", "password", "key", "access")),
    "bulb":      ("مصباح: فكرة، إبداع، اختراع، فهم", "bob", ("فكرة", "أفكار", "إبداع", "اختراع", "idea", "invention", "creativity")),
    "magnifier": ("عدسة مكبّرة: بحث، فحص، استكشاف، تحقق، ملاحظة", "sway", ("بحث", "فحص", "استكشاف", "تحقق", "ملاحظة", "search", "research", "inspection")),
    "envelope":  ("ظرف: رسالة، تواصل، بريد، اتصال", "bounce", ("رسالة", "رسائل", "بريد", "تواصل", "message", "email", "communication")),
    "globe":     ("كرة أرضية: عالم، إنترنت، شبكة، دولي، عولمة", "sun", ("إنترنت", "الانترنت", "شبكة", "شبكات", "عالمي", "دولي", "internet", "network", "global")),
    "flag":      ("علم: وطن، دولة، هدف، إنجاز، بداية", "sway", ("وطن", "دولة", "هدف", "أهداف", "flag", "goal", "nation")),
    "shield":    ("درع: قانون، حقوق، دفاع، مناعة، أمن", "bob", ("قانون", "قوانين", "حقوق", "دفاع", "مناعة", "law", "rights", "defense", "immunity")),
    "cube":      ("مكعب/صندوق: منتج، شيء، مجسم، حجم، كتلة", "wobble", ("منتج", "منتجات", "مكعب", "مجسم", "صندوق", "product", "cube", "box")),
    "chart":     ("رسم بياني: إحصاء، أرقام، نمو، تحليل، اقتصاد", "bounce", ("إحصاء", "إحصائيات", "نمو", "تحليل", "رسم بياني", "statistics", "chart", "growth")),
    "pot":       ("طنجرة: طبخ، طهي، خلط، وصفة، تحضير", "wobble", ("طبخ", "طهي", "وصفة", "مطبخ", "خلط", "cooking", "recipe", "kitchen")),
    "puzzle":    ("قطعة بزل: جزء، مكوّن، تركيب، حل مشكلة", "wiggle", ("جزء", "أجزاء", "مكون", "مكونات", "تركيب", "puzzle", "component", "part")),
    "people":    ("شخصين: مجتمع، فريق، تعاون، عائلة، ناس", "sway", ("مجتمع", "فريق", "تعاون", "عائلة", "أسرة", "سكان", "society", "team", "family", "people")),
    "trophy":    ("كأس: فوز، مسابقة، بطولة، جائزة، إنجاز", "bounce", ("فوز", "مسابقة", "بطولة", "جائزة", "إنجاز", "trophy", "competition", "award")),
    "note":      ("نوتة موسيقية: لحن، نغمة، إيقاع، غناء", "sway", ("لحن", "ألحان", "نغمة", "إيقاع", "غناء", "melody", "rhythm", "song")),
    "ball":      ("كرة: رياضة، لعبة، تمرين", "bounce", ("كرة", "لعبة", "ألعاب", "تمرين", "ball", "game", "exercise")),
    "bag":       ("حقيبة: تجارة، سوق، شراء، بيع، سفر", "wobble", ("سوق", "أسواق", "تجارة", "شراء", "بيع", "حقيبة", "market", "trade", "shopping")),
    "hourglass": ("ساعة رملية: مدة، عصر، حقبة، انتظار", "wobble", ("مدة", "عصر", "حقبة", "انتظار", "duration", "era", "period")),
}
EXTRAS = {"plus": "زيادة/إضافة", "check": "صح/تم", "question": "سؤال/مجهول", "spark": "جديد/لامع", "arrow": "انتقال/ناتج/خروج",
          "heart": "حب/صحة", "star": "مميز/مهم", "link": "ربط/اتصال", "binary": "رقمي/بيانات", "drop": "ماء/سائل",
          "cog": "إعداد/آلة صغيرة", "tune": "صوت/موسيقى"}
MOTIONS = ("bob", "wobble", "bounce", "sway", "sun", "buzz", "wiggle", "drip")   # the moves the page already has
COLORS = 8                                                                      # SUBJ_COLORS in the page
# a word that also adds a badge (no AI): «وحدات الإخراج» → the screen + an arrow going out
WORD_EXTRAS = (("إخراج", "arrow"), ("output", "arrow"), ("إدخال", "arrow"), ("بيانات", "binary"), ("data", "binary"),
               ("رقمي", "binary"), ("digital", "binary"), ("خطأ", "question"), ("جديد", "spark"))


# ---------- keys ----------
def color_of(name: str) -> int:
    """The concept's own colour: the same formula as the page (sum of the UTF-16 codes % 8)."""
    b = str(name or "").encode("utf-16-le")
    return sum(int.from_bytes(b[i:i + 2], "little") for i in range(0, len(b), 2)) % COLORS


def make_key(main: str, extras=(), color: int = 0, motion: str = None) -> str:
    extras = [x for x in (extras or []) if x in EXTRAS][:2]
    motion = motion if motion in MOTIONS else MAINS[main][1]
    return f"lego:{main}:{'+'.join(extras)}:{int(color) % COLORS}:{motion}"


def parse(key: str):
    """«lego:drawers:binary:3:wobble» → {"main", "extras", "color", "motion"} (the same rules as legoParts in the page), or None."""
    if not isinstance(key, str) or not key.startswith("lego:"):
        return None
    p = key.split(":") + ["", "", "", ""]
    if p[1] not in MAINS:
        return None
    m = re.match(r"-?\d+", p[3] or "")
    return {"main": p[1], "extras": [x for x in p[2].split("+") if x in EXTRAS][:2],
            "color": abs(int(m.group())) % COLORS if m else 0, "motion": p[4] if p[4] in MOTIONS else "bob"}


# ---------- 2) by the concept's own words (no AI) ----------
_PREFIXES = ("وال", "بال", "فال", "كال", "لل", "ال", "و", "ب", "ف", "ل")


def _norm(s: str) -> str:
    return re.sub("[أإآ]", "ا", str(s or "").lower())


def _tokens(text: str) -> list:
    out = []
    for w in re.findall(r"[\w؀-ۿ]+", _norm(text)):
        out.append(w)
        for p in _PREFIXES:
            if w.startswith(p) and len(w) - len(p) >= 3:
                out.append(w[len(p):])
                break
    return out


def _has(toks: list, word: str) -> bool:
    """A WHOLE word (a few endings allowed: «ملف» → «ملفات»); a phrase: its words one after the other."""
    word = _norm(word)
    word = word[2:] if word.startswith("ال") and len(word) > 4 else word
    if " " in word:
        return word in " ".join(toks)
    return any(t == word or t in (word + "ة", word + "ات", word + "ين") for t in toks)


def by_words(name: str):
    """A recipe from the concept's NAME only (never from its meaning: that would mix things up). None if no word fits."""
    toks = _tokens(name)
    for main, (_, motion, words) in MAINS.items():
        if any(_has(toks, w) for w in words):
            extras = [x for w, x in WORD_EXTRAS if _has(toks, w)][:1]
            return make_key(main, extras, color_of(name), motion)
    return None


# ---------- 1) the library of built drawings (it grows: one entry per concept, reused by every book) ----------
_STORE = os.environ.get("EXPLAIN_LEGO_FILE") or os.path.join(os.path.dirname(os.path.abspath(__file__)), "lego_library.json")
_CACHE = {"mtime": None, "data": {}}


def set_store(path: str) -> None:
    global _STORE
    _STORE = path
    _CACHE["mtime"] = None


def store_path() -> str:
    return _STORE


def _key_of(name: str) -> str:
    return " ".join(_norm(name).split())


def library() -> dict:
    try:
        m = os.path.getmtime(_STORE)
    except OSError:
        return {}
    if _CACHE["mtime"] != m:
        try:
            with open(_STORE, encoding="utf-8") as f:
                _CACHE["data"] = json.load(f)
        except (OSError, ValueError):
            _CACHE["data"] = {}
        _CACHE["mtime"] = m
    return _CACHE["data"]


def _save(data: dict) -> None:
    os.makedirs(os.path.dirname(_STORE) or ".", exist_ok=True)
    with open(_STORE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    _CACHE["mtime"] = None


def saved(name: str):
    e = library().get(_key_of(name))
    return e["key"] if e and e.get("status") != "rejected" and parse(e.get("key")) else None


def for_concept(name: str, subject: str = ""):
    """The Lego drawing of a concept: the saved one (model / teacher) → by its words → None."""
    return saved(name) or by_words(name)


# ---------- 🤖 the model chooses (once per concept; optional) ----------
PROMPT = """You choose PICTURES for school concepts on an Arabic learning page. You never draw: you BUILD each picture from ready parts.
Subject: «{subject}»
For EACH concept below, think of the best everyday METAPHOR a student understands (memory → a cabinet of drawers,
processor → a chip, a bug in a program → a beetle), then give up to 3 options, best first. Use ONLY these names:
- main (exactly one, the metaphor):
{mains}
- extras (0, 1 or 2 small badges):
{extras}
- motion (one): {motions}
Concepts (name — meaning):
{concepts}
Answer with ONE JSON object and nothing else:
{{"items": [{{"name": "<the concept name exactly>", "metaphor": "<a few Arabic words>", "options": [{{"main": "…", "extras": ["…"], "motion": "…"}}]}}]}}"""


def needs_picture(names: list) -> list:
    """The concepts that have NO saved Lego drawing yet (only those cost a model call)."""
    return [n for n in dict.fromkeys(names) if n and saved(n) is None]


def ask_model(names: list, llm, subject: str = "", meanings: dict = None, limit: int = 30) -> dict:
    """ONE model call for up to `limit` new concepts → checked → saved in the library (the first good option is used at once,
    status «auto»; all good options stay as suggestions for the teacher). Returns {name: key} of what was saved.
    No key / bad answer → {} (nothing changes: the words or the subject character stay)."""
    todo = needs_picture(names)[:limit]
    if not todo:
        return {}
    meanings = meanings or {}
    user = PROMPT.format(subject=str(subject or "").strip(),
                         mains="\n".join(f"  {k}: {v[0]}" for k, v in MAINS.items()),
                         extras="\n".join(f"  {k}: {v}" for k, v in EXTRAS.items()),
                         motions=", ".join(MOTIONS),
                         concepts="\n".join(f"  {n} — {str(meanings.get(n, ''))[:120]}" for n in todo))
    try:
        text = llm("You answer with one JSON object only.", user)
        m = re.search(r"\{.*\}", text or "", re.S)
        items = json.loads(m.group(0)).get("items", []) if m else []
    except Exception:                                    # no key, network, bad JSON… → nothing changes, the book still works
        return {}
    want = {_key_of(n): n for n in todo}
    data, out = dict(library()), {}
    for it in items if isinstance(items, list) else []:
        if not isinstance(it, dict):
            continue
        name = want.get(_key_of(it.get("name", "")))
        if not name:
            continue                                     # a name we did not ask for: ignored
        keys = []
        for o in (it.get("options") or [])[:3]:
            if isinstance(o, dict) and o.get("main") in MAINS:
                k = make_key(o["main"], [x for x in (o.get("extras") or []) if isinstance(x, str)], color_of(name), o.get("motion"))
                if k not in keys:
                    keys.append(k)
        if keys:
            data[_key_of(name)] = {"name": name, "key": keys[0], "suggestions": keys, "metaphor": str(it.get("metaphor") or "")[:60],
                                   "source": "model", "status": "auto", "subject": str(subject or "")}
            out[name] = keys[0]
    if out:
        _save(data)
    return out


def choose(name: str, pick: int = None, reject: bool = False) -> dict:
    """The teacher's decision: pick suggestion number `pick` (0, 1, 2) → «approved», or reject → the subject character again.
    Returns {"name", "old", "new"} (old/new keys, so the books that use it can be updated)."""
    data = dict(library())
    k = _key_of(name)
    e = data.get(k)
    if not e:
        raise KeyError(name)
    old = saved(name) or by_words(name)
    if reject:
        e["status"] = "rejected"
    else:
        sugg = e.get("suggestions") or [e["key"]]
        if pick is None or not (0 <= int(pick) < len(sugg)):
            raise ValueError(f"pick لازم بين 0 و {len(sugg) - 1}")
        e["key"], e["status"] = sugg[int(pick)], "approved"
    data[k] = e
    _save(data)
    return {"name": e.get("name", name), "old": old, "new": saved(name) or by_words(name)}
```

## `03_explain_player_src/lego.js` 🆕 (الدفعة ٢٩)
**🧱 القطع نفسها والتركيب بالصفحة.** ٢٧ قطعة أساسية (كل وحدة: رسمتها بلون المفهوم + مكان الوجه) · ١٢ شارة · مكانين للشارات · ٨ حركات · `legoParts` بيقرا المفتاح · `legoSVG` بيركّب. والقوالب بفراغات `{{FILL}}` `{{INK}}` بتنصدّر للسيرفر.
```js
/* ===== 🧱 LEGO DRAWINGS (batch 29 · 💡 Hareth's idea «ليغو الرسومات + الاستعارة») =====
   A concept with NO drawing of its own gets one BUILT from ready parts drawn in our style:
     ONE main part (the metaphor: memory = drawers, processor = chip, error = bug…) + its face + up to 2 small badges.
   The picture key carries the whole recipe, so it needs nothing else:
     «lego:<main>:<extra>+<extra>:<colour 0-7>:<motion>»      e.g.  lego:drawers:gear+spark:3:wobble
   WHO decides the recipe: the factory (02_question_factory/lego.py) — by the concept's words (no AI), or the MODEL once
   (it only CHOOSES parts from these lists; it never draws). WHO draws: this code + the browser.
   The API draws the SAME pictures: every part is exported with holes ({{FILL}} {{INK}}) to art/art.json, and
   core/art.py puts them together exactly like legoSVG below (a browser test checks both give the same SVG). */
const LEGO_MAIN={   /* C = the concept's colours {f fill, k ink} · every main part: (C) → svg, + where its face goes [x, y, size] */
 drawers:{d:C=>`<rect x="14" y="8" width="72" height="86" rx="8" fill="${C.f}" ${OL}/>${[16,42,68].map(y=>`<rect x="22" y="${y}" width="56" height="20" rx="4" fill="#fff" opacity=".9" ${OL}/><circle cx="50" cy="${y+15}" r="2.6" fill="${C.k}"/>`).join("")}`,face:[50,25,.34]},
 chip:{d:C=>`${[30,42,54,66].map(v=>`<path d="M${v} 10 V22 M${v} 78 V90 M10 ${v} H22 M78 ${v} H90" stroke="#3b2a1a" stroke-width="3" stroke-linecap="round"/>`).join("")}<rect x="20" y="20" width="60" height="60" rx="8" fill="${C.f}" ${OL}/><rect x="31" y="31" width="38" height="38" rx="5" fill="#fff" opacity=".55"/>`,face:[50,51,.52]},
 screen:{d:C=>`<rect x="10" y="8" width="80" height="58" rx="8" fill="${C.f}" ${OL}/><rect x="16" y="14" width="68" height="46" rx="4" fill="#EAF6FB" ${OL}/><path d="M42 66 H58 L62 80 H38Z" fill="#C8CDD2" ${OL}/><rect x="26" y="80" width="48" height="9" rx="4" fill="#9AA6B2" ${OL}/>`,face:[50,38,.55]},
 keyboard:{d:C=>`<rect x="6" y="28" width="88" height="52" rx="9" fill="${C.f}" ${OL}/>${[14,28,42,56,70].map(x=>`<rect x="${x}" y="58" width="11" height="9" rx="2" fill="#fff" ${OL}/>`).join("")}<rect x="30" y="70" width="40" height="6" rx="2" fill="#fff" opacity=".9"/>`,face:[50,43,.42]},
 page:{d:C=>`<path d="M20 6 H62 L82 26 V94 H20Z" fill="#fff" ${OL}/><path d="M62 6 V26 H82Z" fill="${C.f}" ${OL}/>${[64,72,80].map(y=>`<path d="M30 ${y} H72" stroke="${C.k}" stroke-width="3" stroke-linecap="round"/>`).join("")}`,face:[50,40,.5]},
 code:{d:C=>`<rect x="8" y="16" width="84" height="68" rx="12" fill="${C.f}" ${OL}/><text x="50" y="76" text-anchor="middle" font-size="20" font-weight="900" fill="#fff" direction="ltr" font-family="monospace">&lt;/&gt;</text>`,face:[50,40,.46]},
 bug:{d:C=>`<path d="M28 44 L10 36 M26 60 L8 60 M28 76 L12 86 M72 44 L90 36 M74 60 L92 60 M72 76 L88 86 M44 16 L36 4 M56 16 L64 4" stroke="#3b2a1a" stroke-width="3" stroke-linecap="round"/><circle cx="50" cy="24" r="12" fill="#3b2a1a"/><ellipse cx="50" cy="60" rx="26" ry="32" fill="${C.f}" ${OL}/><path d="M50 30 V92" stroke="${C.k}" stroke-width="2.4"/>`,face:[50,58,.5]},
 stairs:{d:C=>`<path d="M8 92 V72 H30 V52 H52 V32 H74 V12 H92 V92Z" fill="${C.f}" ${OL}/><text x="19" y="86" text-anchor="middle" font-size="12" font-weight="900" fill="#fff" direction="ltr">1</text><text x="41" y="66" text-anchor="middle" font-size="12" font-weight="900" fill="#fff" direction="ltr">2</text><text x="63" y="46" text-anchor="middle" font-size="12" font-weight="900" fill="#fff" direction="ltr">3</text>`,face:[78,72,.42]},
 gear:{d:C=>`${[0,45,90,135,180,225,270,315].map(a=>`<rect x="43" y="6" width="14" height="18" rx="3" fill="${C.f}" ${OL} transform="rotate(${a} 50 50)"/>`).join("")}<circle cx="50" cy="50" r="33" fill="${C.f}" ${OL}/>`,face:[50,52,.58]},
 lock:{d:C=>`<path d="M32 46 V30 C32 10 68 10 68 30 V46" fill="none" stroke="#9AA6B2" stroke-width="8"/><rect x="16" y="42" width="68" height="52" rx="10" fill="${C.f}" ${OL}/><circle cx="50" cy="80" r="4" fill="${C.k}"/>`,face:[50,62,.48]},
 key:{d:C=>`<rect x="48" y="44" width="46" height="12" rx="3" fill="${C.f}" ${OL}/><rect x="78" y="54" width="6" height="12" fill="${C.f}" ${OL}/><rect x="88" y="54" width="6" height="16" fill="${C.f}" ${OL}/><circle cx="30" cy="50" r="24" fill="${C.f}" ${OL}/>`,face:[30,50,.48]},
 bulb:{d:C=>`<path d="M12 18 L4 12 M88 18 L96 12 M50 4 V0" stroke="#F2C230" stroke-width="3" stroke-linecap="round"/><circle cx="50" cy="40" r="30" fill="${C.f}" ${OL}/><rect x="37" y="68" width="26" height="9" rx="3" fill="#C8CDD2" ${OL}/><rect x="39" y="77" width="22" height="9" rx="3" fill="#9AA6B2" ${OL}/>`,face:[50,40,.58]},
 magnifier:{d:C=>`<path d="M64 64 L90 90" stroke="#7A4D2B" stroke-width="11" stroke-linecap="round"/><circle cx="42" cy="42" r="32" fill="#EAF6FB" ${OL}/><circle cx="42" cy="42" r="28" fill="none" stroke="${C.f}" stroke-width="7"/>`,face:[42,44,.52]},
 envelope:{d:C=>`<rect x="8" y="20" width="84" height="62" rx="8" fill="${C.f}" ${OL}/><path d="M10 24 L50 54 L90 24" fill="none" stroke="#fff" stroke-width="3.4" stroke-linejoin="round"/>`,face:[50,68,.42]},
 globe:{d:C=>`<circle cx="50" cy="50" r="42" fill="#62A8EE" ${OL}/><path d="M22 34 Q32 22 44 30 Q46 42 34 46 Q24 46 22 34Z M58 22 Q74 20 78 34 Q70 42 60 36Z M54 66 Q68 62 74 72 Q66 84 56 80Z" fill="${C.f}" ${OL}/><ellipse cx="50" cy="50" rx="18" ry="42" fill="none" stroke="#fff" stroke-width="2" opacity=".6"/>`,face:[44,58,.46]},
 flag:{d:C=>`<rect x="16" y="6" width="7" height="88" rx="3" fill="#9AA6B2" ${OL}/><path d="M23 10 H86 L74 30 L86 50 H23Z" fill="${C.f}" ${OL}/>`,face:[50,30,.46]},
 shield:{d:C=>`<path d="M50 6 L88 18 C88 58 72 82 50 94 C28 82 12 58 12 18Z" fill="${C.f}" ${OL}/><path d="M40 70 L48 78 L62 62" fill="none" stroke="#fff" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>`,face:[50,44,.54]},
 cube:{d:C=>`<path d="M12 28 L50 46 V94 L12 76Z" fill="${C.f}" ${OL}/><path d="M88 28 L50 46 V94 L88 76Z" fill="${C.f}" ${OL}/><path d="M88 28 L50 46 V94 L88 76Z" fill="#000" opacity=".12"/><path d="M50 10 L88 28 L50 46 L12 28Z" fill="${C.f}" ${OL}/><path d="M50 10 L88 28 L50 46 L12 28Z" fill="#fff" opacity=".45"/>`,face:[31,62,.36]},
 chart:{d:C=>`<rect x="6" y="8" width="88" height="84" rx="10" fill="#fff" ${OL}/><rect x="50" y="56" width="10" height="28" fill="${C.f}" ${OL}/><rect x="64" y="40" width="10" height="44" fill="${C.f}" ${OL}/><rect x="78" y="22" width="10" height="62" fill="${C.f}" ${OL}/><path d="M12 84 H90" stroke="#3b2a1a" stroke-width="2.6"/>`,face:[27,44,.4]},
 pot:{d:C=>`<path d="M36 22 Q32 14 38 8 M50 22 Q46 14 52 6 M64 22 Q60 14 66 8" fill="none" stroke="#9AA6B2" stroke-width="3" stroke-linecap="round"/><path d="M4 50 H14 M86 50 H96" stroke="#3b2a1a" stroke-width="6" stroke-linecap="round"/><path d="M14 40 H86 V72 C86 86 74 92 50 92 C26 92 14 86 14 72Z" fill="${C.f}" ${OL}/><rect x="8" y="32" width="84" height="10" rx="5" fill="#9AA6B2" ${OL}/>`,face:[50,66,.5]},
 puzzle:{d:C=>`<path d="M18 30 H40 C40 16 60 16 60 30 H82 V50 C96 50 96 72 82 72 V92 H18Z" fill="${C.f}" ${OL}/>`,face:[48,62,.52]},
 people:{d:C=>`<path d="M48 92 V68 C48 54 86 54 86 68 V92Z" fill="${C.k}" ${OL}/><circle cx="67" cy="38" r="12" fill="#F6C9A0" ${OL}/><circle cx="63" cy="37" r="1.8" fill="#2a1d12"/><circle cx="71" cy="37" r="1.8" fill="#2a1d12"/><path d="M12 92 V64 C12 48 56 48 56 64 V92Z" fill="${C.f}" ${OL}/><circle cx="34" cy="30" r="14" fill="#F6C9A0" ${OL}/>`,face:[34,31,.34]},
 trophy:{d:C=>`<path d="M28 18 C10 18 12 42 30 42 M72 18 C90 18 88 42 70 42" fill="none" stroke="${C.k}" stroke-width="5"/><path d="M28 8 H72 V30 C72 50 62 60 50 60 C38 60 28 50 28 30Z" fill="${C.f}" ${OL}/><rect x="44" y="60" width="12" height="16" fill="${C.f}" ${OL}/><rect x="28" y="76" width="44" height="14" rx="3" fill="${C.k}" ${OL}/>`,face:[50,32,.48]},
 note:{d:C=>`<path d="M40 74 V20 M84 64 V10" stroke="#3b2a1a" stroke-width="4"/><path d="M40 18 L84 8 V22 L40 32Z" fill="${C.k}" ${OL}/><ellipse cx="72" cy="66" rx="14" ry="10" fill="${C.f}" ${OL}/><ellipse cx="28" cy="76" rx="16" ry="12" fill="${C.f}" ${OL}/>`,face:[28,76,.34]},
 ball:{d:C=>`<circle cx="50" cy="52" r="40" fill="${C.f}" ${OL}/><path d="M14 40 C34 50 66 50 86 40 M50 12 C40 32 40 72 50 92" fill="none" stroke="#fff" stroke-width="3" opacity=".8"/>`,face:[50,58,.5]},
 bag:{d:C=>`<path d="M36 34 V24 C36 10 64 10 64 24 V34" fill="none" stroke="#7A4D2B" stroke-width="5"/><rect x="14" y="32" width="72" height="60" rx="10" fill="${C.f}" ${OL}/><rect x="14" y="44" width="72" height="8" fill="#fff" opacity=".45"/>`,face:[50,70,.5]},
 hourglass:{d:C=>`<path d="M26 14 H74 C74 36 56 44 56 50 C56 56 74 64 74 86 H26 C26 64 44 56 44 50 C44 44 26 36 26 14Z" fill="#EAF6FB" ${OL}/><path d="M32 22 H68 C66 34 54 40 50 46 C46 40 34 34 32 22Z" fill="${C.f}"/><path d="M30 84 C32 72 44 66 50 64 C56 66 68 72 70 84Z" fill="${C.f}"/><rect x="16" y="6" width="68" height="9" rx="4" fill="#9AA6B2" ${OL}/><rect x="16" y="85" width="68" height="9" rx="4" fill="#9AA6B2" ${OL}/>`,face:[50,76,.3]}};
const LEGO_EXTRA={  /* small badges (drawn around 0,0 inside a white circle r=13) */
 plus:C=>`<path d="M-6 0 H6 M0 -6 V6" stroke="${C.k}" stroke-width="4" stroke-linecap="round"/>`,
 check:C=>`<path d="M-6 0 L-2 5 L7 -5" fill="none" stroke="#2E9E5B" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>`,
 question:C=>`<text y="6" text-anchor="middle" font-size="17" font-weight="900" fill="${C.k}" direction="ltr">?</text>`,
 spark:C=>`<path d="M0 -9 L2.5 -2.5 L9 0 L2.5 2.5 L0 9 L-2.5 2.5 L-9 0 L-2.5 -2.5Z" fill="#F2C230" stroke="#3b2a1a" stroke-width="1.4"/>`,
 arrow:C=>`<path d="M-7 0 H5 M0 -5 L6 0 L0 5" fill="none" stroke="${C.k}" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"/>`,
 heart:C=>`<path d="M0 8 C-12 0 -8 -10 0 -4 C8 -10 12 0 0 8Z" fill="#E8574A" stroke="#3b2a1a" stroke-width="1.4"/>`,
 star:C=>`<path d="M0 -9 L2.6 -3 L9 -2.8 L4 1.4 L5.6 8 L0 4.4 L-5.6 8 L-4 1.4 L-9 -2.8 L-2.6 -3Z" fill="#F2C230" stroke="#3b2a1a" stroke-width="1.4"/>`,
 link:C=>`<rect x="-9" y="-4" width="11" height="8" rx="4" fill="none" stroke="${C.k}" stroke-width="2.6"/><rect x="-2" y="-4" width="11" height="8" rx="4" fill="none" stroke="${C.k}" stroke-width="2.6"/>`,
 binary:C=>`<text y="4" text-anchor="middle" font-size="10" font-weight="900" fill="${C.k}" direction="ltr" font-family="monospace">01</text>`,
 drop:C=>`<path d="M0 -9 C4 -3 7 0 7 3 C7 7 4 9 0 9 C-4 9 -7 7 -7 3 C-7 0 -4 -3 0 -9Z" fill="#62A8EE" stroke="#3b2a1a" stroke-width="1.4"/>`,
 cog:C=>`<circle r="5" fill="#9AA6B2" stroke="#3b2a1a" stroke-width="1.4"/><path d="M0 -9 V-5 M0 5 V9 M-9 0 H-5 M5 0 H9" stroke="#3b2a1a" stroke-width="2.4" stroke-linecap="round"/>`,
 tune:C=>`<path d="M-2 5 V-7 L6 -9 V3" fill="none" stroke="${C.k}" stroke-width="2.4"/><circle cx="-4" cy="5" r="3" fill="${C.k}"/><circle cx="4" cy="3" r="3" fill="${C.k}"/>`};
const LEGO_SPOTS=[[16,14],[84,86]];                                   /* where the badges sit: top-left + bottom-right (away from the faces, and from the scene number at the top-right) */
const LEGO_MOTIONS=["bob","wobble","bounce","sway","sun","buzz","wiggle","drip"];   /* the moves the page already has (alive.css) */
const LEGO_BADGE=i=>`<g transform="translate(${LEGO_SPOTS[i][0]} ${LEGO_SPOTS[i][1]})"><circle r="13" fill="#fff" ${OL}/>`;
function legoParts(e){if(typeof e!=="string"||!e.startsWith("lego:"))return null;const p=e.split(":");const m=p[1];if(!LEGO_MAIN[m])return null;
  const x=(p[2]||"").split("+").filter(k=>LEGO_EXTRA[k]).slice(0,2);const c=Math.abs(parseInt(p[3],10)||0)%SUBJ_COLORS.length;
  return {m:m,x:x,c:c,mo:LEGO_MOTIONS.includes(p[4])?p[4]:"bob"};}
/* the drawing with holes for the colours: what the API gets (art.json → lego) and what the page fills below */
const LEGO_HOLES={f:"{{FILL}}",k:"{{INK}}"};
const legoMainTemplate=m=>{const P=LEGO_MAIN[m];return P.d(LEGO_HOLES)+faceSVG(P.face[0],P.face[1],P.face[2]);};
const legoExtraTemplate=k=>LEGO_EXTRA[k](LEGO_HOLES);
function legoSVG(e){const p=legoParts(e);if(!p)return null;const col=SUBJ_COLORS[p.c];
  const s=legoMainTemplate(p.m)+p.x.map((k,i)=>LEGO_BADGE(i)+legoExtraTemplate(k)+"</g>").join("");
  return s.split("{{FILL}}").join(col[0]).split("{{INK}}").join(col[1]);}
ARTS.lego=legoSVG;
```

## `02_question_factory/identity.py` 🆕 (الدفعة ٢٧)
**🎭 هوية كل مادة: صوت + شخصيات.** بايثون عادي، **بلا AI**. بيستعمله: `offline_generator.icon_for` (شكل الشخصيات) و`player/build_explain_player.pack` (الصفحة).
- `KNOWN`: المواد السبعة اللي عنا. **ما بنغيّر عليها إشي** (صوتها بالصفحة ورسوماتها بالمكتبة).
- `FAMILIES`: ١١ عائلة لمواد جديدة: الكلمات ← الشكل (`emblem`) + الشخصية (`mascot`) + الصوت (`instr` + `root` + `scale`). **بتنفحص قبل المواد اللي عنا**، فـ«Computer Science» و«علوم الحاسوب» = حاسوب، مش «علوم».
- `_has`: **كلمة كاملة بس**: الإنجليزي بـ `\b` (والكلمات الطويلة ممكن تكمل: «comput» ← «computer»)، والعربي كلمة كلمة بعد ما نشيل «ال/و/ب…» من أولها، والعبارة («تربية بدنية») بلا «ال» بكل كلمة. فـ«طب» مش جوا «تطبيقية»، و«دين» مش جوا «مدينتي».
- `generic`: مادة **ما إلها ولا كلمة** ← هوية من **حساب ثابت لاسمها** (`crc32`): آلة من ٨، مقام من ٤، جذر ٥٥–٦٩، وشكل + اسم شخصية من ٦. ونفس الآلة والجذر **ما بيتكرروا** مع مادة من المواد السبعة.
- `of_book`: كل اللي بتحتاجه الصفحة. مادة معروفة ← `new: False` و`sound: None` (الصفحة بتضل زي ما هي **بالبايت**). مادة جديدة ← `kind: "general"` + `family` + `emblem` + `mascot` (`subj:💻:`) + `mascot_name` + `face` + `sound`. **بلا مادة أصلاً** ← زي قبل.
- `emblem`: شكل شخصيات المادة الجديدة (`None` للمواد اللي عنا).
- **فحص:** `tests/test_identity.py` (١١): المواد الـ١٢ ما تغيّرت · العائلات بكلماتها · ولا كلمة جوا كلمة · الهوية الثابتة · كل آلة ومقام **موجودين بالصفحة** (`sound.js`) · كل شكل **إله رسمة بالصفحة** · شخصيات الحاسوب بأسمائها كاملة.

```python
"""🎭 Every subject has its own IDENTITY: a SOUND (instrument + scale) and CHARACTERS (an emblem, a mascot with a name).

   · The 7 subjects we already know (science, maths, physics, chemistry, geography, history, language) keep exactly
     what they have: their sounds live in the page (sound.js) and their drawings in the drawing library.
   · A NEW subject gets its own identity:
       1) by its words (computer, music, art, economics, religion, sport, health, civics, thinking, farming) → a ready family;
       2) nothing matches → a stable identity made from the subject's own name (the same subject always sounds and
          looks the same, and two different subjects almost never share one).
   The families are checked BEFORE the known subjects, so «Computer Science» / «علوم الحاسوب» is the computer, not science.
   Plain Python, no AI. Used by: offline_generator.icon_for (the characters) and player/build_explain_player.pack (the page)."""
import json
import os
import re
import zlib

# the subjects we know (their sounds + drawings already exist in the page) — the page's «subject» value
KNOWN = (("math", ("math", "رياضيات")), ("science", ("science", "biology", "علوم", "أحياء")), ("physics", ("physics", "فيزياء")),
         ("chemistry", ("chem", "كيمياء")), ("geography", ("geograph", "جغرافيا")), ("history", ("history", "تاريخ")),
         ("language", ("arabic", "english", "language", "لغة", "عربي")))

# the instruments and scales the page can play (sound.js → VOICES / SCALE). A test checks they are really there.
INSTRUMENTS = ("marimba", "pluck", "epiano", "glass", "kalimba", "wood", "flute", "bell", "chip", "harp", "vibes", "steel")
SCALES = ("major", "sus", "minor", "egypt")

# ready families for new subjects: words → emblem (the characters' shape) + mascot + sound
FAMILIES = (
    {"id": "computer", "label": "الحاسوب والتكنولوجيا", "emblem": "💻", "mascot": "بِتّو",
     "words": ("computer", "comput", "programming", "coding", "technology", "informatics", "ict", "robot", "حاسوب", "حاسب",
               "artificial intelligence", "ai", "برمجة", "تكنولوجيا", "تقنية", "معلوماتية", "رقمي", "روبوت", "ذكاء اصطناعي"),
     "sound": {"instr": "chip", "root": 64, "scale": "major"}},
    {"id": "music", "label": "الموسيقى", "emblem": "🎵", "mascot": "نغّوم",
     "words": ("music", "موسيقى", "موسيقا", "أناشيد", "إيقاع"), "sound": {"instr": "harp", "root": 62, "scale": "sus"}},
    {"id": "art", "label": "الفنون", "emblem": "🎨", "mascot": "لوّون",
     "words": ("art", "drawing", "design", "فنون", "فن", "تربية فنية", "رسم", "تصميم"), "sound": {"instr": "vibes", "root": 65, "scale": "major"}},
    {"id": "economy", "label": "الاقتصاد والمال", "emblem": "💹", "mascot": "قرّوش",
     "words": ("economic", "business", "finance", "accounting", "entrepreneur", "اقتصاد", "مالية", "محاسبة", "أعمال", "ريادة"),
     "sound": {"instr": "steel", "root": 60, "scale": "major"}},
    {"id": "religion", "label": "التربية الإسلامية", "emblem": "📗", "mascot": "نور", "face": False,
     "words": ("islamic", "religio", "quran", "إسلامية", "دين", "قرآن", "فقه", "حديث", "سيرة", "عقيدة", "تلاوة"),
     "sound": {"instr": "harp", "root": 57, "scale": "egypt"}},
    {"id": "sport", "label": "التربية البدنية", "emblem": "⚽", "mascot": "كوّور",
     "words": ("sport", "physical education", "fitness", "تربية بدنية", "رياضة", "لياقة"), "sound": {"instr": "steel", "root": 67, "scale": "sus"}},
    {"id": "health", "label": "الصحة", "emblem": "🩺", "mascot": "صحّوح",
     "words": ("health", "nutrition", "medic", "first aid", "صحة", "صحية", "تغذية", "طب", "إسعاف"), "sound": {"instr": "vibes", "root": 60, "scale": "sus"}},
    {"id": "civics", "label": "التربية الوطنية والاجتماعية", "emblem": "🏛️", "mascot": "وطّون",
     "words": ("civic", "citizenship", "social studies", "sociology", "وطنية", "مواطنة", "اجتماعيات", "دراسات اجتماعية", "مجتمع"),
     "sound": {"instr": "marimba", "root": 57, "scale": "minor"}},
    {"id": "thinking", "label": "التفكير والفلسفة", "emblem": "💡", "mascot": "فكّور",
     "words": ("philosoph", "logic", "thinking", "psycholog", "فلسفة", "منطق", "تفكير", "علم نفس"), "sound": {"instr": "glass", "root": 64, "scale": "sus"}},
    {"id": "space", "label": "الفلك والفضاء", "emblem": "🪐", "mascot": "كوكوب",
     "words": ("astronom", "space", "فلك", "فضاء"), "sound": {"instr": "glass", "root": 66, "scale": "sus"}},
    {"id": "farming", "label": "الزراعة", "emblem": "🌾", "mascot": "سنبول",
     "words": ("agricultur", "farming", "زراعة", "زراعية"), "sound": {"instr": "kalimba", "root": 60, "scale": "major"}},
)

# anything else: one of these friendly shapes (the page draws each one), chosen from the subject's name
GENERIC_EMBLEMS = ("✦hex", "✦star", "✦cloud", "✦shield", "✦drop", "✦gem")
GENERIC_MASCOTS = ("زهّور", "لمّوع", "نجّوم", "سحّوب", "قطّور", "ماسو")
NEW_INSTRUMENTS = ("chip", "harp", "vibes", "steel", "bell", "glass", "kalimba", "marimba")
# what the known subjects already use (a generic identity never copies one of them exactly)
_TAKEN = {("marimba", 65), ("pluck", 60), ("epiano", 62), ("glass", 69), ("kalimba", 67), ("wood", 57), ("flute", 62), ("bell", 60)}


def _text(subject) -> str:
    return " " + str(subject or "").lower().strip() + " "


_PREFIXES = ("وال", "بال", "فال", "لل", "ال", "و", "ب", "ل")


def _tokens(s: str) -> list:
    """The Arabic words, each also without «ال»/«و»… in front (so «والفنون» → «فنون»)."""
    out = []
    for w in re.findall(r"[\u0600-\u06FF]+", s):
        out.append(w)
        for p in _PREFIXES:
            if w.startswith(p) and len(w) - len(p) >= 2:
                out.append(w[len(p):])
                break
    return out


def _has(s: str, word: str) -> bool:
    """A WHOLE word, never a piece of another one: «طب» is not inside «تطبيقات», «art» is not inside «Earth»."""
    if re.match(r"^[a-z ]+$", word):                  # English: a word that starts here (long words may go on: «comput» → «computer»)
        tail = r"[a-z]*" if len(word) >= 5 else r"s?"
        return re.search(r"\b" + re.escape(word) + tail + r"\b", s) is not None
    if " " in word:                                   # an Arabic phrase: every word without «ال» («التربية البدنية» = «تربية بدنية»)
        bare = lambda x: " ".join(w[2:] if w.startswith("ال") and len(w) > 4 else w for w in x.split())
        return bare(word) in bare(s)
    return any(t == word or (len(word) >= 4 and t.startswith(word)) for t in _tokens(s))


def family(subject):
    """The ready family of a NEW subject (by its words), or None."""
    s = _text(subject)
    for f in FAMILIES:
        if any(_has(s, w) for w in f["words"]):
            return f
    return None


def known_kind(subject):
    """«science» / «math» / … for the subjects the page already knows, or None."""
    s = _text(subject)
    if family(subject):
        return None                                   # «Computer Science» is a new subject, not «science»
    return next((k for k, words in KNOWN if any(w in s for w in words)), None)


def _num(subject, salt: str) -> int:
    return zlib.crc32((salt + "|" + str(subject or "").strip().lower()).encode("utf-8"))


def generic(subject) -> dict:
    """A stable identity for a subject nothing matched: the same name → always the same sound and shape."""
    n = _num(subject, "id")
    instr = NEW_INSTRUMENTS[n % len(NEW_INSTRUMENTS)]
    root = 55 + (n // 7) % 15                         # 55..69: a comfortable middle range
    if (instr, root) in _TAKEN:
        root += 2
    i = (n // 131) % len(GENERIC_EMBLEMS)
    return {"id": "new", "label": str(subject or "مادة جديدة").strip() or "مادة جديدة", "emblem": GENERIC_EMBLEMS[i],
            "mascot": GENERIC_MASCOTS[i],
            "sound": {"instr": instr, "root": root, "scale": SCALES[(n // 977) % len(SCALES)]}}


# ---------- 🤖 batch 28: the MODEL picks an identity that FITS the meaning (once per subject, then it is saved) ----------
# Only for a subject that is not one of the 7 known and not one of the 11 families. The model chooses ONLY from what the page
# can draw and play (the lists above); its answer is checked; no key / bad answer → the stable identity from the name (as before).
EMBLEMS = tuple(f["emblem"] for f in FAMILIES) + GENERIC_EMBLEMS + ("📜", "🧮", "🔬", "📖", "🧭", "🔭", "⚗️")   # every shape the page draws
_STORE = os.environ.get("EXPLAIN_IDENTITY_FILE") or os.path.join(os.path.dirname(os.path.abspath(__file__)), "subject_identities.json")
_CACHE = {"mtime": None, "data": {}}


def set_store(path: str) -> None:
    """Where the chosen identities are saved (the API puts it in its data folder)."""
    global _STORE
    _STORE = path
    _CACHE["mtime"] = None


def _key(subject) -> str:
    return " ".join(str(subject or "").lower().split())


def _saved() -> dict:
    try:
        m = os.path.getmtime(_STORE)
    except OSError:
        return {}
    if _CACHE["mtime"] != m:
        try:
            with open(_STORE, encoding="utf-8") as f:
                _CACHE["data"] = json.load(f)
        except (OSError, ValueError):
            _CACHE["data"] = {}
        _CACHE["mtime"] = m
    return _CACHE["data"]


def chosen(subject):
    """The identity the model chose for this subject (already checked), or None."""
    return _saved().get(_key(subject))


def clean(ans, subject) -> dict:
    """Check the model's answer: only things the page can draw and play. Anything wrong → None (the name identity stays)."""
    if not isinstance(ans, dict):
        return None
    emb, instr, scale, name = ans.get("emblem"), ans.get("instrument"), ans.get("scale"), str(ans.get("mascot_name") or "").strip()
    try:
        root = int(ans.get("root"))
    except (TypeError, ValueError):
        return None
    if emb not in EMBLEMS or instr not in INSTRUMENTS or scale not in SCALES or not (55 <= root <= 69):
        return None
    if not re.fullmatch(r"[\u0621-\u064A\u0651]{2,10}", name):            # one short Arabic name (letters + shadda), nothing else
        return None
    label = str(ans.get("label") or subject or "").strip()[:30] or str(subject)
    return {"id": "chosen", "label": label, "emblem": emb, "mascot": name, "face": bool(ans.get("face", True)),
            "sound": {"instr": instr, "root": root, "scale": scale}}


PROMPT = """You give a NEW school subject its own identity on an Arabic learning page for students.
Subject: «{subject}»
Choose ONLY from these lists (the page can draw and play nothing else):
- emblem (the shape of all its characters; pick the one whose MEANING fits best): {emblems}
- instrument: {instruments}
- scale: {scales}   (major = bright, sus = open/calm, minor = serious, egypt = oriental)
- root: a number 55..69 (lower = deeper)
- mascot_name: ONE short friendly Arabic name for its main character, from the subject's own world, in the style of
  «بِتّو» (computer), «نغّوم» (music), «سنبول» (farming), «كوكوب» (space): 3-8 Arabic letters, a shadda allowed, no vowels, no spaces
- label: the subject's Arabic name for the page
- face: false only if faces would be disrespectful for this subject (e.g. religion), else true
Answer with ONE JSON object and nothing else:
{{"emblem": "…", "instrument": "…", "scale": "…", "root": 60, "mascot_name": "…", "label": "…", "face": true}}"""


def needs_model(subject) -> bool:
    """True when a model could give a better identity: a new subject, not a family, not chosen yet."""
    return bool(str(subject or "").strip()) and not known_kind(subject) and not family(subject) and chosen(subject) is None


def ask_model(subject, llm) -> dict:
    """ONE model call for a new subject → checked → saved (the next books of this subject reuse it, no new cost).
    llm(system, user) -> text. Returns the chosen identity, or None (no change: the name identity stays)."""
    if not needs_model(subject):
        return chosen(subject)
    user = PROMPT.format(subject=str(subject).strip(), emblems=" ".join(EMBLEMS), instruments=", ".join(INSTRUMENTS), scales=", ".join(SCALES))
    try:
        text = llm("You answer with one JSON object only.", user)
        m = re.search(r"\{.*\}", text or "", re.S)
        ans = clean(json.loads(m.group(0)) if m else None, subject)
    except Exception:                                    # no key, network, bad JSON… → the stable name identity (never breaks a book)
        return None
    if ans:
        data = dict(_saved())
        data[_key(subject)] = ans
        os.makedirs(os.path.dirname(_STORE) or ".", exist_ok=True)
        with open(_STORE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=1)
        _CACHE["mtime"] = None
    return ans


def of_book(book: dict) -> dict:
    """Everything the page needs about the book's identity.
    known subject → {"kind": "science", "sound": None, ...} (the page keeps what it has)
    new subject   → {"kind": "general", "family": "computer", "sound": {...}, "emblem": "💻", "mascot": "subj:💻:", "mascot_name": "بِتّو", ...}"""
    subject = (book or {}).get("subject", "")
    kind = known_kind(subject) or ("general" if not str(subject or "").strip() else None)   # no subject at all: as before
    if kind:
        return {"kind": kind, "family": None, "new": False, "label": str(subject), "emblem": None, "mascot": None,
                "mascot_name": None, "face": True, "sound": None}
    f = family(subject) or chosen(subject) or generic(subject)     # family (by words) → the model's choice (saved) → from the name
    return {"kind": "general", "family": f["id"], "new": True, "label": f["label"], "emblem": f["emblem"],
            "mascot": f"subj:{f['emblem']}:", "mascot_name": f["mascot"],
            "face": f.get("face", True), "sound": dict(f["sound"])}   # (how they MOVE is decided by the page: SUBJ_ANIM in part3_core.js)


def emblem(subject):
    """The emblem of a NEW subject's characters (None for the subjects we know: they keep their own)."""
    if known_kind(subject) or not str(subject or "").strip():
        return None
    return (family(subject) or chosen(subject) or generic(subject))["emblem"]
```

---

## `static/home.html` 🆕 (الدفعة ٢٧)
**صفحة السيرفر الرئيسية (`/`):** HTML + JS عادي، عربي، فاتح وغامق، وبتشتغل على التلفون.
- **📚 الكتب:** من `GET /books` (مرتبين من الصف ٤ للـ١٢): الشكل، الصف والمرحلة، كم مشهد، و**«🆕 مادة جديدة»** إذا إلها هوية. زر **«افتح الشرح»** (`page_url`) و**«🗑️ احذف»** (كبستين: الأولى بتسأل «متأكد؟»، بلا نوافذ منبثقة).
- **➕ جراف جديد:** اسحب ملف JSON أو الصقه ← `POST /explanations/generate` ← بيطلعلك: كم درس ومشهد، المرحلة، و**هوية المادة** (شكلها، شخصيتها، آلتها) + زر **«افتح الشرح»**. الخطأ بينكتب **بالسبب** (مثلاً «الجراف ما فيه ولا درس»).

```html
<!doctype html>
<html lang="ar" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>سيرفر الشرح التفاعلي</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Readex+Pro:wght@600;700&family=IBM+Plex+Sans+Arabic:wght@400;600;700&display=swap" rel="stylesheet">
<style>
/* the server's front page: the books on the server + a box to send a new graph. Plain HTML + JS, no AI. */
:root{--bg:#F5F3EE;--panel:#FFFFFF;--ink:#1F2A30;--muted:#5D6A70;--line:#DDD8CE;--chip:#EFEBE3;--accent:#0E6E62;--accent-ink:#fff;--good:#24804F;--bad:#B8322A;--new:#7A45B8;
  --font-display:"Readex Pro",system-ui,sans-serif;--font-body:"IBM Plex Sans Arabic",Tahoma,"Segoe UI",system-ui,sans-serif;--r:14px}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#12171A;--panel:#1A2125;--ink:#E6ECEE;--muted:#9DAAB0;--line:#2E393D;--chip:#232C30;--accent:#46BBA9;--accent-ink:#062420;--good:#55C487;--bad:#F07269;--new:#B79BF0;color-scheme:dark}}
:root[data-theme="dark"]{--bg:#12171A;--panel:#1A2125;--ink:#E6ECEE;--muted:#9DAAB0;--line:#2E393D;--chip:#232C30;--accent:#46BBA9;--accent-ink:#062420;--good:#55C487;--bad:#F07269;--new:#B79BF0;color-scheme:dark}
*{box-sizing:border-box}[hidden]{display:none!important}
body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--font-body);line-height:1.65;font-size:15px}
.wrap{max-width:1040px;margin:0 auto;padding-inline:16px;padding-block:22px 56px;display:grid;gap:16px}
h1,h2,h3{font-family:var(--font-display);line-height:1.3;margin:0;text-wrap:balance}
h1{font-size:clamp(1.5rem,3.4vw,2.1rem)}h2{font-size:1.12rem}
.eyebrow{margin:0;color:var(--accent);font-weight:700;font-size:.82rem;letter-spacing:.04em}
.lede{margin:4px 0 0;color:var(--muted);max-width:70ch}
.row{display:flex;gap:8px;flex-wrap:wrap;align-items:center}
.btn{border:0;background:var(--accent);color:var(--accent-ink);border-radius:10px;padding:10px 16px;font:inherit;font-weight:700;cursor:pointer;text-decoration:none;display:inline-flex;gap:6px;align-items:center;min-height:42px}
.btn.alt{background:var(--panel);color:var(--ink);border:1.5px solid var(--line)}
.btn.warn{background:var(--bad);color:#fff}
.btn[disabled]{opacity:.5;cursor:wait}
.card{background:var(--panel);border:1px solid var(--line);border-radius:var(--r);padding:16px;display:grid;gap:10px;min-width:0}
.small{color:var(--muted);font-size:.86rem;margin:0}
textarea{width:100%;min-height:120px;font:13px/1.5 ui-monospace,Menlo,Consolas,monospace;direction:ltr;border:1px solid var(--line);border-radius:10px;padding:10px;background:var(--bg);color:var(--ink)}
.drop{border:2px dashed var(--line);border-radius:12px;padding:14px;text-align:center;color:var(--muted);cursor:pointer}
.drop.on{border-color:var(--accent);color:var(--accent)}
label.ck{display:inline-flex;gap:8px;align-items:center;min-height:40px;cursor:pointer}
input[type=checkbox]{width:20px;height:20px;accent-color:var(--accent)}
.out{border-radius:12px;padding:12px 14px;background:var(--chip)}
.out.ok{border-inline-start:4px solid var(--good)}.out.bad{border-inline-start:4px solid var(--bad);color:var(--bad);font-weight:700}
.books{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,230px),1fr));gap:10px}
.book{border:1px solid var(--line);border-radius:12px;padding:12px;display:grid;gap:6px;background:var(--panel);align-content:start}
.book header{display:flex;gap:10px;align-items:center}
.book .em{font-size:1.7rem;line-height:1;width:42px;height:42px;display:grid;place-items:center;background:var(--chip);border-radius:12px;flex:none}
.book h3{font-size:.98rem}
.tag{display:inline-block;border-radius:999px;padding:1px 10px;font-size:.78rem;font-weight:700;background:var(--chip)}
.tag.new{background:color-mix(in srgb,var(--new) 16%,var(--panel));color:var(--new)}
.book .row .btn{min-height:38px;padding:6px 12px;font-size:.9rem}
code{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:.85em;background:var(--chip);border-radius:6px;padding:1px 6px;direction:ltr;unicode-bidi:embed}
</style></head>
<body><main class="wrap">
  <header>
    <p class="eyebrow">الشرح التفاعلي · FastAPI</p>
    <h1>سيرفر الشرح التفاعلي</h1>
    <p class="lede">ابعت <b>أي جراف</b>، وبيطلع الشرح كامل: المشاهد، الفعاليات الخمس، الأفلام، وأصوات كل مرحلة عمرية. و<b>المادة الجديدة</b> بتاخد <b>صوت وشخصيات خاصين فيها</b>.</p>
  </header>
  <div class="row"><a class="btn" href="/explain">📖 افتح كل الكتب</a><a class="btn alt" href="/docs">🧾 كل الطلبات (docs)</a></div>

  <section class="card" aria-labelledby="h-new">
    <h2 id="h-new">➕ جراف جديد</h2>
    <p class="small">نفس شكل جرافات المنصة: كتاب ← وحدة ← موضوع ← درس ← مفاهيم، ولكل مفهوم معنى، وللكتاب صف (<code>book.grade</code>) ومادة (<code>book.subject</code>). أمثلة: <code>02_question_factory/*_book_graph.json</code>.</p>
    <div class="drop" id="drop" tabindex="0" role="button">📂 اسحب ملف الجراف (JSON) لهون، أو اكبس لتختاره<input type="file" id="file" accept=".json,application/json" hidden></div>
    <textarea id="graph" placeholder='{"book": {"id": "...", "title": "...", "subject": "...", "grade": 7}, "nodes": [...], ...}' aria-label="الجراف (JSON)"></textarea>
    <div class="row"><label class="ck"><input type="checkbox" id="llm"> ✨ الموديل يحسّن الفقرات (بده مفتاح على السيرفر)</label>
      <button class="btn" id="go">⚙️ ولّد الشرح</button></div>
    <div id="out" hidden></div>
  </section>

  <section class="card" aria-labelledby="h-books">
    <div class="row" style="justify-content:space-between"><h2 id="h-books">📚 الكتب على السيرفر</h2><span class="small" id="count"></span></div>
    <div class="books" id="books"><p class="small">⏳ لحظة…</p></div>
  </section>
</main>
<script>
const $=id=>document.getElementById(id);
const esc=t=>String(t??"").replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const STAGE={kids:"🌈 الصغار",junior:"🧭 ابتدائي عليا",teen:"🔬 إعدادي",senior:"📐 ثانوي"};
const KNOWN=[["math","🔢"],["رياضيات","🔢"],["physic","🧲"],["فيزياء","🧲"],["chem","⚗️"],["كيمياء","⚗️"],["biolog","🧬"],["أحياء","🧬"],["science","🌱"],["علوم","🌱"],["geograph","🌍"],["جغرافيا","🌍"],["history","📜"],["تاريخ","📜"],["arab","🔤"],["عربي","🔤"],["english","🔤"],["لغة","🔤"]];
const NICE={"✦hex":"⬢","✦star":"⭐","✦cloud":"☁️","✦shield":"🛡️","✦drop":"💧","✦gem":"💎"};
const emblemOf=b=>{const id=b.identity||{};if(id.new&&id.emblem)return NICE[id.emblem]||id.emblem;const s=String(b.subject||"").toLowerCase();return (KNOWN.find(([w])=>s.includes(w))||[0,"📘"])[1];};
async function loadBooks(){
  try{const r=await fetch("/books");const list=await r.json();if(!r.ok)throw new Error(list.detail||r.status);
    $("count").textContent=list.length+" كتاب";
    $("books").innerHTML=list.length?list.map(b=>{const id=b.identity||{};
      return `<article class="book"><header><span class="em" aria-hidden="true">${esc(emblemOf(b))}</span><div><h3>${esc(b.title)}</h3><span class="small">${b.grade?"صف "+esc(b.grade)+" · ":""}${esc(STAGE[b.stage]||"")}</span></div></header>
        <div class="row">${id.new?`<span class="tag new">🆕 ${esc(id.label)}</span>`:""}<span class="tag">${esc(b.scenes)} مشهد</span></div>
        <div class="row"><a class="btn" href="${esc(b.page_url||"/explain/"+b.book_id)}">افتح الشرح ←</a><button class="btn alt del" data-id="${esc(b.book_id)}">🗑️ احذف</button></div></article>`;}).join(""):`<p class="small">لسا ما في كتب. ابعت جراف فوق.</p>`;
    document.querySelectorAll(".del").forEach(x=>x.addEventListener("click",()=>del(x)));
  }catch(e){$("books").innerHTML=`<p class="out bad">ما قدرت أجيب الكتب: ${esc(e.message)}</p>`;}
}
async function del(btn){                       /* two clicks: the first asks «متأكد؟» (no pop-up windows) */
  if(!btn.classList.contains("warn")){btn.classList.add("warn");btn.textContent="متأكد؟ اكبس كمان";setTimeout(()=>{btn.classList.remove("warn");btn.textContent="🗑️ احذف";},4000);return;}
  btn.disabled=true;const r=await fetch("/books/"+encodeURIComponent(btn.dataset.id),{method:"DELETE"});if(!r.ok)btn.textContent="ما انحذف";loadBooks();
}
function readFile(f){if(!f)return;const rd=new FileReader();rd.onload=()=>{$("graph").value=rd.result;};rd.readAsText(f,"utf-8");}
$("drop").addEventListener("click",()=>$("file").click());
$("drop").addEventListener("keydown",e=>{if(e.key==="Enter"||e.key===" "){e.preventDefault();$("file").click();}});
$("file").addEventListener("change",e=>readFile(e.target.files[0]));
["dragenter","dragover"].forEach(t=>$("drop").addEventListener(t,e=>{e.preventDefault();$("drop").classList.add("on");}));
["dragleave","drop"].forEach(t=>$("drop").addEventListener(t,e=>{e.preventDefault();$("drop").classList.remove("on");}));
$("drop").addEventListener("drop",e=>readFile(e.dataTransfer.files[0]));
$("go").addEventListener("click",async()=>{
  const out=$("out");out.hidden=false;let graph;
  try{graph=JSON.parse($("graph").value);}catch(e){out.className="out bad";out.textContent="الجراف مش JSON صحيح: "+e.message;return;}
  $("go").disabled=true;out.className="out";out.textContent="⏳ بعمل الشرح…";
  try{const r=await fetch("/explanations/generate",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({graph,use_llm:$("llm").checked})});
    const j=await r.json();if(!r.ok)throw new Error(typeof j.detail==="string"?j.detail:JSON.stringify(j.detail));
    const id=j.identity||{},snd=id.sound?` · صوتها: <b>${esc(id.sound.instr)}</b>`:"";
    out.className="out ok";
    out.innerHTML=`✅ <b>«${esc(j.title)}»</b>: ${j.lessons.length} درس · <b>${j.scenes} مشهد</b> · ${esc(STAGE[j.stage]||"")}
      ${id.new?`<br>🆕 مادة جديدة: <b>${esc(NICE[id.emblem]||id.emblem)} ${esc(id.label)}</b> · شخصيتها «${esc(id.mascot_name)}»${snd}`:""}
      ${j.warnings&&j.warnings.length?`<br><span class="small">⚠️ ${j.warnings.length} ملاحظة (مشاهد انشالت لأنها ما نجحت بالفحص مع الجراف)</span>`:""}
      <div class="row" style="margin-top:8px"><a class="btn" href="${esc(j.page_url)}">📖 افتح الشرح ←</a></div>`;
    loadBooks();
  }catch(e){out.className="out bad";out.textContent="ما زبط: "+e.message;}
  finally{$("go").disabled=false;}
});
loadBooks();
</script></body></html>
```

---

## `tests_browser/test_server_page.py` 🆕 (الدفعة ٢٧)
**صفحة السيرفر بمتصفح حقيقي** (Playwright): (١) الـ API بيرسم **نفس شخصيات الصفحة بالزبط** · (٢) مادة جديدة (الحاسوب) ومادة **ما إلها ولا كلمة** (عالم الحشرات): صوتها الخاص، كل شخصياتها بشكلها، الاسم كامل، لون لكل مفهوم، شخصيتها بتسلّم على الصغار، الكبسة على الشخصية بتطلّع نغمة من آلتها، **وكل الخطوات بتفتح بلا أخطاء** · (٣) الآلات الأربعة الجديدة مسموعة، ما بتشوّش، ومختلفة. **آخر نتيجة: ١٩/١٩.**

```python
"""🆕 batch 27 — the page the SERVER gives, in a real browser (Playwright + Chromium):
  1) the API draws the subject characters EXACTLY like the page (every emblem × long and short names);
  2) a NEW subject (the computer book, never seen by the code) sent to the service → its page works: its own sound (chip),
     its own characters (💻 with whole names, a colour each), its own mascot «بِتّو», every scene opens, no JS error;
  3) a subject NOTHING matches → a stable identity of its own (a friendly shape + its own instrument), and its page works too;
  4) the new instruments really sound: loud enough, never clipping, each one different.
Run:  python tests_browser/test_server_page.py          (from 05_explanation_api)"""
import json
import os
import re
import sys
import tempfile

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.environ["EXPLAIN_DATA_DIR"] = tempfile.mkdtemp(prefix="explain_page_test_")
os.environ["EXPLAIN_SEED"] = "0"
sys.path.insert(0, HERE)
from playwright.sync_api import sync_playwright  # noqa: E402

from core import art, service  # noqa: E402

FACTORY = os.path.join(os.path.dirname(HERE), "02_question_factory")
OUT = tempfile.mkdtemp(prefix="explain_pages_")
oks, fails = [], []


def ok(cond, what, extra=""):
    (oks if cond else fails).append(what)
    print(("✅ " if cond else "❌ ") + what + (f"  · {extra}" if extra else ""))


def page_file(book_ids, name):
    p = os.path.join(OUT, name)
    with open(p, "w", encoding="utf-8") as f:
        f.write(service.page_html(book_ids))
    return "file://" + p


def page_data(url):
    """The data inside a page (the page keeps it private, inside its own function)."""
    html = open(url[len("file://"):], encoding="utf-8").read()
    return json.loads(html.split("const DATA = ")[1].split(";\nconst $")[0])


with open(os.path.join(FACTORY, "examples", "new_subject_computer_g7.json"), encoding="utf-8") as f:
    CS = json.load(f)
cs = service.generate(graph=CS)
odd_graph = json.loads(json.dumps(CS).replace("cs_g7", "bugs_g4"))
odd_graph["book"].update({"subject": "عالم الحشرات", "title": "عالم الحشرات · الصف الرابع", "grade": 4})
odd = service.generate(graph=odd_graph)

with sync_playwright() as p:
    b = p.chromium.launch()

    # ---------- 1) the API's drawings == the page's drawings ----------
    pg = b.new_page()
    pg.goto(page_file(["cs_g7"], "cs.html")); pg.wait_for_timeout(600)
    emblems = pg.evaluate("Object.keys(window.__ART.SUBJ_ART)")
    labels = ["حاسوب", "وحدة المعالجة المركزية", "الخطأ البرمجي", "الكهرومغناطيسية", "الوحدة الثالثة: الوراثة", "", "ذاكرة"]
    js = pg.evaluate("""([es,ls])=>{const o={};es.forEach(e=>ls.forEach(l=>{o[e+'|'+l]=window.__ART.artSVG('subj:'+e+':'+l,'');}));return o;}""", [emblems, labels])
    bad = []
    for key, svg in js.items():
        e, l = key.split("|", 1)
        body_js = re.sub(r"^<svg[^>]*>|</svg>$", "", svg)
        body_py = re.sub(r"^<svg[^>]*>|</svg>$", "", art.art_svg(f"subj:{e}:{l}") or "")
        if body_js != body_py:
            bad.append(key)
    ok(not bad and len(js) == len(emblems) * len(labels), f"الـ API بيرسم نفس شخصيات الصفحة بالزبط ({len(emblems)} شكل × {len(labels)} اسم)", ", ".join(bad[:4]))
    pg.close()

    # ---------- 2) the NEW subject's page ----------
    for name, ids, want_instr in (("الحاسوب (مادة جديدة)", ["cs_g7"], "chip"), ("عالم الحشرات (ما في كلمة بتعرفها)", ["bugs_g4"], odd["identity"]["sound"]["instr"])):
        pg = b.new_page(viewport={"width": 1280, "height": 900}); errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)[:200]))
        url = page_file(ids, ids[0] + ".html")
        pg.goto(url); pg.wait_for_timeout(900)
        prof = pg.evaluate("window.__SOUND.now()")
        ok(prof["instr"] == want_instr, f"{name}: صوتها الخاص", json.dumps(prof))
        data = page_data(url)["graphs"][0]
        idn = data.get("identity") or {}
        icons = [i for l in data["lessons"] for i in (l.get("icons") or {}).values()]
        ok(icons and all(i.startswith(("lego:", "subj:" + idn["emblem"] + ":")) for i in icons),
           f"{name}: كل شخصياتها إلها: 🧱 رسمة مركّبة (ليغو، الدفعة ٢٩) أو بشكل مادتها ({idn.get('emblem')})", icons[:4])
        if ids[0] == "cs_g7":
            whole = pg.evaluate("window.__ART.artSVG('subj:💻:وحدة المعالجة المركزية','')")
            ok(">وحدة المعالجة<" in whole and ">المركزية<" in whole, f"{name}: مفهوم بلا رسمة ولا قطعة ← الاسم كامل على سطرين (ما في «وحدة المعا»)")
        fills = set(pg.evaluate("[...document.querySelectorAll('#stagebox svg.ch, .stage svg.ch, svg.ch')].map(s=>(s.querySelector('[fill]')||{}).getAttribute&&s.querySelector('[fill]').getAttribute('fill')).filter(Boolean)"))
        ok(len(fills) >= 3, f"{name}: لون مختلف لكل مفهوم", f"{len(fills)} لون")
        # the mascot: switch the page to the little ones' look → «أهلاً! أنا «<mascot>»»
        pg.evaluate("""()=>{const s=document.querySelector('#stageSel,select[id*=stage],select[aria-label*="المرحلة"]');if(s){s.value='kids';s.dispatchEvent(new Event('change',{bubbles:true}));}}""")
        pg.wait_for_timeout(500)
        ok(idn.get("mascot_name") and idn["mascot_name"] in pg.inner_text("body"), f"{name}: شخصيتها «{idn.get('mascot_name')}» بتسلّم على الصغار")
        # poke one of its characters → a note of ITS instrument
        n0 = pg.evaluate("window.__SOUND.log.length")
        el = pg.query_selector('.alive[data-k="subj"], .char[data-k="subj"]')
        if el:
            el.dispatch_event("pointerdown")
        pg.wait_for_timeout(150)
        ok(el is not None and pg.evaluate("window.__SOUND.log.length") > n0, f"{name}: بتكبس على الشخصية ← بتطلع نغمة من آلتها")
        # every step of every lesson opens with no error
        steps = 0
        for li in range(len(data["lessons"])):
            pg.click(f'#side .les[data-g="0"][data-l="{li}"]'); pg.wait_for_timeout(120)
            for _ in range(60):
                nx = pg.query_selector("#next")
                if not nx or nx.is_disabled() or "خلص" in (nx.inner_text() or ""):
                    break
                nx.click(); steps += 1; pg.wait_for_timeout(40)
        ok(steps > 20 and not errs, f"{name}: كل الخطوات بتفتح بلا أخطاء", f"{steps} خطوة · {errs[:2]}")
        pg.close()

    # ---------- 4) the new instruments really sound ----------
    pg = b.new_page()
    pg.goto(page_file(["cs_g7"], "cs2.html")); pg.wait_for_timeout(500)
    res = {}
    for instr in ("chip", "harp", "vibes", "steel"):
        res[instr] = pg.evaluate("async i=>await window.__SOUND.render('good','kids',{instr:i,root:62,scale:'major'})", instr)
    for instr, r in res.items():
        ok(0.02 < r["peak"] < 0.98 and r["secs"] > 0.15, f"الآلة الجديدة «{instr}»: مسموعة وما بتشوّش", f"peak {r['peak']:.2f} · {r['secs']:.2f}s")
    sig = {(round(r["bright"] / 150), round(r["secs"], 1)) for r in res.values()}
    ok(len(sig) == 4, "كل آلة جديدة صوتها مختلف عن الثانية", json.dumps({k: [round(v["bright"]), round(v["secs"], 2)] for k, v in res.items()}))
    pg.close()
    b.close()

print(f"\n{len(oks)} ✅ · {len(fails)} ❌")
if fails:
    print("❌", fails)
    sys.exit(1)
```

---

## `02_question_factory/` (مصنع الشرح · كان `engine/`)
🆕 **صار بمكان واحد:** الـ API بيستعمله مباشرة. نفس المصنع اللي شرحناه بـ `EXPLANATION_AR.md`، **+ الجديد:** **`identity.py` (هوية المادة، الدفعة ٢٧)** · `audience.py` (العمر) · `scene_writer.py` و`sdk/scene_sdk.js` (مشاهد الموديل) · **`explain_activities.py` (الفعاليات الخمس، الدفعة ٢٦)**. والباقي: `graph_reader.py` (قراءة الجراف) · `offline_generator.py` (اختيار الرسومات والجمل) · `explain_generator.py` (المشاهد الـ ١٣ + فعالية جديدة لكل مفهوم) · `explain_main.py` (لكل درس: مشاهد ← فحص ← حفظ) · `explain_llm.py` (الموديل بيحسّن الفقرات مع فحص) · `llm_gateway.py` (Gemini ← GPT ← Claude) · `config.py` و`templates.py`.

## `art/art.json`
**ملف واحد:** **١١٩ رسمة** (منها **٣٢ للصفوف الكبيرة**) + **٢٥ شكل** «شخصية المادة» (٨ للمواد اللي عنا + ١١ للعائلات الجديدة + ٦ أشكال عامة)، صدّرناهم من مكتبتنا بـ `scripts/export_art.py`.

## الفحص
🆕 **الدفعة ٢٧: ٤٤ فحص ✅** (الـ٣٣ القديمة + ١١ جديدة: هوية المادة الجديدة، شخصياتها بأسمائها كاملة، كل أنواع الفعاليات إلها، صفحة كتاب وصفحة كل الكتب، **صفحة السيرفر للكتب الـ١٢ = الصفحة المنشورة بالبايت**، الحذف والأرقام الخطرة، قواعد الوجه بالرسومات، والطلبات الجديدة `/` `/explain` `/explain-data` `DELETE /books`). نجحت بالنسخة التجريبية من FastAPI، **ومع Pydantic الحقيقي كمان**. وبالمتصفح: **`tests_browser/test_server_page.py` ١٩/١٩** (نفس الرسومات بالـ API والصفحة · مادة جديدة ومادة ما إلها كلمة: صوتها، شخصياتها، ألوانها، شخصيتها بتسلّم، نغمة لما تكبس، **١١٩ خطوة بلا أخطاء** · الآلات الجديدة مسموعة وما بتشوّش ومختلفة). وبالمصنع: **٤٧ فحص** (منها ١١ لهوية المادة).

**قبل (الدفعة ٢٦): ٣٣ فحص ✅** (الدفعة ٢٦: نفس الـ٣٣ نجحت، ومنها فحص «ما في نوع مشهد الفرونت ما بيعرفه» صار بيغطي الأنواع الخمسة الجديدة): الخدمة **٩/٩** (حقيقية) · مشاهد الموديل **١٦/١٦** (حقيقية، بموديل وهمي) · طلبات HTTP **٨/٨** (الـ API ٦ + مشاهد الموديل ٢) **بنسخة FastAPI تجريبية** عندنا (`PYTHONPATH=tests/local_stub_only_for_sandbox`)؛ **عندكم بتشتغل بالحقيقية** بعد `pip install -r requirements.txt` (التنزيل ممنوع ببيئتنا). وبالمتصفح: **صندوق مشهد الموديل ٨/٨** (`02_question_factory/tests_browser/test_llm_runner.py`: بيرسم، جوا الصورة، السحب، الفقاعة، بلا وجوه بالثانوي، **الإنترنت محجوب**).

**⚠️ اللي ما انجرّب هون:** موديل **حقيقي** (ما في مفاتيح ولا رصيد) و**FastAPI الحقيقي**. هدول بيتجرّبوا عندك.
