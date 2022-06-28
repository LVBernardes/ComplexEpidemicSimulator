from typing import Union

from attr import define, field
from numpy import ndarray

from complex_epidemics.graph.networkx_engine.networkx_bipartitegraph import NetworkxBipartiteGraph
from complex_epidemics.model.model_builder import SimulationModelBuilder
from complex_epidemics.model.simulation_model import SimulationModel
from complex_epidemics.workbench.simulation.population_builder import PopulationBuilder
from complex_epidemics.workbench.simulation.run_session import RunSession


@define
class FixedPopulationParameters:
    individuals_size: Union[int, list[int]] = field()
    household_size_distribution: Union[dict, ndarray] = field(init=False)
    household_individuals_conditions: Union[dict, ndarray] = field()
    occupation_distribution: Union[dict, ndarray] = field

    general_workers: Union[float, ndarray] = field(init=False)
    healthcare_workers: Union[float, ndarray] = field(init=False)
    educational_workers: Union[float, ndarray] = field(init=False)
    students: Union[float, ndarray] = field(init=False)
    unoccupied: Union[float, ndarray] = field(init=False)



class SimulationBuilder:
    def __init__(self):
        self._simulation = None
        self._model_parameters: dict = dict()
        self._agents_parameters: dict = dict()
        self._number_of_iterations: int = 0
        self._parameters_to_test: dict = dict()

    def set_model_parameters(self, clock_start, steps_per_day: int = 24, ):
        pass

    def set_agents_parameters(self, population_params: FixedPopulationParameters, infrastructure_params: dict = None):

        print(dir(population_params))
        for pop_param in dir(population_params):
            if isinstance(getattr(population_params, pop_param), list):
                run_session = RunSession()
                run_session

    def set_simulation_parameters(self, params_to_test: dict = None, number_iterations: int = 1):
        self._parameters_to_test = params_to_test
        self._number_of_iterations = number_iterations

    def build(self):

        if self._parameters_to_test:
            for param_key, param_value in self._parameters_to_test.items():
                model = SimulationModel()
                model.graph = NetworkxBipartiteGraph()
                pop_builder = PopulationBuilder()

    def get_result(self):
        pass
