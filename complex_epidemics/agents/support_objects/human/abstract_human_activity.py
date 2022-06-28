import logging
from abc import ABC, abstractmethod
from datetime import time
from typing import Any, Union

from complex_epidemics.model.support_objects.abstract_model_step_helpers import (
    IModelStepper,
)

LOG = logging.getLogger(__name__)


class HumanBaseActivity(IModelStepper, ABC):

    __slots__ = [
        "_active",
        "_duration_controlled",
        "_duration",
        "_duration_counter",
        "_timed_controlled",
        "_start_time",
        "_end_time",
        "_position_controlled",
        "_start_position",
        "_final_position",
        "_state_controlled",
        "_initial_state",
        "_final_state",
        "movement_plan",
    ]

    def __init__(self, human: Any, **kwargs):
        self._human: Any = human
        self._active: bool = False
        self._started: bool = False
        self._duration_controlled: bool = False
        self._duration: int = kwargs.get("duration", 0)
        self._duration_counter = None
        self._time_controlled: bool = False
        self._start_time: time = kwargs.get("start_time", time(0, 0, 0))
        self._end_time: time = kwargs.get("end_time", time(0, 0, 0))
        self._position_controlled: bool = False
        self._start_position: int = kwargs.get("start_position", 0)
        self._final_position: int = kwargs.get("end_position", 0)
        self._state_controlled: bool = False
        self._initial_state: Any = kwargs.get("initial_state")
        self._final_state: Any = kwargs.get("final_state")
        self.movement_plan: list = list()

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
    def final_position(self) -> int:
        return self._final_position

    @final_position.setter
    def final_position(self, value: int) -> None:
        self._final_position = value

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

    def check_for_available_public_transport(
        self, destination: Any
    ) -> Union[int, str, None]:
        available_transports_ids = self._human.model.get_public_transports_for_route(
            origin=self._human.position, destination=destination
        )
        if len(available_transports_ids) != 0:
            available_transports_nominal_occupancy = dict()
            available_transports_effective_occupancy = dict()
            for transport_id in available_transports_ids:
                transport = self._human.model.get_agent_by_id(transport_id)
                position_availability = transport.check_for_available_position()
                available_transports_nominal_occupancy[
                    transport.graph_node_id
                ] = position_availability[0]
                available_transports_effective_occupancy[
                    transport.graph_node_id
                ] = position_availability[1]
            for (
                transport_id,
                has_position,
            ) in available_transports_nominal_occupancy.items():
                if has_position:
                    return transport_id
            for (
                transport_id,
                has_position,
            ) in available_transports_effective_occupancy.items():
                if has_position:
                    return transport_id
            return None
        else:
            return None

    def define_movement_plan(self, destination: Any) -> None:
        if destination is None or destination == 0:
            self.movement_plan = []
            return None
        plan = list()
        preference = self._human.transport_preference
        preference_class = preference.__class__.__name__
        if preference:
            if preference_class == "PrivateTransport":
                for vehicle in self._human.household.vehicles:
                    if not vehicle.in_use:
                        vehicle.in_use = True
                        vehicle.current_user = self._human.unique_id
                        plan.append(self._human.position)
                        plan.append(destination)
                    else:
                        plan.append(self._human.position)
                        plan.append(destination)
            elif preference_class == "PublicTransport":
                transport = self.check_for_available_public_transport(
                    destination=destination
                )
                if transport is not None:
                    plan.append(transport)
                    plan.append(destination)
                else:
                    plan.append(destination)
        else:
            transport = self.check_for_available_public_transport(
                destination=destination
            )
            if transport is not None:
                plan.append(transport)
                plan.append(destination)
            else:
                plan.append(self._human.position)
                plan.append(destination)
        self.movement_plan = plan

    def end_condition_checker(self):
        defined_condition = (
            self.duration_controlled,
            self.time_controlled,
            self.position_controlled,
            self.state_controlled,
        )

        # duration_true = self.duration_counter == self.duration
        # time_true = self._human.model.clock.get_datetime().time() == self.end_time
        # position_true = self._human.position == self.final_position
        # state_true = self._human.health.health_state == self.final_state

        calculated_condition = (
            self.duration_counter == self.duration,
            self._human.model.clock.get_datetime().time() == self.end_time,
            self._human.position == self.final_position,
            self._human.health.health_state == self.final_state,
        )

        LOG.debug(f"End condition checker: calculated = {calculated_condition}.")
        LOG.debug(f"End condition checker: defined = {defined_condition}.")

        if self.duration_controlled:
            self.duration_counter += 1

        if calculated_condition == defined_condition:
            LOG.debug(f"End condition checker: condition reached.")
            self.duration_counter = None
            self.active = False
            self.started = False

        # match composite_condition:
        #     case (False, False, False, False):
        #         LOG.error(
        #             "All end conditions types flags are false. At least one end condition MUST be set."
        #         )
        #         raise ConfigurationError(
        #             "All end conditions types flags are false. At least one end condition MUST be set."
        #         )
        #     case (True, False, False, False):
        #         self.duration_counter += 1
        #         if duration_true:
        #             self.duration_counter = 0
        #             self.active = False
        #             self.started = False
        #
        #     case (False, True, False, False):
        #         if time_true:
        #             self.active = False
        #             self.started = False
        #
        #     case (True, True, False, False):
        #         self.duration_counter += 1
        #         if duration_true and time_true:
        #             self.active = False
        #             self.started = False
        #             self.duration_counter = 0
        #
        #     case (False, False, True, False):
        #         if position_true:
        #             self.active = False
        #             self.started = False
        #
        #     case (True, False, True, False):
        #         self.duration_counter += 1
        #         if duration_true and position_true:
        #             self.active = False
        #             self.started = False
        #             self.duration_counter = 0
        #
        #     case (True, True, True, False):
        #         self.duration_counter += 1
        #         if duration_true and time_true and position_true:
        #             self.active = False
        #             self.started = False
        #             self.duration_counter = 0
        #
        #     case (False, False, False, True):
        #         if state_true:
        #             self.active = False
        #             self.started = False
        #
        #     case (True, False, False, True):
        #         self.duration_counter += 1
        #         if duration_true and state_true:
        #             self.active = False
        #             self.started = False
        #             self.duration_counter = 0
        #
        #     case (False, True, False, True):
        #         if time_true and state_true:
        #             self.active = False
        #             self.started = False
        #
        #     case (True, True, False, True):
        #         self.duration_counter += 1
        #         if duration_true and time_true and state_true:
        #             self.active = False
        #             self.started = False
        #             self.duration_counter = 0
        #
        #     case (False, False, True, True):
        #         if position_true and state_true:
        #             self.active = False
        #             self.started = False
        #
        #     case (True, False, True, True):
        #         self.duration_counter += 1
        #         if duration_true and position_true and state_true:
        #             self.active = False
        #             self.started = False
        #             self.duration_counter = 0
        #
        #     case (False, True, True, True):
        #         if time_true and position_true and state_true:
        #             self.active = False
        #             self.started = False
        #
        #     case (True, True, True, True):
        #         self.duration_counter += 1
        #         if duration_true and time_true and position_true and state_true:
        #             self.active = False
        #             self.started = False
        #             self.duration_counter = 0

    def step(self):
        if not self.started:
            self.start_logic()
            self.started = True
            self.activity_logic()
            self.end_condition_checker()
        else:
            self.activity_logic()
            self.end_condition_checker()
