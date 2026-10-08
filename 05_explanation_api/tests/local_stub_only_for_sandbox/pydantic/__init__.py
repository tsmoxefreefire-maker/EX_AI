"""LOCAL STUB of pydantic (only to run the API tests in a sandbox without internet) — NOT shipped."""
class _F:
    def __init__(self, default=None, **kw): self.default = default
def Field(default=None, **kw): return _F(default, **kw)
class BaseModel:
    def __init__(self, **kw):
        for k in getattr(self.__class__, "__annotations__", {}):
            d = getattr(self.__class__, k, None); d = d.default if isinstance(d, _F) else d
            setattr(self, k, kw.get(k, d))
    def model_dump(self): return {k: getattr(self, k) for k in self.__class__.__annotations__}
