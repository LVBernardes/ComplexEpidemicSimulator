from typing import Any

from complex_epidemics.agents.human import Human
from complex_epidemics.agents.locale import Household, Locale
from complex_epidemics.agents.support_objects.citizen_factory import CitizenFactory
from complex_epidemics.agents.support_objects.human.abstract_human_activity import (
    HumanBaseActivity,
)
from complex_epidemics.agents.support_objects.human.health_states import HealthState
from complex_epidemics.agents.support_objects.human.human_occupation_categories import (
    WorkerCategory,
)
from complex_epidemics.agents.support_objects.human.low_level_human_behaviour import (
    Routine,
)
from complex_epidemics.workbench.simulation.infrastructure_builder import (
    InfrastructureBuilder,
)
from complex_epidemics.agents.support_objects.locale.locale_categories import (
    EducationalInstitutionCategory,
    HealthCareCategory,
    HouseholdCategory,
    PublicPlaceCategory,
    WorkplaceCategory,
)
from complex_epidemics.agents.transport import PublicTransport
from complex_epidemics.graph.networkx_engine.networkx_bipartitegraph import (
    NetworkxBipartiteGraph,
)
from complex_epidemics.model.simulation_model import SimulationModel


class BaseActivity(HumanBaseActivity):
    def __init__(self, human: Any, **kwargs):
        super().__init__(human=human, **kwargs)
        self._duration_controlled: bool = kwargs.get("duration_controlled", False)
        self._time_controlled: bool = kwargs.get("time_controlled", False)
        self._position_controlled: bool = kwargs.get("position_controlled", False)
        self._state_controlled: bool = kwargs.get("state_controlled", False)
        self.movement_plan: list = list()

    def start_logic(self):
        self.define_movement_plan(destination=self.final_position)

    def activity_logic(self):
        if len(self.movement_plan) != 0:
            self._human.change_position(self.movement_plan.pop(0))


class TestBaseHumanActivity:
    def test_instantiation(self):

        model = SimulationModel()
        human = Human(unique_id=999999, model=model)
        base_activity = BaseActivity(human)

        assert isinstance(base_activity, BaseActivity)

    def test_method_end_condition_checker(self):

        model = SimulationModel()
        model.graph = NetworkxBipartiteGraph()
        model.clock.increment_time_in_hours(1)
        household = Household(unique_id=88888, model=model)
        household.graph_node_id = 88888
        model.graph.add_node_to_component_zero(household.unique_id)
        human = Human(unique_id=999999, model=model)
        model.graph.add_node_to_component_one(human.unique_id)
        human.household = household
        human.change_position(to_pos=household.graph_node_id)
        base_activity = BaseActivity(
            human, state_controlled=True, final_state=HealthState.SICK
        )
        base_activity.active = True
        base_activity.step()
        base_activity.step()
        human.health.health_state = HealthState.SICK
        base_activity.step()

        assert base_activity.active is False and base_activity.started is False

    def test_method_check_for_available_public_transport(self):

        model = SimulationModel()
        model.graph = NetworkxBipartiteGraph()
        model.clock.increment_time_in_hours(1)

        household = Household(unique_id=88888, model=model)
        household.graph_node_id = 88888
        model.graph.add_node_to_component_zero(household.unique_id)

        human = Human(unique_id=999999, model=model)
        human.graph_node_id = 999999
        model.graph.add_node_to_component_one(human.unique_id)
        human.household = household
        human.change_position(to_pos=household.graph_node_id)

        locale_agent_id_list = list()
        transport_agent_id_list = list()
        for i in range(0, 10):
            model.schedule.add(Locale(unique_id=i, model=model))
            model.schedule._agents[i].graph_node_id = i
            model.graph.add_node_to_component_zero(i)
            locale_agent_id_list.append(i)
        for i in range(10, 15):
            model.schedule.add(PublicTransport(unique_id=i, model=model))
            model.schedule._agents[i].graph_node_id = i
            model.schedule._agents[i].max_capacity_nominal = 5
            model.schedule._agents[i].max_capacity_effective = 5
            model.graph.add_node_to_component_zero(i)
            transport_agent_id_list.append(i)

        for i in range(10, 15):
            model.schedule._agents[i].add_serviced_locale(i - 10)
            model.schedule._agents[i].add_serviced_locale(i - 5)

        model.schedule._agents[10].add_serviced_locale(88888)

        base_activity = BaseActivity(human, position_controlled=True, final_position=4)
        base_activity.active = True

        model.step()
        transport_available = base_activity.check_for_available_public_transport(
            destination=5
        )

        assert transport_available == 10

    def test_method_define_movement_plan(self):
        pass

    def test_method_step(self):
        pass


