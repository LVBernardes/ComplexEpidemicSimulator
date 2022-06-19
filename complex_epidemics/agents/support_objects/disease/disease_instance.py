from typing import Any

from complex_epidemics.agents.support_objects.disease.disease_states_and_symptoms import (
    BaseDiseaseInstanceState,
    DiseaseInstanceState,
    Symptoms,
)
from complex_epidemics.agents.support_objects.time_counter import TimeCounter
from complex_epidemics.model.support_objects.abstract_model_stepper import IModelStepper


class DiseaseInstance(IModelStepper):
    __slots__ = (
        "_active",
        "_state",
        "_symptoms_state",
        "_disease",
        "_host",
        "_all_states",
        "_step_counter",
        "_clock",
    )

    def __init__(self):
        self._active: bool = True
        self._state = None
        self._disease = None
        self._host = None
        self._all_states = dict()
        self._step_counter: int = 0
        self.clock: TimeCounter = TimeCounter()

    @property
    def active(self):
        return self._active

    @active.setter
    def active(self, value: bool) -> None:
        self._active = value

    @property
    def disease(self) -> Any:
        return self._disease

    @disease.setter
    def disease(self, value: Any) -> None:
        self._disease = value

    @property
    def host(self) -> Any:
        return self._host

    @host.setter
    def host(self, value: Any) -> None:
        self._host = value

    @property
    def state(self) -> BaseDiseaseInstanceState:
        return self._state

    @state.setter
    def state(self, value: BaseDiseaseInstanceState):
        self._state = value

    @property
    def all_states(self) -> dict:
        return self._all_states

    @all_states.setter
    def all_states(self, value: dict) -> None:
        self._all_states = value

    @property
    def step_counter(self) -> int:
        return self._step_counter

    @step_counter.setter
    def step_counter(self, value: int) -> None:
        self._step_counter = value

    def transition_to_state(self, state: tuple[DiseaseInstanceState, Symptoms]) -> None:
        if self.all_states and len(self.all_states) != 0:
            self.state = self.all_states.get(state)
            self.state.disease_instance = self
        else:
            raise ValueError('"all_states" property MUST NOT be empty.')

    def step(self):
        if self.active:
            print(f"Disease instance clock: {self.clock.counter}")
            print(f"Disease instance step counter: {self.step_counter}")
            if self.step_counter % self.disease.model.steps_per_day == 0:
                self._state.step()
                self.clock.increment()
            self.step_counter += 1
