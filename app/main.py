from fastapi import FastAPI, HTTPException
from app.models import DocumentRequest, DocumentAnalysis
from app.analyzer import analyze_document
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="LegalDoc Analyzer")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/analyze", response_model=DocumentAnalysis)
def analyze(request: DocumentRequest):
    try:
        return analyze_document(request.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))