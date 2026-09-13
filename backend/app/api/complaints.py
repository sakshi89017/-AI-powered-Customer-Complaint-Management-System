"""
Complaint endpoints.

Phase 2: backed by PostgreSQL database via complaint_service.py.
"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import OperationalError

from app.db.session import get_db
from app.schemas.complaint import ComplaintCreate, ComplaintUpdate, ComplaintResponse, DashboardStatsResponse
from app.services import complaint_service

router = APIRouter(prefix="/complaints", tags=["complaints"])


@router.get("/stats", response_model=DashboardStatsResponse)
def get_dashboard_stats(db: Session = Depends(get_db)):
    """Retrieve real-time aggregated dashboard metrics."""
    try:
        return complaint_service.get_dashboard_stats(db)
    except OperationalError:
        raise HTTPException(status_code=503, detail="Database connection unavailable. Please ensure PostgreSQL is running.")


@router.get("", response_model=list[ComplaintResponse])
def list_complaints(
    search: Optional[str] = None,
    severity: Optional[str] = None,
    priority: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Retrieve a list of complaints with optional search and filtering."""
    try:
        return complaint_service.get_complaints(db, search, severity, priority, status)
    except OperationalError:
        raise HTTPException(status_code=503, detail="Database connection unavailable. Please ensure PostgreSQL is running.")


@router.post("", response_model=ComplaintResponse, status_code=201)
def create_complaint(payload: ComplaintCreate, db: Session = Depends(get_db)):
    """Register a new customer complaint."""
    try:
        return complaint_service.create_complaint(db, payload)
    except OperationalError:
        raise HTTPException(status_code=503, detail="Database connection unavailable. Please ensure PostgreSQL is running.")


@router.get("/{complaint_id}", response_model=ComplaintResponse)
def get_complaint(complaint_id: str, db: Session = Depends(get_db)):
    """Retrieve a single complaint by its unique identifier."""
    try:
        record = complaint_service.get_complaint_by_id(db, complaint_id)
        if record is None:
            raise HTTPException(status_code=404, detail="Complaint not found")
        return record
    except OperationalError:
        raise HTTPException(status_code=503, detail="Database connection unavailable. Please ensure PostgreSQL is running.")


@router.patch("/{complaint_id}", response_model=ComplaintResponse)
def update_complaint(complaint_id: str, payload: ComplaintUpdate, db: Session = Depends(get_db)):
    """Partially update an existing complaint (e.g. status change, adding recommended actions)."""
    try:
        record = complaint_service.update_complaint(db, complaint_id, payload)
        if record is None:
            raise HTTPException(status_code=404, detail="Complaint not found")
        return record
    except OperationalError:
        raise HTTPException(status_code=503, detail="Database connection unavailable. Please ensure PostgreSQL is running.")


@router.delete("/{complaint_id}", status_code=204)
def delete_complaint(complaint_id: str, db: Session = Depends(get_db)):
    """Delete a complaint from the database."""
    try:
        success = complaint_service.delete_complaint(db, complaint_id)
        if not success:
            raise HTTPException(status_code=404, detail="Complaint not found")
    except OperationalError:
        raise HTTPException(status_code=503, detail="Database connection unavailable. Please ensure PostgreSQL is running.")

from app.schemas.complaint import ComplaintEventResponse

@router.get("/{complaint_id}/audit", response_model=list[ComplaintEventResponse])
def get_complaint_audit(complaint_id: str, db: Session = Depends(get_db)):
    """Retrieve the audit trail for a single complaint."""
    try:
        return complaint_service.get_audit_trail(db, complaint_id)
    except OperationalError:
        raise HTTPException(status_code=503, detail="Database connection unavailable. Please ensure PostgreSQL is running.")
