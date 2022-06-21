import logging
from typing import Any

import numpy as np

from complex_epidemics.agents.support_objects.human.human_occupation_categories import (
    GenericOccupationCategory,
    StudentCategory,
    WorkerCategory,
)
from complex_epidemics.agents.support_objects.occupation_locale_assigments import (
    OccupationToLocale,
)
from complex_epidemics.model.support_objects.abstract_model_step_helpers import (
    IModelStepper,
)

LOG = logging.getLogger(__name__)


class Occupation(IModelStepper):

    __slots__ = [
        "_category",
        "_occupation_locale",
        "_is_transport_required",
        "_transport_preference",
        "_transport_category_preference",
        "_is_economic_active",
        "_activities",
    ]

    def __init__(self) -> None:
        self._category: Any = None
        self._human: Any = None
        self._occupation_locale: Any = None
        self._is_occupation_locale_assigned: bool = False
        self._is_transport_required: bool = False
        self._transport_category_preference: Any = None
        self._transport_preference: Any = None
        self._is_economic_active: bool = False
        self._activities: list = []

    @property
    def category(self) -> Any:
        return self._category

    @category.setter
    def category(self, value: Any) -> None:
        self._category = value

    @property
    def occupation_locale(self) -> Any:
        return self._occupation_locale

    @occupation_locale.setter
    def occupation_locale(self, value: Any) -> None:
        self._occupation_locale = value

    @property
    def is_occupation_locale_assigned(self) -> bool:
        return self._is_occupation_locale_assigned

    @is_occupation_locale_assigned.setter
    def is_occupation_locale_assigned(self, value: bool) -> None:
        self._is_occupation_locale_assigned = value

    @property
    def is_transport_required(self) -> bool:
        return self._is_transport_required

    @is_transport_required.setter
    def is_transport_required(self, value: bool) -> None:
        self._is_transport_required = value

    @property
    def transport_category_preference(self) -> Any:
        return self._transport_category_preference

    @transport_category_preference.setter
    def transport_category_preference(self, value: Any) -> None:
        self._transport_category_preference = value

    @property
    def transport_preference(self) -> Any:
        return self._transport_preference

    @transport_preference.setter
    def transport_preference(self, value: Any) -> None:
        self._transport_preference = value

    @property
    def is_economic_active(self) -> bool:
        return self._is_economic_active

    @is_economic_active.setter
    def is_economic_active(self, value: bool) -> None:
        self._is_economic_active = value

    def assign_occupation_locale(self) -> None:
        rng = np.random.default_rng()
        loop_counter = 0
        own_occupation = f"{self.category.__class__.__name__}{self.category.name}"
        locales_classes = OccupationToLocale[own_occupation].value
        for locale_class in locales_classes:
            real_locale_id_list = self._human.model.get_agents_by_class(locale_class)
            if real_locale_id_list:
                while not self.is_occupation_locale_assigned and loop_counter < 10:
                    real_locale_id = rng.choice(real_locale_id_list)
                    real_locale = self._human.model.schedule._agents[real_locale_id]
                    loop_counter += 1
                    if (
                        len(real_locale.assigned_occupations)
                        < real_locale.max_capacity_nominal
                    ):
                        LOG.debug(
                            f'Assigning agent with ID "{self._human.graph_node_id}" and occupation "{self.category.__class__.__name__}.{self.category.name}" to locale with ID "{real_locale_id}" and class"{real_locale.__class__.__name__}".'
                        )
                        real_locale.add_assigned_occupant(self._human.graph_node_id)
                        self.occupation_locale = real_locale_id
                        self.is_occupation_locale_assigned = True
                        return None
                if not self.is_occupation_locale_assigned:
                    LOG.error("DID NOT found a suitable locale to be assigned.")
                    raise Exception("DID NOT found a suitable locale to be assigned.")

    def step(self):
        if not self.is_occupation_locale_assigned:
            self.assign_occupation_locale()


class Worker(Occupation):
    def __init__(self) -> None:
        super().__init__()
        self._category: WorkerCategory = WorkerCategory.GENERIC
        self._is_economic_active: bool = True
        self._activities: list = []


class Student(Occupation):
    def __init__(self) -> None:
        super().__init__()
        self._category: StudentCategory = StudentCategory.GENERIC
        self._is_economic_active: bool = False
        self._activities: list = []


class GenericOccupation(Occupation):
    def __init__(self) -> None:
        super().__init__()
        self._category: GenericOccupationCategory = GenericOccupationCategory.GENERIC
        self._is_economic_active: bool = False
        self._activities: list = []
