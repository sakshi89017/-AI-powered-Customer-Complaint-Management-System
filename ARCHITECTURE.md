# System Architecture: PharmaQMS

This document describes the end-to-end architecture of the AI Customer Complaint Management System.

## Architecture Diagram

```ascii
+------------------------------------------------------+
|                       FRONTEND                       |
|  React (Vite) + Redux Toolkit + React Router         |
|                                                      |
|  [ Dashboard ]  [ Complaint Form ]  [ AI Co-Pilot ]  |
|          \               |                 /         |
|           \-- Redux (Single Source of Truth)        |
+--------------------------|---------------------------+
                           | HTTP / REST (Axios)
+--------------------------v---------------------------+
|                       BACKEND                        |
|                  FastAPI (Python 3.13)               |
|                                                      |
|   +-------------------+       +------------------+   |
|   |   API Routers     |       |   LangGraph      |   |
|   | (/complaints, /ai)| ----> | (Agent workflow) |   |
|   +---------|---------+       +--------|---------+   |
|             |                          |             |
|   +---------v---------+       +--------v---------+   |
|   |     Services      |       |  Groq API Cloud  |   |
|   | (complaint_service|       | (gemma2-9b-it)   |   |
|   +---------|---------+       +------------------+   |
|             |                                        |
+-------------|----------------------------------------+
              | SQLAlchemy ORM
+-------------v----------------------------------------+
|                      DATABASE                        |
|                     PostgreSQL                       |
|                                                      |
|   [ complaints table ]   [ complaint_events table ]  |
+------------------------------------------------------+
```

## Frontend Architecture
- **React (Vite):** Fast, component-based UI layer.
- **Redux Toolkit:** Used as the single source of truth (`activeComplaint` in `complaintSlice`). The AI Co-Pilot tools do not maintain local form state; they mutate the Redux state, which flows down to the presentation components (`ComplaintForm`).

## Backend Architecture
- **FastAPI:** High-performance async Python backend.
- **Pydantic:** Strictly validates incoming requests, as well as AI structured outputs, ensuring malformed LLM responses cannot corrupt the database.

## LangGraph & AI Architecture
- **Agent Node (`LangGraph`):** Parses the user's intent to decide whether to answer a generic query or invoke a tool.
- **Tools (`LangChain`):** 
  - `log_complaint`: Converts a free-text complaint into structured fields.
  - `edit_complaint`: Accepts a natural language edit, identifies the specific fields mentioned, and patches them without touching unrelated fields.
  - `extract_complaint_document`: Parses uploaded files (via `pypdf`/`email`) and extracts relevant fields.
- **LLM (`Groq`):** Uses `gemma2-9b-it` for highly responsive, structured reasoning.

## Risk Assessment Flow
When a complaint is logged or edited, the AI tool also generates a risk assessment evaluating Severity (Minor/Major/Critical) and Priority (Low/Medium/High), and suggests immediate actions. This ensures QA teams have an initial starting point for triage.

## Database & Audit Architecture
- **PostgreSQL:** Persists complaints and audit events.
- **Audit Trail (`complaint_events`):** Every time a complaint is saved, the backend compares it to the previous state. Any changed fields (whether altered manually or via AI) are logged immutably with their old and new values.
