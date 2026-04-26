from pydantic import BaseModel


class UploadResponse(BaseModel):
    document_id: str
    filename: str
    chunks_indexed: int


class Citation(BaseModel):
    document_id: str
    filename: str
    page: int
    chunk: str


class QueryRequest(BaseModel):
    question: str
    gemini_api_key: str
    qdrant_url: str
    qdrant_api_key: str


class QueryResponse(BaseModel):
    answer: str
    citations: list[Citation]
