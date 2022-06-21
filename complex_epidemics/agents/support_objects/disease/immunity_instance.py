import logging
from typing import Any

from complex_epidemics.agents.disease import Disease
from complex_epidemics.agents.support_objects.time_counter import TimeCounter
from complex_epidemics.model.support_objects.abstract_model_step_helpers import (
    IModelStepper,
)

LOG = logging.getLogger(__name__)


class ImmunityInstance(IModelStepper):

    __slots__ = (
        "_active",
        "_disease",
        "_expiration",
        "_step_counter",
        "_clock",
    )

    def __init__(self, disease: Disease) -> None:
        self._active: bool = True
        self._disease = disease
        self._expiration: int = disease.immunity_window_in_days
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
    def expiration(self) -> int:
        return self.expiration

    @expiration.setter
    def expiration(self, value: int) -> None:
        self._step_counter = value

    @property
    def step_counter(self) -> int:
        return self._step_counter

    @step_counter.setter
    def step_counter(self, value: int) -> None:
        self._step_counter = value

    def step(self):
        if self.active:
            LOG.debug(f"Immunity instance clock: {self.clock.counter}")
            LOG.debug(f"Immunity instance step counter: {self.step_counter}")
            if self.step_counter % self.disease.model.steps_per_day == 0:
                if self.clock.counter < self.expiration:
                    self.clock.increment()
                else:
                    self.active = False
                    return
            self.step_counter += 1
