"""
FastAPI application entrypoint.

Run with:
    uvicorn app.main:app --reload

Routes are mounted under /api so the frontend's Vite dev proxy (see
frontend/vite.config.js) and any production reverse proxy can forward a
single /api prefix straight to this service.
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import complaints, health, ai
from app.core.config import get_settings
from app.db.session import init_db
from app.models import complaint, audit

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database tables
    init_db()
    yield


app = FastAPI(
    title=settings.APP_NAME,
    version="0.1.0",
    description=(
        "Phase 2 API for the AI-Powered Customer Complaint "
        "Management System. Complaint data is served from PostgreSQL; "
        "the AI Co-Pilot endpoints will be added in a later phase."
    ),
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_ORIGIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api")
app.include_router(complaints.router, prefix="/api")
app.include_router(ai.router, prefix="/api")


@app.get("/")
def root():
    return {"message": "PharmaQMS API is running. See /docs for the interactive API reference."}
