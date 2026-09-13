# AI-Powered Customer Complaint Management System

## Overview
An intelligent, full-stack Quality Management System (QMS) designed for the pharmaceutical industry. This application allows Quality Assurance (QA) personnel to log, edit, and analyze customer complaints using natural language via an AI Co-Pilot, minimizing manual data entry while maintaining strict audit trails.

## Problem Statement
Pharmaceutical QA teams often spend significant time manually transcribing customer complaints from emails and PDFs into complex database forms. This process is slow, prone to data-entry errors, and delays critical risk assessment for potentially severe product quality issues.

## Solution
PharmaQMS solves this by introducing a unified interface where a LangGraph-powered AI Co-Pilot intelligently extracts, maps, and patches complaint data directly into the system's Redux state. QA personnel can upload documents or type naturally, and the system automatically populates the correct fields while simultaneously generating an initial risk assessment.

## Key Features
- **Natural Language Data Entry:** Log and edit complaints by chatting with the AI.
- **Document Extraction:** Automatically parse uploaded complaint PDFs and emails.
- **Differential State Updates:** The AI only patches the specific fields requested, preserving all other existing data.
- **Immutable Audit Trail:** Every field modification (manual or AI-driven) is permanently logged in PostgreSQL, tracking old vs. new values.
- **Dashboard Analytics:** Visual breakdown of complaint severity and workflow statuses.

## How the AI Co-Pilot Works
1. **Natural Language**: The user types a complaint or correction.
2. **LangGraph**: Evaluates the intent (Log, Edit, Chat).
3. **Tool Selection**: LangGraph routes to the proper tool (`log_complaint` or `edit_complaint`).
4. **Structured Output**: The `gemma2-9b-it` model strictly formats the output via Pydantic.
5. **Redux**: The frontend applies a differential patch to the shared state.
6. **Complaint Form**: The UI automatically highlights updated fields.
7. **PostgreSQL**: Changes are saved, generating an immutable Audit Trail.

## Three AI Tools
1. **Log Complaint (`log_complaint`)**: 
   - **Flow:** Natural-language complaint → form population + risk assessment.
2. **Edit Complaint (`edit_complaint`)**: 
   - **Flow:** Natural-language correction → selective field update.
   - *Note: Edits preserve unrelated complaint fields, guaranteeing manual data isn't wiped out.*
3. **Document Extraction (`extract_complaint_document`)**: 
   - **Flow:** Uploaded document (PDF/EML) → text extraction → AI extraction → form population.

## Demo Credentials
**No authentication is required for this technical demonstration.** The prototype simulates a logged-in QA User.

## Sample AI Inputs
To easily test the AI capabilities during a demo, copy and paste these exact inputs:

**LOG:**
> "A customer reported discolored capsules for Neurovit 500 mg, batch NV24081. 20 bottles are affected."

**EDIT:**
> "Correction: the batch number is NV24082 and quantity is 35 bottles."

**DOCUMENT:**
Upload the file: `sample_batch_quality_complaint.pdf` from the `demo_data/` directory.

**EDIT AFTER DOCUMENT:**
> "The affected quantity should be 42 bottles."

## Technology Stack
- **Frontend:** React (Vite), Redux Toolkit, CSS (Google Inter Font)
- **Backend:** FastAPI (Python 3.13), Pydantic
- **Database:** PostgreSQL, SQLAlchemy
- **AI/LLM:** LangGraph, LangChain, Groq API (Model: `gemma2-9b-it` or `llama-3.3-70b-versatile`)
- **Document Processing:** `pypdf`, Python `email.parser`

## Architecture

```ascii
React + Redux
      |
      v
FastAPI
      |
      v
LangGraph
      |
      v
Groq / gemma2-9b-it
      |
      +----------------------+
      |          |           |
      v          v           v
Log Tool    Edit Tool   Document Tool
      |          |           |
      +----------+-----------+
                 |
                 v
          Complaint State
                 |
                 v
             PostgreSQL
```

