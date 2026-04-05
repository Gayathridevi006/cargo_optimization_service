from typing import List
from models import Cargo, Tank, Allocation


def optimize_allocation(cargos: List[Cargo], tanks: List[Tank]) -> List[Allocation]:
    # Sort cargos and tanks (descending for greedy)
    cargos = sorted(cargos, key=lambda x: x.volume, reverse=True)
    tanks = sorted(tanks, key=lambda x: x.capacity, reverse=True)

    allocations = []

    for cargo in cargos:
        remaining = cargo.volume

        for tank in tanks:
            if remaining <= 0:
                break

            # Skip if tank is been already assigned
            if any(a.tank_id == tank.id for a in allocations):
                continue

            if tank.capacity > 0:
                allocated_volume = min(remaining, tank.capacity)

                allocations.append(
                    Allocation(
                        tank_id=tank.id,
                        cargo_id=cargo.id,
                        volume=allocated_volume,
                    )
                )

                tank.capacity -= allocated_volume
                remaining -= allocated_volume

    return allocations