import logging
from abc import ABC, abstractmethod
from datetime import time
from typing import Any

from complex_epidemics.agents.support_objects.human.human_attributes import HealthState
from complex_epidemics.model.support_objects.abstract_model_step_helpers import IModelStepper
from complex_epidemics.utils.exceptions import ConfigurationError

LOG = logging.getLogger(__name__)


class HumanBaseActivity(IModelStepper, ABC):

    __slots__ = [
        "_active",
        "_duration_controlled"
        "_duration",
        "_duration_counter",
        "_timed_controlled",
        "_start_time",
        "_end_time",
        "_position_controlled",
        "_start_position",
        "_end_position",
        "_state_controlled",
        "_final_state"
    ]

    def __init__(self, human: Any):
        self._human: Any = human
        self._active: bool = True
        self._started: bool = False
        self._duration_controlled: bool = False
        self._duration: int = 0
        self._duration_counter: int = 0
        self._time_controlled: bool = False
        self._start_time: time = time(0, 0, 0)
        self._end_time: time = time(0, 0, 0)
        self._position_controlled: bool = False
        self._start_position: int = 0
        self._end_position: int = 0
        self._state_controlled: bool = False
        self._initial_state: Any = None
        self._final_state: Any = None

    @property
    def human(self) -> Any:
        return self._human

    @property
    def started(self) -> bool:
        return self._started

    @started.setter
    def started(self, value: bool) -> None:
        self._started = value

    @property
    def active(self) -> bool:
        return self._active

    @active.setter
    def active(self, value: bool) -> None:
        self._active = value

    @property
    def duration_controlled(self) -> bool:
        return self._duration_controlled

    @duration_controlled.setter
    def duration_controlled(self, value: bool) -> None:
        self._duration_controlled = value

    @property
    def duration(self) -> int:
        return self._duration

    @duration.setter
    def duration(self, value: int) -> None:
        self._duration = value

    @property
    def duration_counter(self) -> int:
        return self._duration_counter

    @duration_counter.setter
    def duration_counter(self, value: int) -> None:
        self._duration_counter = value

    @property
    def time_controlled(self) -> bool:
        return self._time_controlled

    @time_controlled.setter
    def time_controlled(self, value: bool) -> None:
        self._time_controlled = value

    @property
    def start_time(self) -> time:
        return self._start_time

    @start_time.setter
    def start_time(self, value: time) -> None:
        self._start_time = value

    @property
    def end_time(self) -> time:
        return self._end_time

    @end_time.setter
    def end_time(self, value: time) -> None:
        self._end_time = value

    @property
    def position_controlled(self) -> bool:
        return self._position_controlled

    @position_controlled.setter
    def position_controlled(self, value: bool) -> None:
        self._position_controlled = value

    @property
    def start_position(self) -> int:
        return self._start_position

    @start_position.setter
    def start_position(self, value: int) -> None:
        self._start_position = value

    @property
    def end_position(self) -> int:
        return self._end_position

    @end_position.setter
    def end_position(self, value: int) -> None:
        self._end_position = value

    @property
    def state_controlled(self) -> bool:
        return self._state_controlled

    @state_controlled.setter
    def state_controlled(self, value: bool) -> None:
        self._state_controlled = value

    @property
    def initial_state(self) -> Any:
        return self._initial_state

    @initial_state.setter
    def initial_state(self, value: Any) -> None:
        self._initial_state = value

    @property
    def final_state(self) -> Any:
        return self._final_state

    @final_state.setter
    def final_state(self, value: Any) -> None:
        self._final_state = value

    @abstractmethod
    def start_logic(self):
        """Activity start procedure."""

    @abstractmethod
    def activity_logic(self):
        """Activity main logic."""

    def end_condition_checker(self):
        composite_condition = (
            self.duration_controlled,
            self.time_controlled,
            self.position_controlled,
            self.state_controlled
        )

        duration_true = self.duration_counter == self.duration
        time_true = self.human.model.clock.time == self.end_time
        position_true = self.human.model.position == self.end_position
        state_true = self.human.health.health_state == self.final_state

        match composite_condition:
            case (False, False, False, False):
                LOG.error('All end conditions types flags are false. At least one end condition MUST be set.')
                raise ConfigurationError('All end conditions types flags are false. At least one end condition MUST be set.')
            case (True, False, False, False):
                self.duration_counter += 1
                if duration_true:
                    self.duration_counter = 0
                    self.active = False
                    self.started = False

            case (False, True, False, False):
                if time_true:
                    self.active = False
                    self.started = False

            case (True, True, False, False):
                self.duration_counter += 1
                if duration_true and time_true:
                    self.active = False
                    self.started = False
                    self.duration_counter = 0

            case(False, False, True, False):
                if position_true:
                    self.active = False
                    self.started = False

            case(True, False, True, False):
                self.duration_counter += 1
                if duration_true and position_true:
                    self.active = False
                    self.started = False
                    self.duration_counter = 0

            case(True, True, True, False):
                self.duration_counter += 1
                if duration_true and time_true and position_true:
                    self.active = False
                    self.started = False
                    self.duration_counter = 0

            case(False, False, False, True):
                if state_true:
                    self.active = False
                    self.started = False

            case(True, False, False, True):
                self.duration_counter += 1
                if duration_true and state_true:
                    self.active = False
                    self.started = False
                    self.duration_counter = 0

            case(False, True, False, True):
                if time_true and state_true:
                    self.active = False
                    self.started = False

            case(True, True, False, True):
                self.duration_counter += 1
                if duration_true and time_true and state_true:
                    self.active = False
                    self.started = False
                    self.duration_counter = 0

            case(False, False, True, True):
                if position_true and state_true:
                    self.active = False
                    self.started = False

            case(True, False, True, True):
                self.duration_counter += 1
                if duration_true and position_true and state_true:
                    self.active = False
                    self.started = False
                    self.duration_counter = 0

            case(False, True, True, True):
                if time_true and position_true and state_true:
                    self.active = False
                    self.started = False

            case(True, True, True, True):
                self.duration_counter += 1
                if duration_true and time_true and position_true and state_true:
                    self.active = False
                    self.started = False
                    self.duration_counter = 0

    def step(self):
        if self.active:
            if self.started:
                self.start_logic()
                self.started = True
                self.activity_logic()
                self.end_condition_checker()
            else:
                self.activity_logic()
                self.end_condition_checker()


