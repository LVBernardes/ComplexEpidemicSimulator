import logging
from datetime import time
from enum import IntEnum
from typing import Any

import numpy as np

from complex_epidemics.agents.support_objects.human.human_activities import (
    CommonActivity,
    HomeHealthCareActivity,
    LongEntertainmentActivity,
    OccupationActivity,
    ReturnHomeActivity,
    ShortEntertainmentActivity,
    SpecializedHealthCareActivity,
)
from complex_epidemics.agents.support_objects.human.health_states import HealthState
from complex_epidemics.model.support_objects.abstract_model_step_helpers import (
    IModelStepper,
)
from complex_epidemics.utils.distributions_utils import DistUtils
from complex_epidemics.utils.exceptions import InvalidOptionError

LOG = logging.getLogger(__name__)


class Routine(IntEnum):
    SIMPLE = 0
    STANDARD = 1
    SOPHISTICATED = 2


class LowLevelBehaviour(IModelStepper):

    __slots__ = [
        "_human",
        "_routine",
        "_last_activity",
        "_running_activity",
        "_next_activity",
        "_day_planning",
        "_common_activities",
    ]

    def __init__(self, human_agent: Any, routine: Routine) -> None:
        self._human: Any = human_agent
        self._routine: Routine = routine
        self._last_activity = None
        self._running_activity = None
        self._day_planning: list = list()
        self._common_activities: dict = {
            CommonActivity.RETURNHOME: ReturnHomeActivity(self._human),
            CommonActivity.OCCUPATION: OccupationActivity(self._human),
            CommonActivity.SHORTENTERTAINMENT: ShortEntertainmentActivity(self._human),
            CommonActivity.LONGENTERTAINMENT: LongEntertainmentActivity(self._human),
            CommonActivity.HOMEHEALTHCARE: HomeHealthCareActivity(self._human),
            CommonActivity.SPECIALIZEDHEALTHCARE: SpecializedHealthCareActivity(
                self._human
            ),
        }
        self._next_activity = self._common_activities[CommonActivity.RETURNHOME]

    @property
    def routine(self) -> Routine:
        return self._routine

    @property
    def day_planning(self) -> list:
        return self._day_planning

    def generate_simple_routine(self):
        is_healthy = self._human.health.health_state == HealthState.HEALTHY
        original_time = self._human.occupation.locale._activity_time.get(
            "start_time"
        )
        delayed_time_hour = original_time.hour - 1
        delayed_time_minute = original_time.minute
        if is_healthy:
            self._common_activities[CommonActivity.OCCUPATION].start_time = time(
                hour=delayed_time_hour, minute=delayed_time_minute
            )
            self._day_planning.append(self._common_activities[CommonActivity.OCCUPATION])
            self._day_planning.append(self._common_activities[CommonActivity.RETURNHOME])

    def generate_standard_routine(self):
        model_time = self._human.model.clock.get_datetime()
        is_weekday = model_time.weekday() in {0, 1, 2, 3, 4}
        is_healthy = self._human.health.health_state == HealthState.HEALTHY
        if is_weekday and is_healthy:
            original_time = self._human.occupation.locale._activity_time.get(
                "start_time"
            )
            delayed_time_hour = original_time.hour - 1
            delayed_time_minute = original_time.minute
            self._common_activities[CommonActivity.OCCUPATION].start_time = time(
                hour=delayed_time_hour, minute=delayed_time_minute
            )
            self._day_planning.append(
                self._common_activities[CommonActivity.OCCUPATION]
            )
            self._day_planning.append(
                self._common_activities[CommonActivity.RETURNHOME]
            )
        elif not is_weekday and is_healthy:
            long_entert_start_time = time(hour=DistUtils.uniform(8, 11)[0])
            self._common_activities[
                CommonActivity.LONGENTERTAINMENT
            ].start_time = long_entert_start_time
            self._day_planning.append(
                self._common_activities[CommonActivity.LONGENTERTAINMENT]
            )
            self._day_planning.append(
                self._common_activities[CommonActivity.RETURNHOME]
            )

    def generate_sophisticated_routine(self):
        model_time = self._human.model.clock.get_datetime()
        is_weekday = model_time.weekday() in {0, 1, 2, 3, 4}
        is_healthy = self._human.health.health_state == HealthState.HEALTHY
        if is_weekday and is_healthy:
            original_time = self._human.occupation.locale._activity_time.get(
                "start_time"
            )
            delayed_time_hour = original_time.hour - 1
            delayed_time_minute = original_time.minute
            self._common_activities[CommonActivity.OCCUPATION].start_time = time(
                hour=delayed_time_hour, minute=delayed_time_minute
            )
            self._day_planning.append(
                self._common_activities[CommonActivity.OCCUPATION]
            )
            if np.random.default_rng().choice([True, False]):
                self._day_planning.append(
                    self._common_activities[CommonActivity.SHORTENTERTAINMENT]
                )
            self._day_planning.append(
                self._common_activities[CommonActivity.RETURNHOME]
            )
        elif not is_weekday and is_healthy:
            long_entert_start_time = time(hour=DistUtils.uniform(8, 11)[0])
            self._common_activities[
                CommonActivity.LONGENTERTAINMENT
            ].start_time = long_entert_start_time
            self._day_planning.append(
                self._common_activities[CommonActivity.LONGENTERTAINMENT]
            )
            self._day_planning.append(
                self._common_activities[CommonActivity.RETURNHOME]
            )

    def generate_day_plan(self) -> None:
        if self.routine == Routine.SIMPLE:
            self.generate_simple_routine()
        elif self.routine == Routine.STANDARD:
            self.generate_standard_routine()
        elif self.routine == Routine.SOPHISTICATED:
            self.generate_sophisticated_routine()
        else:
            LOG.error("Routine option is not implemented.")
            raise InvalidOptionError("Routine option is not implemented.")

    def step(self) -> None:
        model_datetime = self._human.model.clock.get_datetime()
        # print(f"Model time: {model_datetime} ")
        if model_datetime.time() == time(3, 0, 0):
            self.generate_day_plan()
            # print(
            #     f"Generated plan: {[activity.__class__.__name__ for activity in self._day_planning]}"
            # )

        if (
            self._human.health.health_state == HealthState.SICK
            and self._running_activity
            != self._common_activities[CommonActivity.HOMEHEALTHCARE]
        ):
            self._day_planning = list()
            self._running_activity = self._common_activities[
                CommonActivity.HOMEHEALTHCARE
            ]
            self._next_activity = None
            self._running_activity.active = True
            self._running_activity.step()

        elif (
            (self._human.health.health_state == HealthState.DEBILITADED
             or self._human.health.health_state == HealthState.INCAPACITATED)
            and self._running_activity
            != self._common_activities[CommonActivity.SPECIALIZEDHEALTHCARE]
        ):
            self._day_planning = list()
            self._running_activity = self._common_activities[
                CommonActivity.SPECIALIZEDHEALTHCARE
            ]
            self._next_activity = self._common_activities[
                CommonActivity.RETURNHOME
            ]
            self._running_activity.active = True
            self._running_activity.step()

        elif self._running_activity:
            if self._running_activity.active:
                # print(
                #     f"Executing activity: {self._running_activity.__class__.__name__}."
                # )
                self._running_activity.step()
            else:
                self._last_activity = self._running_activity
                self._running_activity = (
                    self._next_activity if self._next_activity else None
                )
                self._next_activity = (
                    self._day_planning.pop(0) if len(self._day_planning) > 0 else None
                )
                if self._running_activity:
                    self._running_activity.active = True
                    self._running_activity.step()
        else:
            # if len(self._day_planning) > 0:
            #     print(
            #         f"First activity of the day starts at: {self._day_planning[0].start_time}"
            #     )
            if (
                len(self._day_planning) > 0
                and self._day_planning[0].start_time == model_datetime.time()
            ):
                self._running_activity = self._day_planning.pop(0)
                self._next_activity = (
                    self._day_planning.pop(0) if len(self._day_planning) > 0 else None
                )
                self._running_activity.active = True
                self._running_activity.step()
