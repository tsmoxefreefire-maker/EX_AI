"""📚 Sample books for every stage (grades 8 → 12), in the team's hierarchical format: Book → Unit → Topic → Lesson → Entity.
They are SAMPLES to test the age stages (the real graphs come from Omar Essam). The content is written carefully (Jordanian
curriculum style, simple Arabic); each meaning names what it builds on, so «لأنه…» sentences can come from the graph itself.

Run:  python sample_books.py        → writes <id>_book_graph.json next to this file (and nothing else)."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))

# id, title, subject, grade, unit, topic, lessons [(lesson_id, title, [(entity_id, name, meaning, minutes, difficulty)])], prerequisites [(a, b) = «b needs a»]
BOOKS = [
    ("sci_g8", "العلوم · الصف الثامن", "Science", 8, "الوحدة الأولى: الخلية", "تركيب الخلية", [
        ("l_cell_parts", "مكوّنات الخلية", [
            ("cell", "الخلية", "أصغر وحدة حيّة يتكوّن منها جسم الكائن الحي، وتقوم بجميع وظائف الحياة.", 5, "easy"),
            ("membrane", "الغشاء الخلوي", "غشاء رقيق يحيط بالخلية، ويتحكّم في دخول المواد إليها وخروجها منها.", 5, "easy"),
            ("cytoplasm", "السيتوبلازم", "سائل هلامي داخل الغشاء الخلوي، تسبح فيه مكوّنات الخلية وتحدث فيه كثير من التفاعلات.", 5, "medium"),
            ("nucleus", "النواة", "مركز التحكّم في الخلية، يحيط بها السيتوبلازم وتحتوي على المادة الوراثية.", 6, "medium"),
            ("mito", "الميتوكندريا", "عضيّة في السيتوبلازم تُطلق الطاقة من الغذاء لتستخدمها الخلية، وتُسمّى مصنع الطاقة.", 6, "medium")]),
        ("l_plant_animal", "الخلية النباتية والحيوانية", [
            ("cellwall", "الجدار الخلوي", "طبقة صلبة خارج الغشاء الخلوي في الخلية النباتية، تعطيها شكلها الثابت وتحميها.", 5, "easy"),
            ("chloroplast", "البلاستيدات الخضراء", "عضيّات خضراء في السيتوبلازم في الخلية النباتية، يحدث فيها البناء الضوئي لصنع الغذاء.", 6, "medium"),
            ("vacuole", "الفجوة العصارية", "كيس في السيتوبلازم يخزّن الماء والأملاح، ويكون كبيراً في الخلية النباتية.", 5, "easy"),
            ("photosynthesis", "البناء الضوئي", "عملية تصنع فيها البلاستيدات الخضراء الغذاء من الماء وثاني أكسيد الكربون بوجود ضوء الشمس.", 7, "hard")])],
     [("cell", "membrane"), ("membrane", "cytoplasm"), ("cytoplasm", "nucleus"), ("cytoplasm", "mito"), ("membrane", "cellwall"),
      ("cytoplasm", "chloroplast"), ("cytoplasm", "vacuole"), ("chloroplast", "photosynthesis")]),

    ("math_g9", "الرياضيات · الصف التاسع", "Mathematics", 9, "الوحدة الثالثة: الاقترانات والخط المستقيم", "التمثيل البياني", [
        ("l_plane", "المستوى الإحداثي والاقتران", [
            ("plane", "المستوى الإحداثي", "مستوى يتكوّن من محورين متعامدين: محور x الأفقي ومحور y الرأسي، يتقاطعان في نقطة الأصل (0, 0).", 5, "easy"),
            ("pair", "الزوج المرتب", "عددان (x, y) يحدّدان موقع نقطة في المستوى الإحداثي: الأول على محور x والثاني على محور y.", 5, "easy"),
            ("function", "الاقتران", "علاقة تربط كل عنصر من المجال بعنصر واحد فقط من المدى، ويُمثَّل بأزواج مرتبة.", 7, "medium")]),
        ("l_linear", "الاقتران الخطي", [
            ("slope", "الميل", "مقدار انحدار الخط المستقيم: التغيّر الرأسي مقسوماً على التغيّر الأفقي بين زوجين مرتبين عليه.", 7, "medium"),
            ("yint", "المقطع الصادي", "النقطة التي يقطع فيها الخط المستقيم محور y في المستوى الإحداثي، وتكون عندها x = 0.", 5, "easy"),
            ("lineq", "معادلة الخط المستقيم", "المعادلة y = mx + b، حيث m هو الميل و b هو المقطع الصادي.", 7, "medium"),
            ("linear", "الاقتران الخطي", "اقتران تمثيله البياني خط مستقيم، ويُكتب على صورة معادلة الخط المستقيم.", 6, "medium")])],
     [("plane", "pair"), ("pair", "function"), ("pair", "slope"), ("plane", "yint"), ("slope", "lineq"), ("yint", "lineq"),
      ("function", "linear"), ("lineq", "linear")]),

    ("phy_g10", "الفيزياء · الصف العاشر", "Physics", 10, "الوحدة الأولى: الحركة في بُعد واحد", "وصف الحركة", [
        ("l_position", "الموقع والإزاحة", [
            ("position", "الموقع", "مكان الجسم بالنسبة إلى نقطة إسناد على خط مستقيم، ويُقاس بالمتر.", 4, "easy"),
            ("distance", "المسافة", "طول المسار الكلي الذي يقطعه الجسم من موقع إلى آخر، وهي كمية قياسية.", 5, "easy"),
            ("displacement", "الإزاحة", "التغيّر في موقع الجسم من موقعه الابتدائي إلى موقعه النهائي، وهي كمية متجهة لها مقدار واتجاه.", 6, "medium"),
            ("time", "الزمن", "المدة التي تستغرقها الحركة، ويُقاس بالثانية.", 3, "easy")]),
        ("l_speed", "السرعة والتسارع", [
            ("speed", "السرعة المتوسطة", "المسافة الكلية مقسومة على الزمن الكلي، وتُقاس بوحدة متر لكل ثانية (م/ث).", 6, "medium"),
            ("velocity", "السرعة المتجهة", "الإزاحة مقسومة على الزمن، ولها مقدار واتجاه.", 6, "medium"),
            ("accel", "التسارع", "معدل تغيّر السرعة المتجهة مع الزمن، ويُقاس بوحدة م/ث².", 7, "hard"),
            ("freefall", "السقوط الحر", "حركة جسم تحت تأثير الجاذبية فقط، بتسارع ثابت مقداره 9.8 م/ث² تقريباً.", 7, "hard")])],
     [("position", "distance"), ("position", "displacement"), ("distance", "speed"), ("time", "speed"), ("displacement", "velocity"),
      ("time", "velocity"), ("velocity", "accel"), ("accel", "freefall")]),

    ("chem_g11", "الكيمياء · الصف الحادي عشر", "Chemistry", 11, "الوحدة الثانية: الروابط الكيميائية", "الذرة والروابط", [
        ("l_ions", "الإلكترونات والأيونات", [
            ("atom", "الذرة", "أصغر جزء من العنصر يحمل خصائصه، وتتكوّن من نواة موجبة تدور حولها الإلكترونات.", 5, "easy"),
            ("electron", "الإلكترونات", "جسيمات سالبة الشحنة تدور حول نواة الذرة في مستويات طاقة.", 5, "easy"),
            ("valence", "إلكترونات التكافؤ", "الإلكترونات الموجودة في مستوى الطاقة الخارجي للذرة، وهي التي تشارك في تكوين الروابط.", 6, "medium"),
            ("ion", "الأيون", "ذرة فقدت إلكترونات فأصبحت موجبة، أو كسبت إلكترونات فأصبحت سالبة.", 6, "medium")]),
        ("l_bonds", "أنواع الروابط", [
            ("ionic", "الرابطة الأيونية", "قوة تجاذب كهربائي بين أيون موجب وأيون سالب، تنتج عن انتقال إلكترونات التكافؤ من ذرة إلى أخرى.", 7, "medium"),
            ("covalent", "الرابطة التساهمية", "رابطة تنشأ عندما تتشارك ذرتان بزوج أو أكثر من إلكترونات التكافؤ.", 7, "medium"),
            ("ionic_compound", "المركب الأيوني", "مادة صلبة تتكوّن من أيونات موجبة وسالبة مترابطة بالرابطة الأيونية، مثل ملح الطعام.", 6, "medium"),
            ("molecule", "الجزيء", "مجموعة ذرات مترابطة بالرابطة التساهمية، مثل جزيء الماء.", 6, "medium")])],
     [("atom", "electron"), ("electron", "valence"), ("valence", "ion"), ("ion", "ionic"), ("valence", "covalent"),
      ("ionic", "ionic_compound"), ("covalent", "molecule")]),

    ("bio_g12", "الأحياء · الصف الثاني عشر", "Biology", 12, "الوحدة الثالثة: الوراثة", "الوراثة الجزيئية والمندلية", [
        ("l_material", "المادة الوراثية", [
            ("dna", "الحمض النووي (DNA)", "جزيء طويل على شكل سلّم ملتف يحمل المعلومات الوراثية للكائن الحي.", 6, "medium"),
            ("gene", "الجين", "جزء محدد من الحمض النووي DNA يحمل المعلومات اللازمة لصفة معيّنة.", 6, "medium"),
            ("chromosome", "الكروموسوم", "تركيب في نواة الخلية يتكوّن من الحمض النووي DNA ملتفاً حول بروتينات، ويحمل الجينات.", 6, "medium"),
            ("allele", "الأليل", "شكل من أشكال الجين نفسه، ولكل صفة أليلان: واحد من كل أب.", 6, "medium")]),
        ("l_traits", "انتقال الصفات", [
            ("dominant", "الصفة السائدة", "صفة تظهر إذا وُجد أليلها مرة واحدة على الأقل، ويُرمز له بحرف كبير مثل A.", 5, "medium"),
            ("recessive", "الصفة المتنحية", "صفة لا تظهر إلا إذا وُجد أليلها مرتين، ويُرمز له بحرف صغير مثل a.", 5, "medium"),
            ("genotype", "الطراز الجيني", "زوج الأليلات الذي يحمله الفرد لصفة ما، مثل AA أو Aa أو aa.", 6, "hard"),
            ("punnett", "مربع بانيت", "جدول يُستخدم لتوقّع احتمالات الطرز الجينية للأبناء من أليلات الأبوين.", 7, "hard")])],
     [("dna", "gene"), ("dna", "chromosome"), ("gene", "allele"), ("allele", "dominant"), ("allele", "recessive"),
      ("dominant", "genotype"), ("recessive", "genotype"), ("genotype", "punnett")]),
]


def build(spec) -> dict:
    """One book in the hierarchical format (the same shape as plants_book_graph.json)."""
    bid, title, subject, grade, unit, topic, lessons, prereqs = spec
    u, t = f"{bid}_u", f"{bid}_t"
    nodes = [{"id": u, "book_id": bid, "title": unit, "learning_objective": f"يتعرّف الطالب على {topic}.", "level": "unit"},
             {"id": t, "book_id": bid, "title": topic, "learning_objective": f"يفهم الطالب {topic} والعلاقات بين مفاهيمه.", "level": "topic"}]
    rels = [{"id": f"{bid}_r_t", "source_node_id": t, "target_node_id": u, "type": "subsetOf", "weight": 1.0}]
    meta, content = [], []
    for lid, ltitle, ents in lessons:
        nodes.append({"id": lid, "book_id": bid, "title": ltitle, "learning_objective": f"يتعرّف الطالب على {ltitle}.", "level": "lesson"})
        rels.append({"id": f"{bid}_r_{lid}", "source_node_id": lid, "target_node_id": t, "type": "subsetOf", "weight": 1.0})
        for eid, name, meaning, minutes, diff in ents:
            nodes.append({"id": eid, "book_id": bid, "title": name, "learning_objective": meaning, "level": "entity"})
            rels.append({"id": f"{bid}_r_{eid}", "source_node_id": eid, "target_node_id": lid, "type": "subsetOf", "weight": 1.0})
            meta.append({"node_id": eid, "difficulty": diff, "estimated_minutes": minutes, "importance": 0.8})
            content.append({"node_id": eid, "content_type": "text", "content_url": None, "content_text": meaning})
    for i, (a, b) in enumerate(prereqs):
        rels.append({"id": f"{bid}_p{i}", "source_node_id": a, "target_node_id": b, "type": "prerequisiteOf", "weight": 1.0})
    return {"book": {"id": bid, "title": title, "subject": subject, "grade": grade}, "nodes": nodes, "relationships": rels,
            "node_metadata": meta, "node_content": content}


if __name__ == "__main__":
    for spec in BOOKS:
        path = os.path.join(HERE, f"{spec[0]}_book_graph.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(build(spec), f, ensure_ascii=False, indent=1)
        print("wrote", os.path.basename(path))
