import inspect, json, re, urllib.parse
from fastapi import HTTPException
from fastapi.responses import Response
from pydantic import BaseModel
class _R:
    def __init__(self, code, body, headers=None): self.status_code, self._b, self.headers = code, body, headers or {}
    def json(self): return json.loads(self._b)
    @property
    def text(self): return self._b
class TestClient:
    def __init__(self, app): self.app = app
    def _go(self, m, url, params=None, body=None):
        u = urllib.parse.urlsplit(url); q = dict(urllib.parse.parse_qsl(u.query)); q.update(params or {})
        for meth, path, fn in self.app.routes:
            if meth != m: continue
            rx = "^" + re.sub(r"\\\{(\w+)\\\}", r"(?P<\1>[^/]+?)", re.escape(path)) + "$"
            mm = re.match(rx, u.path)
            if not mm: continue
            kw = {k: urllib.parse.unquote(v) for k, v in mm.groupdict().items()}
            for name, p in inspect.signature(fn).parameters.items():
                if name in kw: continue
                if isinstance(p.annotation, type) and issubclass(p.annotation, BaseModel): kw[name] = p.annotation(**(body or {}))
                elif name in q: kw[name] = q[name]
            try: out = fn(**kw)
            except HTTPException as e: return _R(e.status_code, json.dumps({"detail": e.detail}, ensure_ascii=False))
            if isinstance(out, Response): return _R(out.status_code, out.content or "", dict(out.headers, **({"content-type": out.media_type} if out.media_type else {})))
            if isinstance(out, BaseModel): out = out.model_dump()
            return _R(200, json.dumps(out, ensure_ascii=False))
        return _R(404, json.dumps({"detail": "Not Found"}))
    def get(self, url, params=None): return self._go("GET", url, params)
    def post(self, url, json=None, params=None): return self._go("POST", url, params, body=json)
    def delete(self, url): return self._go("DELETE", url)
