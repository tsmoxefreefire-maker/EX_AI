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
