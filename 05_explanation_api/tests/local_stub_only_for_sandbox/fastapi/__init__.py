"""LOCAL STUB of FastAPI (routing + TestClient only) to run the API tests here — NOT shipped. The real thing: pip install fastapi."""
class HTTPException(Exception):
    def __init__(self, status_code, detail=None): self.status_code, self.detail = status_code, detail
def Query(default=None, **kw): return default
class APIRouter:
    def __init__(self): self.routes = []
    def _add(self, m, path, **kw):
        def deco(fn): self.routes.append((m, path, fn)); return fn
        return deco
    def get(self, path, **kw): return self._add("GET", path, **kw)
    def post(self, path, **kw): return self._add("POST", path, **kw)
    def delete(self, path, **kw): return self._add("DELETE", path, **kw)
class FastAPI(APIRouter):
    def __init__(self, **kw): super().__init__(); self.meta = kw
    def add_middleware(self, *a, **k): pass
    def include_router(self, r): self.routes += r.routes
