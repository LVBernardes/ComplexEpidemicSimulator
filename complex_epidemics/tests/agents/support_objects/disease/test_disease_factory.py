from complex_epidemics.agents.disease import Disease
from complex_epidemics.agents.support_objects.disease.disease_factory import (
    DiseaseFactory,
)
from complex_epidemics.agents.support_objects.disease.disease_instance import (
    DiseaseInstance,
)
from complex_epidemics.model.simulation_model import SimulationModel


class TestDiseaseFactory:
    def test_instantiation(self):

        new_factory = DiseaseFactory()

        assert isinstance(new_factory, DiseaseFactory)

    def test_factory_product_covid_19_standard(self):

        new_factory = DiseaseFactory()

        new_disease = new_factory.covid_19_standard(model=SimulationModel(), initial_infected=1)

        assert (
            isinstance(new_disease, Disease)
            and new_disease.name == "COVID-19"
        )
