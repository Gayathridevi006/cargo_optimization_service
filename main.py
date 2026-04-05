from fastapi import FastAPI
from models import InputData
from optimizer import optimize_allocation
import storage ## in memory storage for simplicity

app = FastAPI(title="Cargo Optimization Service")

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


@app.get("/results")
def get_results():
    return {
        "allocations": storage.results_data,
        "total_allocated": sum(a.volume for a in storage.results_data),
    }