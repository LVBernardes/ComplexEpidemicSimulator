import logging
from typing import Any

from complex_epidemics.agents.human import Human
from complex_epidemics.agents.support_objects.human.high_level_human_behaviour import (
    HighLevelBehaviour,
)
from complex_epidemics.agents.support_objects.human.human_attributes import (
    HumanHealth,
    HumanPhysical,
    HumanPsychological,
    HumanSocial,
)
from complex_epidemics.agents.support_objects.human.human_occupation import Occupation
from complex_epidemics.agents.support_objects.human.low_level_human_behaviour import (
    LowLevelBehaviour,
    Routine,
)
from complex_epidemics.model.simulation_model import SimulationModel
from complex_epidemics.utils.id_utils import IDUtils

LOG = logging.getLogger(__name__)


class HumanBuilder:

    __slots__ = [
        "_new_human",
        "_model",
        "_health",
        "_social_attrs",
        "_physical_attrs",
        "_psychological_attrs",
        "_routine",
        "_high_level_behaviour",
        "_occupation",
    ]

    def __init__(self) -> None:
        self._new_human = None
        self._model = None
        self._health = None
        self._social_attrs = None
        self._physical_attrs = None
        self._psychological_attrs = None
        self._routine = None
        self._high_level_behaviour = None
        self._occupation = None

    def get_result(self) -> Human:
        new_human = self._new_human
        self.reset()
        return new_human

    def reset(self) -> None:
        self._new_human = None
        self._model = None
        self._health = None
        self._social_attrs = None
        self._physical_attrs = None
        self._psychological_attrs = None
        self._routine = None
        self._high_level_behaviour = None
        self._occupation = None

    def build(self) -> None:

        if self._model is None:
            LOG.error("Model not defined.")
            raise ValueError("Model not defined.")
        try:
            self._new_human = Human(unique_id=IDUtils.generate_id(), model=self._model)
            self._new_human.graph_node_id = self._new_human.unique_id
            self._new_human.model.graph.add_node_to_component_one(
                self._new_human.unique_id
            )
            self._new_human.model.schedule.add(self._new_human)
            self._new_human.health = self._health if self._health else HumanHealth()
            self._new_human.social = self._social_attrs
            self._new_human.physical = self._physical_attrs
            self._new_human.psychological = self._psychological_attrs
            self._new_human.routine = self._routine
            self._new_human._low_level_behaviour = LowLevelBehaviour(
                self._new_human, routine=self._routine
            )
            self._new_human._high_level_behaviour = self._high_level_behaviour
            self._new_human.occupation = self._occupation
            self._new_human.occupation._human = self._new_human
            LOG.debug(f"{self._new_human.health}")
        except Exception as err:
            LOG.exception(err)

    def set_simulation_model(self, simulation_model: SimulationModel) -> None:
        self._model = simulation_model

    def set_health_attrs(self) -> None:
        self._health = HumanHealth()

    def set_social_attrs(self, attrs: Any = None) -> None:
        if attrs is not None:
            self._social_attrs = HumanSocial()
        else:
            self._social_attrs = None

    def set_physical_attrs(self, attrs: Any = None) -> None:
        if attrs is not None:
            self._physical_attrs = HumanPhysical()
            self._physical_attrs = attrs.get("age", 0)
            self._physical_attrs = attrs.get("height", 0.0)
            self._physical_attrs = attrs.get("weigh", 0.0)
        else:
            self._physical_attrs = None

    def set_psychological_attrs(self, attrs: Any = None) -> None:
        if attrs is not None:
            self._psychological_attrs = HumanPsychological()
        else:
            self._psychological_attrs = None

    def set_routine(self, routine: Routine) -> None:
        self._routine = routine

    def set_high_level_behaviour_controller(self) -> None:
        self._high_level_behaviour = HighLevelBehaviour()

    def set_occupation(self, occupation: Occupation = None) -> None:
        if occupation is not None:
            self._occupation = occupation
        else:
            self._occupation = None