## Project Structure
```
project/
├── frontend/          # React (Vite) frontend
├── backend/           # FastAPI backend
├── demo_data/         # Sample PDFs and emails for testing
├── tests/             # Backend pytest suite
├── .env.example       # Example environment variables
├── DEMO_SCRIPT.md     # Step-by-step evaluator script
├── TROUBLESHOOTING.md # Common issues and fixes
├── ARCHITECTURE.md    # Detailed architecture documentation
├── FINAL_CHECKLIST.md # Project acceptance checklist
└── README.md
```

## Setup

### Prerequisites
- Node.js (v18+)
- Python 3.13
- PostgreSQL Database running locally

### Environment Variables
**1. Backend:**
Copy the backend `.env.example`:
```bash
cd backend
cp .env.example .env
```
Ensure you add your `GROQ_API_KEY` and confirm the `DATABASE_URL` matches your local setup.

**2. Frontend:**
Copy the frontend `.env.example`:
```bash
cd frontend
cp .env.example .env.local
```
This sets `VITE_API_URL` to point to the backend.

### Database Setup
1. Open your PostgreSQL terminal/client.
2. Create the database: `CREATE DATABASE pharma_complaints;`
3. The backend uses SQLAlchemy `create_all()`, which initializes tables automatically on backend startup.

## Run Backend
```bash
cd backend
python -m venv .venv
# Activate environment:
# Windows: .\.venv\Scripts\activate
# Mac/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## Run Frontend
Open a new terminal:
```bash
cd frontend
npm install
npm run dev
```

To build the frontend for production:
```bash
cd frontend
npm run build
```

## Run Tests
To run the automated backend test suite (from the backend directory with environment activated):
```bash
cd backend
python -m pytest tests/ -v
```

## Demo Workflow
Follow the `DEMO_SCRIPT.md` file for a fast, 5-10 minute end-to-end demonstration.

## Recommended Demo Screens
For presentations or reports, we recommend capturing:
1. **Dashboard:** Showing the metrics and recent complaints table.
2. **New Complaint + AI Co-Pilot:** The initial chat interface.
3. **Log Complaint result:** The form populated with pulsing "AI Updated" badges.
4. **Edit Complaint result:** The targeted differential patch of a specific field.
5. **Document Extraction result:** The AI merging PDF data into the form.
6. **Complaint List:** The filterable table of all complaints.
7. **Complaint Detail + Audit Trail:** The persistent database record showing old vs. new values.

## Sample Data
The `demo_data/` directory contains fictional examples ready for testing:
- `sample_batch_quality_complaint.pdf`
- `sample_customer_complaint.eml`
- `sample_discoloration_complaint.txt`

## Optional Deployment Documentation
- **Frontend (Vercel):** The Vite build (`npm run build`) can be deployed directly to Vercel. Set `VITE_API_URL` in the Vercel dashboard to your deployed backend URL.
- **Backend (Render/Heroku):** Deploy the FastAPI application using the provided `requirements.txt`. Set `GROQ_API_KEY`, `DATABASE_URL`, and `FRONTEND_ORIGIN` in the host's environment variables.
- **Database (Supabase/RDS):** Provision a managed PostgreSQL instance and copy its connection string to the backend's `DATABASE_URL`.

## Limitations
- Document processing relies on text extraction. Scanned PDFs without OCR will not parse correctly.
- Application currently runs without authentication/authorization layers for demonstration purposes.

## Future Improvements
- Integrate AWS Textract for OCR capabilities on handwritten forms.
- Implement RBAC (Role-Based Access Control) to restrict approval workflows.

## Submission
**Repository:**
[Paste your GitHub URL here]

**How to run:**
1. Clone the repository.
2. Follow the "Setup" and "Run" instructions above.

**Demo:**
Please refer to the `DEMO_SCRIPT.md` and `EVALUATOR_GUIDE.md` for a comprehensive overview of the application's functionality.

> **Disclaimer:** AI-generated complaint classifications and recommendations are preliminary and require review by authorized Quality personnel. This prototype does not replace approved pharmaceutical QMS procedures or regulatory processes.
