from mesa.time import BaseScheduler

from complex_epidemics.agents.support_objects.locale.locale_categories import (
    EducationalInstitutionCategory,
    HealthCareCategory,
    HouseholdCategory,
    PublicPlaceCategory,
    WorkplaceCategory,
)
from complex_epidemics.workbench.simulation.infrastructure_builder import (
    InfrastructureBuilder,
)
from complex_epidemics.graph.networkx_engine.networkx_bipartitegraph import (
    NetworkxBipartiteGraph,
)
from complex_epidemics.model.simulation_model import SimulationModel


class TestInfrastructureBuilder:
    def test_instantiation(self):

        new_builder = InfrastructureBuilder()

        assert isinstance(new_builder, InfrastructureBuilder)

    def test_infrastructure_building_feature(self):

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
        model.schedule = BaseScheduler(model)

        new_builder.set_model(model=model)
        new_builder.set_household_config(city_data.get("household"))
        new_builder.set_workplace_config(city_data.get("workplace"))
        new_builder.set_educational_config(city_data.get("educational"))
        new_builder.set_healthcare_config(city_data.get("healthcare"))
        new_builder.set_public_config(city_data.get("public"))

        new_builder.build()

        model, city = new_builder.get_result()
        [print(item.__class__.__name__) for item in city]
