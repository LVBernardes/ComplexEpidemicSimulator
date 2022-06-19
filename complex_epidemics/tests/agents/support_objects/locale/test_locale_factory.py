from mesa.time import BaseScheduler

from complex_epidemics.agents.locale import (
    EducationalInstitution,
    HealthCareUnit,
    Household,
    PublicPlace,
    Workplace,
)
from complex_epidemics.agents.support_objects.locale.locale_factory import LocaleFactory
from complex_epidemics.graph.networkx_engine.networkx_bipartitegraph import (
    NetworkxBipartiteGraph,
)
from complex_epidemics.model.simulation_model import SimulationModel


class TestLocaleFactory:
    def test_instantiation(self):

        new_factory = LocaleFactory()

        assert isinstance(new_factory, LocaleFactory)

    def test_method_new_household(self):

        new_factory = LocaleFactory()
        model = SimulationModel()
        model.graph = NetworkxBipartiteGraph()
        model.schedule = BaseScheduler(model)

        capacity_data = {"nominal": {"type": "none", "parameters": [4]}}

        household_a = new_factory.new_household(model=model)
        household_b = new_factory.new_household(
            model=model, capacity_data=capacity_data
        )

        assert (
            isinstance(household_a, Household) and household_b.max_capacity_nominal == 4
        )

    def test_method_new_workplace(self):

        new_factory = LocaleFactory()
        model = SimulationModel()
        model.graph = NetworkxBipartiteGraph()
        model.schedule = BaseScheduler(model)

        capacity_data = {"nominal": {"type": "none", "parameters": [15]}}

        workplace_a = new_factory.new_workplace(model=model)
        workplace_b = new_factory.new_workplace(
            model=model, capacity_data=capacity_data
        )

        assert (
            isinstance(workplace_a, Workplace)
            and workplace_b.max_capacity_nominal == 15
        )

    def test_method_new_educational_institution(self):

        new_factory = LocaleFactory()
        model = SimulationModel()
        model.graph = NetworkxBipartiteGraph()
        model.schedule = BaseScheduler(model)

        capacity_data = {
            "nominal": {"type": "none", "parameters": [50]},
            "students": {"type": "none", "parameters": [40]},
        }

        educational_a = new_factory.new_educational_institution(model=model)
        educational_b = new_factory.new_educational_institution(
            model=model, capacity_data=capacity_data
        )

        assert (
            isinstance(educational_a, EducationalInstitution)
            and educational_b.max_capacity_nominal == 50
            and educational_b.max_capacity_students == 40
        )

    def test_method_new_health_care_unit(self):

        new_factory = LocaleFactory()
        model = SimulationModel()
        model.graph = NetworkxBipartiteGraph()
        model.schedule = BaseScheduler(model)

        capacity_data = {
            "nominal": {"type": "none", "parameters": [30]},
            "patients": {"type": "none", "parameters": [20]},
        }

        healthcareunit_a = new_factory.new_health_care_unit(model=model)
        healthcareunit_b = new_factory.new_health_care_unit(
            model=model, capacity_data=capacity_data
        )

        assert (
            isinstance(healthcareunit_a, HealthCareUnit)
            and healthcareunit_b.max_capacity_nominal == 30
            and healthcareunit_b.max_capacity_patients == 20
        )

    def test_method_new_public_place(self):

        new_factory = LocaleFactory()
        model = SimulationModel()
        model.graph = NetworkxBipartiteGraph()
        model.schedule = BaseScheduler(model)

        capacity_data = {
            "nominal": {"type": "none", "parameters": [50]},
            "effective": {"type": "none", "parameters": [80]},
        }

        publicplace_a = new_factory.new_public_place(model=model)
        publicplace_b = new_factory.new_public_place(
            model=model, capacity_data=capacity_data
        )

        assert (
            isinstance(publicplace_a, PublicPlace)
            and publicplace_b.max_capacity_nominal == 50
            and publicplace_b.max_capacity_effective == 80
        )
