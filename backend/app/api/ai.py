from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Optional

from app.agents.graph import app_graph
from app.db.session import get_db
from app.models.complaint import Complaint
from app.models.audit import ComplaintEvent, EventTypeEnum
from app.schemas.ai import ChatRequest

router = APIRouter(prefix="/ai", tags=["ai"])

@router.post("/chat")
def chat_with_ai(payload: ChatRequest, db: Session = Depends(get_db)):
    """
    Main entry point for AI interactions.
    Invokes the LangGraph workflow which routes intent to the appropriate node.
    """
    try:
        inputs = {
            "messages": [payload.message],
            "current_complaint": payload.current_complaint,
            "complaint_id": payload.complaint_id
        }
        
        result = app_graph.invoke(inputs)
        node_result = result.get("result", {})
        
        if not node_result.get("success", False):
            return {
                "success": False,
                "tool": "error",
                "result": {"error": node_result.get("error", "Unknown error occurred.")}
            }
            
        tool_name = node_result.get("tool")
        tool_data = node_result.get("result", {})
        
        # Check for duplicates if we extracted product_name and batch_number
        if tool_name in ["log_complaint", "extract_complaint_document"]:
            updates = tool_data.get("updates", {})
            prod = updates.get("product_name")
            batch = updates.get("batch_number")
            if prod and batch:
                duplicate_count = db.query(Complaint).filter(
                    Complaint.product_name == prod,
                    Complaint.batch_number == batch,
                    Complaint.id != payload.complaint_id
                ).count()
                if duplicate_count > 0:
                    tool_data.setdefault("duplicate_warnings", []).append(
                        f"Warning: {duplicate_count} existing complaint(s) found for product '{prod}' and batch '{batch}'."
                    )
        
        # Handle database patch if it's an edit_complaint on an existing saved complaint
        if tool_name == "edit_complaint" and payload.complaint_id:
            updates = tool_data.get("updates", {})
            if updates:
                db_complaint = db.query(Complaint).filter(Complaint.id == payload.complaint_id).first()
                if db_complaint:
                    # Save old values for audit
                    old_values = {}
                    for k in updates.keys():
                        old_values[k] = getattr(db_complaint, k, None)
                        setattr(db_complaint, k, updates[k])
                        
                    # Also apply risk updates if they changed
                    if tool_data.get("risk_changed"):
                        risk = tool_data.get("risk_assessment", {})
                        if risk:
                            old_values["severity"] = db_complaint.severity
                            old_values["priority"] = db_complaint.priority
                            db_complaint.severity = risk.get("severity", db_complaint.severity)
                            db_complaint.priority = risk.get("priority", db_complaint.priority)
                            
                        recommended = tool_data.get("recommended_actions")
                        if recommended:
                            old_values["recommended_actions"] = db_complaint.recommended_actions
                            db_complaint.recommended_actions = ", ".join(recommended)
                            
                    # Audit Trail
                    audit_event = ComplaintEvent(
                        complaint_id=payload.complaint_id,
                        event_type=EventTypeEnum.EDIT_COMPLAINT.value,
                        changed_fields=list(old_values.keys()),
                        previous_values=old_values,
                        new_values={k: getattr(db_complaint, k) for k in old_values.keys()}
                    )
                    
                    db.add(audit_event)
                    db.commit()
            
        return {
            "success": True,
            "tool": tool_name,
            "result": tool_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
@router.patch("/edit-complaint")
def direct_edit_complaint(payload: ChatRequest, db: Session = Depends(get_db)):
    """
    Convenience endpoint that explicitly routes to edit_complaint.
    (This behaves identically to chat because LangGraph handles the intent).
    """
    return chat_with_ai(payload, db)

from fastapi import UploadFile, File
from app.services.document_service import extract_text_from_document, DocumentExtractionError

MAX_FILE_SIZE = 10 * 1024 * 1024 # 10MB

import json
from fastapi import UploadFile, File, Form

@router.post("/extract-document")
async def extract_document(
    file: UploadFile = File(...),
    complaint_id: Optional[str] = Form(None),
    current_complaint: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    """
    Reads an uploaded file, extracts raw text, and invokes LangGraph to extract fields.
    """
    # Parse current_complaint JSON
    comp_dict = None
    if current_complaint:
        try:
            comp_dict = json.loads(current_complaint)
        except json.JSONDecodeError:
            pass

    # 1. Validate file size
    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="File too large. Maximum size is 10MB.")
    if len(content) == 0:
        raise HTTPException(status_code=400, detail="Empty file uploaded.")
        
    # 2. Extract Text
    try:
        raw_text = extract_text_from_document(file.filename, content)
    except DocumentExtractionError as e:
        raise HTTPException(status_code=400, detail=str(e))
        
    # 3. Process with LangGraph
    try:
        inputs = {
            "messages": [raw_text],
            "intent": "extract_document", # Bypass intent detection
            "current_complaint": comp_dict,
            "complaint_id": complaint_id
        }
        
        result = app_graph.invoke(inputs)
        node_result = result.get("result", {})
        
        if not node_result.get("success", False):
            return {
                "success": False,
                "tool": "error",
                "result": {"error": node_result.get("error", "Unknown error from AI.")}
            }
            
        tool_name = node_result.get("tool")
        tool_data = node_result.get("result", {})
        
        # Check for duplicates if we extracted product_name and batch_number
        if tool_name in ["log_complaint", "extract_complaint_document"]:
            updates = tool_data.get("updates", {})
            prod = updates.get("product_name")
            batch = updates.get("batch_number")
            if prod and batch:
                duplicate_count = db.query(Complaint).filter(
                    Complaint.product_name == prod,
                    Complaint.batch_number == batch,
                    Complaint.id != complaint_id
                ).count()
                if duplicate_count > 0:
                    tool_data.setdefault("duplicate_warnings", []).append(
                        f"Warning: {duplicate_count} existing complaint(s) found for product '{prod}' and batch '{batch}'."
                    )
        
        return {
            "success": True,
            "tool": tool_name,
            "filename": file.filename,
            "result": tool_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
