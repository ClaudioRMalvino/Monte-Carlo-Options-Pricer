from math import exp, sqrt
import random
from typing import Tuple


class EuropeanOptionPython:
    """
    Class represents a European option which utilizes Monte Carlo numerical
    method to calculate the call and put price.
    """
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

        self.init_stock_price: float = init_stock_price
        self.strike_price: float = strike_price
        self.risk_free_int_rate: float = risk_free_int_rate
        self.volatility: float = volatility
        self.time_to_expire: float = time_to_expire
        self.seed = seed

    def __calculate_st(self, z: float) -> float:
        """
        Function calculates the price path utilizing the analytic solution for Geometric
        Brownian Motion (GMB).

        :param z: random gaussian value with mean 0 and std 1
        :return: float value of the path price
        """
        return self.init_stock_price * exp(
            (self.risk_free_int_rate - 0.5 * (self.volatility * self.volatility))
            * self.time_to_expire
            + (self.volatility * sqrt(self.time_to_expire) * z)
        )

    def calculate_price(self, num_paths: int, seed: int | None = None) -> Tuple[float, float]:
        """
         Runs the Monte Carlo simulation to find the call/put prices.

        :param num_paths: the number of paths to simulate
        :param seed: for reproducibility
        :return: Tuple[float, float] first element is the call price, second element is the put price
        """
        use_seed = seed if seed is not None else self.seed
        rng = random.Random(use_seed)

        payoff_call: float = 0.0
        payoff_put: float = 0.0

        for i in range(num_paths):
            Z: float = rng.gauss(0.0, 1.0)
            price_path: float = self.__calculate_st(Z)

            payoff_call += max((price_path - self.strike_price), 0.0)
            payoff_put += max((self.strike_price - price_path), 0.0)

        avg_payoff_call: float = payoff_call / float(num_paths)
        avg_payoff_put: float = payoff_put / float(num_paths)
        discounted: float = exp(-self.risk_free_int_rate * self.time_to_expire)

        return avg_payoff_call * discounted, avg_payoff_put * discounted
