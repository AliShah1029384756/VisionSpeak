@echo off
title VisionSpeak
cd /d "%~dp0"

if not exist .venv\Scripts\activate.bat (
    echo Please run setup.bat first while connected to the internet.
    pause
    exit /b 1
)

call .venv\Scripts\activate.bat
streamlit run app.py --server.address 127.0.0.1
pause