class OccupationActivity(HumanBaseActivity):

    def __init__(self, human: Any):
        super().__init__(human=human)

    def start_logic(self):
        self.time_controlled = True
        self.position_controlled = True
        self.end_time = self.human.occupation.occupation_locale.activity_time.end
        self.end_position = self.human.occupation.occupation_locale.graph_node_id

    def activity_logic(self):
        pass


class EntertainmentActivity(HumanBaseActivity):

    def __init__(self, human: Any):
        super().__init__(human=human)

    def start_logic(self):
        self.time_controlled = True
        self.position_controlled = True
        self.end_time = self.human.entertainment.activity_time.end
        self.end_position = self.human.entertainment.graph_node_id

    def activity_logic(self):
        pass


class HomeHealthCareActivity(HumanBaseActivity):

    def __init__(self, human: Any):
        super().__init__(human=human)

    def start_logic(self):
        self.position_controlled = True
        self.state_controlled = True
        self.end_position = self.human.household.graph_node_id
        self.initial_state = HealthState.SICK
        self.final_state = HealthState.HEALTHY

    def activity_logic(self):
        pass


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


class ReturnHome(HumanBaseActivity):

    def __init__(self, human: Any):
        super().__init__(human=human)

    def start_logic(self):
        self.position_controlled = True
        self.end_position = self.human.household.graph_node_id

    def activity_logic(self):
        pass
