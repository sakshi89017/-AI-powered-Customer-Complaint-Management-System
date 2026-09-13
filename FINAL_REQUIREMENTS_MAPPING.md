# Final Requirements Mapping

This document maps every core assignment requirement strictly to the actual implementation paths within the repository.

**React**
→ `frontend/`

**Redux**
→ `frontend/src/slices/complaintSlice.js` and `frontend/src/slices/copilotSlice.js`

**FastAPI**
→ `backend/app/main.py` and `backend/app/api/`

**LangGraph**
→ `backend/app/agents/graph.py`

**Groq**
→ `backend/app/core/config.py` (API Key configuration) and `backend/app/tools/`

**gemma2-9b-it**
→ `backend/app/core/config.py` (Default Model configuration)

**Log Complaint**
→ `backend/app/tools/log_complaint.py`

**Edit Complaint**
→ `backend/app/tools/edit_complaint.py`

**Document Extraction**
→ `backend/app/api/ai.py` and `backend/app/services/document_service.py`

**PostgreSQL**
→ `backend/app/models/complaint.py` and `backend/app/db/session.py`

**Audit Trail**
→ `backend/app/models/audit.py` and `frontend/src/components/complaint/AuditTrail.jsx`

**Demo Data**
→ `demo_data/`
