from typing import overload

class EuropeanOption:
    """
    A class for pricing European options via Monte Carlo numerical methods.
    """

    @overload
    def __init__(
        self,
        initStockPrice: float,
        strikePrice: float,
        riskFreeIntRate: float,
        volatility: float,
        timeToExpire: float,
    ) -> None: ...
    @overload
    def __init__(
        self,
        initStockPrice: float,
        strikePrice: float,
        riskFreeIntRate: float,
        volatility: float,
        timeToExpire: float,
        seed: int,
    ) -> None: ...
    def calculatePrice(self, numSimulations: int) -> tuple[float, float]: ...
