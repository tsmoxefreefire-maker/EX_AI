class Response:
    def __init__(self, content=None, media_type=None, headers=None, status_code=200): self.content, self.media_type, self.headers, self.status_code = content, media_type, headers or {}, status_code
class RedirectResponse(Response):
    def __init__(self, url): super().__init__(None, None, {"location": url}, 307)
class HTMLResponse(Response):
    def __init__(self, content=None, headers=None, status_code=200): super().__init__(content, "text/html", headers, status_code)
