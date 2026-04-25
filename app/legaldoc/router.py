from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from app.legaldoc.models import DocumentRequest, DocumentAnalysis
from app.legaldoc.analyzer import analyze_document
from app.legaldoc.extractor import extract_text

router = APIRouter(prefix="/legaldoc", tags=["legaldoc"])


@router.post("/analyze", response_model=DocumentAnalysis)
def analyze(request: DocumentRequest):
    try:
        return analyze_document(request.text, request.api_key, request.model)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze/file", response_model=DocumentAnalysis)
async def analyze_file(
    file: UploadFile = File(...),
    api_key: str = Form(...),
    model: str = Form("gemini-2.5-flash"),
):
    content = await file.read()
    try:
        text = extract_text(file.filename, content)
        return analyze_document(text, api_key, model)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
