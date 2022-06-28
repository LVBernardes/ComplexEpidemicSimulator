import logging
from enum import Enum
from typing import Union

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
        self.update_all_individuals_from_graph_edges()
        self.update_visiting_individuals()


class PublicTransport(Transport):
    def __init__(self, unique_id: int, model: SimulationModel):
        super().__init__(unique_id=unique_id, model=model)
        self._category = TransportCategory.MASS
        self._serviced_locales_set: set = set()

    @property
    def serviced_locales_set(self) -> set:
        return self._serviced_locales_set

    def add_serviced_locale(self, locale: Union[int, str]) -> None:
        self._serviced_locales_set.add(locale)

    def remove_serviced_locale(self, locale: Union[int, str]) -> None:
        self._serviced_locales_set.remove(locale)

    def check_for_available_position(self) -> tuple[bool, bool]:
        self.update_all_individuals_from_graph_edges()
        has_position = (
            True if self.occupancy < self.max_capacity_nominal else False,
            True if self.occupancy < self.max_capacity_effective else False,
        )
        return has_position


class PrivateTransport(Transport):
    def __init__(self, unique_id: int, model: SimulationModel, household: int = 0):
        super().__init__(unique_id=unique_id, model=model)
        self._household: int = household
        self.in_use: bool = False
        self.current_user: Union[int, str] = ""

    @property
    def household(self):
        return self._household

    @household.setter
    def household(self, value: int):
        self._household = value

    @property
    def in_use(self) -> bool:
        return self._in_use

    @in_use.setter
    def in_use(self, value: bool):
        self._in_use = value

    @property
    def current_user(self) -> Union[int, str]:
        return self._current_user

    @current_user.setter
    def current_user(self, user_id: Union[int, str]) -> None:
        self._current_user = user_id

    def use_transport(self, user: Union[int, str]) -> None:
        self.in_use = True
        self.current_user = user
