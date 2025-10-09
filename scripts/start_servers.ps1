# AI AudioBook Generator - Startup Script
Write-Host "Starting AI AudioBook Generator Servers..." -ForegroundColor Green

# Start Backend Server
Write-Host "Starting Backend Server on port 8080..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot'; python server.py serve --port 8080"

# Wait a moment for backend to start
Start-Sleep -Seconds 3

# Start Frontend Server  
Write-Host "Starting Frontend Server on port 5173..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot\frontend'; npm run dev"

Write-Host ""
Write-Host "===========================================" -ForegroundColor Cyan
Write-Host "Servers Starting..." -ForegroundColor Green
Write-Host "===========================================" -ForegroundColor Cyan
Write-Host "Backend:  http://localhost:8080" -ForegroundColor White
Write-Host "Frontend: http://localhost:5173" -ForegroundColor White
Write-Host "Health:   http://localhost:8080/health" -ForegroundColor White
Write-Host ""
Write-Host "Press any key to exit this script..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
