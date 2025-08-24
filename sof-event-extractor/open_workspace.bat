@echo off
echo 🚢 SoF Event Extractor - Opening Workspace
echo ========================================

REM Check if VS Code is installed
where code >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ VS Code is not installed or not in PATH
    echo Please install VS Code from: https://code.visualstudio.com/
    pause
    exit /b 1
)

echo ✅ VS Code found
echo 🔄 Opening workspace...

REM Open the workspace file
code sof-event-extractor.code-workspace

echo ✅ Workspace opened in VS Code!
echo.
echo 📋 Quick Start:
echo   • Press F5 to start Flask server with debugging
echo   • Use Ctrl+Shift+P for Command Palette
echo   • Check WORKSPACE_GUIDE.md for detailed instructions
echo.
echo 🎯 Happy coding! 🚢⚓
timeout /t 3 /nobreak >nul
