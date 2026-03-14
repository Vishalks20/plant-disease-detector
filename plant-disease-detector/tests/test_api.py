"""Basic API route tests using Flask test client."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from unittest.mock import patch

@pytest.fixture
def client():
    from app import create_app
    app = create_app("development")
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c

def test_health_endpoint(client):
    resp = client.get("/api/health")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["status"] == "ok"

def test_predict_no_file(client):
    resp = client.post("/api/predict")
    assert resp.status_code == 400

def test_index_page(client):
    resp = client.get("/")
    assert resp.status_code == 200
