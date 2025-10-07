@echo off
echo Starting FastAPI Backend...
start cmd /k "cd backend && python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000"

echo Starting React Frontend...
start cmd /k "cd frontend && npm start"

echo Both servers are starting...
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000