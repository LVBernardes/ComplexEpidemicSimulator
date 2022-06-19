from complex_epidemics.agents.disease import Disease
from complex_epidemics.agents.human import Human
from complex_epidemics.agents.support_objects.disease.disease_instance import (
    DiseaseInstance,
)
from complex_epidemics.agents.support_objects.disease.disease_states_and_symptoms import (
    DiseaseInstanceState,
    Symptoms,
    IncubatedNoSymptoms,
    NonInfectiousNoSymptoms,
    NonInfectiousDeath,
    InfectiousNoSymptoms,
    InfectiousMildModerateSymptoms,
    InfectiousSevereSymptoms,
    InfectiousCriticalSymptoms,
)
from complex_epidemics.model.simulation_model import SimulationModel
from complex_epidemics.utils.disease_state_utils import (
    LogNormalUtils,
    SkewedNormalUtils,
)


class TesteDiseaseInstance:
    def test_instantiation(self):

        new_instance = DiseaseInstance()

        assert isinstance(new_instance, DiseaseInstance)

    def test_method_transition_to_state(self):

        incubated_no_symptoms_state = IncubatedNoSymptoms()
        incubated_no_symptoms_state.transition_table = {
            (DiseaseInstanceState.INFECTIOUS, Symptoms.NONE): 0.3,
            (DiseaseInstanceState.INFECTIOUS, Symptoms.MILDMODERATE): 0.7,
        }
        non_infectious_no_symptoms_state = NonInfectiousNoSymptoms()
        non_infectious_no_symptoms_state.transition_table = {}
        non_infectious_death_state = NonInfectiousDeath()
        non_infectious_death_state.transition_table = {}
        infectious_no_symptoms_state = InfectiousNoSymptoms()
        infectious_no_symptoms_state.transition_table = {
            (DiseaseInstanceState.NONINFECTIOUS, Symptoms.NONE): 1.0
        }
        infectious_mild_moderate_symptoms_state = InfectiousMildModerateSymptoms()
        infectious_mild_moderate_symptoms_state.transition_table = {
            (DiseaseInstanceState.NONINFECTIOUS, Symptoms.NONE): 0.85,
            (DiseaseInstanceState.INFECTIOUS, Symptoms.SEVERE): 0.15,
        }
        infectious_severe_symptoms_state = InfectiousSevereSymptoms()
        infectious_severe_symptoms_state.transition_table = {
            (DiseaseInstanceState.NONINFECTIOUS, Symptoms.NONE): 0.8,
            (DiseaseInstanceState.INFECTIOUS, Symptoms.CRITICAL): 0.05,
            (DiseaseInstanceState.NONINFECTIOUS, Symptoms.DEATH): 0.15,
        }
        infectious_critical_symptoms_state = InfectiousCriticalSymptoms()
        infectious_critical_symptoms_state.transition_table = {
            (DiseaseInstanceState.NONINFECTIOUS, Symptoms.NONE): 0.5,
            (DiseaseInstanceState.NONINFECTIOUS, Symptoms.DEATH): 0.5,
        }

        new_instance = DiseaseInstance()
        all_states = {
            (
                DiseaseInstanceState.INCUBATED,
                Symptoms.NONE,
            ): incubated_no_symptoms_state,
            (
                DiseaseInstanceState.INFECTIOUS,
                Symptoms.NONE,
            ): infectious_no_symptoms_state,
            (
                DiseaseInstanceState.INFECTIOUS,
                Symptoms.MILDMODERATE,
            ): infectious_mild_moderate_symptoms_state,
            (
                DiseaseInstanceState.INFECTIOUS,
                Symptoms.SEVERE,
            ): infectious_severe_symptoms_state,
            (
                DiseaseInstanceState.INFECTIOUS,
                Symptoms.CRITICAL,
            ): infectious_critical_symptoms_state,
            (
                DiseaseInstanceState.NONINFECTIOUS,
                Symptoms.NONE,
            ): non_infectious_no_symptoms_state,
            (
                DiseaseInstanceState.NONINFECTIOUS,
                Symptoms.DEATH,
            ): non_infectious_death_state,
        }
        new_instance.all_states = all_states

        transition_one_expected = "IncubatedNoSymptoms"
        transition_two_expected = "InfectiousNoSymptoms"

        new_instance.transition_to_state(
            (DiseaseInstanceState.INCUBATED, Symptoms.NONE)
        )
        transition_one_response = new_instance.state.__class__.__name__

        new_instance.transition_to_state(
            (DiseaseInstanceState.INFECTIOUS, Symptoms.NONE)
        )

        transition_two_response = new_instance.state.__class__.__name__

        print()
        print(transition_one_response)
        print(transition_two_response)
        print()

        assert (
            transition_one_expected == transition_one_response
            and transition_two_expected == transition_two_response
        )

    def test_method_step(self):

        model = SimulationModel()
        disease = Disease(unique_id=10101010, model=model)
        new_disease_instance = DiseaseInstance()
        self.disease_recipe = {
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

        all_states = dict()
        for key, value in self.disease_recipe["states"].items():
            new_built_state = eval(f'{value.get("state_class")}()')

            new_built_state.disease_instance = new_disease_instance
            new_built_state.transition_table = value.get("transition_table")

            evaluator_name = value.get("evaluator_class")
            evaluator_params = value.get("evaluator_params")
            if evaluator_name == "lognorm":
                if evaluator_params:
                    evaluator = LogNormalUtils.get_instance(
                        s=evaluator_params.get("s"),
                        loc=evaluator_params.get("loc"),
                        scale=evaluator_params.get("scale"),
                    )
                else:
                    raise ValueError(
                        'Not parameters for evaluator of type "lognorm" informed.'
                    )
            elif evaluator_name == "skewnorm":
                if evaluator_params:
                    evaluator = SkewedNormalUtils.get_instance(
                        a=evaluator_params.get("a"),
                        loc=evaluator_params.get("loc"),
                        scale=evaluator_params.get("scale"),
                    )
                else:
                    raise ValueError(
                        'Not parameters for evaluator of type "skewnorm" informed.'
                    )
            else:
                raise ValueError("Evaluator class not implemented.")
            new_built_state._transition_evaluator = evaluator

            all_states[key] = new_built_state

        new_disease_instance.all_states = all_states
        new_disease_instance.transition_to_state(
            (DiseaseInstanceState.INCUBATED, Symptoms.NONE)
        )
        new_disease_instance.host = Human(0, SimulationModel())
        new_disease_instance.disease = disease

        i = 0
        while i < 24 * 30:
            new_disease_instance.step()
            print()
            print("---------------------------------------------------")
            print(f"Step: {i}.")
            i += 1
