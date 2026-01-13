@echo off
cd /d "D:\projects\flowhive\backend"
start "Flowhive Server" cmd /k "call .venv\Scripts\activate.bat && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
