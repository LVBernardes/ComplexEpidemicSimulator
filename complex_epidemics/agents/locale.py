import logging
from datetime import time
from typing import Union

from complex_epidemics.agents.support_objects.base_agents import ContainerAgent
from complex_epidemics.agents.support_objects.human.health_states import HealthState
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
        self._activity_time: dict = {
            "start_time": time(0, 0, 0),
            "end_time": time(0, 0, 0),
        }
        # self._allowed_occupations: set[
        #     WorkerCategory, StudentCategory, GenericOccupationCategory
        # ]

    @property
    def essential(self) -> bool:
        return self._essential

    @essential.setter
    def essential(self, value: bool) -> None:
        self._essential: bool = value

    @property
    def activity_time(self) -> dict:
        return self._activity_time

    def remove_occupation_individual(self, agent_id) -> None:
        try:
            self._occupation_individuals.remove(agent_id)
            agent = self.model.get_agent_by_id(agent_id)
            agent.remove_occupation_attribute()
        except Exception as err:
            LOG.exception(err)

    def step(self) -> None:
        self.update_all_individuals_from_graph_edges()
        self.update_visiting_individuals()


class Household(Locale):
    def __init__(self, unique_id: int, model: SimulationModel):
        super().__init__(unique_id=unique_id, model=model)
        self._essential = True
        self._residents: list = list(Union[int, str])
        self._activity_time: dict = {
            "start_time": time(9, 0, 0),
            "end_time": time(18, 0, 0),
        }
        # self._allowed_occupations: set[GenericOccupationCategory] = {
        #     category for category in GenericOccupationCategory
        # }

    def add_occupation_individual(self, agent_id) -> None:
        try:
            self._occupation_individuals.add(agent_id)
            agent = self.model.get_agent_by_id(agent_id)
            if agent.physical and agent.physical.age != 0:
                if 0 < agent.physical.age <= 5:
                    agent.add_occupation_attribute(
                        self,
                        locale=self,
                        category=GenericOccupationCategory.INFANT
                    )
                elif 5 < agent.physical.age <= 18:
                    agent.add_occupation_attribute(
                        self,
                        locale=self,
                        category=GenericOccupationCategory.GENERIC
                    )
                elif 18 < agent.physical.age <= 65:
                    agent.add_occupation_attribute(
                        self,
                        locale=self,
                        category=GenericOccupationCategory.HOUSECARE
                    )
                elif 65 < agent.physical.age:
                    agent.add_occupation_attribute(
                        self,
                        locale=self,
                        category=GenericOccupationCategory.RETIRED
                    )
            else:
                agent.add_occupation_attribute(
                    self,
                    locale=self,
                    category=GenericOccupationCategory.GENERIC
                )
        except Exception as err:
            LOG.exception(err)

    def step(self) -> None:
        self.update_all_individuals_from_graph_edges()
        self.update_visiting_individuals()


class Workplace(Locale):
    def __init__(self, unique_id: int, model: SimulationModel):
        super().__init__(unique_id=unique_id, model=model)
        self._essential = False
        self._activity_time: dict = {
            "start_time": time(8, 00, 0),
            "end_time": time(17, 00, 0),
        }
        # self._allowed_occupations: set[WorkerCategory] = {
        #     category
        #     for category in WorkerCategory
        #     if category.name in {"GENERIC", "INDUSTRY", "SERVICES"}
        # }

    def add_occupation_individual(self, agent_id) -> None:
        try:
            self._occupation_individuals.add(agent_id)
            agent = self.model.get_agent_by_id(agent_id)
            agent.add_occupation_attribute(
                self,
                locale=self,
                category=WorkerCategory.GENERIC
            )
        except Exception as err:
            LOG.exception(err)

    def step(self) -> None:
        self.update_all_individuals_from_graph_edges()
        self.update_visiting_individuals()


