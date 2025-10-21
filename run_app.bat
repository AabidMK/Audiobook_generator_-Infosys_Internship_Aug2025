@echo off
echo Starting Audiobook Generator Application...

echo.
echo Starting Backend API Server...
start "Backend API" cmd /k "cd /d %~dp0 && python start_api.py"

echo.
echo Waiting for backend to start...
timeout /t 5 /nobreak > nul

echo.
echo Starting Frontend Development Server...
start "Frontend Dev" cmd /k "cd /d %~dp0\frontend && npm run dev"

echo.
echo Both services are starting...
echo Backend API: http://localhost:8000
echo Frontend: http://localhost:5173
echo API Docs: http://localhost:8000/docs
echo.
pause