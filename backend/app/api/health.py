"""GET /api/health -- simple liveness check for the frontend to verify connectivity."""
from datetime import datetime

from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "PharmaQMS Complaint Management API",
        "timestamp": datetime.utcnow().isoformat(),
    }
