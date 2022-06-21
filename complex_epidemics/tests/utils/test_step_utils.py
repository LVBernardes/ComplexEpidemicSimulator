from typing import Any

from mesa import Agent, Model

from complex_epidemics.model.support_objects.abstract_model_step_helpers import (
    IModelStepper,
)
from complex_epidemics.utils.step_utils import StepUtils


class AttributeClassA(IModelStepper):
    def __init__(self):
        self.attr_class_C = AttributeClassC()

    def step(self):
        print(f"AttributeClassA step method executed.")


class AttributeClassB(IModelStepper):
    def __init__(self):
        pass

    def step(self):
        print(f"AttributeClassB step method executed.")


class AttributeClassC(IModelStepper):
    def __init__(self):
        pass

    def step(self):
        print(f"AttributeClassC step method executed.")


class MockAgent(Agent):
    def __init__(self, model):
        self.unique_id = 0
        self.model = model
        self.attr_class_A = AttributeClassA()
        self.attr_class_B = AttributeClassB()

    def step(self):
        print(f"MockAgent({self.unique_id}) step method executed.")

    def mock_method(self):
        print(f"MockAgent({self.unique_id}) mock method executed.")


class MockModel(Model):
    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)

    def step(self):
        print(f"MockModel step method executed.")


class TestStepUtils:
    def test_method_remove_dunder_methods(self):

        dunder_list = ["__dunder1__", "__dunder2__"]
        nondunder_list = ["nondunder1", "nondunder2"]

        test_list = []
        test_list.extend(dunder_list)
        test_list.extend(nondunder_list)

        assert StepUtils.remove_dunder_methods(test_list) == nondunder_list

    def test_method_get_elements_with_step_method(self):

        print()
        print("-----------------------------------------")
        model = MockModel()
        agent_a = MockAgent(model)
        agent_b = MockAgent(model)
        agent_a.attr_agent = agent_b

        test_elements_list = [
            "agent_a.attr_class_A",
            "agent_a.attr_class_A.attr_class_C",
            "agent_a.attr_class_B",
        ]

        assert (
            StepUtils.get_elements_with_step_method(agent_a, "agent_a")
            == test_elements_list
        )
