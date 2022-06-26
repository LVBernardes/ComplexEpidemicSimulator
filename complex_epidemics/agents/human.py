import logging
import sys

from complex_epidemics.agents.support_objects.base_agents import MobileAgent
from complex_epidemics.agents.support_objects.human.human_attributes import (
    HumanHealth,
)
from complex_epidemics.agents.support_objects.human.health_states import HealthState
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
            LOG.info(f"Agent deceased: '{self.unique_id}'.")

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