class EducationalInstitution(Locale):
    def __init__(self, unique_id: int, model: SimulationModel):
        super().__init__(unique_id=unique_id, model=model)
        self._essential = False
        self._activity_time: dict = {
            "start_time": time(7, 0, 0),
            "end_time": time(13, 0, 0),
        }
        self._max_capacity_students: int = 0
        self._students: set[int] = set()
        # self._allowed_occupations: set[StudentCategory] = {
        #     category for category in StudentCategory
        # }

    def add_occupation_individual(self, agent_id) -> None:
        try:
            self._occupation_individuals.add(agent_id)
            agent = self.model.get_agent_by_id(agent_id)
            agent.add_occupation_attribute(
                self,
                locale=self,
                category=WorkerCategory.EDUCATION
            )
        except Exception as err:
            LOG.exception(err)

    @property
    def max_capacity_students(self) -> int:
        return self._max_capacity_students

    @max_capacity_students.setter
    def max_capacity_students(self, value: int) -> None:
        self._max_capacity_students = value

    @property
    def students(self) -> set[int]:
        return self._students

    def add_student(self, student_id: Union[int, str]) -> None:
        try:
            self._students.add(student_id)
            agent = self.model.get_agent_by_id(student_id)
            if agent.physical and agent.physical.age != 0:
                if 5 < agent.physical.age <= 10:
                    agent.add_occupation_attribute(
                        self,
                        locale=self,
                        category=StudentCategory.ELEMENTARY
                    )
                elif 10 < agent.physical.age <= 13:
                    agent.add_occupation_attribute(
                        self,
                        locale=self,
                        category=StudentCategory.MIDDLESCHOOL
                    )
                elif 13 < agent.physical.age <= 18:
                    agent.add_occupation_attribute(
                        self,
                        locale=self,
                        category=StudentCategory.HIGHSCHOOL
                    )
                elif 18 < agent.physical.age <= 22:
                    agent.add_occupation_attribute(
                        self,
                        locale=self,
                        category=StudentCategory.COLLEGE
                    )
            else:
                agent.add_occupation_attribute(
                    self,
                    locale=self,
                    category=StudentCategory.GENERIC
                )
        except Exception as err:
            LOG.exception(err)

    def remove_student(self, student_id: Union[int, str]) -> None:
        try:
            self._students.remove(student_id)
            agent = self.model.get_agent_by_id(student_id)
            agent.remove_occupation_attribute()
        except Exception as err:
            LOG.exception(err)

    # def update_students_occupants(self) -> None:
    #     for agent_id in self.all_individuals:
    #         agent = self.model.get_agent_by_id(agent_id)
    #         if agent.occupation.category in self.allowed_occupations:
    #             self.students.add(agent_id)

    def step(self) -> None:
        self.update_all_individuals_from_graph_edges()
        self.update_visiting_individuals()
        # self.update_students_occupants()


class HealthCareUnit(Locale):

    __slots__ = [
        "_max_capacity_patients",
        "_max_capacity_common_beds",
        "_max_capacity_icu_beds",
        "_available_common_beds",
        "_available_icu_beds",
        "_all_patients",
        "_common_patients",
        "icu_patients"
    ]

    def __init__(self, unique_id: int, model: SimulationModel):
        super().__init__(unique_id=unique_id, model=model)
        self._essential = True
        self._activity_time: dict = {
            "start_time": time(8, 0, 0),
            "end_time": time(17, 0, 0),
        }
        self._max_capacity_patients: int = 0
        self._max_capacity_common_beds: int = 0
        self._max_capacity_icu_beds: int = 0
        self._available_common_beds: int = 0
        self._available_icu_beds: int = 0
        self._all_patients: set[int] = set()
        self._common_patients: set[int] = set()
        self._icu_patients: set[int] = set()
        # self._allowed_occupations: set[WorkerCategory] = {
        #     category for category in WorkerCategory if category.name == "HEALTH"
        # }

    def add_occupation_individual(self, agent_id) -> None:
        try:
            self._occupation_individuals.add(agent_id)
            agent = self.model.get_agent_by_id(agent_id)
            agent.add_occupation_individual(
                self,
                locale=self,
                category=WorkerCategory.HEALTH
            )
        except Exception as err:
            LOG.exception(err)

    def remove_occupation_individual(self, agent_id) -> None:
        try:
            self._occupation_individuals.remove(agent_id)
            agent = self.model.get_agent_by_id(agent_id)
            agent.remove_occupation_attribute()
        except Exception as err:
            LOG.exception(err)

    @property
    def max_capacity_patients(self) -> int:
        return self._max_capacity_patients

    @max_capacity_patients.setter
    def max_capacity_patients(self, value: int) -> None:
        self._max_capacity_patients = value

    @property
    def max_capacity_common_beds(self) -> int:
        return self._max_capacity_common_beds

    @max_capacity_common_beds.setter
    def max_capacity_common_beds(self, value: int) -> None:
        self._max_capacity_common_beds = value

    @property
    def max_capacity_icu_beds(self) -> int:
        return self._max_capacity_icu_beds

    @max_capacity_icu_beds.setter
    def max_capacity_icu_beds(self, value: int) -> None:
        self._max_capacity_icu_beds = value

    @property
    def available_common_beds(self) -> int:
        return self._available_common_beds

    @available_common_beds.setter
    def available_common_beds(self, value: int) -> None:
        self._available_common_beds = value

    @property
    def available_icu_beds(self) -> int:
        return self._available_icu_beds

    @available_icu_beds.setter
    def available_icu_beds(self, value: int) -> None:
        self._available_icu_beds = value

    @property
    def all_patients(self) -> set[int]:
        return self._all_patients

    @all_patients.setter
    def all_patients(self, all_patients_set: set[int]) -> None:
        self._all_patients = all_patients_set

    @property
    def common_patients(self) -> set[int]:
        return self._common_patients

    @common_patients.setter
    def common_patients(self, common_patients_set: set[int]) -> None:
        self._common_patients = common_patients_set

    @property
    def icu_patients(self) -> set[int]:
        return self._icu_patients

    @icu_patients.setter
    def icu_patients(self, icu_patients_set: set[int]) -> None:
        self._icu_patients = icu_patients_set

    def update_patients_related_attributes(self) -> None:
        liberated_patients = self.all_patients - self.all_individuals
        for patient_id in liberated_patients:
            if patient_id in self.common_patients:
                self._common_patients.remove(patient_id)
                self.available_common_beds += 1
            if patient_id in self.icu_patients:
                self._icu_patients.remove(patient_id)
                self.available_icu_beds += 1
        self.all_patients = self.common_patients | self.icu_patients

    def update_patients_bed_conditions(self) -> None:
        new_patients = (self.all_individuals - self.all_patients)
        if new_patients:
            for patient_id in new_patients:
                patient = self.model.get_agent_by_id(patient_id)
                if patient.health.health_state == HealthState.DEBILITADED and self.available_common_beds < self.max_capacity_common_beds:
                    self._common_patients.add(patient_id)
                    self._all_patients.add(patient_id)
                    self.available_common_beds -= 1
                if patient.health.health_state == HealthState.INCAPACITATED and self.available_icu_beds < self.max_capacity_icu_beds:
                    self._icu_patients.add(patient_id)
                    self._all_patients.add(patient_id)
                    self.available_icu_beds -= 1
        for patient_id in self.common_patients:
            patient = self.model.get_agent_by_id(patient_id)
            if patient.health.health_state == HealthState.INCAPACITATED and self.available_icu_beds < self.max_capacity_icu_beds:
                self._icu_patients.add(patient_id)
                self.available_icu_beds -= 1

    def step(self) -> None:
        self.update_all_individuals_from_graph_edges()
        self.update_visiting_individuals()
        self.update_patients_related_attributes()
        self.update_patients_bed_conditions()


