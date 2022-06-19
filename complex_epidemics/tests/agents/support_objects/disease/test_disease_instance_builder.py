from complex_epidemics.agents.disease import Disease
from complex_epidemics.agents.human import Human
from complex_epidemics.agents.support_objects.disease.disease_instance_builder import (
    DiseaseInstanceBuilder,
)
from complex_epidemics.agents.support_objects.disease.disease_states_and_symptoms import (
    DiseaseInstanceState,
    Symptoms,
)
from complex_epidemics.model.simulation_model import SimulationModel


class TestDiseaseInstanceBuilder:
    def test_instantiation(self):

        new_factory = DiseaseInstanceBuilder()

        assert isinstance(new_factory, DiseaseInstanceBuilder)

    def test_new_instance_build_process(self):

        disease_recipe = {
            "incubated_transition_evaluator": {
                "name": "lognorm",
                "module": "scipy.stats",
                "params": "",
            },
            "infectious_transition_evaluator": {
                "name": "norm",
                "module": "scipy.stats",
                "params": "",
            },
            "states": {
                (DiseaseInstanceState.INCUBATED, Symptoms.NONE): {
                    "state_class": "IncubatedNoSymptoms",
                    "evaluator_class": "lognorm",
                    "evaluator_params": {
                        "s": 0.6948414667108022,
                        "loc": 0.0,
                        "scale": 6.781675060386135,
                    },
                    "transition_table": {
                        (DiseaseInstanceState.INFECTIOUS, Symptoms.NONE): 0.3,
                        (DiseaseInstanceState.INFECTIOUS, Symptoms.MILDMODERATE): 0.7,
                    },
                },
                (DiseaseInstanceState.INFECTIOUS, Symptoms.NONE): {
                    "state_class": "InfectiousNoSymptoms",
                    "evaluator_class": "skewnorm",
                    "evaluator_params": {"a": -3.0, "loc": 13.0, "scale": 3.5},
                    "transition_table": {
                        (DiseaseInstanceState.NONINFECTIOUS, Symptoms.NONE): 1.0
                    },
                },
                (DiseaseInstanceState.INFECTIOUS, Symptoms.MILDMODERATE): {
                    "state_class": "InfectiousMildModerateSymptoms",
                    "evaluator_class": "skewnorm",
                    "evaluator_params": {"a": -3.0, "loc": 15.0, "scale": 5.0},
                    "transition_table": {
                        (DiseaseInstanceState.NONINFECTIOUS, Symptoms.NONE): 0.85,
                        (DiseaseInstanceState.INFECTIOUS, Symptoms.SEVERE): 0.15,
                    },
                },
                (DiseaseInstanceState.INFECTIOUS, Symptoms.SEVERE): {
                    "state_class": "InfectiousSevereSymptoms",
                    "evaluator_class": "skewnorm",
                    "evaluator_params": {"a": 0.0, "loc": 22.5, "scale": 1.0},
                    "transition_table": {
                        (DiseaseInstanceState.NONINFECTIOUS, Symptoms.NONE): 0.8,
                        (DiseaseInstanceState.INFECTIOUS, Symptoms.CRITICAL): 0.05,
                        (DiseaseInstanceState.NONINFECTIOUS, Symptoms.DEATH): 0.15,
                    },
                },
                (DiseaseInstanceState.INFECTIOUS, Symptoms.CRITICAL): {
                    "state_class": "InfectiousCriticalSymptoms",
                    "evaluator_class": "skewnorm",
                    "evaluator_params": {"a": -5, "loc": 25.0, "scale": 1.0},
                    "transition_table": {
                        (DiseaseInstanceState.NONINFECTIOUS, Symptoms.NONE): 0.5,
                        (DiseaseInstanceState.NONINFECTIOUS, Symptoms.DEATH): 0.5,
                    },
                },
                (DiseaseInstanceState.NONINFECTIOUS, Symptoms.NONE): {
                    "state_class": "NonInfectiousNoSymptoms",
                    "evaluator_class": "skewnorm",
                    "evaluator_params": {"a": -5, "loc": 25.0, "scale": 1.0},
                    "transition_table": {},
                },
                (DiseaseInstanceState.NONINFECTIOUS, Symptoms.DEATH): {
                    "state_class": "NonInfectiousDeath",
                    "evaluator_class": "skewnorm",
                    "evaluator_params": {"a": -5, "loc": 25.0, "scale": 1.0},
                    "transition_table": {},
                },
            },
        }

        mock_model = SimulationModel()
        new_builder = DiseaseInstanceBuilder()
        new_builder.set_disease_recipe(recipe=disease_recipe)
        new_builder.set_disease_instance_platform(
            disease=Disease(0, mock_model), host=Human(1, mock_model)
        )
        new_builder.build()
        new_instance = new_builder.get_result()

        i = 0
        while i < 30:
            new_instance.step()
            print()
            print("---------------------------------------------------")
            print(f"Step: {i}.")
            i += 1
