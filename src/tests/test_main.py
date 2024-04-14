from fastapi.testclient import TestClient


def test_index(client: TestClient) -> None:
    response = client.get("/")
    assert response.json()["message"] == "Hello World"
    assert response.status_code == 200
