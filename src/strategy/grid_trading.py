from collections import defaultdict
from enum import Enum
from math import inf
from typing import List, Union, Callable

from src.environment.base import Environment
from src.types.order import OrderSide, OrderType, OrderStatus, Order
from src.strategy.base import Strategy


class GridUpdate(Enum):
    RISE = 0
    FALL = 1
    NOOP = 2


class GridTrading(Strategy):
    def __init__(self, environment: Environment, grids: List[float]):
        super().__init__(environment)
        assert len(grids) > 1, "more than one grid is required"

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

        # for order in orders.values():
        #     if order.status == OrderStatus.SETTLED:
        #         continue

        #     if order.type == OrderType.STOP:
        #         price_orders_map[order.limit_price].append(order)

        # if update == GridUpdate.RISE:
        #     curr_grid = self.grids[self.grid_index]
        #     next_grid = self.grids[self.grid_index + 1]

        #     sell_curr_grid = True

        #     for order in price_orders_map[curr_grid]:
        #         if order.side == OrderSide.SELL:
        #             sell_curr_grid = False
        #             break

        #     if sell_curr_grid:
        #         n = (len(self.grids) - 3) - len(price_orders_map)
        #         budget = self.environment.get_budget() / n
        #         budget = 0.95 * budget
        #         self.environment.place_stop_sell_order(budget / price, curr_grid, curr_grid)

        #     buy_next_grid = True

        #     for order in price_orders_map[next_grid]:
        #         if order.side == OrderSide.BUY:
        #             buy_next_grid = False
        #             break

        #     if buy_next_grid:
        #         n = (len(self.grids) - 3) - len(price_orders_map)
        #         budget = self.environment.get_budget() / n
        #         budget = 0.95 * budget
        #         self.environment.place_stop_buy_order(budget / price, next_grid, next_grid)

        # elif update == GridUpdate.FALL:
        #     curr_grid = self.grids[self.grid_index]
        #     next_grid = self.grids[self.grid_index + 1]


if __name__ == '__main__':
    ...
