import os
import tempfile
import traceback
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.main import run_analysis

app = FastAPI(title="Resume Intelligence API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def make_serializable(obj):
    if isinstance(obj, dict):
        return {k: make_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [make_serializable(item) for item in obj]
    elif hasattr(obj, '__dict__'):
        return make_serializable(obj.__dict__)
    return obj


@app.get("/health")
async def health_check():
    return {"status": "ok", "version": "2.0.0"}


@app.post("/analyze")
async def analyze_resume(
    file: UploadFile = File(...),
    jd_text: str = Form(default=None),
    skip_semantic: bool = Form(default=False),
    skip_ai: bool = Form(default=False),
):
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="File must be a PDF")
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        contents = await file.read()
        tmp_file.write(contents)
        tmp_path = tmp_file.name
    
    try:
        report = run_analysis(
            pdf_path=tmp_path,
            jd_text=jd_text.strip() if jd_text and jd_text.strip() else None,
            skip_semantic=skip_semantic,
            skip_ai=skip_ai,
        )
        
        serializable_report = make_serializable(report)
        return JSONResponse(content=serializable_report, status_code=200)
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid resume: {str(e)}")
    except Exception as e:
        traceback.print_exc()
        error_msg = str(e)
        if "GEMINI" in error_msg.upper():
            return JSONResponse(
                content={
                    "error": "AI analysis unavailable",
                    "message": "Gemini API error - other analysis completed",
                    "status": "partial_success"
                },
                status_code=206
            )
        raise HTTPException(status_code=500, detail=error_msg)
    
    finally:
        if os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except:
                pass


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
