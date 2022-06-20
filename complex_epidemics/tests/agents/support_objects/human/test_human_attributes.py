from complex_epidemics.agents.disease import Disease
from complex_epidemics.agents.support_objects.disease.disease_instance import (
    DiseaseInstance,
)
from complex_epidemics.agents.support_objects.human.health_protection_measures import (
    MaskType,
    MaskWearing,
    ProtectionMeasureType,
)
from complex_epidemics.agents.support_objects.human.human_attributes import (
    HealthState,
    HumanHealth,
)
from complex_epidemics.model.simulation_model import SimulationModel


class TestHumanHealth:
    def test_instantiation(self):

        health = HumanHealth()

        assert isinstance(health, HumanHealth)

    def test_method_step(self):

        print()

        health = HumanHealth()

        health.step()

    def test_method_update_susceptibility_default(self):

        health = HumanHealth()

        health.update_susceptibility()
        susceptible_test_a_real = health.is_susceptible
        susceptible_test_a_expected = True
        health.health_state = HealthState.DECEASED
        health.update_susceptibility()
        susceptible_test_b_real = health.is_susceptible
        susceptible_test_b_expected = False

        assert (
            susceptible_test_a_real == susceptible_test_a_expected
            and susceptible_test_b_real == susceptible_test_b_expected
        )

    def test_method_update_susceptibility_with_immunity(self):

        health = HumanHealth()

        disease = Disease(unique_id=0, model=SimulationModel())
        disease.immunity_window_in_days = 180

        health.add_immunity_instance(disease)

        health.update_susceptibility()
        susceptible_test_a_real = health.is_susceptible
        susceptible_test_a_expected = False

        assert susceptible_test_a_real == susceptible_test_a_expected

    def test_method_update_susceptibility_with_disease(self):

        health = HumanHealth()

        disease_instance = DiseaseInstance()

        health.add_disease_instance(disease_instance)

        health.update_susceptibility()
        susceptible_test_a_real = health.is_susceptible
        susceptible_test_a_expected = False

        assert susceptible_test_a_real == susceptible_test_a_expected

    def test_method_add_protection_measure(self):

        health = HumanHealth()

        health.start_protection_measure(
            measure=ProtectionMeasureType.MASKWEARING, options=MaskType.RESPIRATOR
        )

        expected_measure_dict = {
            ProtectionMeasureType.MASKWEARING.name: MaskWearing(MaskType.RESPIRATOR)
        }

        real_measure_dict = health.protection_measures

        assert expected_measure_dict.keys() == real_measure_dict.keys()

    def test_method_drop_protection_measure(self):

        health = HumanHealth()

        health.start_protection_measure(measure=ProtectionMeasureType.HANDWASHING)

        health.drop_protection_behaviour(measure=ProtectionMeasureType.HANDWASHING)

        expected_measure_dict = {}

        real_measure_dict = health.protection_measures

        assert expected_measure_dict.keys() == real_measure_dict.keys()
