from enum import Enum

from complex_epidemics.model.simulation_model import SimulationModel
from complex_epidemics.model.support_objects.abstract_model_builder import IModelBuilder


class SimulationModelBuilder(IModelBuilder):
    def __init__(self):
        self._model = SimulationModel()

    def get_result(self):
        assembled_model = self._model
        self.reset()
        return assembled_model

    def reset(self):
        self._model = SimulationModel()

    def assemble_element(self, element: Enum):
        element_name_lowercase = element.name.lower()
        setattr(self._model, element_name_lowercase, element.value)
