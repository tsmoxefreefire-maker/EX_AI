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
