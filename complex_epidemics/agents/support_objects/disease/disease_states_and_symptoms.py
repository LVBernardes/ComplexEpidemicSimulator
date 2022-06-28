import logging
from enum import Enum
from typing import Any

import numpy as np

from complex_epidemics.agents.support_objects.human.health_states import HealthState
from complex_epidemics.agents.support_objects.time_counter import TimeCounter
from complex_epidemics.model.support_objects.abstract_model_step_helpers import (
    IModelStepper,
)


LOG = logging.getLogger(__name__)


class DiseaseInstanceState(Enum):

    INCUBATED = "Incubated"
    INFECTIOUS = "Infectious"
    NONINFECTIOUS = "NonInfectious"


class Symptoms(Enum):
    NONE = "NoSymptoms"
    MILDMODERATE = "MildModerateSymptoms"
    SEVERE = "SevereSymptoms"
    CRITICAL = "CriticalSymptoms"
    DEATH = "Death"


class SymptomsToHealth(Enum):
    NONE = "HEALTHY"
    MILDMODERATE = "SICK"
    SEVERE = "DEBILITADED"
    CRITICAL = "INCAPACITATED"
    DEATH = "DECEASED"


class TimerCounter:
    pass


class BaseDiseaseInstanceState(IModelStepper):

    __slots__ = (
        "_active",
        "_disease_instance",
        "_clock",
        "_transition_table",
        "_transition_evaluator",
        "_infection_state",
        "_symptoms",
    )

    def __init__(self):
        self._active: bool = False
        self._disease_instance = Any
        self.clock: TimeCounter = TimeCounter()
        self._transition_table: dict = dict()
        self._transition_evaluator: Any = None
        self._infection_state = None
        self._symptoms = None

    @property
    def active(self) -> bool:
        return self._active

    @active.setter
    def active(self, value) -> None:
        self._active = value

    @property
    def disease_instance(self) -> Any:
        return self._disease_instance

    @disease_instance.setter
    def disease_instance(self, value: Any) -> None:
        self._disease_instance = value

    @property
    def transition_table(self) -> dict:
        return self._transition_table

    @transition_table.setter
    def transition_table(self, value: dict) -> None:
        self._transition_table = value

    def make_transition(self) -> bool:
        evaluator = self._transition_evaluator
        probability_of_transition = evaluator.cdf(self.disease_instance.clock.counter)
        # print(f"Transition probability: {probability_of_transition} .")
        result = np.random.choice(
            [True, False], p=[probability_of_transition, 1 - probability_of_transition]
        )
        # print(f"Make transition: {result} .")
        return result

    def choose_next_state(self) -> None:
        choices_names = dict()
        choices_probs = dict()
        for index, (key, value) in enumerate(self.transition_table.items()):
            choices_names[index] = key
            choices_probs[index] = value
        chosen = np.random.choice(
            a=list(choices_probs.keys()), p=list(choices_probs.values())
        )
        next_state = choices_names[chosen]
        # print(f"Next state: {next_state} .")
        self.disease_instance.transition_to_state(next_state)
        self.disease_instance.host.health.health_state = HealthState[
            SymptomsToHealth[next_state[1].name].value
        ]

    def step(self) -> None:
        # print(f"{self.__class__.__name__} state Clock: {self.clock.counter}")
        if self.make_transition():
            self.choose_next_state()
        self.clock.increment()


class IncubatedNoSymptoms(BaseDiseaseInstanceState):
    def __init__(self):
        super().__init__()
        self._infection_state = DiseaseInstanceState.INCUBATED
        self._symptoms = Symptoms.NONE

    def step(self) -> None:
        # print(f"{self.__class__.__name__} state Clock: {self.clock.counter}")
        if self.make_transition():
            self.choose_next_state()
            self.disease_instance.host.health.is_infectious = True
            LOG.info(f"Host '{self.disease_instance.host.unique_id} is now infectious.'")
        else:
            self.clock.increment()


class NonInfectiousNoSymptoms(BaseDiseaseInstanceState):
    def __init__(self):
        super().__init__()
        self._infection_state = DiseaseInstanceState.NONINFECTIOUS
        self._symptoms = Symptoms.NONE

    def step(self) -> None:
        self.disease_instance.host.health.is_infectious = False
        self.disease_instance.active = False
        self.disease_instance.host.health.add_immunity_instance(
            disease=self.disease_instance.disease
        )
        LOG.info(f"Agent recovered: '{self.disease_instance.host.unique_id}'.")


class NonInfectiousDeath(BaseDiseaseInstanceState):
    def __init__(self):
        super().__init__()
        self._infection_state = DiseaseInstanceState.NONINFECTIOUS
        self._symptoms = Symptoms.DEATH

    def step(self) -> None:
        self.disease_instance.host.health.is_infectious = False
        self.disease_instance.active = False


class InfectiousNoSymptoms(BaseDiseaseInstanceState):
    def __init__(self):
        super().__init__()
        self._infection_state = DiseaseInstanceState.INFECTIOUS
        self._symptoms = Symptoms.NONE


class InfectiousMildModerateSymptoms(BaseDiseaseInstanceState):
    def __init__(self):
        super().__init__()
        self._transition_table = {}
        self._infection_state = DiseaseInstanceState.INFECTIOUS
        self._symptoms = Symptoms.MILDMODERATE


class InfectiousSevereSymptoms(BaseDiseaseInstanceState):
    def __init__(self):
        super().__init__()
        self._transition_table = {}
        self._infection_state = DiseaseInstanceState.INFECTIOUS
        self._symptoms = Symptoms.SEVERE


class InfectiousCriticalSymptoms(BaseDiseaseInstanceState):
    def __init__(self):
        super().__init__()
        self._transition_table = {}
        self._infection_state = DiseaseInstanceState.INFECTIOUS
        self._symptoms = Symptoms.CRITICAL
