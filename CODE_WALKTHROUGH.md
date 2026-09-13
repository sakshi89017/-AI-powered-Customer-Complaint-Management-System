# Code Walkthrough Checklist

During **PART 4 — SHOW CODE FOR LOG COMPLAINT** of your demo video, open your IDE and show the following exact files in this order. Keep explanations to 10-15 seconds per file.

### 1. React AI Co-Pilot Component
- **File:** `frontend/src/components/copilot/CopilotPanel.jsx`
- **Why it matters:** This is where the user interacts with the AI.
- **What to show:** Briefly highlight the `handleSendMessage` function, showing how it dispatches the natural language string to Redux.

### 2. Redux Complaint Slice
- **File:** `frontend/src/slices/complaintSlice.js`
- **Why it matters:** This is the single source of truth for the complaint form on the frontend.
- **What to show:** Highlight the `applyComplaintAIUpdate` reducer. Show how it takes the AI's JSON output and dynamically patches the `currentComplaint` state, which instantly updates the UI.

### 3. FastAPI AI Route
- **File:** `backend/app/api/ai.py`
- **Why it matters:** This is the bridge between the frontend and the AI agent.
- **What to show:** Highlight the `POST /api/ai/chat` endpoint. Show how it receives the request and calls the LangGraph `graph.invoke()` function.

### 4. LangGraph Graph/State
- **File:** `backend/app/agents/graph.py`
- **Why it matters:** This orchestrates the intelligent routing, eliminating brittle hardcoded rules.
- **What to show:** Show the `AgentState` TypedDict and the node definitions. Highlight the `route_request` function, showing how the LLM decides which tool to run based on intent.

### 5. Log Complaint Tool
- **File:** `backend/app/tools/log_complaint.py`
- **Why it matters:** This performs the actual data extraction and risk assessment for a new complaint.
- **What to show:** Show the `SYSTEM_PROMPT` containing the extraction rules. Highlight the `structured_llm.invoke()` call, demonstrating how we enforce structured output.

### 6. Edit Complaint Tool
- **File:** `backend/app/tools/edit_complaint.py`
- **Why it matters:** This proves the AI performs a differential update instead of regenerating everything.
- **What to show:** Show the `SYSTEM_PROMPT` emphasizing the "Return ONLY the fields that the user explicitly asked to change" rule.

### 7. Document Extraction Tool / Service
- **File:** `backend/app/services/document_service.py`
- **Why it matters:** This shows how files are processed securely before hitting the AI.
- **What to show:** Show the `extract_text_from_file` function handling `.pdf`, `.txt`, and `.eml` extraction without relying on production OCR.

### 8. Pydantic Schemas
- **File:** `backend/app/schemas/ai.py`
- **Why it matters:** This guarantees the backend will not crash from malformed LLM responses.
- **What to show:** Show the `LogComplaintResult` and `EditComplaintResult` classes.

### 9. Database Model
- **File:** `backend/app/models/complaint.py`
- **Why it matters:** This proves the data is actually stored in a relational PostgreSQL schema.
- **What to show:** Show the `Complaint` SQLAlchemy class.

### 10. Audit Service / Model
- **File:** `backend/app/models/audit.py`
- **Why it matters:** This demonstrates QMS regulatory compliance (tracking old vs new values).
- **What to show:** Show the `ComplaintEvent` class, specifically the `previous_values` and `new_values` JSONB columns.
