import logging
from statistics import mean
from typing import Any, Union

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
        "_graph_node_id",
        "_category",
        "_sub_category",
        "_max_capacity_nominal",
        "_max_capacity_effective",
        "_all_individuals",
        "_occupancy",
        "_occupation_individuals",
        "_visiting_individuals",
        "_allowed_occupations",
        "_infectivity"
    )

    def __init__(self, unique_id: int, model: SimulationModel):
        self.model = model
        self.unique_id = unique_id
        self._graph_node_id = unique_id
        self._category = None
        self._sub_category = None
        self._max_capacity_nominal: int = 0
        self._max_capacity_effective: int = 0
        self._all_individuals: set[int] = set()
        self._occupancy: int = 0
        self._occupation_individuals: set[int] = set()
        self._visiting_individuals: set[int] = set()
        self._allowed_occupations: set = set()
        self._infectivity: dict[str, Union[float, list[float]]] = {
            'instant': 0.0,
            'average': 0.0,
            'history': list[float]
        }

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
    def all_individuals(self) -> set[int]:
        return self._all_individuals

    @all_individuals.setter
    def all_individuals(self, agent_id_set: set) -> None:
        self._all_individuals = agent_id_set

    @property
    def occupancy(self) -> int:
        return self._occupancy

    @occupancy.setter
    def occupancy(self, value: int) -> None:
        self._occupancy = value

    def update_all_individuals_from_graph_edges(self) -> None:
        connected_agents = set(self.model.graph.get_node_neighbours(self.graph_node_id))
        self.all_individuals = connected_agents
        self.occupancy = len(connected_agents) if connected_agents else 0

    @property
    def occupation_individuals(self) -> set[int]:
        return self._occupation_individuals

    def add_occupation_individual(self, agent_id) -> None:
        self._occupation_individuals.add(agent_id)

    def remove_occupation_individual(self, agent_id) -> None:
        self._occupation_individuals.remove(agent_id)

    @property
    def allowed_occupations(self) -> set:
        return self._allowed_occupations

    @property
    def visiting_individuals(self) -> set:
        return self._visiting_individuals

    @visiting_individuals.setter
    def visiting_individuals(self, value: set) -> None:
        self._visiting_individuals = value

    def update_visiting_individuals(self) -> None:
        self.visiting_individuals = self.all_individuals - self.occupation_individuals

    @property
    def infectivity(self) -> dict:
        return self._infectivity

    def get_instant_infectivity(self) -> float:
        return self._infectivity.get('instant')

    def set_instant_infectivity(self, value: float) -> None:
        self._infectivity['instant'] = value
        self._infectivity['history'].append(value)
        self.update_average_infectivity()

    def get_average_infectivity(self) -> float:
        return self._infectivity['average']

    def update_average_infectivity(self) -> None:
        self._infectivity['average'] = mean(self._infectivity['history'])


class MobileAgent(Agent, GraphAgent):

    __slots__ = "unique_id", "model", "_position", "_last_positions"

    def __init__(self, unique_id: int, model: SimulationModel):
        self.unique_id = unique_id
        self.model = model
        self._graph_node_id = unique_id
        self._position: int = 0
        self._last_positions: dict[str, Union[int, str]] = dict()

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
            self._last_positions[self.model.clock.get_datetime_formated()] = from_pos
            self.position = to_pos

    def get_last_positions(self) -> dict[str, Union[int, str]]:
        positions = self._last_positions
        return positions
