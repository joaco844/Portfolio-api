from google import genai
from google.genai import types
from qdrant_client import QdrantClient
from app.rag.indexer import COLLECTION_NAME, EMBEDDING_MODEL
from app.rag.models import Citation

TOP_K = 5


def retrieve(
    question: str,
    gemini_api_key: str,
    qdrant_url: str,
    qdrant_api_key: str,
) -> list[Citation]:
    client = genai.Client(api_key=gemini_api_key, http_options=types.HttpOptions(api_version='v1'))
    result = client.models.embed_content(model=EMBEDDING_MODEL, contents=question)
    query_vector = result.embeddings[0].values

    qdrant = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)
    hits = qdrant.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vector,
        limit=TOP_K,
        with_payload=True,
    )

    return [
        Citation(
            document_id=hit.payload["document_id"],
            filename=hit.payload["filename"],
            page=hit.payload["page"],
            chunk=hit.payload["chunk"],
        )
        for hit in hits
    ]
