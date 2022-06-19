import logging
from typing import Any

from mesa import Agent

from complex_epidemics.agents.human import Human
from complex_epidemics.agents.support_objects.base_agents import ContainerAgent
from complex_epidemics.model.simulation_model import SimulationModel

LOG = logging.getLogger(__name__)


class Disease(Agent):

    __slots__ = "_disease_instance_prototype", "_name", "_strain", "_immunity_window_in_days"

    def __init__(self, unique_id: int, model: SimulationModel):
        super().__init__(unique_id=unique_id, model=model)
        self._disease_instance_prototype = None
        self._name = None
        self._strain = None
        self._immunity_window_in_days: int = 0

    @property
    def disease_instance_prototype(self) -> Any:
        return self._disease_instance_prototype

    @disease_instance_prototype.setter
    def disease_instance_prototype(self, value: Any) -> None:
        self._disease_instance_prototype = value

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value

    @property
    def strain(self) -> str:
        return self._strain

    @strain.setter
    def strain(self, value: str):
        self._strain = value

    @property
    def immunity_window_in_days(self) -> int:
        return self._immunity_window_in_days

    @immunity_window_in_days.setter
    def immunity_window_in_days(self, value: int) -> None:
        self._immunity_window_in_days = value

    def get_container_agents(self) -> list:
        return self.model.container_agents

    def get_mobile_agents(self) -> list:
        return self.model.mobile_agents

    def get_susceptible_hosts(self, container_agent: ContainerAgent):
        susceptible_host_list = list()
        for host_id in container_agent.occupants:
            host = self.model.schedule.agents[host_id]
            if host.health.is_susceptible:
                susceptible_host_list.append(host_id)
        return susceptible_host_list

    def get_infectious_hosts(self, container_agent: ContainerAgent):
        infectious_host_list = list()
        for host_id in container_agent.occupants:
            host = self.model.schedule.agents[host_id]
            if host.health.is_infectious:
                infectious_host_list.append(host_id)
        return infectious_host_list

    def generate_infectivity_in_container_agent(self, container_agent: ContainerAgent, infectious_host_list: list) -> float:

        for host_id in infectious_host_list:
            host = self.model.schedule.agents[host_id]
            if len()


    @staticmethod
    def try_infecting_host(host: Human, infectivity: float) -> None:

        if host.

    def spread_through_container(self, container_agent: ContainerAgent):
        susceptible_hosts = self.get_susceptible_hosts(container_agent=container_agent)
        infectious_hosts = self.get_infectious_hosts(container_agent=container_agent)
        container_infectivity = self.generate_infectivity_in_container_agent(
            container_agent=container_agent,
            infectious_host_list=infectious_hosts
        )

        for potential_host_id in susceptible_hosts:
            potential_host = self.model.schedule.agents[potential_host_id]
            self.try_infecting_host(infectivity=container_infectivity, host=potential_host)

    def spread(self):

        for container_agent_id in self.get_container_agents()
            container_obj = self.model.schedule.agents[container_agent_id]
            self.spread_through_container(container_agent=container_obj)

    def step(self):
        self.spread()
