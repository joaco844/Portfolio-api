from google import genai
import json
from app.legaldoc.models import DocumentAnalysis


def analyze_document(text: str, api_key: str, model: str) -> DocumentAnalysis:
    prompt = f"""
    Analyze the following legal document and respond ONLY with a JSON object.
    No markdown, no explanation, just the JSON.

    JSON structure:
    {{
        "document_type": "type of document",
        "parties": ["party1", "party2"],
        "key_clauses": ["clause1", "clause2"],
        "risk_flags": ["risk1", "risk2"]
    }}

    Document:
    {text}
    """

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model=model,
        contents=prompt
    )

    data = json.loads(response.text)
    return DocumentAnalysis(**data)
