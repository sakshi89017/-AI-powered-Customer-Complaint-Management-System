"""
Pydantic request and response schemas for Complaints.
Supports both standard snake_case and frontend camelCase attributes seamlessly.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Optional
from pydantic import BaseModel, ConfigDict, Field, computed_field, model_validator

from app.models.complaint import PriorityEnum, SeverityEnum, StatusEnum

ALIASES = {
    "productName": "product_name",
    "productStrength": "strength",
    "batchNumber": "batch_number",
    "manufacturingDate": "manufacturing_date",
    "expiryDate": "expiry_date",
    "quantityAffected": "quantity_affected",
    "complaintType": "complaint_type",
    "complaintDate": "complaint_date",
    "complaintDescription": "description",
    "initialSeverity": "severity",
    "complaintSource": "complaint_source",
    "customerName": "customer_name",
    "recommendedActions": "recommended_actions",
}


class ComplaintBase(BaseModel):
    model_config = ConfigDict(extra="ignore", from_attributes=True)

    complaint_source: Optional[str] = None
    customer_name: Optional[str] = None
    product_name: Optional[str] = None
    strength: Optional[str] = None
    batch_number: Optional[str] = None
    manufacturing_date: Optional[str] = None
    expiry_date: Optional[str] = None
    quantity_affected: Optional[str] = None
    complaint_type: Optional[str] = None
    complaint_date: Optional[str] = None
    description: Optional[str] = None
    severity: Optional[str] = SeverityEnum.MINOR.value
    priority: Optional[str] = PriorityEnum.MEDIUM.value
    recommended_actions: Optional[str] = None
    status: Optional[str] = StatusEnum.PENDING_TRIAGE.value

    @model_validator(mode="before")
    @classmethod
    def remap_camel_case(cls, data: Any) -> Any:
        if isinstance(data, dict):
            new_data = dict(data)
            for camel, snake in ALIASES.items():
                if camel in new_data and (snake not in new_data or new_data[snake] is None):
                    new_data[snake] = new_data[camel]
            return new_data
        return data


class ComplaintCreate(ComplaintBase):
    """Payload for creating a new complaint. Product Name and Description are required."""
    product_name: str
    description: str

    @model_validator(mode="before")
    @classmethod
    def validate_required_fields(cls, data: Any) -> Any:
        if isinstance(data, dict):
            remapped = cls.remap_camel_case(data)
            prod = remapped.get("product_name")
            desc = remapped.get("description")
            if not prod or not str(prod).strip():
                raise ValueError("Product Name is required to register a complaint.")
            if not desc or not str(desc).strip():
                raise ValueError("Complaint Description is required to register a complaint.")
            return remapped
        return data


class ComplaintUpdate(BaseModel):
    """Payload for partial updates via PATCH. Only provided fields will be updated."""
    model_config = ConfigDict(extra="ignore")

    complaint_source: Optional[str] = None
    customer_name: Optional[str] = None
    product_name: Optional[str] = None
    strength: Optional[str] = None
    batch_number: Optional[str] = None
    manufacturing_date: Optional[str] = None
    expiry_date: Optional[str] = None
    quantity_affected: Optional[str] = None
    complaint_type: Optional[str] = None
    complaint_date: Optional[str] = None
    description: Optional[str] = None
    severity: Optional[str] = None
    priority: Optional[str] = None
    recommended_actions: Optional[str] = None
    status: Optional[str] = None

    @model_validator(mode="before")
    @classmethod
    def remap_camel_case(cls, data: Any) -> Any:
        if isinstance(data, dict):
            new_data = dict(data)
            for camel, snake in ALIASES.items():
                if camel in new_data and (snake not in new_data or new_data[snake] is None):
                    new_data[snake] = new_data[camel]
            return new_data
        return data


class ComplaintResponse(BaseModel):
    """Outbound schema serialized to clients, supporting both snake_case and camelCase."""
    model_config = ConfigDict(from_attributes=True)

    id: str
    complaint_source: Optional[str] = None
    customer_name: Optional[str] = None
    product_name: str
    strength: Optional[str] = None
    batch_number: Optional[str] = None
    manufacturing_date: Optional[str] = None
    expiry_date: Optional[str] = None
    quantity_affected: Optional[str] = None
    complaint_type: Optional[str] = None
    complaint_date: Optional[str] = None
    description: str
    severity: str
    priority: str
    recommended_actions: Optional[str] = None
    status: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    # Computed camelCase aliases for React frontend compatibility
    @computed_field
    def productName(self) -> str:
        return self.product_name

    @computed_field
    def productStrength(self) -> Optional[str]:
        return self.strength

    @computed_field
    def batchNumber(self) -> Optional[str]:
        return self.batch_number

    @computed_field
    def manufacturingDate(self) -> Optional[str]:
        return self.manufacturing_date

    @computed_field
    def expiryDate(self) -> Optional[str]:
        return self.expiry_date

    @computed_field
    def quantityAffected(self) -> Optional[str]:
        return self.quantity_affected

    @computed_field
    def complaintType(self) -> Optional[str]:
        return self.complaint_type

    @computed_field
    def complaintDate(self) -> Optional[str]:
        return self.complaint_date

    @computed_field
    def complaintDescription(self) -> str:
        return self.description

    @computed_field
    def initialSeverity(self) -> str:
        return self.severity

    @computed_field
    def complaintSource(self) -> Optional[str]:
        return self.complaint_source

    @computed_field
    def customerName(self) -> Optional[str]:
        return self.customer_name

    @computed_field
    def recommendedActions(self) -> Optional[str]:
        return self.recommended_actions

    @computed_field
    def createdAt(self) -> Optional[datetime]:
        return self.created_at

    @computed_field
    def updatedAt(self) -> Optional[datetime]:
        return self.updated_at


class DashboardStatsResponse(BaseModel):
    """Real-time metrics aggregated across all complaints in PostgreSQL."""
    total_complaints: int
    pending_triage: int
    under_investigation: int
    qa_review: int
    action_required: int
    closed: int
    critical_complaints: int
    high_priority: int

class ComplaintEventResponse(BaseModel):
    """Schema for audit trail events."""
    model_config = ConfigDict(from_attributes=True)

    id: str
    complaint_id: str
    event_type: str
    changed_fields: list[str]
    previous_values: dict
    new_values: dict
    timestamp: datetime
    user_id: Optional[str] = None
