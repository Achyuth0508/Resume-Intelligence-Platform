@echo off
echo Starting Resume Intelligence Platform...
echo.

if not exist "venv\Scripts\activate.bat" (
    python -m venv venv
)

call venv\Scripts\activate.bat
pip install -q -r requirements.txt

echo.
echo Backend: http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo.

uvicorn app.api:app --reload --port 8000

pause

