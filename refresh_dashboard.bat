@echo off
REM Double-click this file to refresh the Wheel dashboard and open it.
cd /d "%~dp0"
".venv\Scripts\python.exe" wheel_screener.py
if errorlevel 1 (
    echo.
    echo Screener failed. Press any key to close.
    pause >nul
    exit /b 1
)
start "" "Wheel_Dashboard.html"
