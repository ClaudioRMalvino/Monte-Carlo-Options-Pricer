from math import exp, sqrt
import random
from typing import Tuple


class EuropeanOptionPython:
    def __init__(
        self,
        init_stock_price: float,
        strike_price: float,
        risk_free_int_rate: float,
        volatility: float,
        time_to_expire: float,
        seed=None,
    ) -> None:
        if volatility < 0:
            raise ValueError("volatility can only be a positive value")

        if init_stock_price < 0 or strike_price < 0:
            raise ValueError(
                "init_stock_price and strike_price can only be a positive value"
            )

        if time_to_expire < 0:
            raise ValueError("time_to_expire can only be a positive value")

        if seed:
            random.seed(seed)

        self.init_stock_price: float = init_stock_price
        self.strike_price: float = strike_price
        self.risk_free_int_rate: float = risk_free_int_rate
        self.volatility: float = volatility
        self.time_to_expire: float = time_to_expire

    def __calculate_st(self, z: float) -> float:
        return self.init_stock_price * exp(
            (self.risk_free_int_rate - 0.5 * (self.volatility * self.volatility))
            * self.time_to_expire
            + (self.volatility * sqrt(self.time_to_expire) * z)
        )

    def calculate_price(self, num_simulations: int) -> Tuple[float, float]:
        payoff_call: float = 0.0
        payoff_put: float = 0.0

        for i in range(num_simulations):
            rand_gaussian: float = random.gauss(0, 1)
            price_path: float = self.__calculate_st(rand_gaussian)

            payoff_call += max((price_path - self.strike_price), 0.0)
            payoff_put += max((self.strike_price - price_path), 0.0)

        avg_payoff_call: float = payoff_call / float(num_simulations)
        avg_payoff_put: float = payoff_put / float(num_simulations)
        discounted: float = exp(-self.risk_free_int_rate * self.time_to_expire)

        return avg_payoff_call * discounted, avg_payoff_put * discounted
