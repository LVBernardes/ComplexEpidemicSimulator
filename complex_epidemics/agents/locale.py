import logging
from enum import Enum

from complex_epidemics.agents.support_objects.base_agents import ContainerAgent
from complex_epidemics.model.simulation_model import SimulationModel

LOG = logging.getLogger(__name__)


class HouseholdCategory(Enum):
    GENERIC = "Household"


class WorkplaceCategory(Enum):
    GENERIC = "Workplace"
    CUSTOMERSERVICESPLACE = "CustomerServicesPlace"
    NONCUSTOMERSERVICESPLACE = "NonCustomerServicesPlace"
    INDUSTRY = "Industry"


class EducationalInstitutionCategory(Enum):
    GENERIC = "EducationalInstitution"
    # PRIMARY = 'Primary'
    # SECONDARY = 'Secondary'
    # COLLEGE = 'College'


class HealthCareCategory(Enum):
    GENERIC = "HealthCareUnit"
    # SMALLCLINIC = 'SmallClinic'
    # LARGECLINIC = 'LargeClinic'
    # HOSPITAL = 'Hospital'


class PublicPlaceCategory(Enum):
    GENERIC = "PublicPlace"
    # PARK = 'Park'
    # THEATER = 'Theater'
    # MOVIETHEATER = 'Movietheater'


class Locale(ContainerAgent):
    def __init__(self, unique_id: int, model: SimulationModel):
        super().__init__(unique_id=unique_id, model=model)
        self._essential = False

    @property
    def essential(self) -> bool:
        return self._essential

    @essential.setter
    def essential(self, value: bool) -> None:
        self._essential: bool = value

    def step(self) -> None:
        self.update_occupants_from_graph_edges()


class Household(Locale):
    def __init__(self, unique_id: int, model: SimulationModel):
        super().__init__(unique_id=unique_id, model=model)


class Workplace(Locale):
    def __init__(self, unique_id: int, model: SimulationModel):
        super().__init__(unique_id=unique_id, model=model)


class EducationalInstitution(Locale):
    def __init__(self, unique_id: int, model: SimulationModel):
        super().__init__(unique_id=unique_id, model=model)
        self._max_capacity_students: int = 0
        self._occupation_students: int = 0

    @property
    def max_capacity_students(self) -> int:
        return self._max_capacity_students

    @max_capacity_students.setter
    def max_capacity_students(self, value: int) -> None:
        self._max_capacity_students = value

    @property
    def occupation_students(self) -> int:
        return self._occupation_students

    @occupation_students.setter
    def occupation_students(self, value: int) -> None:
        self._occupation_students = value


class HealthCareUnit(Locale):
    def __init__(self, unique_id: int, model: SimulationModel):
        super().__init__(unique_id=unique_id, model=model)
        self._max_capacity_patients: int = 0
        self._occupation_patients: int = 0

    @property
    def max_capacity_patients(self) -> int:
        return self._max_capacity_patients

    @max_capacity_patients.setter
    def max_capacity_patients(self, value: int) -> None:
        self._max_capacity_patients = value

    @property
    def occupations_patients(self) -> int:
        return self._occupation_patients

    @occupations_patients.setter
    def occupations_patients(self, value: int) -> None:
        self._occupation_patients = value


class PublicPlace(Locale):
    def __init__(self, unique_id: int, model: SimulationModel):
        super().__init__(unique_id=unique_id, model=model)


class CustomerServicesPlace(Workplace):
    def __init__(self, unique_id: int, model: SimulationModel):
        super().__init__(unique_id=unique_id, model=model)


class NonCustomerServicesPlace(Workplace):
    def __init__(self, unique_id: int, model: SimulationModel):
        super().__init__(unique_id=unique_id, model=model)


class Industry(Workplace):
    def __init__(self, unique_id: int, model: SimulationModel):
        super().__init__(unique_id=unique_id, model=model)
