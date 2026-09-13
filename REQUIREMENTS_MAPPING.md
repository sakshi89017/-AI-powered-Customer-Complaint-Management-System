# Requirements Mapping

This document explicitly maps the assignment requirements to the actual implementation paths within the repository.

**Requirement:**
React
**Implementation:**
`frontend/`

**Requirement:**
Redux
**Implementation:**
`frontend/src/store/` & `frontend/src/slices/`

**Requirement:**
FastAPI
**Implementation:**
`backend/app/main.py` & `backend/app/api/`

**Requirement:**
PostgreSQL
**Implementation:**
`backend/app/db/session.py` & `backend/app/models/`

**Requirement:**
LangGraph
**Implementation:**
`backend/app/agents/graph.py`

**Requirement:**
Groq gemma2-9b-it
**Implementation:**
`backend/app/core/config.py` (via `GROQ_MODEL`) & `backend/app/tools/`

**Requirement:**
Log Complaint Tool
**Implementation:**
`backend/app/tools/log_complaint.py`

**Requirement:**
Edit Complaint Tool
**Implementation:**
`backend/app/tools/edit_complaint.py`

**Requirement:**
Document Extraction Tool
**Implementation:**
`backend/app/tools/document_extraction.py` (or integrated within `backend/app/api/ai.py` & `backend/app/services/document_service.py`)

**Requirement:**
Audit Trail
**Implementation:**
`backend/app/models/audit.py` & `frontend/src/components/complaint/AuditTrail.jsx`

**Requirement:**
Demo Data
**Implementation:**
`demo_data/`
