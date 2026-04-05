from pydantic import BaseModel
from typing import List


class Cargo(BaseModel):
    id: str
    volume: float


class Tank(BaseModel):
    id: str
    capacity: float


class InputData(BaseModel):
    cargos: List[Cargo]
    tanks: List[Tank]


class Allocation(BaseModel):
    tank_id: str
    cargo_id: str
    volume: float