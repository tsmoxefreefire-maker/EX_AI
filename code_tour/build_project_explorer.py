"""Builds code_tour/PROJECT_EXPLORER.html: the whole project like PyCharm (💡 Hareth's idea).
Left: every file of the project (a tree). Middle: the file's REAL code (read from the files right now, with line numbers and colours).
Right: its Arabic explanation (written once in code_tour/notes/*.py), what it depends on and who uses it, and every function inside it
with a short explanation; «🔢 خطوة خطوة» walks the files (and the 41 functions of the code tour) in the real order of the work.
Links between files and functions are found by READING the code (imports, calls), not written by hand.
Run after changing the code:   python code_tour/build_project_explorer.py        (plain Python, no installs, no AI)"""
import ast
import importlib.util
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import explorer_scan as scan  # noqa: E402
from steps_ar import PHASES as FPHASES, STEPS as FSTEPS  # noqa: E402

# 🔤 change a word EVERYWHERE in the Arabic text with one line, e.g. {"المصنع": "المُخرج"} (empty = the words as written)
NAME_MAP = {}

PROJECT = {
    "title": "كود الشرح التفاعلي، ملف ملف",
    "lead": "كل ملفات المشروع عاليسار. اختار أي ملف: بيطلع كوده الحقيقي بالنص، وجنبه شرحه بالعربي، وعلى شو بيعتمد ومين بيستعمله، "
            "وكل فانكشن جواه بسطر شرح. أو امشِ «خطوة خطوة» من أول ما الجراف يوصل للسيرفر لآخر ما المتصفح يرسم.",
    "who": "بايثون (عند السيرفر) بيقرر وبيكتب: بيقرأ الجراف، بيعرف المرحلة العمرية، بيختار رسمة كل مفهوم، وبيكتب المشاهد ويفحصها ويحفظها. "
           "JavaScript (بمتصفح الطالب) بينفّذ: بيرسم الرسمات (SVG مكتوبة بالكود)، بيحرّكها، وبيعمل الأصوات بالحساب (Web Audio). "
           "الموديل اختياري: بيختار من قوائمنا بس، ومشهده بيحتاج موافقة المعلم.",
}

FOLDERS = {
    "02_question_factory": "بايثون: بيقرأ الجراف وبيكتب المشاهد",
    "02_question_factory/player": "الصفحة الجاهزة وقالبها",
    "02_question_factory/tests": "فحوصات بايثون",
    "02_question_factory/tests_browser": "فحوصات بمتصفح حقيقي",
    "02_question_factory/examples": "مادة جديدة للتجربة",
    "02_question_factory/llm_scenes_demo": "مثال مشهد موديل",
    "02_question_factory/sdk": "أدوات مشاهد الموديل",
    "03_explain_player_src": "كود الصفحة: JavaScript + CSS",
    "05_explanation_api": "السيرفر (FastAPI)",
    "05_explanation_api/api": "أبواب السيرفر",
    "05_explanation_api/core": "قلب السيرفر",
    "05_explanation_api/art": "الرسومات بملف واحد",
    "05_explanation_api/scripts": "سكربتات مساعدة",
    "05_explanation_api/static": "صفحة السيرفر الرئيسية",
    "05_explanation_api/tests": "فحوصات السيرفر",
    "05_explanation_api/tests_browser": "فحوصات بمتصفح حقيقي",
    "05_explanation_api/tests/local_stub_only_for_sandbox": "نسخة وهمية للفحص بس",
    "code_tour": "رحلة الكود وهالصفحة",
}

