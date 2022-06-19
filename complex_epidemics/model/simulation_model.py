# -*- coding: utf-8 -*-
"""Simulation models module.
"""


import logging

from mesa import Model

from complex_epidemics.model.model_scheduler import ModelScheduler

LOG = logging.getLogger(__name__)


class SimulationModel(Model):

    __slots__ = (
        "clock",
        "graph",
        "schedule",
        "_steps_per_day",
        "_activation_order",
        "_is_activation_order_configured",
    )

    def __init__(self):
        super().__init__()
        self.clock = None
        self.graph = None
        self.schedule = ModelScheduler(self)
        self._steps_per_day = 24
        self._activation_order: list = list()
        self._is_activation_order_configured: bool = False
        self._container_agents: list = list()
        self._mobile_agents: list = list()

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
            self._container_agents = self.get_agents_by_class('ContainerAgent')
            return self._container_agents

    @property
    def mobile_agents(self) -> list:
        if len(self._mobile_agents) != 0:
            return self._mobile_agents
        else:
            self._mobile_agents = self.get_agents_by_class('MobileAgent')
            return self._mobile_agents

    def get_agents_by_class(self, agent_class: str) -> list[int]:

        try:
            class_list = list()
            for agent in self.schedule.agents:
                if {agent_class}.intersection(set(agent.__class__.__mro__)):
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
                    agent_list=class_agents_id_list, order=index
                )
        except Exception as err:
            LOG.exception(err)
            raise err
        else:
            self.is_activation_order_configured = True

    def step(self):
        if not self.is_activation_order_configured:
            self.set_activation_order(class_list=self.activation_order)

        self.schedule.step()
