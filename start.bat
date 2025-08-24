@echo off
echo 🚢 SoF Event Extractor - Quick Start (Windows)
echo ================================================

echo.
echo 🔄 Starting Flask Backend...
start "Flask Backend" cmd /k "cd backend && python app.py"

echo.
echo ⏳ Waiting for backend to start...
timeout /t 3 /nobreak >nul

echo.
echo 🌐 Starting Frontend Server...
start "Frontend Server" cmd /k "cd frontend && python -m http.server 8000"

echo.
echo ⏳ Waiting for frontend to start...
timeout /t 2 /nobreak >nul

echo.
echo 🎉 SoF Event Extractor is starting up!
echo.
echo 📋 Access Points:
echo    Frontend: http://localhost:8000
echo    API:      http://localhost:5000/api
echo    Health:   http://localhost:5000/api/health
echo.
echo 🌐 Opening frontend in browser...
start http://localhost:8000

echo.
echo ✅ Setup complete! Both servers are running in separate windows.
echo    Press any key to exit this window...
pause >nul
