from typing import Dict
from pandas import DataFrame
from uuid import uuid4

from src.environment.base import Environment
from src.types.order import OrderSide, Order, StopOrder, LimitOrder, MarketOrder
from src.types.position import Position
from src.types.quote import Quote


class SimulationEnvironment(Environment):
    def __init__(self, security: str, dataframe: DataFrame, budget: float, volume: float, transaction_fee: float):
        """simulation environment

        Note:
            dataframe expects to have the following columns: ['timestamp', 'security', 'open', 'high', 'low', 'close']

        Args:
            security (str): security
            dataframe (DataFrame): dataframe with the data to be used in the simulation
            budget (float): budget
            volume (float): volume
            transaction_fee (float): transaction fee
        """
        super().__init__(security)
        self.dataframe = dataframe
        self.budget = budget
        self.volume = volume
        self.transaction_fee = transaction_fee

        self.orders: Dict[str, Order] = {}
        self.positions: Dict[str, Position] = {}

    def place_stop_buy_order(self, volume: float, stop_price: float, limit_price: float) -> str:
        order_id = str(uuid4())
        self.orders[order_id] = StopOrder(
            order_id, volume, OrderSide.BUY, stop_price, limit_price)

        return order_id

    def place_stop_sell_order(self, volume: float, stop_price: float, limit_price: float) -> str:
        order_id = str(uuid4())
        self.orders[order_id] = StopOrder(
            order_id, volume, OrderSide.SELL, stop_price, limit_price)

        return order_id

    def place_limit_buy_order(self, volume: float, limit_price: float) -> str:
        order_id = str(uuid4())
        self.orders[order_id] = LimitOrder(
            order_id, volume, OrderSide.BUY, limit_price)

        return order_id

    def place_limit_sell_order(self, volume: float, limit_price: float) -> str:
        order_id = str(uuid4())
        self.orders[order_id] = LimitOrder(
            order_id, volume, OrderSide.SELL, limit_price)

        return order_id

    def place_market_buy_order(self, volume: float) -> str:
        order_id = str(uuid4())
        self.orders[order_id] = MarketOrder(order_id, volume, OrderSide.BUY)

        return order_id

    def place_market_sell_order(self, volume: float) -> str:
        order_id = str(uuid4())
        self.orders[order_id] = MarketOrder(order_id, volume, OrderSide.SELL)

        return order_id

    def cancel_order(self, order_id: str) -> None:
        del self.orders[order_id]

    def get_budget(self) -> float:
        return self.budget

    def get_volume(self) -> float:
        return self.volume

    def get_orders(self) -> Dict[str, Order]:
        return self.orders

    def get_positions(self) -> Dict[str, Position]:
        return self.positions

    def _execute_buy(self, price: float, order: Order):
        cost = order.volume * price * \
            (1 + self.transaction_fee)

        if cost > self.budget:
            print('not enough budget')
        else:
            self.budget -= cost
            self.volume += order.volume

    def _execute_sell(self, price: float, order: Order):
        gain = order.volume * price * \
            (1 - self.transaction_fee)

        if order.volume > self.volume:
            print('not enough volume')
        else:
            self.budget += gain
            self.volume -= order.volume

    def start(self):
        for index, row in self.dataframe.iterrows():
            quote = Quote(index, **row)

            for handler in self.events['update']:
                handler(quote.close)

            for order in self.orders.values():
                if isinstance(order, MarketOrder) and order.side == OrderSide.BUY:
                    self._execute_buy(quote.close, order)

                elif isinstance(order, MarketOrder) and order.side == OrderSide.SELL:
                    self._execute_sell(quote.close, order)

                elif isinstance(order, LimitOrder) and order.side == OrderSide.BUY:
                    if quote.close <= order.limit_price:
                        self._execute_buy(quote.close, order)

                elif isinstance(order, LimitOrder) and order.side == OrderSide.SELL:
                    if quote.close >= order.limit_price:
                        self._execute_sell(quote.close, order)

                elif isinstance(order, StopOrder) and order.side == OrderSide.BUY:
                    if order.limit_price >= quote.close >= order.stop_price:
                        self._execute_buy(quote.close, order)

                elif isinstance(order, StopOrder) and order.side == OrderSide.SELL:
                    if order.limit_price <= quote.close <= order.stop_price:
                        self._execute_sell(quote.close, order)
