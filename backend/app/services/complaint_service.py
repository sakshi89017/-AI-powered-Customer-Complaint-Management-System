"""
Complaint Database Service / Repository Layer.

Handles all persistence and querying against the PostgreSQL database.
Isolated from HTTP routing so future AI agent tools (e.g., LangGraph tools)
can call these functions directly.
"""
from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from app.models.complaint import Complaint, PriorityEnum, SeverityEnum, StatusEnum
from app.schemas.complaint import ComplaintCreate, ComplaintUpdate


def create_complaint(db: Session, complaint_in: ComplaintCreate) -> Complaint:
    """Create a new complaint record in the database."""
    complaint_data = complaint_in.model_dump(exclude_unset=True)
    db_complaint = Complaint(**complaint_data)
    db.add(db_complaint)
    db.commit()
    db.refresh(db_complaint)
    return db_complaint


def get_complaints(
    db: Session,
    search: Optional[str] = None,
    severity: Optional[str] = None,
    priority: Optional[str] = None,
    status: Optional[str] = None,
) -> list[Complaint]:
    """
    Retrieve complaints matching optional search term (across ID, customer, product, batch)
    and optional filters (severity, priority, status).
    """
    query = db.query(Complaint)

    if search and search.strip():
        term = f"%{search.strip()}%"
        query = query.filter(
            or_(
                Complaint.id.ilike(term),
                Complaint.customer_name.ilike(term),
                Complaint.product_name.ilike(term),
                Complaint.batch_number.ilike(term),
            )
        )

    if severity and severity.strip() and severity.strip() != "All":
        query = query.filter(Complaint.severity == severity.strip())

    if priority and priority.strip() and priority.strip() != "All":
        query = query.filter(Complaint.priority == priority.strip())

    if status and status.strip() and status.strip() != "All":
        query = query.filter(Complaint.status == status.strip())

    return query.order_by(Complaint.created_at.desc()).all()


def get_complaint_by_id(db: Session, complaint_id: str) -> Optional[Complaint]:
    """Retrieve a single complaint by its unique identifier."""
    return db.query(Complaint).filter(Complaint.id == complaint_id).first()


def update_complaint(
    db: Session,
    complaint_id: str,
    complaint_in: ComplaintUpdate,
) -> Optional[Complaint]:
    """
    Partially update an existing complaint.
    Only fields explicitly provided in complaint_in will be updated;
    all other fields remain untouched.
    """
    db_complaint = get_complaint_by_id(db, complaint_id)
    if not db_complaint:
        return None

    update_data = complaint_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if value is not None:
            setattr(db_complaint, field, value)

    db_complaint.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(db_complaint)
    return db_complaint


def delete_complaint(db: Session, complaint_id: str) -> bool:
    """Delete a complaint record by ID."""
    db_complaint = get_complaint_by_id(db, complaint_id)
    if not db_complaint:
        return False

    db.delete(db_complaint)
    db.commit()
    return True


def get_dashboard_stats(db: Session) -> dict:
    """
    Calculate dynamic dashboard metrics aggregated directly from PostgreSQL:
    - Total Complaints
    - Status breakdown (Pending Triage, Under Investigation, QA Review, Action Required, Closed)
    - Critical Complaints
    - High Priority
    """
    total_complaints = db.query(func.count(Complaint.id)).scalar() or 0

    pending_triage = (
        db.query(func.count(Complaint.id))
        .filter(Complaint.status == StatusEnum.PENDING_TRIAGE.value)
        .scalar()
        or 0
    )
    under_investigation = (
        db.query(func.count(Complaint.id))
        .filter(Complaint.status == StatusEnum.UNDER_INVESTIGATION.value)
        .scalar()
        or 0
    )
    qa_review = (
        db.query(func.count(Complaint.id))
        .filter(Complaint.status == StatusEnum.QA_REVIEW.value)
        .scalar()
        or 0
    )
    action_required = (
        db.query(func.count(Complaint.id))
        .filter(Complaint.status == StatusEnum.ACTION_REQUIRED.value)
        .scalar()
        or 0
    )
    closed = (
        db.query(func.count(Complaint.id))
        .filter(Complaint.status == StatusEnum.CLOSED.value)
        .scalar()
        or 0
    )

    critical_complaints = (
        db.query(func.count(Complaint.id))
        .filter(Complaint.severity == SeverityEnum.CRITICAL.value)
        .scalar()
        or 0
    )
    high_priority = (
        db.query(func.count(Complaint.id))
        .filter(Complaint.priority.in_([PriorityEnum.HIGH.value, PriorityEnum.URGENT.value]))
        .scalar()
        or 0
    )

    return {
        "total_complaints": total_complaints,
        "pending_triage": pending_triage,
        "under_investigation": under_investigation,
        "qa_review": qa_review,
        "action_required": action_required,
        "closed": closed,
        "critical_complaints": critical_complaints,
        "high_priority": high_priority,
    }

from app.models.audit import ComplaintEvent

def get_audit_trail(db: Session, complaint_id: str) -> list[ComplaintEvent]:
    """Retrieve the audit trail events for a specific complaint."""
    return db.query(ComplaintEvent).filter(ComplaintEvent.complaint_id == complaint_id).order_by(ComplaintEvent.timestamp.desc()).all()
