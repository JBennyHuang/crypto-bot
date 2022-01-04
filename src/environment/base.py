from collections import defaultdict
from typing import Any, Callable, Dict

from src.types.order import Order
from src.types.position import Position


class Environment:
    def __init__(self, security: str):
        self.security = security
        self.events: Dict[str, Any] = defaultdict(list)

    def bind(self, event: str,  callback: Callable[[float], None]):
        """subscribes to the environment

        Args:
            event (str): event
            callback (Callable[[float], None]): callback
        """
        self.events[event].append(callback)

    def unbind(self, event: str, callback: Callable[[float], None]):
        """unsubscribes to the environment

        Args:
            event (str): event
            callback (Callable[[float], None]): callback
        """
        self.events[event].remove(callback)

    def place_stop_buy_order(self, volume: float, stop_price: float, limit_price: float) -> str:
        """places a stop buy order

        Args:
            volume (float): volume of order
            stop_price (float): stop price of order
            limit_price (float): limit price of order

        Raises:
            NotImplementedError: must be implemented by subclass

        Returns:
            str: order id
        """
        raise NotImplementedError

    def place_stop_sell_order(self, volume: float, stop_price: float, limit_price: float) -> str:
        """places a stop sell order

        Args:
            volume (float): volume of order
            stop_price (float): stop price of order
            limit_price (float): limit price of order

        Raises:
            NotImplementedError: must be implemented by subclass

        Returns:
            str: order id
        """
        raise NotImplementedError

    def place_limit_buy_order(self, volume: float, limit_price: float) -> str:
        """places a limit buy order

        Args:
            volume (float): volume of order
            limit_price (float): limit price of order

        Raises:
            NotImplementedError: must be implemented by subclass

        Returns:
            str: order id
        """
        raise NotImplementedError

    def place_limit_sell_order(self, volume: float, limit_price: float) -> str:
        """places a limit sell order

        Args:
            volume (float): volume of order
            limit_price (float): limit price of order

        Raises:
            NotImplementedError: must be implemented by subclass

        Returns:
            str: order id
        """
        raise NotImplementedError

    def place_market_buy_order(self, volume: float) -> str:
        """places a market buy order

        Args:
            volume (float): volume of order

        Raises:
            NotImplementedError: must be implemented by subclass

        Returns:
            str: order id
        """
        raise NotImplementedError

    def place_market_sell_order(self, volume: float) -> str:
        """places a market sell order

        Args:
            volume (float): volume of order

        Raises:
            NotImplementedError: must be implemented by subclass

        Returns:
            str: order id
        """
        raise NotImplementedError

    def cancel_order(self, order_id: str):
        """cancels an order

        Args:
            order_id (str): order id

        Raises:
            NotImplementedError: must be implemented by subclass
        """
        raise NotImplementedError

    def get_budget(self) -> float:
        """returns the current budget

        Raises:
            NotImplementedError: must be implemented by subclass

        Returns:
            float: current budget
        """
        raise NotImplementedError

    def get_volume(self) -> float:
        """returns the current volume

        Raises:
            NotImplementedError: must be implemented by subclass

        Returns:
            float: current volume
        """
        raise NotImplementedError

    def get_orders(self) -> Dict[str, Order]:
        """returns the current orders

        Raises:
            NotImplementedError: must be implemented by subclass

        Returns:
            Dict[str, Order]: current orders
        """
        raise NotImplementedError

    def get_positions(self) -> Dict[str, Position]:
        """returns the current positions

        Raises:
            NotImplementedError: must be implemented by subclass

        Returns:
            Dict[str, Position]: current positions
        """
        raise NotImplementedError
