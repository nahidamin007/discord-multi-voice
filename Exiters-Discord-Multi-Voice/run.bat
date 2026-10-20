@echo off
title Multi-Token-Voice Safe Launcher
cls

echo ====================================================
echo         MULTI-TOKEN VOICE LAUNCHER (Windows)
echo ====================================================

REM 1. Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python Not installed! Please install. Python and select "Add to PATH".
    pause
    exit /b
)

REM 2. Create/Check Venv
if not exist ".venv" (
    echo [INFO] Creating a virtual environment (.venv)...
    python -m venv .venv
    if %errorlevel% neq 0 (
        echo [ERROR] Unable to create venv.
        pause
        exit /b
    )
    
    echo [INFO] Installing the library (first time)...
    call .venv\Scripts\activate.bat
    python -m pip install --upgrade pip
    pip install -r requirements.txt
) else (
    echo [INFO] Detecting an existing virtual environment.
    call .venv\Scripts\activate.bat
)

REM 3. Run Dashboard
echo [INFO] Starting Bot...
echo ----------------------------------------------------
python dashboard.py
echo ----------------------------------------------------

echo [INFO] Bot Started!
pause
