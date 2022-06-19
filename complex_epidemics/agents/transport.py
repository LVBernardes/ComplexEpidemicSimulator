import logging
from enum import Enum

from complex_epidemics.agents.support_objects.base_agents import ContainerAgent
from complex_epidemics.agents.support_objects.transport.transport_enums import (
    TransportCategory,
)
from complex_epidemics.model.simulation_model import SimulationModel

LOG = logging.getLogger(__name__)


class PublicTransportCategory(Enum):
    GENERIC = "PublicTransport"
    # BUS = "Bus"
    # SUBWAY = "Subway"


class PrivateTransportCategory(Enum):
    GENERIC = "PrivateTransport"
    # CAR = "CAR"
    # MOTORCYCLE = "Motorcycle"


class Transport(ContainerAgent):
    def __init__(self, unique_id: int, model: SimulationModel):
        super().__init__(unique_id=unique_id, model=model)

    def step(self) -> None:
        self.update_occupants_from_graph_edges()


class PublicTransport(Transport):
    def __init__(self, unique_id: int, model: SimulationModel):
        super().__init__(unique_id=unique_id, model=model)
        self._category = TransportCategory.MASS


class PrivateTransport(Transport):
    def __init__(self, unique_id: int, model: SimulationModel, owner: int = 0):
        super().__init__(unique_id=unique_id, model=model)
        self._owner: int = owner

    @property
    def owner(self):
        return self._owner

    @owner.setter
    def owner(self, value: int):
        self._owner = value
