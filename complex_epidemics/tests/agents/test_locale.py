from complex_epidemics.agents.human import Human
from complex_epidemics.agents.locale import (
    EducationalInstitution,
    HealthCareUnit,
    Household,
    Locale,
    Workplace,
)
from complex_epidemics.agents.support_objects.human.human_occupation import (
    GenericOccupation,
    Student,
    Worker,
)
from complex_epidemics.agents.support_objects.human.human_occupation_categories import (
    GenericOccupationCategory,
    StudentCategory,
    WorkerCategory,
)
from complex_epidemics.graph.networkx_engine.networkx_bipartitegraph import (
    NetworkxBipartiteGraph,
)
from complex_epidemics.model.simulation_model import SimulationModel


class TestLocale:
    def test_instantiation(self):

        model = SimulationModel()
        new_locale = Locale(unique_id=0, model=model)

        assert isinstance(new_locale, Locale)

    def test_init_attributes(self):

        model = SimulationModel()
        new_household = Household(unique_id=0, model=model)
        new_workplace = Workplace(unique_id=1, model=model)
        new_educational_institution = EducationalInstitution(unique_id=2, model=model)
        new_health_care_unit = HealthCareUnit(unique_id=3, model=model)

        assert (
            new_household.assigned_occupations
            == {category for category in GenericOccupationCategory}
            and new_workplace.assigned_occupations
            == {
                category
                for category in WorkerCategory
                if category.name in {"GENERIC", "INDUSTRY", "SERVICES"}
            }
            and new_educational_institution.assigned_occupations
            == {category for category in StudentCategory}
            and new_health_care_unit.assigned_occupations
            == {category for category in WorkerCategory if category.name == "HEALTH"}
        )


class TestEducationalInstitution:
    def test_method_update_students_occupation(self):

        model = SimulationModel()
        graph = NetworkxBipartiteGraph()
        model.graph = graph

        locale_agent_id_list = list()
        human_agent_id_list = list()
        for i in range(11, 13):
            locale = EducationalInstitution(unique_id=i, model=model)
            locale.max_capacity_nominal = 10
            model.schedule.add(locale)
            model.graph.add_node_to_component_zero(i)
            locale_agent_id_list.append(i)
        for i in range(0, 10):
            human = Human(unique_id=i, model=model)
            model.schedule.add(human)
            new_occupation = Student()
            new_occupation.category = StudentCategory.GENERIC
            human.occupation = new_occupation
            human.occupation._human = human
            model.graph.add_node_to_component_one(i)
            human_agent_id_list.append(i)

        locale_occupants = dict()
        locale_special_occupants = dict()

        for j in range(2):
            model.step()
            locale_occupants[j] = dict()
            locale_special_occupants[j] = dict()

            for i in range(11, 13):
                locale_occupants[j][i] = list()
                locale_special_occupants[j][i] = list()
                occupants = model.schedule._agents[i].occupants
                locale_occupants[j][i].extend(occupants) if len(occupants) > 0 else None
                special_occupants = model.schedule._agents[i].students_occupants
                locale_special_occupants[j][i].extend(special_occupants) if len(
                    special_occupants
                ) > 0 else None
                print(f"Locale {i} has: {locale_occupants[j][i]}")
                print(f"Locale {i} has special: {locale_special_occupants[j][i]}")
            for i in range(5 * j, 5 * j + 5):
                mobile_agent = model.schedule._agents[i]
                mobile_agent.change_position(j + 11)
                print(
                    f"Human {i} position is: {mobile_agent.position}; "
                    f"and last positions was {mobile_agent.get_last_positions()}"
                )

        model.step()
        locale_occupants[2] = dict()
        locale_special_occupants[2] = dict()
        for i in range(11, 13):
            locale_occupants[2][i] = list()
            locale_special_occupants[2][i] = list()
            occupants = model.schedule._agents[i].occupants
            locale_occupants[2][i].extend(occupants) if len(occupants) > 0 else None
            special_occupants = model.schedule._agents[i].students_occupants
            locale_special_occupants[2][i].extend(special_occupants) if len(
                special_occupants
            ) > 0 else None
            print(f"Locale {i} has: {locale_occupants[2][i]}")
            print(f"Locale {i} has special: {locale_special_occupants[2][i]}")

        assert (
            locale_special_occupants[0][11] == []
            and locale_special_occupants[0][12] == []
            and locale_special_occupants[1][11] == human_agent_id_list[0:5]
            and locale_special_occupants[1][12] == []
            and locale_special_occupants[2][11] == human_agent_id_list[0:5]
            and locale_special_occupants[2][12] == human_agent_id_list[5:10]
        )


