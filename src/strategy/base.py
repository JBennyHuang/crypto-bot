from src.environment.base import Environment
from src.types.order import Order


class Strategy:
    def __init__(self, environment: Environment) -> None:
        self.environment = environment

    def update(self, price: float) -> None:
        raise NotImplementedError
