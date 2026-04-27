@echo off
:: Hermes Quick Launch - Windows Launcher
:: Double-click to launch the GUI (no console window)

echo ==========================================
echo    Hermes Quick Launch for Hermes Agent
echo ==========================================
echo.

:: Check if Python is available
where pythonw.exe >nul 2>nul
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH.
    echo.
    echo Please install Python 3.x:
    echo   https://www.python.org/downloads/
    echo.
    echo During installation, check "Add Python to PATH"
    pause
    exit /b 1
)

:: Launch the GUI (pythonw runs without console window)
pythonw.exe "%~dp0hermes_quick_launch.pyw"

if errorlevel 1 (
    echo.
    echo Launcher exited with an error.
    echo Trying with console output for debugging...
    python.exe "%~dp0hermes_quick_launch.pyw"
    pause
)
