from google import genai
from app.rag.models import Citation

MODEL = "gemini-2.5-flash"


def generate_answer(question: str, citations: list[Citation], gemini_api_key: str) -> str:
    context_blocks = "\n\n".join(
        f"[{c.filename} — página {c.page}]\n{c.chunk}" for c in citations
    )

    prompt = f"""Sos un asistente legal. Respondé la pregunta basándote únicamente en los fragmentos de documentos proporcionados.
Si la información no es suficiente para responder con certeza, indicalo claramente.

FRAGMENTOS:
{context_blocks}

PREGUNTA: {question}

RESPUESTA:"""

    client = genai.Client(api_key=gemini_api_key)
    response = client.models.generate_content(model=MODEL, contents=prompt)
    return response.text
