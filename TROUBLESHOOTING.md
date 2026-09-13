# Troubleshooting Guide

Common issues and solutions for the PharmaQMS application.

## Backend / Database

### 1. PostgreSQL Unavailable / Wrong DATABASE_URL
**Symptom:** Backend throws `sqlalchemy.exc.OperationalError` or `Connection refused`.
**Solution:**
- Ensure your PostgreSQL service is actively running on port 5432.
- Verify that you have created the database: `CREATE DATABASE pharma_complaints;`
- Check your `backend/.env` file. The `DATABASE_URL` format must be exact. E.g., `postgresql://postgres:password@localhost:5432/pharma_complaints`

### 2. Port Already in Use
**Symptom:** `[Errno 98] Address already in use` when starting FastAPI.
**Solution:**
- Another application is using port 8000. Start uvicorn on a different port:
  `uvicorn app.main:app --reload --port 8001`
- If you do this, remember to update `VITE_API_BASE_URL` in the frontend `.env.local` to point to port 8001.

## AI Co-Pilot

### 3. Groq API Key Missing or Invalid
**Symptom:** The AI Co-Pilot throws a 500 error or says "Unknown error from AI."
**Solution:**
- Check that `GROQ_API_KEY` is present in `backend/.env`.
- Ensure it is a valid, active key with remaining quota.

### 4. AI Response Error / Timeout
**Symptom:** The Co-Pilot hangs or returns an incomplete response.
**Solution:**
- LLMs can occasionally fail to respond within a timeframe. Try re-sending the message.
- Ensure you are connected to the internet.

## Frontend

### 5. Frontend Cannot Reach Backend
**Symptom:** Network Error or `AxiosError: Network Error` in the console. Dashboard shows "Unable to connect to the server."
**Solution:**
- Ensure the FastAPI backend is running (typically `http://localhost:8000`).
- Ensure your frontend proxy settings in `vite.config.js` or `VITE_API_BASE_URL` are correct.

### 6. Document Upload Failure
**Symptom:** Uploading a PDF shows a "Failed" status.
**Solution:**
- Ensure the PDF is not password protected or corrupted.
- Check the backend console for specific Python exceptions during `pypdf` extraction.
