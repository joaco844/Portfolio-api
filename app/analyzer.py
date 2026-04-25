from google import genai
from google.genai import types
import os
import json
from dotenv import load_dotenv
from app.models import DocumentAnalysis

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def analyze_document(text: str) -> DocumentAnalysis:
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

    response = client.models.generate_content(
        model="gemini-1.5-flash-latest",
        contents=prompt
    )

    data = json.loads(response.text)
    return DocumentAnalysis(**data)