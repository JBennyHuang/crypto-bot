from dataclasses import dataclass
from enum import Enum
from typing import Union


class OrderSide(Enum):
    BUY = 0
    SELL = 1


@dataclass
class Order:
    order_id: str
    volume: float
    side: OrderSide


@dataclass
class StopOrder(Order):
    stop_price: float
    limit_price: float
    triggered: bool = False


@dataclass
class LimitOrder(Order):
    limit_price: float


@dataclass
class MarketOrder(Order):
    pass
