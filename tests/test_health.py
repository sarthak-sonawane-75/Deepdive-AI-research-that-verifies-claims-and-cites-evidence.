from fastapi.testclient import TestClient
from app.api.main import app


def test_health_reports_mesh_gateway():
    client = TestClient(app)
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json()['llm_gateway'] == 'Mesh API'
