@echo off
REM Quick Start Script for AI Portfolio Backend (Windows)
REM Run this after copying all files to set everything up

echo ======================================
echo AI Portfolio Backend - Quick Setup
echo ======================================
echo.

REM Check Python
echo Checking Python version...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed
    exit /b 1
)
for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo [OK] %PYTHON_VERSION%
echo.

REM Create virtual environment
echo Creating virtual environment...
if not exist ".venv" (
    python -m venv .venv
    echo [OK] Virtual environment created
) else (
    echo [WARNING] Virtual environment already exists
)
echo.

REM Activate virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate.bat
echo [OK] Virtual environment activated
echo.

REM Upgrade pip
echo Upgrading pip...
python -m pip install --quiet --upgrade pip
echo [OK] pip upgraded
echo.

REM Install dependencies
echo Installing dependencies...
pip install --quiet -r requirements.txt
echo [OK] Dependencies installed
echo.

REM Create .env from example
if not exist ".env" (
    echo Creating .env file...
    copy .env.example .env >nul
    echo [OK] .env file created
    echo.
) else (
    echo [WARNING] .env file already exists (not overwriting)
    echo.
)

REM Check Ollama status
echo Checking Ollama status...
curl -s http://localhost:11434/api/tags >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Ollama is running
) else (
    echo [WARNING] Ollama is not running
    echo.
    echo To install Ollama:
    echo   Download from: https://ollama.ai/download
    echo.
    echo After installing, run:
    echo   ollama serve          (in one terminal^)
    echo   ollama pull llama3.2:3b   (in another terminal^)
)
echo.

REM Summary
echo ======================================
echo Setup Complete!
echo ======================================
echo.
echo Next steps:
echo.
echo 1. Make sure Ollama is running:
echo    ollama serve
echo.
echo 2. Pull the model (if not already done^):
echo    ollama pull llama3.2:3b
echo.
echo 3. Start the backend:
echo    .venv\Scripts\activate.bat
echo    uvicorn main:app --reload --port 8000
echo.
echo 4. In your frontend folder, create .env:
echo    echo VITE_API_BASE=http://localhost:8000 ^> .env
echo.
echo 5. Start your frontend:
echo    npm run dev
echo.
echo ======================================
echo.
echo Test the backend:
echo   http://localhost:8000          - API info
echo   http://localhost:8000/docs     - Interactive docs
echo   http://localhost:8000/api/health - Health check
echo.
echo ======================================
echo.
pause