F = "02_question_factory/"
P = "03_explain_player_src/"
A = "05_explanation_api/"
JPHASES = [
    ("p1", "السيرفر بيستلم", "١ · السيرفر بيستلم الجراف", "FastAPI بيفتح الأبواب، بياخد الجراف، وبيسلّمه لمدير الشغل."),
    ("p2", "بايثون بيقرأ وبيقرر", "٢ · بايثون بيقرأ وبيقرر", "بيقرأ الجراف، بيعرف المرحلة العمرية، وبيختار هوية المادة ورسمة كل مفهوم."),
    ("p3", "بايثون بيكتب المشاهد", "٣ · بايثون بيكتب المشاهد", "بيكتب مشاهد كل درس من الجراف، بيفحصها، وبيحفظها."),
    ("p4", "الصفحة بتنجهّز", "٤ · الصفحة بتنجهّز", "كود الصفحة بينلزق بقالب واحد، والسيرفر بيحط فيه داتا الكتاب."),
    ("p5", "المتصفح بيعرض", "٥ · المتصفح بيعرض", "JavaScript بمتصفح الطالب بيرسم، بيحرّك، بيطلّع الأصوات، وبيتفاعل."),
    ("p6", "الموديل (اختياري)", "٦ · الموديل (اختياري)", "بس مع المفاتيح: الموديل بيختار من قوائمنا، أو بيكتب مشهد بيوافق عليه المعلم."),
    ("p7", "أدوات وفحوصات", "٧ · أدوات البناء والفحوصات", "سكربتات بتبني الصفحة والرسومات، وفحوصات بتتأكد إنه ما في إشي خربان."),
]
JOURNEY = [
    ("p1", A + "main.py", "تشغيل السيرفر", "بيعمل تطبيق FastAPI وبيوصّل فيه الأبواب. من هون بيبلش كل إشي."),
    ("p1", A + "api/routes.py", "الأبواب", "كل رابط بالسيرفر: شو بياخد وشو بيرجّع. أهمهم POST /explanations/generate و GET /explain/{book_id}."),
    ("p1", A + "api/schemas.py", "شكل الطلب والجواب", "بيتأكد إن الجراف الداخل والجواب الطالع بالشكل الصح."),
    ("p1", A + "core/settings.py", "الإعدادات", "وين بتنحفظ الداتا، وأسماء المجلدات."),
    ("p1", A + "core/service.py", "مدير الشغل", "بيوزّع الشغل: بيسمّي الكتاب، بينادي بايثون اللي بيكتب المشاهد، وبيرجّع النتيجة والرابط."),
    ("p2", F + "explain_main.py", "زر التشغيل", "الفانكشن run: بتقرأ الجراف، بتكتب مشاهد كل درس، بتفحصها، وبتحفظها."),
    ("p2", F + "graph_reader.py", "قراءة الجراف", "بيحوّل ملف الجراف لمفاهيم وأسهم «بيحتاج» ودروس، بترتيب التعلّم."),
    ("p2", F + "audience.py", "المرحلة العمرية", "من الصف: أطفال، إعدادي، متوسط، ثانوي. وكلام كل مرحلة."),
    ("p2", F + "identity.py", "هوية المادة الجديدة", "صوت وشعار وألوان وشخصية لأي مادة مش من موادنا."),
    ("p2", F + "offline_generator.py", "اختيار الرسمات", "لكل مفهوم اسم رسمة: من المكتبة، أو ليغو، أو شخصية المادة مع الاسم."),
    ("p2", F + "lego.py", "رسومات القطع (ليغو)", "رسمة بتنركّب من قطع لما ما في رسمة جاهزة، وبتنحفظ عشان تنعاد."),
    ("p3", F + "explain_generator.py", "كتابة المشاهد", "أنواع المشاهد كلها، كل مشهد بخطواته وجمله، من الجراف بس. وفحص إن ولا جملة بتكذب."),
    ("p3", F + "explain_activities.py", "الفعاليات الخمس", "الشروط، ارسم الأسهم، قارن، اشرح لزميلك، السلّم."),
    ("p3", A + "core/storage.py", "الحفظ", "بيحفظ المشاهد والكتب كملفات JSON وبيقرأها."),
    ("p4", P + "build_explain_template.py", "لزق كود الصفحة", "بيجمع الهيكل و CSS و JavaScript بقالب واحد: player/explain_template.html."),
    ("p4", F + "player/build_explain_player.py", "تعبئة القالب", "بيحط داتا الكتاب جوا القالب، والنتيجة صفحة HTML وحدة."),
    ("p5", P + "explain_shell.html", "هيكل الصفحة", "القائمة، الترحيب، مكان المشهد، والأزرار."),
    ("p5", P + "part3_core.js", "الرسم والأدوات", "بيحوّل اسم الرسمة لـ SVG، وفيه الأصوات القديمة وأدوات كثيرة."),
    ("p5", P + "explain.js", "مشغّل المشاهد", "بيعرض كل مشهد خطوة خطوة: القائمة، الأسهم، الفقاعات، الأزرار."),
    ("p5", P + "stage.js", "شكل كل مرحلة", "الشكل والكلام وأصوات كل مرحلة، ولحن المرحلة لما توصلها."),
    ("p5", P + "lego.js", "تركيب الليغو", "بيقرأ وصفة الليغو وبيركّب الرسمة من القطع."),
    ("p5", P + "sound.js", "الأصوات", "أصوات بالحساب بلا ملفات: آلة المادة وطابع المرحلة."),
    ("p5", P + "narrator.js", "الراوي والفيديو", "التشغيل التلقائي، الفقاعات، وصوت الفارة على الشخصيات."),
    ("p5", P + "more_scenes.js", "مشاهد إضافية ١", "المقابلة والبطاقات."),
    ("p5", P + "more_scenes2.js", "مشاهد إضافية ٢", "الشريط، الحوار، العدسة، ركّب الصورة…"),
    ("p5", P + "more_scenes3.js", "الفعاليات الخمس بالصفحة", "رسم وتفاعل الفعاليات الخمس."),
    ("p5", P + "play.js", "الأفلام", "محرّك الأفلام القصيرة: كل خطوة بتشغّل جزء، وبعدين «دورك»."),
    ("p5", P + "world.js", "عالم الدرس", "مشهد العالم: الدرس كله كمكان واحد حي."),
    ("p6", F + "llm_gateway.py", "باب الموديل", "بيحكي مع Gemini أو OpenAI، والمفاتيح من متغيرات البيئة بس."),
    ("p6", F + "explain_llm.py", "تحسين «ليش؟»", "مع الموديل بس: بيحسّن جمل «ليش؟»."),
    ("p6", A + "core/llm_scenes.py", "مشهد من الموديل", "الموديل بيكتب مشهد، بيتفحص، والمعلم بيوافق قبل ما يطلع للطالب."),
    ("p6", A + "core/contract.py", "قواعد الأمان", "الشروط اللي لازم مشهد الموديل يمشي عليها."),
    ("p7", A + "core/art.py", "الرسومات من السيرفر", "نفس رسومات الصفحة كـ SVG، لأي فرونت إند ثاني."),
    ("p7", A + "scripts/export_art.py", "تصدير الرسومات", "بياخد الرسومات من الصفحة لملف واحد art/art.json."),
    ("p7", F + "build_all_books.py", "بناء الكتب الـ١٢", "بيبني الصفحة المنشورة player/explain.html من الجرافات."),
    ("p7", F + "tests_browser/audit_every_scene.py", "فحص كل المشاهد", "بيفتح كل مشهد بكل حالاته بمتصفح حقيقي وبيدوّر على مشاكل."),
]

