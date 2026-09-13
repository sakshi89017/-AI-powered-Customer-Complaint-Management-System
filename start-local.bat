@echo off
echo ===================================================
echo   Starting PharmaQMS Local Development Servers
echo ===================================================

echo [1/2] Starting Backend (FastAPI on http://localhost:8000)...
start "PharmaQMS Backend" cmd /k "cd /d %~dp0backend && .venv\Scripts\python.exe -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000"

echo [2/2] Starting Frontend (React/Vite on http://localhost:5173)...
start "PharmaQMS Frontend" cmd /k "cd /d %~dp0frontend && npm run dev -- --host 127.0.0.1 --port 5173"

echo.
echo Servers are launching in separate windows!
echo Frontend:  http://localhost:5173
echo Backend:   http://localhost:8000
echo API Docs:  http://localhost:8000/docs
echo.
timeout /t 3 >nul
start http://localhost:5173
