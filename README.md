# LegalDoc Analyzer 🏛️

AI-powered tool for analyzing legal documents using LLMs.
Built with Python, FastAPI, and Google Gemini API.

## Features
- Document type classification (contract, NDA, invoice, etc.)
- Key parties extraction
- Main clauses summary
- Risk flags detection

## Tech Stack
Python · FastAPI · Google Gemini API · Pydantic

## Getting Started

### 1. Clone the repo
git clone https://github.com/joaco_diaz/legaldoc-analyzer

### 2. Install dependencies
pip install -r requirements.txt

### 3. Set up environment variables
cp .env.example .env
# Add your Gemini API key to .env

### 4. Run the app
uvicorn app.main:app --reload

## API Endpoints
POST /analyze — Analyze a legal document
GET /health  — Health check

## Example Request
{
  "text": "This agreement is entered into between Company A and Company B..."
}

## Example Response
{
  "document_type": "Service Agreement",
  "parties": ["Company A", "Company B"],
  "key_clauses": ["Payment terms: 30 days", "Termination: 60 days notice"],
  "risk_flags": ["No limitation of liability clause detected"]
}