GLOSSARY = [
    ("الجراف", "ملف JSON فيه مفاهيم الكتاب، والأسهم بينها (مين بيحتاج مين)، والدروس، والصف والمادة. هو المدخل الوحيد."),
    ("مفهوم", "فكرة وحدة بالدرس، زي «الكسر» أو «المقام». كل مفهوم بيصير شخصية بالمشهد."),
    ("سهم «بيحتاج»", "علاقة بالجراف: «المقام بيحتاج الكسر» يعني لازم تفهم الكسر أول."),
    ("ترتيب التعلّم", "ترتيب المفاهيم بحيث اللي بيحتاجه المفهوم بييجي قبله."),
    ("مشهد", "شاشة وحدة بالشرح (زي «تعرّف عليّ» أو «شو لو؟»)، مقسومة خطوات، وكل خطوة إلها جملة."),
    ("المرحلة العمرية", "أطفال (١–٤)، إعدادي (٥–٧)، متوسط (٨–٩)، ثانوي (١٠–١٢). بتغيّر الكلام والشكل والأصوات."),
    ("الهوية", "اللي بتاخده المادة الجديدة: آلة صوت، شعار، ألوان، وشخصية باسمها."),
    ("مفتاح الرسمة", "اسم قصير للرسمة زي sec:slope. بايثون بيختاره، والمتصفح بيرسمه."),
    ("الليغو", "رسمة بتنركّب من قطع جاهزة (تشبيه + شارة + لون + حركة) لما ما في رسمة بالمكتبة. مفتاحها lego:<قطعة>:<شارات>:<لون>:<حركة>."),
    ("FastAPI", "مكتبة بايثون بتعمل السيرفر: كل «باب» (رابط) إله فانكشن."),
    ("endpoint / باب", "رابط بالسيرفر زي POST /explanations/generate: بتبعتله إشي وبيرجّعلك جواب."),
    ("JSON", "طريقة لكتابة الداتا كنص مرتّب (أسماء وقيم). الجراف والمشاهد المحفوظة كلها JSON."),
    ("Pydantic", "بتفحص إن الداتا الداخلة للسيرفر بالشكل الصح، وبترفض الغلط برسالة واضحة."),
    ("SVG", "رسمة مكتوبة كنص (دوائر، خطوط، ألوان). المتصفح بيقرأها وبيرسمها، وما بتخرب لما تكبر."),
    ("Web Audio", "أداة بالمتصفح بتعمل الأصوات بالحساب (موجات)، بلا ملفات صوت."),
    ("القالب (template)", "الصفحة الجاهزة بدون داتا. السيرفر بيحط داتا الكتاب مكان /*DATA*/null."),
    ("الموديل (LLM)", "ذكاء اصطناعي زي Gemini. عنا اختياري: بيختار من قوائمنا بس، والمفاتيح من متغيرات البيئة."),
    ("الفحص (test)", "كود بيشغّل الكود الأصلي وبيتأكد إن النتيجة صح. بنشغّله بعد كل تعديل."),
    ("unittest", "أداة الفحص اللي جاية مع بايثون."),
    ("Playwright", "بيشغّل متصفح حقيقي (Chromium) من الكود: بيفتح الصفحة، بيكبس، وبيقيس."),
    ("stub", "نسخة وهمية صغيرة من مكتبة، بنستعملها بالفحص بس لما المكتبة الحقيقية مش موجودة."),
    ("AST", "بايثون بيقرأ ملف كود كشجرة (فانكشنز، استدعاءات…). هالصفحة بتستعمله عشان تلاقي مين بينادي مين."),
]

