import logging
from typing import Any

from mesa import Agent

from complex_epidemics.model.simulation_model import SimulationModel
from complex_epidemics.utils.exceptions import InvalidActionError

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
        "_assigned_occupants",
        "_assigned_occupations",
    )

    def __init__(self, unique_id: int, model: SimulationModel):
        self.model = model
        self.unique_id = unique_id
        self._graph_node_id = unique_id
        self._category = None
        self._sub_category = None
        self._max_capacity_nominal: int = 0
        self._max_capacity_effective: int = 0
        self._occupants: set[int] = set()
        self._occupancy: int = 0
        self._assigned_occupants: set[int] = set()
        self._assigned_occupations: set
        self._infectivity: float = 0

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
    def occupants(self) -> set[int]:
        return self._occupants

    @occupants.setter
    def occupants(self, agent_id_set: set) -> None:
        self._occupants = agent_id_set

    @property
    def occupancy(self) -> int:
        return self._occupancy

    @occupancy.setter
    def occupancy(self, value: int) -> None:
        self._occupancy = value

    @property
    def infectivity(self) -> float:
        return self._infectivity

    @infectivity.setter
    def infectivity(self, value: float) -> None:
        self._infectivity = value

    @property
    def assigned_occupants(self) -> set[int]:
        return self._assigned_occupants

    @property
    def assigned_occupations(self) -> set:
        return self._assigned_occupations

    def add_assigned_occupant(self, agent_id) -> None:
        self._assigned_occupants.add(agent_id)

    def remove_assigned_occupant(self, agent_id) -> None:
        self._assigned_occupants.remove(agent_id)

    def update_occupants_from_graph_edges(self):
        related_agents = set(self.model.graph.get_node_neighbours(self.graph_node_id))
        self.occupants = related_agents
        self.occupancy = len(related_agents) if related_agents else 0


class MobileAgent(Agent, GraphAgent):

    __slots__ = "unique_id", "model", "_position", "_last_positions"

    def __init__(self, unique_id: int, model: SimulationModel):
        self.unique_id = unique_id
        self.model = model
        self._graph_node_id = unique_id
        self._position: int = 0
        self._last_positions: list[int] = list()

    @property
    def position(self) -> int:
        return self._position

    @position.setter
    def position(self, value: int) -> None:
        self._position = value

    def change_position(self, to_pos: Any, from_pos: Any = None) -> None:

        if from_pos is None:
            from_pos = self.position

        if not self.model.graph.has_node(to_pos):
            LOG.error(f'Position node ID "{to_pos}" DOES NOT exist in model graph.')
            raise ValueError(
                f'Position node ID "{to_pos}" DOES NOT exist in model graph.'
            )

        if (
            self.model.graph.get_node_attributes(to_pos)["bipartite"]
            == self.model.graph.get_node_attributes(self.graph_node_id)["bipartite"]
        ):
            LOG.error(f'Position node ID "{to_pos}" is on the same graph as the agent.')
            raise InvalidActionError(
                f'Position node ID "{to_pos}" is on the same graph as the agent.'
            )

        try:
            if self.model.graph.has_edge(self.graph_node_id, from_pos):
                self.model.graph.remove_edge(self.graph_node_id, from_pos)
            self.model.graph.add_edge(self.graph_node_id, to_pos)
        except Exception as err:
            LOG.error(
                f"Could NOT add or remove edge between {self.graph_node_id} "
                f'and one or both nodes "{to_pos}" and "{from_pos}".'
            )
            raise err
        else:
            LOG.debug(
                f"Agent {self.unique_id} moved from node {from_pos} to node {to_pos}."
            )
            self._last_positions.append(from_pos)
            self.position = to_pos

    def get_last_positions(self) -> list[int]:
        positions = self._last_positions
        return positions
