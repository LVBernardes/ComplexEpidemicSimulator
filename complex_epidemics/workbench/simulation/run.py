from attr import define, field
from mesa import Model

from complex_epidemics.workbench.simulation.run_session import RunSession


@define
class Run:

    session_run: RunSession = field()
    model: Model = field()
    stop_criteria: dict = field()

    def execute(self):
        steps = self.stop_criteria.get("steps", None)

        if steps is not None:
            step_counter = 0
            while step_counter <= steps:
                self.model.step()
