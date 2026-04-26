from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from app.legaldoc.extractor import extract_pages
from app.rag.indexer import index_document
from app.rag.retriever import retrieve
from app.rag.generator import generate_answer
from app.rag.models import UploadResponse, QueryRequest, QueryResponse

router = APIRouter(prefix="/rag", tags=["rag"])

MAX_FILES = 5


@router.post("/upload", response_model=list[UploadResponse])
async def upload(
    files: list[UploadFile] = File(...),
    gemini_api_key: str = Form(...),
    qdrant_url: str = Form(...),
    qdrant_api_key: str = Form(...),
):
    if len(files) > MAX_FILES:
        raise HTTPException(status_code=422, detail=f"Maximum {MAX_FILES} files per upload.")

    results = []
    for file in files:
        content = await file.read()
        try:
            pages = extract_pages(file.filename, content)
        except ValueError as e:
            raise HTTPException(status_code=422, detail=f"{file.filename}: {e}")

        try:
            document_id, chunks_indexed = index_document(
                filename=file.filename,
                pages=pages,
                gemini_api_key=gemini_api_key,
                qdrant_url=qdrant_url,
                qdrant_api_key=qdrant_api_key,
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"{file.filename}: {e}")

        results.append(UploadResponse(
            document_id=document_id,
            filename=file.filename,
            chunks_indexed=chunks_indexed,
        ))

    return results


@router.post("/query", response_model=QueryResponse)
def query(request: QueryRequest):
    try:
        citations = retrieve(
            question=request.question,
            gemini_api_key=request.gemini_api_key,
            qdrant_url=request.qdrant_url,
            qdrant_api_key=request.qdrant_api_key,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if not citations:
        return QueryResponse(answer="No encontré información relevante en los documentos indexados.", citations=[])

    try:
        answer = generate_answer(
            question=request.question,
            citations=citations,
            gemini_api_key=request.gemini_api_key,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return QueryResponse(answer=answer, citations=citations)
