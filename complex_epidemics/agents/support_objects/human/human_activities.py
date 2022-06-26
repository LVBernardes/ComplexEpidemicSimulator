import logging
from enum import Enum
from typing import Any

from complex_epidemics.agents.support_objects.human.abstract_human_activity import (
    HumanBaseActivity,
)
from complex_epidemics.agents.support_objects.human.health_states import HealthState
from complex_epidemics.utils.distributions_utils import DistUtils

LOG = logging.getLogger(__name__)


class OccupationActivity(HumanBaseActivity):
    def __init__(self, human: Any):
        super().__init__(human=human)

    def start_logic(self):
        self.time_controlled = True
        self.position_controlled = True
        self.end_time = self.human.occupation.occupation_locale.activity_time.get(
            "end_time"
        )
        self.final_position = self.human.occupation.occupation_locale.graph_node_id
        self.define_movement_plan(destination=self.final_position)

    def activity_logic(self):
        if len(self.movement_plan) != 0:
            # print(f"Agent next position: {self.movement_plan[0]}")
            self._human.change_position(self.movement_plan.pop(0))


class ShortEntertainmentActivity(HumanBaseActivity):
    def __init__(self, human: Any):
        super().__init__(human=human)

    def start_logic(self):
        self.duration_controlled = True
        self.position_controlled = True
        self.duration_counter = 0
        self.final_position = self.human.entertainment.graph_node_id
        self.duration = DistUtils.uniform(1, 2)
        self.define_movement_plan(destination=self.final_position)

    def activity_logic(self):
        if len(self.movement_plan) != 0:
            # print(f"Agent next position: {self.movement_plan[0]}")
            self._human.change_position(self.movement_plan.pop(0))


class LongEntertainmentActivity(HumanBaseActivity):
    def __init__(self, human: Any):
        super().__init__(human=human)

    def start_logic(self):
        self.duration_controlled = True
        self.position_controlled = True
        self.duration_counter = 0
        self.final_position = self.human.entertainment.graph_node_id
        self.duration = DistUtils.uniform(5, 8)
        self.define_movement_plan(destination=self.final_position)

    def activity_logic(self):
        if len(self.movement_plan) != 0:
            # print(f"Agent next position: {self.movement_plan[0]}")
            self._human.change_position(self.movement_plan.pop(0))


class HomeHealthCareActivity(HumanBaseActivity):
    def __init__(self, human: Any):
        super().__init__(human=human)

    def start_logic(self):
        self.position_controlled = True
        self.state_controlled = True
        self.final_position = self.human.household.graph_node_id
        self.initial_state = HealthState.SICK
        self.final_state = HealthState.HEALTHY
        self.define_movement_plan(destination=self.final_position)

    def activity_logic(self):
        if len(self.movement_plan) != 0:
            # print(f"Agent next position: {self.movement_plan[0]}")
            self._human.change_position(self.movement_plan.pop(0))


class SpecializedHealthCareActivity(HumanBaseActivity):
    def __init__(self, human: Any):
        super().__init__(human=human)

    def start_logic(self):
        self.position_controlled = True
        self.state_controlled = True
        self.initial_state = HealthState.DEBILITADED
        self.final_state = HealthState.HEALTHY

    def activity_logic(self):
        pass


class ReturnHomeActivity(HumanBaseActivity):
    def __init__(self, human: Any):
        super().__init__(human=human)

    def start_logic(self):
        self.position_controlled = True
        self.final_position = self.human.household.graph_node_id
        self.define_movement_plan(destination=self.final_position)

    def activity_logic(self):
        if len(self.movement_plan) != 0:
            # print(f"Agent next position: {self.movement_plan[0]}")
            self._human.change_position(self.movement_plan.pop(0))


class CommonActivity(Enum):
    OCCUPATION = OccupationActivity
    SHORTENTERTAINMENT = ShortEntertainmentActivity
    LONGENTERTAINMENT = LongEntertainmentActivity
    HOMEHEALTHCARE = HomeHealthCareActivity
    SPECIALIZEDHEALTHCARE = SpecializedHealthCareActivity
    RETURNHOME = ReturnHomeActivity
