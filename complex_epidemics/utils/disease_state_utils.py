import itertools
from typing import Any

import numpy as np
from scipy.stats import lognorm, skewnorm


class LogNormalUtils:
    @staticmethod
    def generate_fitting_data() -> np.array:
        # data origin: Fig4 from https://medcentral.net/doi/full/10.1186/s40249-021-00901-9#sec-2
        data_dict = {
            1: 8,
            2: 15,
            3: 9,
            4: 17,
            5: 24,
            6: 19,
            7: 20,
            8: 9,
            9: 18,
            10: 14,
            11: 12,
            12: 13,
            13: 8,
            14: 5,
            15: 8,
            16: 6,
            17: 6,
            19: 3,
            20: 1,
            21: 1,
            23: 1,
            26: 1,
        }

        data_list = []
        for key, value in data_dict.items():
            data_list.extend(itertools.repeat(key, value))

        return np.array(data_list)

    @staticmethod
    def get_distribution_fit_params(data: np.array) -> tuple[float, float, float]:
        s, loc, scale = lognorm.fit(data, floc=0)
        return s, loc, scale

    @staticmethod
    def get_instance(s: float, loc: float, scale: float) -> Any:

        return lognorm(s=s, loc=loc, scale=scale)
        # s=0.6948414667108022, loc=0, scale=6.781675060386135


class SkewedNormalUtils:
    @staticmethod
    def generate_fitting_data() -> np.array:
        pass

    @staticmethod
    def get_distribution_fit_params(data: np.array) -> tuple[float, float, float]:
        s, loc, scale = skewnorm.fit(data, floc=0)
        return s, loc, scale

    @staticmethod
    def get_instance(a: float, loc: float, scale: float) -> Any:

        return skewnorm(a=a, loc=loc, scale=scale)
