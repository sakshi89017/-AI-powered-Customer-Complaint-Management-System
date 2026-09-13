"""
SQLAlchemy database model for Customer Complaints in PharmaQMS.
"""
import enum
import secrets
from sqlalchemy import Column, DateTime, String, Text, func

from app.db.base import Base


class SeverityEnum(str, enum.Enum):
    MINOR = "Minor"
    MAJOR = "Major"
    CRITICAL = "Critical"


class PriorityEnum(str, enum.Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    URGENT = "Urgent"


class StatusEnum(str, enum.Enum):
    PENDING_TRIAGE = "Pending Triage"
    UNDER_INVESTIGATION = "Under Investigation"
    QA_REVIEW = "QA Review"
    ACTION_REQUIRED = "Action Required"
    CLOSED = "Closed"


def generate_complaint_id() -> str:
    """Generate a pharmaceutical industry standard complaint identifier (e.g. CC-49210)."""
    random_num = secrets.randbelow(90000) + 10000
    return f"CC-{random_num}"


class Complaint(Base):
    __tablename__ = "complaints"

    id = Column(String(50), primary_key=True, default=generate_complaint_id, index=True)

    # Origin & Customer Details
    complaint_source = Column(String(120), nullable=True)
    customer_name = Column(String(200), nullable=True, index=True)

    # Product & Batch Identification
    product_name = Column(String(200), nullable=False, index=True)
    strength = Column(String(100), nullable=True)
    batch_number = Column(String(100), nullable=True, index=True)
    manufacturing_date = Column(String(50), nullable=True)
    expiry_date = Column(String(50), nullable=True)
    quantity_affected = Column(String(100), nullable=True)

    # Complaint Details
    complaint_type = Column(String(120), nullable=True)
    complaint_date = Column(String(50), nullable=True)
    description = Column(Text, nullable=False)

    # Assessment & Triage
    severity = Column(String(50), default=SeverityEnum.MINOR.value, nullable=False)
    priority = Column(String(50), default=PriorityEnum.MEDIUM.value, nullable=False)

    # Actions & Workflow Status
    recommended_actions = Column(Text, nullable=True)
    root_cause = Column(Text, nullable=True)
    capa = Column(Text, nullable=True)
    status = Column(String(50), default=StatusEnum.PENDING_TRIAGE.value, nullable=False, index=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
