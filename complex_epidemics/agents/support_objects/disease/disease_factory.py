from complex_epidemics.agents.disease import Disease
from complex_epidemics.agents.support_objects.disease.disease_instance_builder import (
    DiseaseInstanceBuilder,
)
from complex_epidemics.agents.support_objects.disease.disease_recipes import (
    DiseaseRecipe,
)
from complex_epidemics.model.simulation_model import SimulationModel
from complex_epidemics.utils.id_utils import IDUtils


class DiseaseFactory:
    @staticmethod
    def covid_19_standard(model: SimulationModel, initial_infected: float, base_infection_probability: float = 0.04) -> Disease:

        disease_global = Disease(unique_id=IDUtils.generate_id(), model=model)
        disease_global.name = "COVID-19"
        disease_global.strain = "Generic-Alpha"
        disease_global.initial_infected_population = initial_infected
        disease_global.recipe = DiseaseRecipe.COVID19STANDARD
        disease_global._disease_instance_builder = DiseaseInstanceBuilder()
        disease_global.infectivity = base_infection_probability
        disease_global.immunity_window_in_days = 60

        return disease_global
