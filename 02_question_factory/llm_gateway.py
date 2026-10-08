"""The team's LLM gateway: ONE function, generate(system, user) -> text, with a back-up chain for availability.

Order (default): Google Gemini → OpenAI (GPT) → Anthropic (Claude). If one fails (no credit, busy, model gone, no key),
the next one answers. Keys and order live in ONE small text file next to this code: api_key.txt

    gemini: AIza...          ← Google AI Studio (has a free tier)
    openai: sk-...           ← OpenAI platform
    claude: sk-ant-...       ← Anthropic console
    order: gemini, openai, claude

Only the Python standard library is used (no installs). Model names change often, so each provider tries a short list.
"""
import json
import os
import re
import urllib.error
import urllib.request

PROJECT_KEY_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "api_key.txt")
KEY_FILE = os.path.join(os.path.expanduser("~"), "anthropic_key.txt")      # old place, still read
TIMEOUT_SECONDS = 120
MAX_TOKENS = 8000
DEFAULT_ORDER = ["gemini", "openai", "claude"]
MODELS = {
    "gemini": ["gemini-3.8-flash", "gemini-3.5-flash", "gemini-3-flash-preview"],   # used only if api_key.txt has no «gemini_models:»
    "openai": ["gpt-4.1-mini", "gpt-4o-mini", "gpt-5-mini"],
    "claude": ["claude-haiku-4-5-20251001", "claude-sonnet-5-5"],
}
LAST_PROVIDER = None            # which one answered last (shown on the screen)
API_URL = "https://api.anthropic.com/v1/messages"
API_VERSION = "2023-06-01"


class LLMError(RuntimeError):
    pass


# ---------- keys ----------
def _guess(line: str):
    """A bare key without «name:» — recognise it by its shape."""
    if line.startswith("sk-ant-"): return "claude"
    if line.startswith("AIza"): return "gemini"
    if line.startswith("sk-"): return "openai"
    return None


def read_settings(path: str = None) -> dict:
    keys, order, models = {}, list(DEFAULT_ORDER), {}
    for p in [path or PROJECT_KEY_FILE, KEY_FILE]:
        if not os.path.exists(p):
            continue
        with open(p, encoding="utf-8") as f:
            for raw in f:
                line = raw.strip()
                if not line or line.startswith("#"):
                    continue
                name, _, value = line.partition(":")
                name, value = name.strip().lower(), value.strip()
                if name == "order" and value:
                    order = [x.strip().lower() for x in value.split(",") if x.strip()]
                elif name in ("gemini_models", "openai_models", "claude_models") and value:
                    models.setdefault(name.split("_")[0], [x.strip() for x in value.split(",") if x.strip()])
                elif name in ("gemini", "openai", "claude") and value:
                    keys.setdefault(name, value)
                elif _guess(line):
                    keys.setdefault(_guess(line), line)
    if os.environ.get("ANTHROPIC_API_KEY", "").strip(): keys["claude"] = os.environ["ANTHROPIC_API_KEY"].strip()
    if os.environ.get("GEMINI_API_KEY", "").strip(): keys["gemini"] = os.environ["GEMINI_API_KEY"].strip()
    if os.environ.get("OPENAI_API_KEY", "").strip(): keys["openai"] = os.environ["OPENAI_API_KEY"].strip()
    return {"keys": keys, "order": order, "models": {p: models.get(p) or list(MODELS[p]) for p in MODELS}}


def api_key_from_anywhere() -> str:
    """Any key at all? (used to tell the student early when there is none)."""
    k = read_settings()["keys"]
    return next(iter(k.values()), "")


# ---------- the three providers (request + how to read the answer) ----------
def build_request(system: str, user: str, api_key: str, model: str) -> urllib.request.Request:      # Claude (kept for old tests)
    body = {"model": model, "max_tokens": MAX_TOKENS, "system": system, "messages": [{"role": "user", "content": user}]}
    return urllib.request.Request(API_URL, data=json.dumps(body).encode("utf-8"), method="POST",
                                  headers={"x-api-key": api_key, "anthropic-version": API_VERSION, "content-type": "application/json"})


