# -*- coding: utf-8 -*-
"""Simulation models module.
"""


import logging

from mesa.datacollection import DataCollector
from mesa import Model

from complex_epidemics.model.model_scheduler import ModelScheduler
from complex_epidemics.model.support_objects.clock import Clock
from complex_epidemics.model.support_objects.data_collectors import ModelCollectors
from complex_epidemics.model.support_objects.days_of_week import DayOfWeek

LOG = logging.getLogger(__name__)


class SimulationModel(Model):

    __slots__ = (
        "clock",
        "graph",
        "schedule",
        "_steps_per_day",
        "_activation_order",
        "_is_activation_order_configured",
        "datacollector",
    )

    def __init__(self):
        super().__init__()
        self.clock = Clock()
        self.graph = None
        self.schedule = ModelScheduler(self)
        self._steps_per_day = 24
        self._activation_order: list = list()
        self._is_activation_order_configured: bool = False
        self._container_agents: set = set()
        self._mobile_agents: set = set()
        self._locale_agents: set = set()
        self._transport_agents: set = set()
        self.datacollector = None

    @property
    def steps_per_day(self) -> int:
        return self._steps_per_day

    @steps_per_day.setter
    def steps_per_day(self, value: int) -> None:
        self._steps_per_day = value

    @property
    def activation_order(self) -> list:
        return self._activation_order

    @activation_order.setter
    def activation_order(self, value: list) -> None:
        self._activation_order = value

    @property
    def is_activation_order_configured(self) -> bool:
        return self._is_activation_order_configured

    @is_activation_order_configured.setter
    def is_activation_order_configured(self, value) -> None:
        self._is_activation_order_configured = value

    @property
    def container_agents(self) -> list:
        if len(self._container_agents) != 0:
            return self._container_agents
        else:
            self._container_agents = self.get_agents_by_class("ContainerAgent")
            return self._container_agents

    @property
    def mobile_agents(self) -> list:
        if len(self._mobile_agents) != 0:
            return self._mobile_agents
        else:
            self._mobile_agents = self.get_agents_by_class("MobileAgent")
            return self._mobile_agents

    @property
    def locale_agents(self) -> list:
        if len(self._mobile_agents) != 0:
            return self._locale_agents
        else:
            self._locale_agents = self.get_agents_by_class("Locale")
            return self._locale_agents

    @property
    def transport_agents(self) -> list:
        if len(self._mobile_agents) != 0:
            return self._transport_agents
        else:
            self._transport_agents = self.get_agents_by_class("Transport")
            return self._transport_agents

    def get_agents_by_class(self, agent_class: str) -> list[int]:

        try:
            class_list = list()
            for agent in self.schedule.agents:
                if {agent_class}.intersection(
                    {ag_class.__name__ for ag_class in agent.__class__.__mro__}
                ):
                    class_list.append(agent.unique_id)
        except Exception as err:
            LOG.exception(err)
            raise err
        else:
            return class_list

    def set_activation_order(self, class_list: list = None):

        if class_list is None:
            class_list = ["Human", "Locale", "Transport", "Disease"]

        try:
            for index, class_name in enumerate(class_list):
                class_agents_id_list = self.get_agents_by_class(agent_class=class_name)
                self.schedule.add_agent_to_activation_order(
                    agent_id_list=class_agents_id_list, order=index
                )
        except Exception as err:
            LOG.exception(err)
            raise err
        else:
            self.is_activation_order_configured = True

    def get_public_transports_for_route(
        self, origin: int | str, destination: int | str
    ) -> list:
        transports = list()
        for agent_id in set(self.transport_agents):
            agent = self.schedule._agents[agent_id]
            if (
                origin in agent.serviced_locales_set
                and destination in agent.serviced_locales_set
            ):
                transports.append(agent_id)
        return transports

    def step(self):
        if not self.is_activation_order_configured:
            self.set_activation_order()
            LOG.debug("Model starting: configuring activation order.")

        if self.datacollector is None:
            self.datacollector = DataCollector(
                model_reporters={
                    "Susceptible": ModelCollectors.collect_susceptible_population,
                    "Incubated": ModelCollectors.collect_incubated_no_symptoms_population,
                    "Infectious-Asymptomatic": ModelCollectors.collect_infectious_no_symptoms_population,
                    "Infectious-MildModerateSymptoms": ModelCollectors.collect_infectious_mild_moderated_symptoms_population,
                    "Infectious-SevereSymptoms": ModelCollectors.collect_infectious_severe_symptoms_population,
                    "Infectious-CriticalSymptoms": ModelCollectors.collect_infectious_critical_symptoms_population,
                    "Recovered-TemporaryImmunity": ModelCollectors.collect_recovered_immune_population,
                    "Deceased": ModelCollectors.collect_deceased_population,
                }
            )

        LOG.info(
            f"Model date: {self.clock.get_datetime_formated()}. Day of week: {[day.name for day in DayOfWeek if day.value == self.clock.get_datetime().weekday()][0]}"
        )

        self.schedule.step()
        self.datacollector.collect(self)
        self.clock.increment_time_in_hours(1)
