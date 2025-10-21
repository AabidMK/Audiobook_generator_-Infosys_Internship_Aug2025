@echo off
echo AudioBook Generator - Starting on Localhost
echo =============================================

echo Checking environment...
if not exist .env (
    echo ERROR: .env file not found
    echo Please create .env file with GEMINI_API_KEY
    pause
    exit /b 1
)

echo Starting Backend API...
echo Backend will be available at: http://localhost:8000
echo API docs at: http://localhost:8000/docs
echo.
echo To start frontend separately, run:
echo   cd frontend
echo   npm install
echo   npm run dev
echo.
echo Press Ctrl+C to stop the server
echo.

python start_api.py

pause