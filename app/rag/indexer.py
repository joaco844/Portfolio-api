import uuid
import tiktoken
from google import genai
from google.genai import types
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PointStruct

COLLECTION_NAME = "rag_documents"
EMBEDDING_MODEL = "text-embedding-004"
EMBEDDING_DIM = 768
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50


def _get_qdrant(url: str, api_key: str) -> QdrantClient:
    return QdrantClient(url=url, api_key=api_key)


def _ensure_collection(client: QdrantClient) -> None:
    existing = [c.name for c in client.get_collections().collections]
    if COLLECTION_NAME not in existing:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=EMBEDDING_DIM, distance=Distance.COSINE),
        )


def _chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    enc = tiktoken.get_encoding("cl100k_base")
    tokens = enc.encode(text)
    chunks = []
    start = 0
    while start < len(tokens):
        end = min(start + chunk_size, len(tokens))
        chunks.append(enc.decode(tokens[start:end]))
        start += chunk_size - overlap
    return chunks


def _embed(texts: list[str], gemini_api_key: str) -> list[list[float]]:
    client = genai.Client(api_key=gemini_api_key, http_options=types.HttpOptions(api_version='v1'))
    embeddings = []
    for text in texts:
        result = client.models.embed_content(model=EMBEDDING_MODEL, contents=text)
        embeddings.append(result.embeddings[0].values)
    return embeddings


def index_document(
    filename: str,
    pages: list[tuple[int, str]],
    gemini_api_key: str,
    qdrant_url: str,
    qdrant_api_key: str,
) -> tuple[str, int]:
    """Index a document into Qdrant. Returns (document_id, chunks_indexed)."""
    document_id = str(uuid.uuid4())
    qdrant = _get_qdrant(qdrant_url, qdrant_api_key)
    _ensure_collection(qdrant)

    points = []
    for page_num, page_text in pages:
        for chunk in _chunk_text(page_text):
            points.append((page_num, chunk))

    if not points:
        raise ValueError("No text chunks could be extracted from the document")

    texts = [chunk for _, chunk in points]
    embeddings = _embed(texts, gemini_api_key)

    qdrant_points = [
        PointStruct(
            id=str(uuid.uuid4()),
            vector=embedding,
            payload={
                "document_id": document_id,
                "filename": filename,
                "page": page_num,
                "chunk": chunk,
            },
        )
        for (page_num, chunk), embedding in zip(points, embeddings)
    ]

    qdrant.upsert(collection_name=COLLECTION_NAME, points=qdrant_points)
    return document_id, len(qdrant_points)
