from enum import Enum
from typing import Any

from complex_epidemics.model.support_objects.abstract_model_stepper import IModelStepper


class WorkerCategory(Enum):
    GENERIC = "GenericWorker"
    HEALTH = "HealthWorker"
    INDUSTRY = "IndustryWorker"
    SERVICES = "ServicesWorker"
    EDUCATION = "EducationWorker"


class StudentCategory(Enum):
    GENERIC = "GenericStudent"
    ELEMENTARY = "ElementaryStudent"
    MIDDLESCHOOL = "MiddleSchoolStudent"
    HIGHSCHOOL = "HighSchoolStudent"
    COLLEGE = "CollegeStudent"


class GenericOccupationCategory(Enum):
    GENERIC = "GenericOccupation"
    HOUSECARE = "Housecare"
    RETIRED = "Retired"
    INFANT = "Infant"


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
        self._occupation_locale: Any = None
        self._is_transport_required: bool = False
        self._transport_category_preference: Any = None
        self._transport_preference: Any = None
        self._is_economic_active: bool = False
        self._activities: list = []

    @property
    def occupation_locale(self) -> Any:
        return self._occupation_locale

    @occupation_locale.setter
    def occupation_locale(self, value: Any) -> None:
        self._occupation_locale = value

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

    def step(self):
        pass


class Worker(Occupation):
    def __init__(self) -> None:
        self._category: WorkerCategory = WorkerCategory.GENERIC
        self._is_economic_active: bool = True
        self._activities: list = []


class Student(Occupation):
    def __init__(self) -> None:
        self._category: StudentCategory = StudentCategory.GENERIC
        self._is_economic_active: bool = False
        self._activities: list = []


class GenericOccupation(Occupation):
    def __init__(self) -> None:
        self._category: GenericOccupationCategory = GenericOccupationCategory.GENERIC
        self._is_economic_active: bool = False
        self._activities: list = []
