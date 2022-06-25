from datetime import time
from enum import Enum, auto

from complex_epidemics.agents.support_objects.human.abstract_human_activity import HumanBaseActivity
from complex_epidemics.agents.support_objects.human.human_activities import CommonActivity, EntertainmentActivity, \
    HomeHealthCareActivity, \
    OccupationActivity, \
    ReturnHomeActivity, SpecializedHealthCareActivity
from complex_epidemics.agents.support_objects.human.human_attributes import HealthState
from complex_epidemics.model.support_objects.abstract_model_step_helpers import (
    IModelAdvancer, IModelStepper,
)

class Routine(Enum):
    SIMPLE = auto()
    STANDARD = auto()
    SOPHISTICATED = auto()


class LowLevelBehaviour(IModelStepper):

    __slots__ = [
        "_human",
        "_common_activities",
        "_last_activity",
        "_running_activity",
        "_next_activity",
        "_day_planning"
    ]

    def __init__(self, human_agent, routine: Routine) -> None:
        self._human = human_agent
        self._common_activities: dict = {
            CommonActivity.RETURNHOME: ReturnHomeActivity(self._human),
            CommonActivity.OCCUPATION: OccupationActivity(self._human),
            CommonActivity.ENTERTAINMENT: EntertainmentActivity(self._human),
            CommonActivity.HOMEHEALTHCARE: HomeHealthCareActivity(self._human),
            CommonActivity.SPECIALIZEDHEALTHCARE: SpecializedHealthCareActivity(self._human),
        }
        self._last_activity = None
        self._running_activity = None
        self._next_activity = self._common_activities[CommonActivity.RETURNHOME]
        self._day_planning: list = list()
        self._routine: Routine = routine

    def simple_routine(self):

    def standard_routine(self):

    def sophisticated_routine(self):

    def generate_day_plan(self):
        if
        weekday = self._human.model.clock.weekday() in {0,1,2,3,4}
        healthy = self._human.health.health_state == HealthState.HEALTHY
        if weekday and healthy:
            self._common_activities[
                CommonActivity.OCCUPATION].start_time = self._human.occupation.occupation_locale.activity_time.start
            self._day_planning.append(self._common_activities[CommonActivity.OCCUPATION])
            self._day_planning.append(self._common_activities[CommonActivity.RETURNHOME])
        elif not weekday and healthy:
            self._day_planning.append(self._common_activities[CommonActivity.ENTERTAINMENT])
            self._day_planning.append(self._common_activities[CommonActivity.RETURNHOME])


    def step(self):
        model_time = self._human.model.clock.time
        if model_time == time(0, 0, 0):
            self.generate_day_plan()

        if self._human.health.health_state == HealthState.SICK:
            self.

        if self._running_activity:
            if self._running_activity.active:
                self._running_activity.step()
            else:
                self._last_activity = self._running_activity
                self._running_activity = self._next_activity if self._next_activity else None
                self._next_activity = self._day_planning.pop(0) if len(self._day_planning) > 0 else None
                self._running_activity.active = True
                self._running_activity.step()
        else:
            if len(self._day_planning) > 0 and self._day_planning[0].start_time == model_time:
                self._running_activity = self._day_planning.pop(0)
                self._next_activity = self._day_planning.pop(0) if len(self._day_planning) > 0 else None




class HighLevelBehaviour(IModelAdvancer):
    def __init__(self) -> None:
        pass

    def advance(self):
        pass
