@echo off
title VisionSpeak Setup
cd /d "%~dp0"

echo =====================================
echo          VisionSpeak Setup
echo =====================================
echo.

where python >nul 2>nul
if errorlevel 1 (
    echo Python was not found. Install Python 3.11 from python.org and tick "Add Python to PATH".
    pause
    exit /b 1
)

if not exist .venv (
    python -m venv .venv
    if errorlevel 1 (
        echo Could not create virtual environment.
        pause
        exit /b 1
    )
)

call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo Package installation failed. Check your internet connection and try again.
    pause
    exit /b 1
)

python download_model.py
if errorlevel 1 (
    echo Model download failed. Re-run setup.bat when internet is available.
    pause
    exit /b 1
)

echo.
echo Setup complete. You can now run run.bat, including without internet.
pause
