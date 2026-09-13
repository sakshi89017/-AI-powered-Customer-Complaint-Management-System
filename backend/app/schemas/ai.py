from typing import List, Optional
from pydantic import BaseModel, Field

class ComplaintUpdates(BaseModel):
    """The fields extracted from the user's natural language complaint."""
    complaint_source: Optional[str] = Field(description="The source of the complaint (e.g. 'Customer', 'Email', 'Phone', 'Web Portal'). Return null if unknown.", default=None)
    customer_name: Optional[str] = Field(description="The name of the customer. Return null if unknown.", default=None)
    product_name: Optional[str] = Field(description="The name of the product. Return null if unknown.", default=None)
    strength: Optional[str] = Field(description="The strength of the product (e.g. '500 mg'). Return null if unknown.", default=None)
    batch_number: Optional[str] = Field(description="The batch or lot number. Return null if unknown.", default=None)
    manufacturing_date: Optional[str] = Field(description="The manufacturing date. Return null if unknown.", default=None)
    expiry_date: Optional[str] = Field(description="The expiry date. Return null if unknown.", default=None)
    quantity_affected: Optional[str] = Field(description="The quantity affected, keeping units (e.g. '20 bottles'). Return null if unknown.", default=None)
    complaint_type: Optional[str] = Field(description="The classified complaint type (e.g. 'Product Quality', 'Packaging', 'Adverse Event', etc.). Return null if unknown.", default=None)
    complaint_date: Optional[str] = Field(description="The date the complaint occurred or was reported by the customer. Return null if unknown.", default=None)
    description: Optional[str] = Field(description="A concise summary of the complaint description based on the user's text.", default=None)

class RiskAssessment(BaseModel):
    severity: str = Field(description="The assessed severity: 'Minor', 'Major', or 'Critical'.")
    priority: str = Field(description="The assessed priority: 'Low', 'Medium', 'High', or 'Urgent'.")

class LogComplaintResult(BaseModel):
    """The structured result of the log_complaint AI tool."""
    tool: str = Field(description="Always 'log_complaint'.", default="log_complaint")
    updates: ComplaintUpdates = Field(description="The extracted fields from the natural language text.")
    risk_assessment: RiskAssessment = Field(description="The initial AI risk assessment.")
    recommended_actions: List[str] = Field(description="A list of 1-3 recommended QA actions.")
    root_cause_recommendation: Optional[str] = Field(description="The AI's suggested root cause based on the complaint text.", default=None)
    capa_recommendation: Optional[str] = Field(description="The AI's suggested Corrective and Preventive Actions (CAPA).", default=None)
    missing_critical_fields: List[str] = Field(description="A list of mandatory fields (like Product Name or Batch Number) that the user failed to provide.", default_factory=list)
    changed_fields: List[str] = Field(description="A list of field names in `updates` that have a non-null extracted value.")
    explanation: str = Field(description="A short explanation of the AI's reasoning for the extraction and risk assessment.")
    duplicate_warnings: List[str] = Field(description="A list of warnings if similar complaints exist.", default_factory=list)

class DocumentExtractionResult(BaseModel):
    """The structured result of the document extraction AI tool."""
    tool: str = Field(description="Always 'extract_complaint_document'.", default="extract_complaint_document")
    updates: ComplaintUpdates = Field(description="The extracted fields from the document text. Missing information should be left null/None.")
    risk_assessment: RiskAssessment = Field(description="The initial AI risk assessment.")
    recommended_actions: List[str] = Field(description="A list of 1-3 recommended QA actions.")
    root_cause_recommendation: Optional[str] = Field(description="The AI's suggested root cause based on the document text.", default=None)
    capa_recommendation: Optional[str] = Field(description="The AI's suggested Corrective and Preventive Actions (CAPA).", default=None)
    missing_critical_fields: List[str] = Field(description="A list of mandatory fields (like Product Name or Batch Number) that the document failed to provide.", default_factory=list)
    changed_fields: List[str] = Field(description="A list of field names in `updates` that have a non-null extracted value.")
    explanation: str = Field(description="A short explanation of the AI's reasoning for the extraction and risk assessment.")
    duplicate_warnings: List[str] = Field(description="A list of warnings if similar complaints exist.", default_factory=list)

class EditComplaintResult(BaseModel):
    """The structured result of the edit_complaint AI tool."""
    tool: str = Field(description="Always 'edit_complaint'.", default="edit_complaint")
    updates: dict = Field(description="A dictionary of ONLY the fields that should be updated. Keys must match the complaint schema.")
    changed_fields: List[str] = Field(description="A list of the field names being updated.")
    risk_changed: bool = Field(description="True if the changes affect risk, False otherwise.")
    risk_assessment: Optional[RiskAssessment] = Field(description="The new risk assessment, if risk_changed is true.", default=None)
    recommended_actions: Optional[List[str]] = Field(description="The new recommended actions, if risk_changed is true.", default=None)
    root_cause_recommendation: Optional[str] = Field(description="The updated root cause recommendation, if risk_changed is true.", default=None)
    capa_recommendation: Optional[str] = Field(description="The updated CAPA recommendation, if risk_changed is true.", default=None)
    message: str = Field(description="A user-friendly confirmation message, or a clarifying question if the request was ambiguous.")
    duplicate_warnings: List[str] = Field(description="A list of warnings if similar complaints exist (e.g. if batch changes).", default_factory=list)

class ChatRequest(BaseModel):
    message: str
    complaint_id: Optional[str] = None
    current_complaint: Optional[dict] = None
