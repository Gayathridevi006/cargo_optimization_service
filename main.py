from fastapi import FastAPI
from models import InputData
from optimizer import optimize_allocation
import storage ## in memory storage for simplicity
import requests

app = FastAPI(title="Cargo Optimization Service")
EC2_IP = "http://65.2.179.246:8000/"
@app.post("/input")
def input_data(data: InputData):
    storage.cargos_data = data.cargos
    storage.tanks_data = data.tanks
    return {"message": "Input stored successfully"}


@app.post("/optimize")
def optimize():
    if not storage.cargos_data or not storage.tanks_data:
        return {"error": "No input data provided"}

    storage.results_data = optimize_allocation(
        storage.cargos_data,
        storage.tanks_data,
    )

    return {"message": "Optimization completed"}

def test_live_api():
    base_url = "http://{EC2_IP}:8000"

    payload = {
        "cargos": [{"id": "C1", "volume": 1000}],
        "tanks": [{"id": "T1", "capacity": 1000}]
    }

    requests.post(f"{base_url}/input", json=payload)
    requests.post(f"{base_url}/optimize")

    response = requests.get(f"{base_url}/results")

    assert response.status_code == 200

@app.get("/results")
def get_results():
    return {
        "allocations": storage.results_data,
        "total_allocated": sum(a.volume for a in storage.results_data),
    }

