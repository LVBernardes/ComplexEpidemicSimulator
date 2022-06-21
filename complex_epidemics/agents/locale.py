import logging

from complex_epidemics.agents.support_objects.base_agents import ContainerAgent
from complex_epidemics.agents.support_objects.human.human_occupation_categories import (
    GenericOccupationCategory,
    StudentCategory,
    WorkerCategory,
)
from complex_epidemics.model.simulation_model import SimulationModel

LOG = logging.getLogger(__name__)


class Locale(ContainerAgent):
    def __init__(self, unique_id: int, model: SimulationModel):
        super().__init__(unique_id=unique_id, model=model)
        self._essential = False
        self._assigned_occupations: set[
            WorkerCategory, StudentCategory, GenericOccupationCategory
        ]

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
        self._assigned_occupations: set[GenericOccupationCategory] = {
            category for category in GenericOccupationCategory
        }


class Workplace(Locale):
    def __init__(self, unique_id: int, model: SimulationModel):
        super().__init__(unique_id=unique_id, model=model)
        self._assigned_occupations: set[WorkerCategory] = {
            category
            for category in WorkerCategory
            if category.name in {"GENERIC", "INDUSTRY", "SERVICES"}
        }


class EducationalInstitution(Locale):
    def __init__(self, unique_id: int, model: SimulationModel):
        super().__init__(unique_id=unique_id, model=model)
        self._max_capacity_students: int = 0
        self._students_occupants: set[int] = set()
        self._assigned_occupations: set[StudentCategory] = {
            category for category in StudentCategory
        }

    @property
    def max_capacity_students(self) -> int:
        return self._max_capacity_students

    @max_capacity_students.setter
    def max_capacity_students(self, value: int) -> None:
        self._max_capacity_students = value

    @property
    def students_occupants(self) -> set[int]:
        return self._students_occupants

    @students_occupants.setter
    def students_occupants(self, value: set[int]) -> None:
        self._students_occupants = value

    def update_students_occupants(self) -> None:
        for agent_id in self.occupants:
            agent = self.model.schedule._agents[agent_id]
            if agent.occupation.category in self.assigned_occupations:
                self.students_occupants.add(agent_id)

    def step(self) -> None:
        self.update_occupants_from_graph_edges()
        self.update_students_occupants()


class HealthCareUnit(Locale):
    def __init__(self, unique_id: int, model: SimulationModel):
        super().__init__(unique_id=unique_id, model=model)
        self._max_capacity_patients: int = 0
        self._patients_occupants: set[int] = set()
        self._assigned_occupations: set[WorkerCategory] = {
            category for category in WorkerCategory if category.name == "HEALTH"
        }

    @property
    def max_capacity_patients(self) -> int:
        return self._max_capacity_patients

    @max_capacity_patients.setter
    def max_capacity_patients(self, value: int) -> None:
        self._max_capacity_patients = value

    @property
    def patients_occupants(self) -> set[int]:
        return self._patients_occupants

    @patients_occupants.setter
    def patients_occupants(self, value: set[int]) -> None:
        self._patients_occupants = value

    def update_patients_occupants(self) -> None:
        for agent_id in self.occupants:
            agent = self.model.schedule._agents[agent_id]
            if agent.occupation.category not in self.assigned_occupations:
                self.patients_occupants.add(agent_id)

    def step(self) -> None:
        self.update_occupants_from_graph_edges()
        self.update_patients_occupants()


class PublicPlace(Locale):
    def __init__(self, unique_id: int, model: SimulationModel):
        super().__init__(unique_id=unique_id, model=model)
        self._assigned_occupations: set[WorkerCategory] = {
            category
            for category in WorkerCategory
            if category.name in {"GENERIC", "SERVICES", "PUBLIC"}
        }


class CustomerServicesPlace(Workplace):
    def __init__(self, unique_id: int, model: SimulationModel):
        super().__init__(unique_id=unique_id, model=model)
        self._assigned_occupations: set[WorkerCategory] = {
            category for category in WorkerCategory if category.name == "SERVICES"
        }


class NonCustomerServicesPlace(Workplace):
    def __init__(self, unique_id: int, model: SimulationModel):
        super().__init__(unique_id=unique_id, model=model)
        self._assigned_occupations: set[WorkerCategory] = {
            category for category in WorkerCategory if category.name == "SERVICES"
        }


class Industry(Workplace):
    def __init__(self, unique_id: int, model: SimulationModel):
        super().__init__(unique_id=unique_id, model=model)
        self._assigned_occupations: set[WorkerCategory] = {
            category for category in WorkerCategory if category.name == "INDUSTRY"
        }
