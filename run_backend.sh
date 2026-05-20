#!/bin/bash
echo "Starting Resume Intelligence Platform..."
echo ""

if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

source venv/bin/activate
pip install -q -r requirements.txt

echo ""
echo "Backend: http://localhost:8000"
echo "API Docs: http://localhost:8000/docs"
echo ""

uvicorn app.api:app --reload --port 8000

