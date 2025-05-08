from fastapi.testclient import TestClient
from pydantic import json
from your_project.main import app  # Your FastAPI app

client = TestClient(app)

def test_stream_users():
    response = client.get("/stream?limit=1000", stream=True)
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"

    lines = list(response.iter_lines())
    assert len(lines) > 0  # Should return at least one user
    for line in lines:
        user = json.loads(line)
        assert "id" in user
        assert "name" in user
