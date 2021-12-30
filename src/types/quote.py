from dataclasses import dataclass


@dataclass
class Quote:
    timestamp: int
    security: str
    open: float
    high: float
    low: float
    close: float
