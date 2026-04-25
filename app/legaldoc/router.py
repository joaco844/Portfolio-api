from fastapi import APIRouter, HTTPException, UploadFile, File
from app.legaldoc.models import DocumentRequest, DocumentAnalysis
from app.legaldoc.analyzer import analyze_document
from app.legaldoc.extractor import extract_text

router = APIRouter(prefix="/legaldoc", tags=["legaldoc"])


@router.post("/analyze", response_model=DocumentAnalysis)
def analyze(request: DocumentRequest):
    try:
        return analyze_document(request.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze/file", response_model=DocumentAnalysis)
async def analyze_file(file: UploadFile = File(...)):
    content = await file.read()
    try:
        text = extract_text(file.filename, content)
        return analyze_document(text)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
