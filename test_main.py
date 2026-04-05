from fastapi.testclient import TestClient
from main import app
import storage
import pytest

client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_storage():
    storage.cargos_data = []
    storage.tanks_data = []
    storage.results_data = []


def test_input_endpoint():
    payload = {
        "cargos": [
            {"id": "C1", "volume": 1000},
            {"id": "C2", "volume": 2000}
        ],
        "tanks": [
            {"id": "T1", "capacity": 1500},
            {"id": "T2", "capacity": 2000}
        ]
    }

    response = client.post("/input", json=payload)
    assert response.status_code == 200
    assert response.json()["message"] == "Input stored successfully"


def test_optimize_endpoint():
    payload = {
        "cargos": [{"id": "C1", "volume": 1000}],
        "tanks": [{"id": "T1", "capacity": 1000}]
    }

    client.post("/input", json=payload)
    response = client.post("/optimize")

    assert response.status_code == 200
    assert "message" in response.json()


def test_results_endpoint():
    response = client.get("/results")
    assert response.status_code == 200
    data = response.json()

    assert "allocations" in data
    assert "total_allocated" in data
    assert isinstance(data["total_allocated"], (int, float))


def test_full_flow():
    payload = {
        "cargos": [{"id": "C1", "volume": 3000}],
        "tanks": [
            {"id": "T1", "capacity": 1000},
            {"id": "T2", "capacity": 2000}
        ]
    }

    client.post("/input", json=payload)
    client.post("/optimize")
    response = client.get("/results")

    data = response.json()

    assert data["total_allocated"] == 3000
    assert len(data["allocations"]) > 0


def test_empty_input():
    response = client.post("/input", json={"cargos": [], "tanks": []})
    assert response.status_code == 200

    client.post("/optimize")
    response = client.get("/results")

    data = response.json()
    assert data["total_allocated"] == 0