from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from app.models import DocumentRequest, DocumentAnalysis
from app.analyzer import analyze_document
from app.extractor import extract_text
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="LegalDoc Analyzer")

app.add_middleware(
    CORSMiddleware,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/analyze", response_model=DocumentAnalysis)
def analyze(request: DocumentRequest):
    try:
        return analyze_document(request.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze/file", response_model=DocumentAnalysis)
async def analyze_file(file: UploadFile = File(...)):
    content = await file.read()
    try:
        text = extract_text(file.filename, content)
        return analyze_document(text)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))