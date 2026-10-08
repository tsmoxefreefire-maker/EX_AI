"""🎵 The sounds (batch 26), measured — not by ear (that needs a person), but by numbers:
  · every event renders OFFLINE (no speakers) for every stage × subject: no clipping (peak < 1), and it is a real sound (or silent where it should be);
  · the stages: kids louder than junior, junior than teen, teen than senior; 🆕 batch 29: EVERY stage sounds on every event and on
    hover, each in its own way (the senior one octave lower: a «big», calm sound);
  · the subjects sound different: each instrument has its own «fingerprint» (brightness + length);
  · never the same note twice in a row (30 taps in a row); right moves in a row climb up; each character has its own voice.
    python tests_browser/test_sounds.py"""
import pathlib
import sys
from itertools import combinations

from playwright.sync_api import sync_playwright

PAGE = pathlib.Path(__file__).resolve().parent.parent / "player" / "explain.html"
SUBJECTS = ["science", "math", "physics", "chemistry", "geography", "history", "language", "general"]
STAGES = ["kids", "junior", "teen", "senior"]
EVENTS = ["pick", "place", "nope", "ready", "flip", "on", "connect", "rung", "hover"]
fails, oks = [], []


def ok(c, what):
    (oks if c else fails).append(what)
    if not c:
        print("❌", what)


with sync_playwright() as p:
    b = p.chromium.launch(args=["--autoplay-policy=no-user-gesture-required"])
    pg = b.new_page(); errs = []; pg.on("pageerror", lambda e: errs.append(str(e)[:200])); pg.route("**/fonts.*/**", lambda r: r.abort())
    pg.goto(PAGE.as_uri()); pg.wait_for_timeout(400)
    has = pg.evaluate("typeof window.__SOUND")
    ok(has == "object", "the page exposes the sound engine for tests (window.__SOUND)")
    R = {}
    for st in STAGES:
        for sub in SUBJECTS:
            for ev in EVENTS:
                R[(st, sub, ev)] = pg.evaluate("([e,st,sub])=>window.__SOUND.render(e,st,sub,{n:1,id:'root'})", [ev, st, sub])
    clip = [k for k, v in R.items() if v["peak"] >= 0.99]
    ok(not clip, f"no clipping in {len(R)} sounds (peak < 1) {clip[:3]}")
    silent_ok = set()                                               # 🆕 batch 29: no stage is silent any more
    for (st, sub, ev), v in R.items():
        if (st, ev) in silent_ok:
            ok(v["rms"] < 1e-5, f"{st}/{sub}/{ev}: silent as it should be")
        else:
            ok(v["rms"] > 1e-4 and v["secs"] > 0.05, f"{st}/{sub}/{ev}: a real sound")
    for sub in SUBJECTS:
        for ev in ("place", "ready", "pick"):
            r = [R[(st, sub, ev)]["loud"] for st in STAGES]                      # the energy in the same 2.6 s window (fair for a tick and a tune)
            ok(r[0] > r[1] > r[2] > r[3], f"{sub}/{ev}: louder for the little ones, quieter for the big ones {[round(x, 4) for x in r]}")
    # the subjects: a fingerprint per instrument (the same fixed note: «on» n=0), averaged over 3 renders (tiny random detune)
    fp = {}
    for sub in SUBJECTS:                                            # the same event, the same place in the scale: only the instrument + key change
        xs = [pg.evaluate("([sub])=>window.__SOUND.render('on','junior',sub,{n:0})", [sub]) for _ in range(3)]
        fp[sub] = {k: sum(x[k] for x in xs) / 3 for k in ("pitch", "bright", "secs")}
    diff = lambda a, b, k: abs(fp[a][k] - fp[b][k]) / max(fp[a][k], fp[b][k], 1e-9)
    close = [(a, b) for a, b in combinations(SUBJECTS, 2) if diff(a, b, "pitch") < 0.03 and diff(a, b, "bright") < 0.10 and diff(a, b, "secs") < 0.15]
    ok(not close, f"every subject has its own sound (key / brightness / length) {close}")
    print("   fingerprints:", {k: (round(v['pitch']), round(v['bright']), round(v['secs'], 2)) for k, v in fp.items()})
    # never the same note twice in a row · a streak climbs · each character its own voice
    seq = pg.evaluate("""async()=>{const S=window.__SOUND;S.log.length=0;S._force({stage:'kids',subject:'science'});const out=[];
        for(let i=0;i<30;i++){const n=S.log.length;S.play('pick');out.push(S.log[n]);await new Promise(r=>setTimeout(r,70));}return out;}""")
    ok(all(a != b for a, b in zip(seq, seq[1:])) and None not in seq, f"30 taps: never the same note twice in a row ({len(set(seq))} different notes)")
    climb = pg.evaluate("""async()=>{const S=window.__SOUND;S.log.length=0;S._force({stage:'teen',subject:'math'});const first=[];
        for(let i=0;i<5;i++){const n=S.log.length;S.play('place');first.push(S.log[n]);await new Promise(r=>setTimeout(r,120));}return first;}""")
    ok(climb[-1] > climb[0], f"right answers in a row climb up the scale {climb}")
    voices = pg.evaluate("""()=>{const S=window.__SOUND;S.log.length=0;S._force({stage:'junior',subject:'science'});const v={};
        for(const id of ['root','leaf','stem','water','soil']){const n=S.log.length;S.hover(id);v[id]=[S.log[n],S.voiceOf(id)];}return v;}""")
    same = all((voices[a][0] == voices[b][0]) == (voices[a][1] == voices[b][1]) for a, b in combinations(voices, 2))
    ok(same and len({v[1] for v in voices.values()}) >= 3, f"each character has its own voice (its pitch comes from its name) {voices}")
    hov = pg.evaluate("""()=>{const S=window.__SOUND;const o={};for(const st of ['kids','junior','teen','senior']){S.log.length=0;S._force({stage:st,subject:'science'});
        S.hover('root');o[st]=S.log.slice();}S._force(null);return o;}""")
    ok(all(hov[st] for st in hov), f"🆕 every stage makes a sound when the mouse is on a character {hov}")
    ok(len(hov["kids"]) > len(hov["teen"]) > len(hov["senior"]) >= 1, f"each stage its own hover: a giggle · «همم؟» · two notes · one note {[len(v) for v in hov.values()]}")
    ok(max(hov["senior"]) < min(hov["kids"]) and max(hov["senior"]) < max(hov["teen"]), f"the senior's sound is deeper (a «big» sound) {hov['senior']} < {hov['kids']}")
    for ev in ("flip", "step", "sparkle", "bloom"):
        v = pg.evaluate("([e])=>window.__SOUND.render(e,'senior','physics',{n:1})", [ev])
        ok(v["rms"] > 1e-4, f"🆕 senior/{ev}: a real sound now (it used to be silent)")
    ok(not errs, f"JS errors: {errs[:2]}")
    b.close()
print(f"✅ {len(oks)} sound checks passed · ❌ {len(fails)} failed")
sys.exit(1 if fails else 0)
