import importlib
import logging
from typing import Any, Union

from complex_epidemics.agents.support_objects.base_agents import ContainerAgent, MobileAgent
from complex_epidemics.agents.support_objects.human.human_attributes import (
    HumanHealth, HumanPhysical, HumanPsychological, HumanSocial,
)
from complex_epidemics.agents.support_objects.human.health_states import HealthState
from complex_epidemics.agents.support_objects.human.human_occupation import GenericOccupation
from complex_epidemics.model.simulation_model import SimulationModel
from complex_epidemics.model.support_objects.abstract_model_step_helpers import (
    IModelStepper,
)
from complex_epidemics.utils.step_utils import StepUtils

LOG = logging.getLogger(__name__)


class Human(MobileAgent, IModelStepper):

    __slots__ = (
        "_is_alive",
        "health",
        "social",
        "physical",
        "psychological",
        "occupation",
        "household",
        "entertainment",
        "transport_preference",
        "routine",
        "_low_level_behaviour",
        "_high_level_behaviour",
    )

    def __init__(self, unique_id: int, model: SimulationModel):
        super().__init__(unique_id=unique_id, model=model)
        self._is_alive: bool = True
        self.health = HumanHealth()
        self.social = None
        self.physical = None
        self.psychological = None
        self.occupation = None
        self.household = None
        self.entertainment = None
        self.transport_preference = None
        self.routine = None
        self._low_level_behaviour = None
        self._high_level_behaviour = None

    @property
    def is_alive(self) -> bool:
        return self._is_alive

    @is_alive.setter
    def is_alive(self, value: bool) -> None:
        self._is_alive = value

    def check_if_alive(self):
        if self.health and self.health.health_state == HealthState.DECEASED:
            self.is_alive = False
            self.change_position(self.household.graph_node_id)
            LOG.info(f"Agent deceased: '{self.unique_id}'.")

    def add_social_attribute(self, **kwargs) -> None:
        self.social = HumanSocial(**kwargs)

    def remove_social_attribute(self) -> None:
        self.social = None

    def add_physical_attribute(self, **kwargs) -> None:
        self.physical = HumanPhysical(**kwargs)

    def remove_physical_attribute(self) -> None:
        self.physical = None

    def add_psychological_attribute(self, **kwargs) -> None:
        self.psychological = HumanPsychological(**kwargs)

    def remove_psychological_attribute(self) -> None:
        self.psychological = None

    def add_occupation_attribute(self, locale: ContainerAgent, category: Any) -> None:
        occupation_module = importlib.import_module(
            f'complex_epidemics.agents.support_objects.human.human_occupation'
        )
        occupation_class = getattr(occupation_module, category.value)
        self.occupation = occupation_class()
        self.occupation.locale = locale

    def remove_occupation_attribute(self) -> None:
        self.occupation = None

    def add_household_attribute(self, locale: ContainerAgent) -> None:
        self.household = locale

    def remove_household_attribute(self) -> None:
        self.household = None

    def step(self) -> None:
        if self.is_alive:
            for element in StepUtils.get_elements_with_step_method(
                self, "self", remove_protected=True
            ):
                eval(f"{element}.step()")
            if self._low_level_behaviour:
                self._low_level_behaviour.step()
            self.check_if_alive()

    def advance(self) -> None:
        if self.is_alive and self._high_level_behaviour:
            self._high_level_behaviour.advance()
