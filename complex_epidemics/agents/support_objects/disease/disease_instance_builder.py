import importlib

from complex_epidemics.agents.disease import Disease
from complex_epidemics.agents.human import Human
from complex_epidemics.agents.support_objects.disease.disease_instance import (
    DiseaseInstance,
)
from complex_epidemics.agents.support_objects.disease.abstract_disease_instance_builder import (
    IDiseaseInstanceBuilder,
)
from complex_epidemics.utils.disease_state_utils import (
    LogNormalUtils,
    SkewedNormalUtils,
)
from complex_epidemics.agents.support_objects.disease.disease_states_and_symptoms import (
    DiseaseInstanceState,
    Symptoms,
)


class DiseaseInstanceBuilder(IDiseaseInstanceBuilder):
    def __init__(
        self,
    ):
        self.new_disease_instance = None
        self.disease_instance_states = dict()
        self.disease_symptoms_states = dict()
        self.disease_recipe = None

    def get_result(self):
        new_instance = self.new_disease_instance
        self.reset()
        return new_instance

    def reset(self):
        self.new_disease_instance = None
        self.disease_instance_states = dict()
        self.disease_symptoms_states = dict()
        self.disease_recipe = None

    def set_disease_instance_platform(self, disease: Disease, host: Human):
        self.new_disease_instance = DiseaseInstance()
        self.new_disease_instance.disease = disease
        self.new_disease_instance.host = host

    def set_disease_recipe(self, recipe: dict) -> None:
        self.disease_recipe = recipe

    def build(self):
        all_states = dict()
        for key, value in self.disease_recipe["states"].items():
            state_module = importlib.import_module(
                f"complex_epidemics.agents."
                f"support_objects."
                f"disease."
                f"disease_states_and_symptoms"
            )
            state_class = getattr(state_module, f'{value.get("state_class")}')
            new_built_state = state_class()

            new_built_state.disease_instance = self.new_disease_instance
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
            print(evaluator)
            new_built_state._transition_evaluator = evaluator
            all_states[key] = new_built_state

        self.new_disease_instance.all_states = all_states
        self.new_disease_instance.transition_to_state(
            (DiseaseInstanceState.INCUBATED, Symptoms.NONE)
        )