class TestCommonActivities:
    def test_execution_simple_routine(self):
        new_builder = InfrastructureBuilder()

        city_data = {
            "household": [
                {
                    "category": HouseholdCategory.GENERIC,
                    "count": 40,
                    "capacity": {"nominal": {"type": "uniform", "parameters": [3, 5]}},
                }
            ],
            "workplace": [
                {
                    "category": WorkplaceCategory.GENERIC,
                    "count": 10,
                    "capacity": {
                        "nominal": {"type": "uniform", "parameters": [10, 15]}
                    },
                }
            ],
            "educational": [
                {
                    "category": EducationalInstitutionCategory.GENERIC,
                    "count": 2,
                    "capacity": {
                        "nominal": {"type": "uniform", "parameters": [50, 60]},
                        "students": {"type": "uniform", "parameters": [45, 50]},
                    },
                }
            ],
            "healthcare": [
                {
                    "category": HealthCareCategory.GENERIC,
                    "count": 2,
                    "capacity": {
                        "nominal": {"type": "none", "parameters": [30]},
                        "patients": {"type": "none", "parameters": [20]},
                    },
                }
            ],
            "public": [
                {
                    "category": PublicPlaceCategory.GENERIC,
                    "count": 1,
                    "capacity": {
                        "nominal": {"type": "none", "parameters": [40]},
                        "effective": {"type": "none", "parameters": [50]},
                    },
                }
            ],
        }

        model = SimulationModel()
        model.graph = NetworkxBipartiteGraph()

        new_builder.set_model(model=model)
        new_builder.set_household_config(city_data.get("household"))
        new_builder.set_workplace_config(city_data.get("workplace"))
        new_builder.set_educational_config(city_data.get("educational"))
        new_builder.set_healthcare_config(city_data.get("healthcare"))
        new_builder.set_public_config(city_data.get("public"))

        new_builder.build()

        model, city = new_builder.get_result()

        citizen_factory = CitizenFactory(model)

        generic_worker = citizen_factory.new_worker()
        generic_student = citizen_factory.new_student()
        generic_unoccupied = citizen_factory.new_generic_citizen()
        generic_health_worker = citizen_factory.new_worker(
            category=WorkerCategory.HEALTH
        )
        generic_public_worker = citizen_factory.new_worker(
            category=WorkerCategory.PUBLIC
        )

        household_list = [
            house_id for house_id in model.get_agents_by_class("Household")
        ]

        generic_worker.household = model.schedule._agents[household_list[0]]
        generic_student.household = model.schedule._agents[household_list[1]]
        generic_unoccupied.household = model.schedule._agents[household_list[2]]
        generic_health_worker.household = model.schedule._agents[household_list[3]]
        generic_public_worker.household = model.schedule._agents[household_list[4]]

        generic_worker.position = generic_worker.household.graph_node_id
        generic_student.position = generic_student.household.graph_node_id
        generic_unoccupied.position = generic_unoccupied.household.graph_node_id
        generic_health_worker.position = generic_health_worker.household.graph_node_id
        generic_public_worker.position = generic_public_worker.household.graph_node_id

        print()
        print("---------------------------------------------------------")
        print(model.clock.get_datetime_formated())
        print(generic_worker.position)
        # print(generic_worker._low_level_behaviour._day_planning)
        # print(generic_worker._low_level_behaviour._last_activity)
        # print(generic_worker._low_level_behaviour._running_activity)
        # print(generic_worker._low_level_behaviour._next_activity)
        print(generic_student.position)
        # print(generic_student._low_level_behaviour._day_planning)
        # print(generic_student._low_level_behaviour._last_activity)
        # print(generic_student._low_level_behaviour._running_activity)
        # print(generic_student._low_level_behaviour._next_activity)
        model.step()
        print("---------------------------------------------------------")
        print(model.clock.get_datetime_formated())
        print(generic_worker.position)
        # print(generic_worker._low_level_behaviour._day_planning)
        # print(generic_worker._low_level_behaviour._last_activity)
        # print(generic_worker._low_level_behaviour._running_activity)
        # print(generic_worker._low_level_behaviour._next_activity)
        print(generic_student.position)
        # print(generic_student._low_level_behaviour._day_planning)
        # print(generic_student._low_level_behaviour._last_activity)
        # print(generic_student._low_level_behaviour._running_activity)
        # print(generic_student._low_level_behaviour._next_activity)

        for i in range(24):
            model.step()
            print("---------------------------------------------------------")
            print(model.clock.get_datetime_formated())
            print(generic_worker.position)
            # print(generic_worker._low_level_behaviour._day_planning)
            # print(generic_worker._low_level_behaviour._last_activity)
            # print(generic_worker._low_level_behaviour._running_activity)
            # print(generic_worker._low_level_behaviour._next_activity)
            print(generic_student.position)
            # print(generic_student._low_level_behaviour._day_planning)
            # print(generic_student._low_level_behaviour._last_activity)
            # print(generic_student._low_level_behaviour._running_activity)
            # print(generic_student._low_level_behaviour._next_activity)

    def test_execution_standard_routine(self):
        new_builder = InfrastructureBuilder()

        city_data = {
            "household": [
                {
                    "category": HouseholdCategory.GENERIC,
                    "count": 40,
                    "capacity": {"nominal": {"type": "uniform", "parameters": [3, 5]}},
                }
            ],
            "workplace": [
                {
                    "category": WorkplaceCategory.GENERIC,
                    "count": 10,
                    "capacity": {
                        "nominal": {"type": "uniform", "parameters": [10, 15]}
                    },
                }
            ],
            "educational": [
                {
                    "category": EducationalInstitutionCategory.GENERIC,
                    "count": 2,
                    "capacity": {
                        "nominal": {"type": "uniform", "parameters": [50, 60]},
                        "students": {"type": "uniform", "parameters": [45, 50]},
                    },
                }
            ],
            "healthcare": [
                {
                    "category": HealthCareCategory.GENERIC,
                    "count": 2,
                    "capacity": {
                        "nominal": {"type": "none", "parameters": [30]},
                        "patients": {"type": "none", "parameters": [20]},
                    },
                }
            ],
            "public": [
                {
                    "category": PublicPlaceCategory.GENERIC,
                    "count": 1,
                    "capacity": {
                        "nominal": {"type": "none", "parameters": [40]},
                        "effective": {"type": "none", "parameters": [50]},
                    },
                }
            ],
        }

        model = SimulationModel()
        model.graph = NetworkxBipartiteGraph()

        new_builder.set_model(model=model)
        new_builder.set_household_config(city_data.get("household"))
        new_builder.set_workplace_config(city_data.get("workplace"))
        new_builder.set_educational_config(city_data.get("educational"))
        new_builder.set_healthcare_config(city_data.get("healthcare"))
        new_builder.set_public_config(city_data.get("public"))

        new_builder.build()

        model, city = new_builder.get_result()

        citizen_factory = CitizenFactory(model)

        generic_worker = citizen_factory.new_worker(routine=Routine.STANDARD)
        generic_student = citizen_factory.new_student(routine=Routine.STANDARD)
        generic_unoccupied = citizen_factory.new_generic_citizen(
            routine=Routine.STANDARD
        )
        generic_health_worker = citizen_factory.new_worker(
            category=WorkerCategory.HEALTH, routine=Routine.STANDARD
        )
        generic_public_worker = citizen_factory.new_worker(
            category=WorkerCategory.PUBLIC, routine=Routine.STANDARD
        )

        household_list = [
            house_id for house_id in model.get_agents_by_class("Household")
        ]

        generic_worker.household = model.schedule._agents[household_list[0]]
        generic_student.household = model.schedule._agents[household_list[1]]
        generic_unoccupied.household = model.schedule._agents[household_list[2]]
        generic_health_worker.household = model.schedule._agents[household_list[3]]
        generic_public_worker.household = model.schedule._agents[household_list[4]]

        generic_worker.position = generic_worker.household.graph_node_id
        generic_student.position = generic_student.household.graph_node_id
        generic_unoccupied.position = generic_unoccupied.household.graph_node_id
        generic_health_worker.position = generic_health_worker.household.graph_node_id
        generic_public_worker.position = generic_public_worker.household.graph_node_id

        generic_worker.entertainment = model.schedule._agents[household_list[5]]
        generic_student.entertainment = model.schedule._agents[household_list[6]]
        generic_unoccupied.entertainment = model.schedule._agents[household_list[7]]
        generic_health_worker.entertainment = model.schedule._agents[household_list[8]]
        generic_public_worker.entertainment = model.schedule._agents[household_list[9]]

        print()
        print("---------------------------------------------------------")
        print(model.clock.get_datetime_formated())
        print(generic_worker.position)
        # print(generic_worker._low_level_behaviour._day_planning)
        # print(generic_worker._low_level_behaviour._last_activity)
        # print(generic_worker._low_level_behaviour._running_activity)
        # print(generic_worker._low_level_behaviour._next_activity)
        print(generic_student.position)
        # print(generic_student._low_level_behaviour._day_planning)
        # print(generic_student._low_level_behaviour._last_activity)
        # print(generic_student._low_level_behaviour._running_activity)
        # print(generic_student._low_level_behaviour._next_activity)
        model.step()
        print("---------------------------------------------------------")
        print(model.clock.get_datetime_formated())
        print(generic_worker.position)
        # print(generic_worker._low_level_behaviour._day_planning)
        # print(generic_worker._low_level_behaviour._last_activity)
        # print(generic_worker._low_level_behaviour._running_activity)
        # print(generic_worker._low_level_behaviour._next_activity)
        print(generic_student.position)
        # print(generic_student._low_level_behaviour._day_planning)
        # print(generic_student._low_level_behaviour._last_activity)
        # print(generic_student._low_level_behaviour._running_activity)
        # print(generic_student._low_level_behaviour._next_activity)

        for i in range(24 * 7):
            model.step()
            print("---------------------------------------------------------")
            print(model.clock.get_datetime_formated())
            print(generic_worker.position)
            # print(generic_worker._low_level_behaviour._day_planning)
            # print(generic_worker._low_level_behaviour._last_activity)
            # print(generic_worker._low_level_behaviour._running_activity)
            # print(generic_worker._low_level_behaviour._next_activity)
            print(generic_student.position)
            # print(generic_student._low_level_behaviour._day_planning)
            # print(generic_student._low_level_behaviour._last_activity)
            # print(generic_student._low_level_behaviour._running_activity)
            # print(generic_student._low_level_behaviour._next_activity)

    def test_execution_sophisticated_routine(self):
        new_builder = InfrastructureBuilder()

        city_data = {
            "household": [
                {
                    "category": HouseholdCategory.GENERIC,
                    "count": 40,
                    "capacity": {"nominal": {"type": "uniform", "parameters": [3, 5]}},
                }
            ],
            "workplace": [
                {
                    "category": WorkplaceCategory.GENERIC,
                    "count": 10,
                    "capacity": {
                        "nominal": {"type": "uniform", "parameters": [10, 15]}
                    },
                }
            ],
            "educational": [
                {
                    "category": EducationalInstitutionCategory.GENERIC,
                    "count": 2,
                    "capacity": {
                        "nominal": {"type": "uniform", "parameters": [50, 60]},
                        "students": {"type": "uniform", "parameters": [45, 50]},
                    },
                }
            ],
            "healthcare": [
                {
                    "category": HealthCareCategory.GENERIC,
                    "count": 2,
                    "capacity": {
                        "nominal": {"type": "none", "parameters": [30]},
                        "patients": {"type": "none", "parameters": [20]},
                    },
                }
            ],
            "public": [
                {
                    "category": PublicPlaceCategory.GENERIC,
                    "count": 1,
                    "capacity": {
                        "nominal": {"type": "none", "parameters": [40]},
                        "effective": {"type": "none", "parameters": [50]},
                    },
                }
            ],
        }

        model = SimulationModel()
        model.graph = NetworkxBipartiteGraph()

        new_builder.set_model(model=model)
        new_builder.set_household_config(city_data.get("household"))
        new_builder.set_workplace_config(city_data.get("workplace"))
        new_builder.set_educational_config(city_data.get("educational"))
        new_builder.set_healthcare_config(city_data.get("healthcare"))
        new_builder.set_public_config(city_data.get("public"))

        new_builder.build()

        model, city = new_builder.get_result()

        citizen_factory = CitizenFactory(model)

        generic_worker = citizen_factory.new_worker(routine=Routine.SOPHISTICATED)
        generic_student = citizen_factory.new_student(routine=Routine.SOPHISTICATED)
        generic_unoccupied = citizen_factory.new_generic_citizen(
            routine=Routine.SOPHISTICATED
        )
        generic_health_worker = citizen_factory.new_worker(
            category=WorkerCategory.HEALTH, routine=Routine.SOPHISTICATED
        )
        generic_public_worker = citizen_factory.new_worker(
            category=WorkerCategory.PUBLIC, routine=Routine.SOPHISTICATED
        )

        household_list = [
            house_id for house_id in model.get_agents_by_class("Household")
        ]

        generic_worker.household = model.schedule._agents[household_list[0]]
        generic_student.household = model.schedule._agents[household_list[1]]
        generic_unoccupied.household = model.schedule._agents[household_list[2]]
        generic_health_worker.household = model.schedule._agents[household_list[3]]
        generic_public_worker.household = model.schedule._agents[household_list[4]]

        generic_worker.position = generic_worker.household.graph_node_id
        generic_student.position = generic_student.household.graph_node_id
        generic_unoccupied.position = generic_unoccupied.household.graph_node_id
        generic_health_worker.position = generic_health_worker.household.graph_node_id
        generic_public_worker.position = generic_public_worker.household.graph_node_id

        generic_worker.entertainment = model.schedule._agents[household_list[5]]
        generic_student.entertainment = model.schedule._agents[household_list[6]]
        generic_unoccupied.entertainment = model.schedule._agents[household_list[7]]
        generic_health_worker.entertainment = model.schedule._agents[household_list[8]]
        generic_public_worker.entertainment = model.schedule._agents[household_list[9]]

        print()
        print("---------------------------------------------------------")
        print(model.clock.get_datetime_formated())
        print(generic_worker.position)
        # print(generic_worker._low_level_behaviour._day_planning)
        # print(generic_worker._low_level_behaviour._last_activity)
        # print(generic_worker._low_level_behaviour._running_activity)
        # print(generic_worker._low_level_behaviour._next_activity)
        print(generic_student.position)
        # print(generic_student._low_level_behaviour._day_planning)
        # print(generic_student._low_level_behaviour._last_activity)
        # print(generic_student._low_level_behaviour._running_activity)
        # print(generic_student._low_level_behaviour._next_activity)
        model.step()
        print("---------------------------------------------------------")
        print(model.clock.get_datetime_formated())
        print(generic_worker.position)
        # print(generic_worker._low_level_behaviour._day_planning)
        # print(generic_worker._low_level_behaviour._last_activity)
        # print(generic_worker._low_level_behaviour._running_activity)
        # print(generic_worker._low_level_behaviour._next_activity)
        print(generic_student.position)
        # print(generic_student._low_level_behaviour._day_planning)
        # print(generic_student._low_level_behaviour._last_activity)
        # print(generic_student._low_level_behaviour._running_activity)
        # print(generic_student._low_level_behaviour._next_activity)

        for i in range(24 * 7):
            model.step()
            print("---------------------------------------------------------")
            print(model.clock.get_datetime_formated())
            print(generic_worker.position)
            # print(generic_worker._low_level_behaviour._day_planning)
            # print(generic_worker._low_level_behaviour._last_activity)
            # print(generic_worker._low_level_behaviour._running_activity)
            # print(generic_worker._low_level_behaviour._next_activity)
            print(generic_student.position)
            # print(generic_student._low_level_behaviour._day_planning)
            # print(generic_student._low_level_behaviour._last_activity)
            # print(generic_student._low_level_behaviour._running_activity)
            # print(generic_student._low_level_behaviour._next_activity)

    def test_execution_home_health_care(self):
        new_builder = InfrastructureBuilder()

        city_data = {
            "household": [
                {
                    "category": HouseholdCategory.GENERIC,
                    "count": 40,
                    "capacity": {"nominal": {"type": "uniform", "parameters": [3, 5]}},
                }
            ],
            "workplace": [
                {
                    "category": WorkplaceCategory.GENERIC,
                    "count": 10,
                    "capacity": {
                        "nominal": {"type": "uniform", "parameters": [10, 15]}
                    },
                }
            ],
            "educational": [
                {
                    "category": EducationalInstitutionCategory.GENERIC,
                    "count": 2,
                    "capacity": {
                        "nominal": {"type": "uniform", "parameters": [50, 60]},
                        "students": {"type": "uniform", "parameters": [45, 50]},
                    },
                }
            ],
            "healthcare": [
                {
                    "category": HealthCareCategory.GENERIC,
                    "count": 2,
                    "capacity": {
                        "nominal": {"type": "none", "parameters": [30]},
                        "patients": {"type": "none", "parameters": [20]},
                    },
                }
            ],
            "public": [
                {
                    "category": PublicPlaceCategory.GENERIC,
                    "count": 1,
                    "capacity": {
                        "nominal": {"type": "none", "parameters": [40]},
                        "effective": {"type": "none", "parameters": [50]},
                    },
                }
            ],
        }

        model = SimulationModel()
        model.graph = NetworkxBipartiteGraph()

        new_builder.set_model(model=model)
        new_builder.set_household_config(city_data.get("household"))
        new_builder.set_workplace_config(city_data.get("workplace"))
        new_builder.set_educational_config(city_data.get("educational"))
        new_builder.set_healthcare_config(city_data.get("healthcare"))
        new_builder.set_public_config(city_data.get("public"))

        new_builder.build()

        model, city = new_builder.get_result()

        citizen_factory = CitizenFactory(model)

        generic_worker = citizen_factory.new_worker(routine=Routine.SOPHISTICATED)
        generic_student = citizen_factory.new_student(routine=Routine.SOPHISTICATED)
        generic_unoccupied = citizen_factory.new_generic_citizen(
            routine=Routine.SOPHISTICATED
        )
        generic_health_worker = citizen_factory.new_worker(
            category=WorkerCategory.HEALTH, routine=Routine.SOPHISTICATED
        )
        generic_public_worker = citizen_factory.new_worker(
            category=WorkerCategory.PUBLIC, routine=Routine.SOPHISTICATED
        )

        household_list = [
            house_id for house_id in model.get_agents_by_class("Household")
        ]

        generic_worker.household = model.schedule._agents[household_list[0]]
        generic_student.household = model.schedule._agents[household_list[1]]
        generic_unoccupied.household = model.schedule._agents[household_list[2]]
        generic_health_worker.household = model.schedule._agents[household_list[3]]
        generic_public_worker.household = model.schedule._agents[household_list[4]]

        generic_worker.position = generic_worker.household.graph_node_id
        generic_student.position = generic_student.household.graph_node_id
        generic_unoccupied.position = generic_unoccupied.household.graph_node_id
        generic_health_worker.position = generic_health_worker.household.graph_node_id
        generic_public_worker.position = generic_public_worker.household.graph_node_id

        generic_worker.entertainment = model.schedule._agents[household_list[5]]
        generic_student.entertainment = model.schedule._agents[household_list[6]]
        generic_unoccupied.entertainment = model.schedule._agents[household_list[7]]
        generic_health_worker.entertainment = model.schedule._agents[household_list[8]]
        generic_public_worker.entertainment = model.schedule._agents[household_list[9]]

        print()
        print("---------------------------------------------------------")
        print(model.clock.get_datetime_formated())
        print(generic_worker.position)
        # print(generic_worker._low_level_behaviour._day_planning)
        # print(generic_worker._low_level_behaviour._last_activity)
        # print(generic_worker._low_level_behaviour._running_activity)
        # print(generic_worker._low_level_behaviour._next_activity)
        print(generic_student.position)
        # print(generic_student._low_level_behaviour._day_planning)
        # print(generic_student._low_level_behaviour._last_activity)
        # print(generic_student._low_level_behaviour._running_activity)
        # print(generic_student._low_level_behaviour._next_activity)
        model.step()
        print("---------------------------------------------------------")
        print(model.clock.get_datetime_formated())
        print(generic_worker.position)
        # print(generic_worker._low_level_behaviour._day_planning)
        # print(generic_worker._low_level_behaviour._last_activity)
        # print(generic_worker._low_level_behaviour._running_activity)
        # print(generic_worker._low_level_behaviour._next_activity)
        print(generic_student.position)
        # print(generic_student._low_level_behaviour._day_planning)
        # print(generic_student._low_level_behaviour._last_activity)
        # print(generic_student._low_level_behaviour._running_activity)
        # print(generic_student._low_level_behaviour._next_activity)

        for i in range(24 * 2):
            model.step()
            print("---------------------------------------------------------")
            print(model.clock.get_datetime_formated())
            print(generic_worker.position)
            # print(generic_worker._low_level_behaviour._day_planning)
            # print(generic_worker._low_level_behaviour._last_activity)
            # print(generic_worker._low_level_behaviour._running_activity)
            # print(generic_worker._low_level_behaviour._next_activity)
            print(generic_student.position)
            # print(generic_student._low_level_behaviour._day_planning)
            # print(generic_student._low_level_behaviour._last_activity)
            # print(generic_student._low_level_behaviour._running_activity)
            # print(generic_student._low_level_behaviour._next_activity)

        generic_worker.health.health_state = HealthState.SICK
        generic_health_worker.health.health_state = HealthState.SICK

        for i in range(24 * 2):
            model.step()
            print("---------------------------------------------------------")
            print(model.clock.get_datetime_formated())
            print(generic_worker.position)
            # print(generic_worker._low_level_behaviour._day_planning)
            # print(generic_worker._low_level_behaviour._last_activity)
            # print(generic_worker._low_level_behaviour._running_activity)
            # print(generic_worker._low_level_behaviour._next_activity)
            print(generic_student.position)

        generic_worker.health.health_state = HealthState.HEALTHY
        generic_health_worker.health.health_state = HealthState.HEALTHY
        generic_student.health.health_state = HealthState.SICK
        generic_unoccupied.health.health_state = HealthState.SICK

        for i in range(24 * 2):
            model.step()
            print("---------------------------------------------------------")
            print(model.clock.get_datetime_formated())
            print(generic_worker.position)
            # print(generic_worker._low_level_behaviour._day_planning)
            # print(generic_worker._low_level_behaviour._last_activity)
            # print(generic_worker._low_level_behaviour._running_activity)
            # print(generic_worker._low_level_behaviour._next_activity)
            print(generic_student.position)
