import logging
from enum import Enum
from typing import Union

from attr import define, field
from numpy import ndarray

from complex_epidemics.model.simulation_model import SimulationModel
from complex_epidemics.utils.step_utils import StepUtils

LOG = logging.getLogger(__name__)


@define
class SRPopulationParameters:
    size: int = field()
    has_gender_segregation: bool = field(init=False)
    male_proportion: Union[float, ndarray] = field(init=False)
    female_proportion: Union[float, ndarray] = field(init=False)
    has_age_structure: bool = field(init=False)
    age_structure: Union[dict, ndarray] = field(init=False)
    age_distribution: Union[dict, ndarray] = field(init=False)
    has_household_data: bool = field(init=False)
    household_income: Union[dict, ndarray] = field(init=False)
    household_veicules: Union[int, ndarray] = field(init=False)
    household_residents_distribution: Union[dict, ndarray] = field(init=False)
    household_residents_structure: Union[dict, ndarray] = field(init=False)

    def __post__init__(self):
        if (
            self.has_gender_segregation
            and not self.male_proportion
            and self.female_proportion
        ):
            LOG.exception(
                "Option for gender segregation TRUE but NO data on Male/Female proportion found."
            )
            raise ValueError(
                "Option for gender segregation TRUE but NO data on Male/Female proportion found."
            )

        if self.has_age_structure and (not self.age_structure or self.age_distribution):
            LOG.exception(
                "Option for age structure TRUE but NO data on age distribution or structure found."
            )
            raise ValueError(
                "Option for age structure TRUE but NO data on age distribution or structure found."
            )

        if self.has_household_data and (
            not self.household_residents_structure
            or not self.household_residents_distribution
        ):
            LOG.exception(
                "Option for household data TRUE but NO data on household distribution or structure found."
            )
            raise ValueError(
                "Option for household data TRUE but NO data on household distribution or structure found."
            )


        self.reference_parameters = {
            'population_size': self.population_size,
            'household_data': {
                'head': 0,
                'members': list(),
                'number_of_members': 0,
                'types:': ['unipersonal', 'nuclear', 'extended', 'composed']
            },
            'individual_data': {
                'age': 0,
                'household_condition': ['head', 'spouse', 'child', 'relative', 'aggregate', 'housemate'],
                'gender': ['male', 'female'],
                'occupation': ['worker', 'student', 'unoccupied', 'housecare']
            }

        }





class SyntheticPopAlgorithm(Enum):
    pass




class PopulationBuilder:
    def __init__(self):
        self._model = None
        self._population = None
        self._pop_size = None
        self._mold = None
        self._individuals = None
        self._households = None

    def reset(self):
        self._model = None
        self._population = None
        self._pop_size = None
        self._mold = None
        self._individuals = None
        self._households = None

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

    def _simple_population_generator(self, mold: dict) -> None:


    def set_model(self, model: SimulationModel) -> None:
        self._model = model

    def set_population_parameters(self, params: FixedPopulationParameters) -> None:

        parameters_names = StepUtils.clean_attributes(dir(params))
        self._mold = dict()
        for name in parameters_names:
            self._mold[name] = getattr(params, name)

        if self._mold['has_gender_segregation'] and self._mold['has_age_grouping']:
            pass
        elif self._mold['has_gender_segregation'] and not self._mold['has_age_grouping']:
            pass
        elif not self._mold['has_gender_segregation'] and not self._mold['has_age_grouping']:
            self._individuals = self._individual_generator()
            self._households = self._household_generator()




