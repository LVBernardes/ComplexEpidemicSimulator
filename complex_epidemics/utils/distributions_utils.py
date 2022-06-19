import numpy as np
from numpy import ndarray


class DistUtils:
    @staticmethod
    def uniform(
        lower_bound: int, upper_bound: int = None, size: int | tuple[int] = 1
    ) -> int | ndarray:
        rng = np.random.default_rng()
        return rng.integers(low=lower_bound, high=upper_bound, size=size, endpoint=True)

    @staticmethod
    def normal(
        mean: float, standard_deviation: float, size: int | tuple[int] = 1
    ) -> int | float | ndarray:
        rng = np.random.default_rng()
        return rng.normal(loc=mean, scale=standard_deviation, size=size)

    @staticmethod
    def power(power: float, size: int | tuple[int] = 1) -> int | float | ndarray:
        rng = np.random.default_rng()
        return rng.power(a=power, size=size)

    @staticmethod
    def pareto(shape: float, size: int | tuple[int] = 1) -> int | float | ndarray:
        rng = np.random.default_rng()
        return rng.pareto(a=shape, size=size)