class TestHealthCareUnit:
    def test_method_update_patients_occupation(self):

        model = SimulationModel()
        graph = NetworkxBipartiteGraph()
        model.graph = graph

        locale_agent_id_list = list()
        human_agent_id_list = list()
        for i in range(11, 13):
            locale = HealthCareUnit(unique_id=i, model=model)
            locale.max_capacity_nominal = 10
            model.schedule.add(locale)
            model.graph.add_node_to_component_zero(i)
            locale_agent_id_list.append(i)
        for i in range(0, 5):
            human = Human(unique_id=i, model=model)
            model.schedule.add(human)
            new_occupation = Worker()
            new_occupation.category = WorkerCategory.GENERIC
            human.occupation = new_occupation
            human.occupation._human = human
            model.graph.add_node_to_component_one(i)
            human_agent_id_list.append(i)
        for i in range(5, 10):
            human = Human(unique_id=i, model=model)
            model.schedule.add(human)
            new_occupation = GenericOccupation()
            new_occupation.category = GenericOccupationCategory.GENERIC
            human.occupation = new_occupation
            human.occupation._human = human
            model.graph.add_node_to_component_one(i)
            human_agent_id_list.append(i)

        locale_occupants = dict()
        locale_special_occupants = dict()

        for j in range(2):
            model.step()
            locale_occupants[j] = dict()
            locale_special_occupants[j] = dict()

            for i in range(11, 13):
                locale_occupants[j][i] = list()
                locale_special_occupants[j][i] = list()
                occupants = model.schedule._agents[i].occupants
                locale_occupants[j][i].extend(occupants) if len(occupants) > 0 else None
                special_occupants = model.schedule._agents[i].patients_occupants
                locale_special_occupants[j][i].extend(special_occupants) if len(
                    special_occupants
                ) > 0 else None
                print(f"Locale {i} has: {locale_occupants[j][i]}")
                print(f"Locale {i} has special: {locale_special_occupants[j][i]}")
            for i in range(5 * j, 5 * j + 5):
                mobile_agent = model.schedule._agents[i]
                mobile_agent.change_position(j + 11)
                print(
                    f"Human {i} position is: {mobile_agent.position}; "
                    f"and last positions was {mobile_agent.get_last_positions()}"
                )

        model.step()
        locale_occupants[2] = dict()
        locale_special_occupants[2] = dict()
        for i in range(11, 13):
            locale_occupants[2][i] = list()
            locale_special_occupants[2][i] = list()
            occupants = model.schedule._agents[i].occupants
            locale_occupants[2][i].extend(occupants) if len(occupants) > 0 else None
            special_occupants = model.schedule._agents[i].patients_occupants
            locale_special_occupants[2][i].extend(special_occupants) if len(
                special_occupants
            ) > 0 else None
            print(f"Locale {i} has: {locale_occupants[2][i]}")
            print(f"Locale {i} has special: {locale_special_occupants[2][i]}")

        assert (
            locale_special_occupants[0][11] == []
            and locale_special_occupants[0][12] == []
            and locale_special_occupants[1][11] == human_agent_id_list[0:5]
            and locale_special_occupants[1][12] == []
            and locale_special_occupants[2][11] == human_agent_id_list[0:5]
            and locale_special_occupants[2][12] == human_agent_id_list[5:10]
        )
