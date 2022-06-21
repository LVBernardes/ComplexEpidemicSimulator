from complex_epidemics.model.support_objects.abstract_model_step_helpers import (
    IModelAdvancer,
)


class HumanBehaviour(IModelAdvancer):
    def __init__(self) -> None:
        pass

    def advance(self):
        pass


class StandardBehaviour(HumanBehaviour):
    def __init__(self) -> None:
        pass

    def advance(self):
        pass
