from dataclasses import dataclass


@dataclass
class Position:
    position_id: str
    security: str
    volume: float
    price: float
