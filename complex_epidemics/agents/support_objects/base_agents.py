import logging
from typing import Any

from mesa import Agent

from complex_epidemics.model.simulation_model import SimulationModel

LOG = logging.getLogger(__name__)


class GraphAgent:

    __slots__ = "_graph_node_id"

    def __init__(self):
        self._graph_node_id = None

    @property
    def graph_node_id(self) -> Any:
        return self._graph_node_id

    @graph_node_id.setter
    def graph_node_id(self, value: Any):
        self._graph_node_id = value


class ContainerAgent(Agent, GraphAgent):

    __slots__ = (
        "model",
        "unique_id",
        "_category",
        "_sub_category",
        "_max_capacity_nominal",
        "_max_capacity_effective",
        "_occupants",
        "_occupancy",
    )

    def __init__(self, unique_id: int, model: SimulationModel):
        self.model = model
        self.unique_id = unique_id
        self._graph_node_id = None
        self._category = None
        self._sub_category = None
        self._max_capacity_nominal: int = 0
        self._max_capacity_effective: int = 0
        self._occupants: list = list()
        self._occupancy: int = 0

    @property
    def category(self) -> Any:
        return self._category

    @category.setter
    def category(self, value: Any) -> None:
        self._category = value

    @property
    def sub_category(self) -> Any:
        return self._sub_category

    @sub_category.setter
    def sub_category(self, value: Any) -> None:
        self._sub_category = value

    @property
    def max_capacity_nominal(self) -> int:
        return self._max_capacity_nominal

    @max_capacity_nominal.setter
    def max_capacity_nominal(self, value: int) -> None:
        self._max_capacity_nominal = value

    @property
    def max_capacity_effective(self) -> int:
        return self._max_capacity_effective

    @max_capacity_effective.setter
    def max_capacity_effective(self, value: int) -> None:
        self._max_capacity_effective = value

    @property
    def occupants(self) -> list:
        return self._occupants

    @occupants.setter
    def occupants(self, value: list) -> None:
        self._occupants = value

    @property
    def occupancy(self) -> int:
        return self._occupancy

    @occupancy.setter
    def occupancy(self, value: int) -> None:
        self._occupancy = value

    def add_occupant(self, agent_id) -> None:
        new_occupant_list = self.occupants
        new_occupant_list.append(agent_id)
        self.occupants = new_occupant_list

    def remove_occupant(self, agent_id) -> None:
        new_occupant_list = self.occupants
        new_occupant_list.remove(agent_id)
        self.occupants = new_occupant_list

    def update_occupants_from_graph_edges(self):
        related_agents = self.model.graph.get_node_neighbours(self.graph_node_id)
        self.occupants = related_agents
        self.occupancy = len(related_agents)


class MobileAgent(Agent, GraphAgent):

    __slots__ = "unique_id", "model", "_position", "_last_positions"

    def __init__(self, unique_id: int, model: SimulationModel):
        self.unique_id = unique_id
        self.model = model
        self._graph_node_id = None
        self._position: int = 0
        self._last_positions: list[int] = list()

    @property
    def position(self) -> int:
        return self._position

    @position.setter
    def position(self, value: int) -> None:
        self._position = value

    def change_position(self, to_pos: int, from_pos: int = position) -> None:
        self._last_positions.append(from_pos)
        self.position = to_pos

    def get_last_positions(self) -> list[int]:
        positions = self._last_positions
        return positions
