from complex_epidemics.agents.disease import Disease
from complex_epidemics.agents.human import Human
from complex_epidemics.agents.support_objects.disease.disease_instance import (
    DiseaseInstance,
)
from complex_epidemics.agents.support_objects.human.health_protection_measures import (
    ProtectionMeasureType,
)
from complex_epidemics.model.simulation_model import SimulationModel


class TestDisease:
    def test_instantiation(self):

        model = SimulationModel()
        new_disease = Disease(unique_id=0, model=model)

        assert isinstance(new_disease, Disease)

    def test_method_try_infecting_host(self):

        model = SimulationModel()
        host_a = Human(unique_id=1, model=model)
        host_a.health.start_protection_measure(ProtectionMeasureType.SOCIALDISTANCING)
        host_b = Human(unique_id=1, model=model)

        new_disease = Disease(unique_id=0, model=model)

        disease_instance = DiseaseInstance()
        disease_instance.disease = new_disease

        new_disease.infectivity = 0.04
        new_disease.disease_instance_prototype = disease_instance

        host_a_infected = new_disease.try_infecting_host(
            host=host_a, infectivity=new_disease.infectivity
        )
        host_b_infected = new_disease.try_infecting_host(
            host=host_b, infectivity=new_disease.infectivity
        )
        print()
        print(host_a.health.diseases)
        print(host_a.health.diseases)

        assert isinstance(host_a_infected, bool) and isinstance(host_b_infected, bool)

    # def test_method_spread_through_container(self):
    #
    #     model = SimulationModel()
    #     host_a = Human(unique_id=1, model=model)
    #     host_a.health.start_protection_measure(ProtectionMeasureType.SOCIALDISTANCING)
    #     host_b = Human(unique_id=1, model=model)
    #
    #     for i in range(1, 11):
    #         model.schedule.add(Human(unique_id=i, model=model))
    #
    #
    #
    #
    #
    #     new_disease = Disease(unique_id=0, model=model)
    #
    #     disease_instance = DiseaseInstance()
    #     disease_instance.disease = new_disease
    #
    #     new_disease.infectivity = 0.04
    #     new_disease.disease_instance_prototype = disease_instance
