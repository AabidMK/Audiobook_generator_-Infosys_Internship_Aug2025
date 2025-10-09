@echo off
echo ==========================================
echo AI AudioBook Generator - Status Check
echo ==========================================
echo.

echo Checking Backend Server (Port 8080)...
curl -s http://localhost:8080/health >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Backend Server: RUNNING
) else (
    echo ❌ Backend Server: NOT RUNNING
)

echo.
echo Checking Frontend Server (Port 5173)...
curl -s http://localhost:5173 >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Frontend Server: RUNNING
) else (
    echo ❌ Frontend Server: NOT RUNNING
)

echo.
echo ==========================================
echo Access URLs:
echo ==========================================
echo 🌐 Frontend Web Interface: http://localhost:5173
echo 🔧 Backend API: http://localhost:8080
echo ❤️ Health Check: http://localhost:8080/health
echo.
echo Press any key to exit...
pause >nul
