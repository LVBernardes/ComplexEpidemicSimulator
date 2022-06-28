from complex_epidemics.agents.support_objects.disease.disease_factory import DiseaseFactory
from complex_epidemics.agents.support_objects.disease.immunity_instance import ImmunityInstance
from complex_epidemics.model.simulation_model import SimulationModel


class TestImmunityInstance:

    def test_instantiation(self):

        model = SimulationModel()
        disease = DiseaseFactory.covid_19_standard(model, 0.04)
        immunity_instance = ImmunityInstance(disease)

        assert isinstance(immunity_instance, ImmunityInstance)

    def test_method_step(self):

        model = SimulationModel()
        disease = DiseaseFactory.covid_19_standard(model, 0.04)
        immunity_instance = ImmunityInstance(disease)

        expiration = immunity_instance.expiration

        for _ in range(expiration+1):
            immunity_instance.step()

        assert immunity_instance.active == False
