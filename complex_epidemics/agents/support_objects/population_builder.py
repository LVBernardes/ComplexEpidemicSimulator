import logging
from enum import Enum

from attr import define, field
from numpy import ndarray

from complex_epidemics.model.simulation_model import SimulationModel

LOG = logging.getLogger(__name__)


@define
class PopulationParameters:
    size: int = field()
    has_gender_segregation: bool = field(init=False)
    male_proportion: float | ndarray = field(init=False)
    female_proportion: float | ndarray = field(init=False)
    has_age_structure: bool = field(init=False)
    age_structure: dict | ndarray = field(init=False)
    age_distribution: dict | ndarray = field(init=False)
    has_household_data: bool = field(init=False)
    household_income: dict | ndarray = field(init=False)
    household_veicules: int | ndarray = field(init=False)
    household_residents_distribution: dict | ndarray = field(init=False)
    household_residents_structure: dict | ndarray = field(init=False)

    def __post__init__(self):
        if (
            self.has_gender_segregation
            and not self.male_proportion
            and self.female_proportion
        ):
            LOG.error(
                "Option for gender segregation TRUE but NO data on Male/Female proportion found."
            )
            raise ValueError(
                "Option for gender segregation TRUE but NO data on Male/Female proportion found."
            )

        if self.has_age_structure and (not self.age_structure or self.age_distribution):
            LOG.error(
                "Option for age structure TRUE but NO data on age distribution or structure found."
            )
            raise ValueError(
                "Option for age structure TRUE but NO data on age distribution or structure found."
            )

        if self.has_household_data and (
            not self.household_residents_structure
            or not self.household_residents_distribution
        ):
            LOG.error(
                "Option for household data TRUE but NO data on household distribution or structure found."
            )
            raise ValueError(
                "Option for household data TRUE but NO data on household distribution or structure found."
            )


class SyntheticPopAlgorithm(Enum):
    pass


class PopulationBuilder:
    def __init__(self):
        self._model = None
        self._population = None
        self._pop_size

    def reset(self):
        self._model = None
        self._population = None
        self._pop_size

    def get_result(self):
        population = self._population
        self.reset()
        return population

    def set_algorithm(self, algorithm: SyntheticPopAlgorithm):
        pass

    def build(self):
        pass

    def _individual_generator(self):
        pass

    def _household_generator(self):
        pass

    def set_model(self, model: SimulationModel) -> None:
        self._model = model

    def set_population_parameters(self, parameters: PopulationParameters) -> None:
        pop_param = parameters

        self._pop_size = pop_param.size
