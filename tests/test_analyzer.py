from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200

def test_analyze_basic():
    response = client.post("/analyze", json={
        "text": "This agreement is between Company A and Company B. Payment is due within 30 days."
    })
    assert response.status_code == 200
    data = response.json()
    assert "document_type" in data
    assert "parties" in data