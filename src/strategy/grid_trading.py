from collections import defaultdict
from enum import Enum
from math import inf
from typing import List, Union, Callable

from src.environment.base import Environment
from src.types.order import LimitOrder, MarketOrder, Order, StopBuyOrder, StopOrder, StopSellOrder
from src.strategy.base import Strategy


class GridUpdate(Enum):
    RISE = 0
    FALL = 1
    NOOP = 2


class GridTrading(Strategy):
    def __init__(self, environment: Environment, grids: List[float]):
        super().__init__(environment)
        assert len(grids) > 0, "grids must not be empty"

        if not grids[0] == 0.:
            grids = [0.] + grids

        if not grids[-1] == inf:
            grids = grids + [inf]

        self.grids = grids
        self.grid_index = 0

    def _update_grid_index(self, price: float) -> GridUpdate:
        if price < self.grids[self.grid_index]:
            while price < self.grids[self.grid_index]:
                self.grid_index -= 1

            return GridUpdate.FALL

        elif price >= self.grids[self.grid_index + 1]:
            while price >= self.grids[self.grid_index + 1]:
                self.grid_index += 1

            return GridUpdate.RISE
        else:
            return GridUpdate.NOOP

    def update(self, price: float) -> None:
        update = self._update_grid_index(price)

        orders = self.environment.get_orders()

        price_orders_map = defaultdict(list)

        for order in orders:
            if isinstance(order, StopOrder):
                price_orders_map[order.stop_price].append(order)
            elif isinstance(order, LimitOrder):
                price_orders_map[order.limit_price].append(order)
            elif isinstance(order, MarketOrder):
                price_orders_map[order.price].append(order)

        for i in range(len(self.grids - 1)):
            for order in price_orders_map[self.grids[self.grid_index]]:
                ...


if __name__ == '__main__':
    ...
