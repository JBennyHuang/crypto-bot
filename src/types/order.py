from dataclasses import dataclass
from enum import Enum
from typing import Union


class OrderSide(Enum):
    BUY = 0
    SELL = 1


class OrderType(Enum):
    STOP = 0
    LIMIT = 1
    MARKET = 2


class OrderStatus(Enum):
    OPEN = 0
    PENDING = 1
    ACTIVE = 2
    DONE = 3
    SETTLED = 4


@dataclass
class Order:
    order_id: str
    volume: float
    side: OrderSide
    type: OrderType
    status: OrderStatus
    limit_price: Union[float, None] = None
    stop_price: Union[float, None] = None
    # fill_fees: Union[float, None] = None
    # filled_volume: Union[float, None] = None
    timestamp: Union[int, None] = None
    executed_value: Union[float, None] = None
