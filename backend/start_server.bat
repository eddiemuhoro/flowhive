@echo off
cd /d "D:\projects\flowhive\backend"
call .venv\Scripts\activate.bat
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