def _gemini_request(system, user, key, model):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
    body = {"systemInstruction": {"parts": [{"text": system}]}, "contents": [{"role": "user", "parts": [{"text": user}]}],
            "generationConfig": {"maxOutputTokens": MAX_TOKENS}}
    return urllib.request.Request(url, data=json.dumps(body).encode("utf-8"), method="POST",
                                  headers={"x-goog-api-key": key, "content-type": "application/json"})


def _openai_request(system, user, key, model):
    body = {"model": model, "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}]}
    return urllib.request.Request("https://api.openai.com/v1/chat/completions", data=json.dumps(body).encode("utf-8"), method="POST",
                                  headers={"authorization": f"Bearer {key}", "content-type": "application/json"})


def _read(provider, data):
    if provider == "gemini":
        parts = ((data.get("candidates") or [{}])[0].get("content") or {}).get("parts") or []
        return "".join(p.get("text", "") for p in parts)
    if provider == "openai":
        return (((data.get("choices") or [{}])[0].get("message") or {}).get("content")) or ""
    return "".join(b.get("text", "") for b in data.get("content", []) if b.get("type") == "text")


REQUEST = {"gemini": _gemini_request, "openai": _openai_request, "claude": build_request}


def _model_gone(code: int, text: str) -> bool:
    t = text.lower()
    return code == 404 or ("model" in t and ("not found" in t or "does not exist" in t or "not supported" in t or "unknown" in t))


def _busy(code: int, text: str) -> bool:
    """Temporary: the model is crowded / overloaded / rate-limited for a moment → wait a little, try again, then another version."""
    t = text.lower()
    if any(w in t for w in ("credit", "billing", "insufficient_quota", "no credits", "balance")):
        return False                                   # money, not crowd: go to the next provider
    return code in (500, 502, 503, 504, 529) or (code == 429 and any(w in t for w in ("rate", "resource_exhausted", "too many", "overloaded", "demand")))


RETRIES = 2              # tries per model when it is busy
WAIT_SECONDS = 3         # first wait; doubles each time


def generate(system: str, user: str, opener=urllib.request.urlopen, sleep=None) -> str:
    """Ask the first provider that has a key. Crowded? wait and retry, then another version of the SAME provider.
    No credit / bad key? the next provider. Raises LLMError with every reason if all fail."""
    import time
    sleep = sleep or time.sleep
    global LAST_PROVIDER
    s = read_settings()
    tried = []
    for provider in s["order"]:
        key = s["keys"].get(provider)
        if not key:
            continue
        queue = list(s["models"].get(provider, []))
        while queue:
            model = queue.pop(0)
            next_provider = False
            for attempt in range(RETRIES + 1):
                try:
                    with opener(REQUEST[provider](system, user, key, model), timeout=TIMEOUT_SECONDS) as resp:
                        text = _read(provider, json.loads(resp.read().decode("utf-8")))
                    if text:
                        LAST_PROVIDER = f"{provider} ({model})"
                        return text
                    tried.append(f"{provider}/{model}: empty answer")
                    break
                except urllib.error.HTTPError as e:
                    msg = e.read().decode("utf-8", "ignore")[:220]
                    if _busy(e.code, msg) and attempt < RETRIES:
                        sleep(WAIT_SECONDS * (2 ** attempt))      # crowded for a moment: wait, then try again
                        continue
                    tried.append(f"{provider}/{model}: {e.code} {' '.join(msg.split())[:160]}")
                    hint = re.search(r"use models/([A-Za-z0-9._\-]+)", msg)              # Google says which name to use → try it next
                    if hint and hint.group(1) not in queue and hint.group(1) != model:
                        queue.insert(0, hint.group(1))
                    per_model_quota = provider == "gemini" and e.code == 429      # Google counts the free quota PER MODEL → try another version first
                    if not (_busy(e.code, msg) or _model_gone(e.code, msg) or per_model_quota):
                        next_provider = True             # no credit / bad key → the next provider
                    break                                # still busy or name gone → another version of the same provider
                except urllib.error.URLError as e:
                    tried.append(f"{provider}: cannot reach ({e.reason})")
                    next_provider = True
                    break
            if next_provider:
                break
    if not tried:
        raise LLMError(f"no API key: paste one in {PROJECT_KEY_FILE} (gemini: … / openai: … / claude: …)")
    raise LLMError("all models failed → " + " | ".join(tried))
