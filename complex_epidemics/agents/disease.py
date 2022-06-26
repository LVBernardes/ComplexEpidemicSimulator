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
        "_recipe",
        "_name",
        "_strain",
        "_immunity_window_in_days",
        "_infectivity",
        "_is_initial_infection_setup",
        "_initial_infected_population",
        "_disease_instance_builder"
    )

    def __init__(self, unique_id: int, model: SimulationModel):
        super().__init__(unique_id=unique_id, model=model)
        self._recipe = None
        self._name = None
        self._strain = None
        self._immunity_window_in_days: int = 0
        self._infectivity: float = 0.0
        self._is_initial_infection_setup: bool = False
        self._initial_infected_population: float = 0.0
        self._disease_instance_builder: Any = None

    @property
    def recipe(self) -> Any:
        return self._recipe

    @recipe.setter
    def recipe(self, value: Any) -> None:
        self._recipe = value

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

    @property
    def is_initial_infection_setup(self) -> bool:
        return self._is_initial_infection_setup

    @is_initial_infection_setup.setter
    def is_initial_infection_setup(self, value: bool) -> None:
        self._is_initial_infection_setup = value

    @property
    def initial_infected_population(self) -> float:
        return self._initial_infected_population

    @initial_infected_population.setter
    def initial_infected_population(self, value: float) -> None:
        self._initial_infected_population = value

    def get_container_agents(self) -> list:
        return self.model.container_agents

    def get_mobile_agents(self) -> list:
        return self.model.mobile_agents

    def setup_initial_infection(self):
        rng = np.random.default_rng()

        if self.initial_infected_population >= 1.0:
            susceptible_host_list = self.model.mobile_agents
            number_infected_hosts = int(self.initial_infected_population)
            for host_id in rng.choice(
                susceptible_host_list, size=number_infected_hosts, replace=False
            ).tolist():
                host = self.model.schedule._agents[host_id]
                self.set_new_infection(host)
            self.is_initial_infection_setup = True

        elif 0.0 < self.initial_infected_population < 1.0:
            susceptible_host_list = self.model.mobile_agents
            number_infected_hosts = round(
                self.initial_infected_population * len(susceptible_host_list)
            )
            for host_id in rng.choice(
                susceptible_host_list, size=number_infected_hosts, replace=False
            ).tolist():
                host = self.model.schedule._agents[host_id]
                self.set_new_infection(host)
            self.is_initial_infection_setup = True

        elif self.initial_infected_population == 0.0:
            LOG.error("Initial infected population value must be greater than ZERO.")
            raise ValueError(
                "Initial infected population value must be greater than ZERO."
            )

        else:
            LOG.error(
                "Initial infected population value must a positive, float number greater than ZERO."
            )
            raise ValueError(
                "Initial infected population value must a positive, float number greater than ZERO."
            )

    def get_susceptible_hosts(self, container_agent: ContainerAgent):
        susceptible_host_list = list()
        for host_id in container_agent.occupants:
            host = self.model.schedule._agents[host_id]
            if host.health.is_susceptible:
                susceptible_host_list.append(host_id)
        return susceptible_host_list

    def get_infectious_hosts(self, container_agent: ContainerAgent):
        infectious_host_list = list()
        for host_id in container_agent.occupants:
            host = self.model.schedule._agents[host_id]
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

    def set_new_infection(self, host: Any) -> None:
        if self._disease_instance_builder is None:
            LOG.error("Disease instance builder is not available or not defined.")
            raise ValueError(
                "Disease instance builder is not available or not defined"
            )

        self._disease_instance_builder.set_disease_instance_platform(
            disease=self, host=host
        )
        self._disease_instance_builder.set_disease_recipe(recipe=self.recipe.value)
        self._disease_instance_builder.build()
        new_infection = self._disease_instance_builder.get_result()
        host.health.add_disease_instance(new_infection)
        LOG.info(f"Agent infected: '{host.unique_id}'.")

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
            self.set_new_infection(host=host)
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
            potential_host = self.model.schedule._agents[potential_host_id]
            self.try_infecting_host(
                infectivity=container_infectivity, host=potential_host
            )

    def spread(self):

        for container_agent_id in self.get_container_agents():
            container_obj = self.model.schedule._agents[container_agent_id]
            self.spread_through_container(container_agent=container_obj)

    def step(self):
        if not self.is_initial_infection_setup:
            self.setup_initial_infection()
        self.spread()