GEN_SHOWN = 60
GEN_COLS = 300
JS_STOP = scan.JS_STOP | {"seen", "last", "push", "keys", "join", "html"}


def ar(text):
    if not isinstance(text, str):
        return text
    for a, b in NAME_MAP.items():
        text = text.replace(a, b)
    return text


def load_notes():
    out = {}
    d = os.path.join(HERE, "notes")
    for fn in sorted(os.listdir(d)):
        if fn.endswith(".py") and not fn.startswith("_"):
            spec = importlib.util.spec_from_file_location("notes_" + fn[:-3], os.path.join(d, fn))
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            out.update(mod.FILES)
    return out


# ------------------------------------------------------------------ who calls whom (function level)
def _aliases(tree):
    out = {}
    for n in ast.walk(tree):
        if isinstance(n, ast.Import):
            for a in n.names:
                out[a.asname or a.name.split(".")[0]] = a.name.split(".")[-1]
        elif isinstance(n, ast.ImportFrom) and n.module:
            for a in n.names:
                out[a.asname or a.name] = a.name if n.module in ("core", "api") else n.module.split(".")[-1]
    return out


def py_links(info):
    mods = {}
    for p, r in info.items():
        if r["lang"] == "python":
            m = os.path.splitext(os.path.basename(p))[0]
            test = "/tests" in p or "local_stub" in p
            if m not in mods or (not test and ("/tests" in mods[m] or "local_stub" in mods[m])):
                mods[m] = p
    keys = {(p, it["key"]) for p, r in info.items() for it in r["items"]}
    links = {}
    for p, r in info.items():
        if r["lang"] != "python" or not r["items"]:
            continue
        try:
            tree = ast.parse(r["_src"])
        except SyntaxError:
            continue
        al = _aliases(tree)
        nodes = {}
        for n in tree.body:
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
                nodes[n.name] = (n, None)
            elif isinstance(n, ast.ClassDef):
                for m in n.body:
                    if isinstance(m, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        nodes[f"{n.name}.{m.name}"] = (m, n.name)
        for key, (node, cls) in nodes.items():
            hits = []
            for x in ast.walk(node):
                tgt = None
                if isinstance(x, ast.Attribute) and isinstance(x.ctx, ast.Load) and isinstance(x.value, ast.Name):
                    v = x.value.id
                    if v in ("self", "cls") and cls:
                        tgt = (p, f"{cls}.{x.attr}")
                    elif v in al and al[v] in mods:
                        m = mods[al[v]]
                        # Graph.load where «Graph» is a CLASS imported by name → the method Graph.load
                        tgt = (m, f"{v}.{x.attr}") if (m, f"{v}.{x.attr}") in keys else (m, x.attr)
                    elif (p, f"{v}.{x.attr}") in keys:
                        tgt = (p, f"{v}.{x.attr}")
                elif isinstance(x, ast.Name) and isinstance(x.ctx, ast.Load):
                    nm = x.id
                    if nm == "cls" and cls:
                        tgt = (p, f"{cls}.__init__")
                    elif (p, nm) in keys:
                        tgt = (p, nm)
                    elif nm in al and al[nm] != nm and al[nm] in mods:
                        tgt = (mods[al[nm]], nm)
                if tgt and tgt in keys and tgt != (p, key) and tgt not in hits:
                    hits.append(tgt)
            links[(p, key)] = hits
    return links


def js_links(info):
    defs = {}
    for p, r in info.items():
        if r["lang"] == "js" and p.startswith(scan._SRC):
            for it in r["items"]:
                k = it["key"]
                if len(k) >= 4 and k not in JS_STOP:
                    defs.setdefault(k, (p, k))
    pat = {k: re.compile(r"(?<![\w$.])" + re.escape(k) + r"(?![\w$])") for k in defs}
    links = {}
    for p, r in info.items():
        if r["lang"] != "js":
            continue
        lines = r["_src"].split("\n")
        for it in r["items"]:
            if it["kind"] != "func":
                continue
            body = "\n".join(lines[it["start"] - 1:it["end"]])
            hits = []
            for k, tgt in defs.items():
                if tgt == (p, it["key"]) or k not in body:
                    continue
                m = pat[k].search(body)
                if m and not (tgt[0] == p and k == it["key"]):
                    hits.append(tgt)
            links[(p, it["key"])] = hits[:16]
    return links


def main():
    files, info = scan.scan()
    notes = load_notes()
    idx = {p: i for i, p in enumerate(files)}
    links = {**py_links(info), **js_links(info)}
    called_by = {}
    for src, tgts in links.items():
        for t in tgts:
            called_by.setdefault(t, []).append(src)
    fstep_of = {}
    for n, st in enumerate(FSTEPS, 1):
        if st.get("file") and st.get("func"):
            fstep_of[(st["file"], st["func"])] = n
    step_of = {p: n for n, (_, p, _, _) in enumerate(JOURNEY, 1)}
    missing_cards, missing_items = [], []
    out_files = []
    for p in files:
        r = info[p]
        src = r["_src"]
        rec = {"p": p, "lang": r["lang"], "lines": r["lines"], "uses": r["uses"], "used_by": r["used_by"], "step": step_of.get(p)}
        if r["generated"]:
            shown = src.split("\n")[:GEN_SHOWN]
            rec.update(code="\n".join(l[:GEN_COLS] + (" …" if len(l) > GEN_COLS else "") for l in shown), gen=r["generated"], truncated=True, shown=len(shown))
        else:
            rec["code"] = src.rstrip("\n")
        card = notes.get(p)
        if card:
            rec["card"] = {k: (ar(v) if isinstance(v, str) else [ar(x) if isinstance(x, str) else [ar(y) for y in x] for x in v])
                           for k, v in card.items() if k != "items"}
        else:
            missing_cards.append(p)
        texts = (card or {}).get("items", {})
        items = []
        for it in r["items"]:
            t = texts.get(it["key"], "")
            if not t and it["kind"] != "section":
                missing_items.append(f"{p}::{it['key']}")
            calls = [[idx[q], k] for q, k in links.get((p, it["key"]), []) if q in idx]
            by = [[idx[q], k] for q, k in called_by.get((p, it["key"]), []) if q in idx][:16]
            e = {"key": it["key"], "kind": it["kind"], "start": it["start"], "end": it["end"], "text": ar(t)}
            if calls:
                e["calls"] = calls
            if by:
                e["by"] = by
            if (p, it["key"]) in fstep_of:
                e["fstep"] = fstep_of[(p, it["key"])]
            items.append(e)
        rec["items"] = items
        out_files.append(rec)
    data = {
        "project": {k: ar(v) for k, v in PROJECT.items()},
        "folders": {k: ar(v) for k, v in FOLDERS.items()},
        "jphases": [{"id": a, "short": ar(b), "title": ar(c), "desc": ar(d)} for a, b, c, d in JPHASES],
        "journey": [{"n": n, "phase": ph, "p": p, "title": ar(t), "what": ar(w)} for n, (ph, p, t, w) in enumerate(JOURNEY, 1) if p in idx],
        "fphases": [{"id": a, "title": ar(b), "desc": ar(c)} for a, b, c in FPHASES],
        "fsteps": [{"n": n, "phase": st["phase"], "file": st.get("file"), "func": st.get("func"), "title": ar(st["title"]), "what": ar(st.get("what", "")),
                    "takes": [ar(x) for x in st.get("takes", [])], "does": [ar(x) for x in st.get("does", [])], "gives": ar(st.get("gives", "")),
                    "optional": bool(st.get("optional")), "note": ar(st.get("note", ""))} for n, st in enumerate(FSTEPS, 1)],
        "glossary": [[ar(a), ar(b)] for a, b in GLOSSARY],
        "files": out_files,
    }
    bad = [p for _, p, _, _ in JOURNEY if p not in idx]
    page = open(os.path.join(HERE, "explorer_template.html"), encoding="utf-8").read()
    js = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/").replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")
    out = page.replace("/*EXPLORER*/null", js, 1)
    with open(os.path.join(HERE, "PROJECT_EXPLORER.html"), "w", encoding="utf-8") as f:
        f.write(out)
    n_items = sum(len([i for i in f["items"] if i["kind"] != "section"]) for f in out_files)
    n_links = sum(len(i.get("calls", [])) for f in out_files for i in f["items"])
    print(f"PROJECT_EXPLORER.html: {len(files)} files · {n_items} functions/tables · {n_links} function links · {len(data['journey'])} journey steps · {len(out) // 1024} KB")
    print(f"  without a card: {len(missing_cards)} {missing_cards[:8]}")
    print(f"  functions without a line: {len(missing_items)} {missing_items[:8]}")
    if bad:
        print("  ⚠️ journey files that do not exist:", bad)


if __name__ == "__main__":
    main()
