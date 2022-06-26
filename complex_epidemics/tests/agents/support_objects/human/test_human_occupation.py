from complex_epidemics.agents.support_objects.citizen_factory import CitizenFactory
from complex_epidemics.agents.support_objects.human.human_occupation import Occupation
from complex_epidemics.agents.support_objects.human.human_occupation_categories import (
    WorkerCategory,
)
from complex_epidemics.agents.support_objects.infrastructure_builder import (
    InfrastructureBuilder,
)
from complex_epidemics.agents.support_objects.locale.locale_categories import (
    EducationalInstitutionCategory,
    HealthCareCategory,
    HouseholdCategory,
    PublicPlaceCategory,
    WorkplaceCategory,
)
from complex_epidemics.graph.networkx_engine.networkx_bipartitegraph import (
    NetworkxBipartiteGraph,
)
from complex_epidemics.model.simulation_model import SimulationModel


class TestHumanOccupation:
    def test_instantiation(self):

        new_occupation = Occupation()

        assert isinstance(new_occupation, Occupation)

    def test_method_assign_occupation_locale(self):

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

        model.step()
        model.step()

        result_generic_worker_occupation_locale_class = model.schedule._agents[
            generic_worker.occupation.occupation_locale.unique_id
        ].__class__.__name__
        result_generic_student_occupation_locale_class = model.schedule._agents[
            generic_student.occupation.occupation_locale.unique_id
        ].__class__.__name__
        result_generic_unoccupation_locale_class = model.schedule._agents[
            generic_unoccupied.occupation.occupation_locale.unique_id
        ].__class__.__name__
        result_generic_health_worker_locale_class = model.schedule._agents[
            generic_health_worker.occupation.occupation_locale.unique_id
        ].__class__.__name__
        result_generic_public_worker_locale_class = model.schedule._agents[
            generic_public_worker.occupation.occupation_locale.unique_id
        ].__class__.__name__

        expected_generic_worker_occupation_locale_class = "Workplace"
        expected_generic_student_occupation_locale_class = "EducationalInstitution"
        expected_generic_unoccupation_locale_class = "Household"
        expected_generic_health_worker_locale_class = "HealthCareUnit"
        expected_generic_public_worker_locale_class = "PublicPlace"

        assert (
            result_generic_worker_occupation_locale_class
            == expected_generic_worker_occupation_locale_class
            and result_generic_student_occupation_locale_class
            == expected_generic_student_occupation_locale_class
            and result_generic_unoccupation_locale_class
            == expected_generic_unoccupation_locale_class
            and result_generic_health_worker_locale_class
            == expected_generic_health_worker_locale_class
            and result_generic_public_worker_locale_class
            == expected_generic_public_worker_locale_class
        )
