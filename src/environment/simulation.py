from typing import Dict
from pandas import DataFrame
from uuid import uuid4
from matplotlib import pyplot as plt

from src.environment.base import Environment
from src.types.order import OrderSide, OrderType, OrderStatus, Order
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
        self.orders[order_id] = Order(order_id, volume, OrderSide.BUY, OrderType.STOP, OrderStatus.OPEN, limit_price=limit_price, stop_price=stop_price)

        return order_id

    def place_stop_sell_order(self, volume: float, stop_price: float, limit_price: float) -> str:
        order_id = str(uuid4())
        self.orders[order_id] = Order(order_id, volume, OrderSide.SELL, OrderType.STOP, OrderStatus.OPEN, limit_price=limit_price, stop_price=stop_price)

        return order_id

    def place_limit_buy_order(self, volume: float, limit_price: float) -> str:
        order_id = str(uuid4())
        self.orders[order_id] = Order(order_id, volume, OrderSide.BUY, OrderType.LIMIT, OrderStatus.ACTIVE, limit_price=limit_price)

        return order_id

    def place_limit_sell_order(self, volume: float, limit_price: float) -> str:
        order_id = str(uuid4())
        self.orders[order_id] = Order(order_id, volume, OrderSide.SELL, OrderType.LIMIT, OrderStatus.ACTIVE, limit_price=limit_price)

        return order_id

    def place_market_buy_order(self, volume: float) -> str:
        order_id = str(uuid4())
        self.orders[order_id] = Order(order_id, volume, OrderSide.BUY, OrderType.MARKET, OrderStatus.ACTIVE)

        return order_id

    def place_market_sell_order(self, volume: float) -> str:
        order_id = str(uuid4())
        self.orders[order_id] = Order(order_id, volume, OrderSide.SELL, OrderType.MARKET, OrderStatus.ACTIVE)

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

    def _execute_buy(self, timestamp: int, price: float, order: Order):
        cost = order.volume * price * \
            (1 + self.transaction_fee)

        if cost > self.budget:
            order.status = OrderStatus.PENDING
            print('not enough budget')

        else:
            order.status = OrderStatus.SETTLED
            order.timestamp = timestamp
            order.executed_value = price
            self.budget -= cost
            self.volume += order.volume

    def _execute_sell(self, timestamp: int, price: float, order: Order):
        gain = order.volume * price * \
            (1 - self.transaction_fee)

        if order.volume > self.volume:
            order.status = OrderStatus.PENDING
            print('not enough volume')

        else:
            order.status = OrderStatus.SETTLED
            order.timestamp = timestamp
            order.executed_value = price
            self.budget += gain
            self.volume -= order.volume

    def start(self):
        for index, row in self.dataframe.iterrows():
            quote = Quote(index, **row)

            print(quote.close, self.budget)

            for handler in self.events['update']:
                handler(quote.close)

            for order in self.orders.values():
                if order.status == OrderStatus.SETTLED:
                    continue

                if order.side == OrderSide.BUY and order.type == OrderType.MARKET:
                    self._execute_buy(quote.timestamp, quote.close, order)

                elif order.side == OrderSide.SELL and order.type == OrderType.MARKET:
                    self._execute_sell(quote.timestamp, quote.close, order)

                elif order.side == OrderSide.BUY and order.type == OrderType.LIMIT:
                    if quote.close <= order.limit_price:
                        self._execute_buy(quote.timestamp, quote.close, order)

                elif order.side == OrderSide.SELL and order.type == OrderType.LIMIT:
                    if quote.close >= order.limit_price:
                        self._execute_sell(quote.timestamp, quote.close, order)

                elif order.side == OrderSide.BUY and order.type == OrderType.STOP:
                    if quote.close >= order.stop_price and order.status == OrderStatus.OPEN:
                        order.status = OrderStatus.ACTIVE

                    if quote.close <= order.limit_price and order.status == OrderStatus.ACTIVE:
                        self._execute_buy(quote.timestamp, quote.close, order)

                elif order.side == OrderSide.SELL and order.type == OrderType.STOP:
                    if quote.close <= order.stop_price and order.status == OrderStatus.OPEN:
                        order.status = OrderStatus.ACTIVE

                    if quote.close >= order.limit_price and order.status == OrderStatus.ACTIVE:
                        self._execute_sell(quote.timestamp, quote.close, order)

    def plot(self):
        for order in self.orders.values():
            if order.status == OrderStatus.SETTLED:
                if order.side == OrderSide.BUY:
                    self.dataframe.loc[order.timestamp, 'buy'] = order.executed_value
                elif order.side == OrderSide.SELL:
                    self.dataframe.loc[order.timestamp, 'sell'] = order.executed_value

        plt.plot(self.dataframe.index, self.dataframe.close)

        if 'buy' in self.dataframe.columns:
            buy_df = self.dataframe[self.dataframe.buy.notnull()]
            plt.scatter(buy_df.index, buy_df.buy, c='g')

        if 'sell' in self.dataframe.columns:
            sell_df = self.dataframe[self.dataframe.sell.notnull()]
            plt.scatter(sell_df.index, sell_df.sell, c='r')

        plt.xlabel('Time')
        plt.ylabel('Price')
        plt.show()
