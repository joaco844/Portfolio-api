from pydantic import BaseModel


class DocumentRequest(BaseModel):
    text: str
    api_key: str
    model: str


class DocumentAnalysis(BaseModel):
    document_type: str
    parties: list[str]
    key_clauses: list[str]
    risk_flags: list[str]
