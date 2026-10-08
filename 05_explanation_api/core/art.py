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
