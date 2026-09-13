import enum
import uuid
from sqlalchemy import Column, String, DateTime, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.compiler import compiles

from app.db.base import Base

# Fallback for SQLite testing (since JSONB is Postgres specific, SQLAlchemy translates JSON to String in SQLite)
from sqlalchemy import JSON

class EventTypeEnum(str, enum.Enum):
    EDIT_COMPLAINT = "EDIT_COMPLAINT"

def generate_uuid() -> str:
    return str(uuid.uuid4())

class ComplaintEvent(Base):
    """
    Audit trail event for recording changes to a complaint.
    """
    __tablename__ = "complaint_events"

    id = Column(String(36), primary_key=True, default=generate_uuid, index=True)
    complaint_id = Column(String(50), nullable=False, index=True)
    event_type = Column(String(50), nullable=False)
    
    # Store lists and dicts
    changed_fields = Column(JSON, nullable=False)
    previous_values = Column(JSON, nullable=False)
    new_values = Column(JSON, nullable=False)
    
    source = Column(String(50), nullable=False, default="AI")
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
