"""The door of the service: creates the FastAPI app and plugs in the endpoints.
Run:  uvicorn main:app --reload  → open http://127.0.0.1:8000/  (the books + send a graph) · /explain (the page) · /docs (every endpoint)"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import router
from core import settings

app = FastAPI(title="Interactive Explanation API · الشرح التفاعلي", version=settings.API_VERSION,
              description="بياخد أي جراف وبيعمل الشرح التفاعلي كامل: الصفحة نفسها (/explain) بكل التفاعلات والأصوات، "
                          "والداتا (JSON) ورسومات الشخصيات (SVG) لأي فرونت إند. المادة الجديدة بتاخد هوية خاصة فيها (صوت وشخصيات).")
app.add_middleware(CORSMiddleware, allow_origins=settings.CORS_ORIGINS, allow_methods=["*"], allow_headers=["*"])
app.include_router(router)
