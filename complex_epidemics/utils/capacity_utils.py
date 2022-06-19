import logging

import numpy as np

from complex_epidemics.utils.distributions_utils import DistUtils
from complex_epidemics.utils.exceptions import MissingDataError

LOG = logging.getLogger(__name__)


class CapUtils:
    @staticmethod
    def get_cap_value_from_distribution(dist_type: str, dist_params: list) -> int:

        match dist_type.lower():
            case "none":
                cap = np.array(dist_params)
            case "uniform":
                cap = DistUtils.uniform(
                    lower_bound=dist_params[0],
                    upper_bound=dist_params[1],
                )
            case "normal":
                cap = DistUtils.normal(
                    mean=dist_params[0],
                    standard_deviation=dist_params[1],
                ).round()
            case _:
                LOG.error(f"Distribution type not implemented.")
                raise InvalidOptionError("Distribution type not implemented.")

        cap = (cap.tolist())[0]
        LOG.debug(
            f'Returning value {cap} for distribution "{dist_type}" '
            f"with parameters {dist_params}."
        )

        return cap

    @staticmethod
    def generata_capacity_data(
        cap_input: dict, specific_cap_type_list: list = None
    ) -> dict:

        cap_result = dict()
        cap_input_type_list = cap_input.keys()

        if "nominal" in set(cap_input_type_list):
            cap_data = cap_input["nominal"]
            cap_value = CapUtils.get_cap_value_from_distribution(
                dist_type=cap_data.get("type"), dist_params=cap_data.get("parameters")
            )
            cap_result["nominal"] = cap_value
        else:
            LOG.debug('Missing "nominal" capacity data.')
            raise MissingDataError('Missing "nominal" capacity data.')

        if "effective" in set(cap_input_type_list):
            cap_data = cap_input["effective"]
            cap_value = 0

            while cap_value < cap_result["nominal"]:
                cap_value = CapUtils.get_cap_value_from_distribution(
                    dist_type=cap_data.get("type"),
                    dist_params=cap_data.get("parameters"),
                )

            cap_result["effective"] = cap_value
        else:
            cap_result["effective"] = cap_result["nominal"]

        if specific_cap_type_list is not None:
            for cap_type in specific_cap_type_list:
                if cap_type in set(cap_input_type_list):
                    cap_data = cap_input[cap_type]
                    cap_value = CapUtils.get_cap_value_from_distribution(
                        dist_type=cap_data.get("type"),
                        dist_params=cap_data.get("parameters"),
                    )

                    while cap_value > cap_result["nominal"]:
                        cap_value = CapUtils.get_cap_value_from_distribution(
                            dist_type=cap_data.get("type"),
                            dist_params=cap_data.get("parameters"),
                        )
                    cap_result[cap_type] = cap_value
                else:
                    LOG.error(f"Missing data for {cap_type} capacity type")
                    raise MissingDataError(f"Missing data for {cap_type} capacity type")

        LOG.debug(f"Capacity generated: {cap_result}")
        return cap_result
