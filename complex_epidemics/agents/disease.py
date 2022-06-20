import copy
import logging
from typing import Any

from mesa import Agent
import numpy as np

from complex_epidemics.agents.support_objects.base_agents import ContainerAgent
from complex_epidemics.agents.support_objects.human.health_protection_measures import (
    ProtectionMeasureType,
)
from complex_epidemics.model.simulation_model import SimulationModel

LOG = logging.getLogger(__name__)


class Disease(Agent):

    __slots__ = (
        "_disease_instance_prototype",
        "_name",
        "_strain",
        "_immunity_window_in_days",
        "_infectivity",
    )

    def __init__(self, unique_id: int, model: SimulationModel):
        super().__init__(unique_id=unique_id, model=model)
        self._disease_instance_prototype = None
        self._name = None
        self._strain = None
        self._immunity_window_in_days: int = 0
        self._infectivity: float = 0.0

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

    @property
    def infectivity(self) -> float:
        return self._infectivity

    @infectivity.setter
    def infectivity(self, value: float) -> None:
        self._infectivity = value

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

    def generate_infectivity_in_container_agent(
        self, container_agent: ContainerAgent, infectious_host_list: list
    ) -> float:

        # for host_id in infectious_host_list:
        #     host = self.model.schedule.agents[host_id]
        #     if len(host.protection_measures) != 0:
        #         host_hand_efficacy = host.protection_measures.get(ProtectionMeasureType.MASKWEARING.name, None)
        #         host_mask_efficacy = host.protection_measures.get(ProtectionMeasureType.MASKWEARING.name, None)
        #         host_distance_efficacy = host.protection_measures.get(ProtectionMeasureType.MASKWEARING.name, None)
        #         host_infectivity = self.infectivity

        infectivity = self.infectivity
        container_agent.infectivity = infectivity

        return infectivity

    def try_infecting_host(self, host: Any, infectivity: float) -> bool:

        if len(host.health.protection_measures) != 0:
            hand_washing_measure = host.health.protection_measures.get(
                ProtectionMeasureType.HANDWASHING.name, None
            )
            mask_wearing_measure = host.health.protection_measures.get(
                ProtectionMeasureType.MASKWEARING.name, None
            )
            social_distancing_measure = host.health.protection_measures.get(
                ProtectionMeasureType.SOCIALDISTANCING.name, None
            )

            if hand_washing_measure is not None:
                hand_washing_efficacy = hand_washing_measure.get_efficacy()
            else:
                hand_washing_efficacy = 0.0
            if mask_wearing_measure is not None:
                mask_wearing_efficacy = mask_wearing_measure.get_efficacy()
            else:
                mask_wearing_efficacy = 0.0
            if social_distancing_measure is not None:
                social_distancing_efficacy = social_distancing_measure.get_efficacy()
            else:
                social_distancing_efficacy = 0.0
        else:
            hand_washing_efficacy = 0.0
            mask_wearing_efficacy = 0.0
            social_distancing_efficacy = 0.0

        infectivity_attenuator_list = [
            hand_washing_efficacy,
            mask_wearing_efficacy,
            social_distancing_efficacy,
        ]

        LOG.debug(f"Attenuation factor list: {infectivity_attenuator_list}.")

        attenuation_factor = max(infectivity_attenuator_list)

        LOG.debug(f"Attenuation factor chosen: {attenuation_factor} .")

        infection_probability = infectivity * (1 - attenuation_factor)

        LOG.debug(f"Effective infection probability list: {infection_probability} .")

        infect_host = np.random.choice(
            [True, False], p=[infection_probability, 1 - infection_probability]
        )

        LOG.debug(f"New infection: {infect_host}.")

        if infect_host:
            if self.disease_instance_prototype is None:
                LOG.error("Disease instance prototype is not available or not defined.")
                raise ValueError(
                    "Disease instance prototype is not available or not defined"
                )

            new_infection = copy.deepcopy(self.disease_instance_prototype)
            new_infection.host = host
            host.health.add_disease_instance(new_infection)
            return True
        else:
            return False

    def spread_through_container(self, container_agent: ContainerAgent):
        susceptible_hosts = self.get_susceptible_hosts(container_agent=container_agent)
        infectious_hosts = self.get_infectious_hosts(container_agent=container_agent)
        container_infectivity = self.generate_infectivity_in_container_agent(
            container_agent=container_agent, infectious_host_list=infectious_hosts
        )

        for potential_host_id in susceptible_hosts:
            potential_host = self.model.schedule.agents[potential_host_id]
            self.try_infecting_host(
                infectivity=container_infectivity, host=potential_host
            )

    def spread(self):

        for container_agent_id in self.get_container_agents():
            container_obj = self.model.schedule.agents[container_agent_id]
            self.spread_through_container(container_agent=container_obj)

    def step(self):
        self.spread()
