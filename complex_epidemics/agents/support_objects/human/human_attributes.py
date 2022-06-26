import importlib
import logging
from typing import Any

from complex_epidemics.agents.support_objects.disease.immunity_instance import (
    ImmunityInstance,
)
from complex_epidemics.agents.support_objects.human.health_protection_measures import (
    ProtectionMeasureType,
)
from complex_epidemics.agents.support_objects.human.health_states import HealthState
from complex_epidemics.model.support_objects.abstract_model_step_helpers import (
    IModelStepper,
)
from complex_epidemics.utils.exceptions import InvalidOptionError

LOG = logging.getLogger(__name__)


class HumanHealth(IModelStepper):

    __slots__ = (
        "_health_state",
        "_diseases",
        "_is_susceptible",
        "_is_infectious",
        "_protection_measures",
    )

    def __init__(self) -> None:
        self._health_state: HealthState = HealthState.HEALTHY
        self._diseases: list = list()
        self._immunity: list = list()
        self._is_susceptible: bool = True
        self._is_infectious: bool = False
        self._protection_measures: dict = dict()

    @property
    def health_state(self) -> HealthState:
        return self._health_state

    @health_state.setter
    def health_state(self, state: HealthState) -> None:
        self._health_state = state

    @property
    def is_susceptible(self) -> bool:
        return self._is_susceptible

    @is_susceptible.setter
    def is_susceptible(self, value: bool) -> None:
        self._is_susceptible = value

    @property
    def is_infectious(self) -> bool:
        return self._is_infectious

    @is_infectious.setter
    def is_infectious(self, value: bool) -> None:
        self._is_infectious = value

    @property
    def protection_measures(self) -> dict:
        return self._protection_measures

    @property
    def diseases(self) -> list:
        return self._diseases

    @property
    def immunity(self) -> list:
        return self._immunity

    def start_protection_measure(
        self, measure: ProtectionMeasureType, options: Any = None
    ) -> None:
        match measure:
            case ProtectionMeasureType.HANDWASHING:
                measure_module = importlib.import_module(
                    f"complex_epidemics.agents."
                    f"support_objects.human."
                    f"health_protection_measures"
                )
                measure_class = getattr(
                    measure_module, f"{ProtectionMeasureType.HANDWASHING.value}"
                )
                measure_obj = measure_class()
            case ProtectionMeasureType.MASKWEARING:
                if options is None:
                    LOG.error("Missing mask type input.")
                    raise ValueError("Missing mask type input.")
                else:
                    measure_module = importlib.import_module(
                        f"complex_epidemics.agents."
                        f"support_objects.human."
                        f"health_protection_measures"
                    )
                    measure_class = getattr(
                        measure_module, f"{ProtectionMeasureType.MASKWEARING.value}"
                    )
                    measure_obj = measure_class(options)
            case ProtectionMeasureType.SOCIALDISTANCING:
                measure_module = importlib.import_module(
                    f"complex_epidemics.agents."
                    f"support_objects.human."
                    f"health_protection_measures"
                )
                measure_class = getattr(
                    measure_module, f"{ProtectionMeasureType.SOCIALDISTANCING.value}"
                )
                measure_obj = measure_class()
            case _:
                LOG.debug("Protection measure type option not implemented.")
                raise InvalidOptionError(
                    "Protection measure type option not implemented."
                )

        self._protection_measures[measure.name] = measure_obj

    def drop_protection_behaviour(self, measure: ProtectionMeasureType) -> None:
        if self.protection_measures is not None or len(self.protection_measures) != 0:
            self._protection_measures.pop(measure.name)

    def update_susceptibility(self):
        if self.health_state != HealthState.DECEASED:
            all_instances = self._diseases + self._immunity
            for instance in all_instances:
                if instance.active:
                    self.is_susceptible = False
                else:
                    self.is_susceptible = True
        else:
            self.is_susceptible = False

    def add_disease_instance(self, instance: Any):
        self._diseases.append(instance)

    def add_immunity_instance(self, disease: Any):
        self._immunity.append(ImmunityInstance(disease=disease))

    def step(self):
        LOG.debug("HumanHealth step method called.")
        if len(self._diseases) != 0:
            for disease_instance in self._diseases:
                if disease_instance.active:
                    disease_instance.step()
        if len(self._immunity) != 0:
            for immunity_instance in self._immunity:
                if immunity_instance.active:
                    immunity_instance.step()
        self.update_susceptibility()


class HumanSocial(IModelStepper):
    def __init__(self) -> None:
        pass

    def step(self):
        pass


class HumanPhysical(IModelStepper):
    def __init__(self) -> None:
        self._age: int = 0
        self._height: float = 0.0
        self._weight: float = 0.0

    @property
    def age(self) -> int:
        return self._age

    @age.setter
    def age(self, value: int) -> None:
        self._age = value

    @property
    def height(self) -> float:
        return self._height

    @height.setter
    def height(self, value: float) -> None:
        self._height = value

    @property
    def weight(self) -> float:
        return self._weight

    @weight.setter
    def weight(self, value: float) -> None:
        self._weight = value

    def step(self):
        pass


class HumanPsychological(IModelStepper):
    def __init__(self) -> None:
        pass

    def step(self):
        pass
