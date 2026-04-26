# Portfolio API

Backend for my portfolio projects. Built with Python and FastAPI, deployed on Railway.

## Modules

### 🏛️ LegalDoc Analyzer
AI-powered legal document analysis using Google Gemini. Upload a PDF or paste raw text and get back document type, involved parties, key clauses, and risk flags as structured JSON.

### 🦊 GitLab Release Summary
Connects to a GitLab repository, reads the commit history, and generates structured release notes using an LLM. Optionally creates a GitLab issue with the summary automatically.

### 🔍 Legal RAG
RAG (Retrieval-Augmented Generation) pipeline for legal documents, built without frameworks. Documents are chunked with tiktoken, embedded with Gemini text-embedding-004, and stored in Qdrant. At query time, the top-5 most semantically similar chunks are retrieved and passed to Gemini as context — returning an answer with exact source citations (document name and page number).

## Tech Stack
Python · FastAPI · Google Gemini · Qdrant · pypdf · tiktoken · python-gitlab · Pydantic

## Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/joaco844/Portfolio-api
```

### 2. Create and activate a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the app
```bash
uvicorn app.main:app --reload
```

## API Endpoints

### LegalDoc
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/legaldoc/analyze` | Analyze a legal document from plain text |
| POST | `/legaldoc/analyze/file` | Analyze a legal document from a PDF or TXT file |

### GitLab
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/gitlab/summary` | Generate a release summary from a GitLab repo |

### RAG
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/rag/upload` | Extract, chunk, embed and index documents (max 5) |
| POST | `/rag/query` | Ask a question over indexed documents |

### Health
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
