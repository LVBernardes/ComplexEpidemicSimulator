import logging
import sys

from complex_epidemics.agents.support_objects.base_agents import MobileAgent
from complex_epidemics.agents.support_objects.human.human_attributes import HumanHealth
from complex_epidemics.model.simulation_model import SimulationModel
from complex_epidemics.model.support_objects.abstract_model_stepper import IModelStepper
from complex_epidemics.utils.step_utils import StepUtils

LOG = logging.getLogger(__name__)


class Human(MobileAgent, IModelStepper):

    __slots__ = (
        "_is_alive",
        "health",
        "social",
        "physical",
        "psychological",
        "behaviour",
        "occupation",
    )

    def __init__(self, unique_id: int, model: SimulationModel):
        super().__init__(unique_id=unique_id, model=model)
        self._is_alive: bool = True
        self.health = HumanHealth()
        self.social = None
        self.physical = None
        self.psychological = None
        self.behaviour = None
        self.occupation = None

    @property
    def is_alive(self) -> bool:
        return self._is_alive

    @is_alive.setter
    def is_alive(self, value: bool) -> None:
        self._is_alive = value

    def step(self) -> None:
        for element in StepUtils.get_elements_with_step_method(
            self, "self", remove_protected=True
        ):
            print(element)
            eval(f"{element}.step()")

    def advance(self) -> None:
        pass


if __name__ == "__main__":
    model = SimulationModel()
    agent = Human(0, model)
    agent.step()
    print(sys.getsizeof(model))
    print(sys.getsizeof(agent))

    print([item.__name__ for item in agent.__class__.__mro__])