class PublicPlace(Locale):
    def __init__(self, unique_id: int, model: SimulationModel):
        super().__init__(unique_id=unique_id, model=model)
        self._essential = False
        self._activity_time: dict = {
            "start_time": time(7, 0, 0),
            "end_time": time(21, 0, 0),
        }
        # self._allowed_occupations: set[WorkerCategory] = {
        #     category
        #     for category in WorkerCategory
        #     if category.name in {"GENERIC", "SERVICES", "PUBLIC"}
        # }

    def add_occupation_individual(self, agent_id) -> None:
        try:
            self._occupation_individuals.add(agent_id)
            agent = self.model.get_agent_by_id(agent_id)
            agent.add_occupation_individual(
                self,
                locale=self,
                category=WorkerCategory.PUBLIC
            )
        except Exception as err:
            LOG.exception(err)

    def step(self) -> None:
        self.update_all_individuals_from_graph_edges()
        self.update_visiting_individuals()


class CustomerServicesPlace(Workplace):
    def __init__(self, unique_id: int, model: SimulationModel):
        super().__init__(unique_id=unique_id, model=model)
        # self._allowed_occupations: set[WorkerCategory] = {
        #     category for category in WorkerCategory if category.name == "SERVICES"
        # }

    def add_occupation_individual(self, agent_id) -> None:
        try:
            self._occupation_individuals.add(agent_id)
            agent = self.model.get_agent_by_id(agent_id)
            agent.add_occupation_individual(
                self,
                locale=self,
                category=WorkerCategory.CUSTOMERSERVICES
            )
        except Exception as err:
            LOG.exception(err)


class NonCustomerServicesPlace(Workplace):
    def __init__(self, unique_id: int, model: SimulationModel):
        super().__init__(unique_id=unique_id, model=model)
        # self._allowed_occupations: set[WorkerCategory] = {
        #     category for category in WorkerCategory if category.name == "SERVICES"
        # }

    def add_occupation_individual(self, agent_id) -> None:
        try:
            self._occupation_individuals.add(agent_id)
            agent = self.model.get_agent_by_id(agent_id)
            agent.add_occupation_individual(
                self,
                locale=self,
                category=WorkerCategory.NONCUSTOMERSERVICES
            )
        except Exception as err:
            LOG.exception(err)


class Industry(Workplace):
    def __init__(self, unique_id: int, model: SimulationModel):
        super().__init__(unique_id=unique_id, model=model)
        # self._allowed_occupations: set[WorkerCategory] = {
        #     category for category in WorkerCategory if category.name == "INDUSTRY"
        # }

    def add_occupation_individual(self, agent_id) -> None:
        try:
            self._occupation_individuals.add(agent_id)
            agent = self.model.get_agent_by_id(agent_id)
            agent.add_occupation_individual(
                self,
                locale=self,
                category=WorkerCategory.INDUSTRY
            )
        except Exception as err:
            LOG.exception(err)
