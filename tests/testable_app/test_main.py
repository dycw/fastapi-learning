from fastapi.testclient import TestClient

from fastapi_learning.testable_app.main import app


client = TestClient(app)


def test_main() -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}
