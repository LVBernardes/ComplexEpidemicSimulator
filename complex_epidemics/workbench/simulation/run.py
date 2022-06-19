from attr import define, field
from mesa import Model

from complex_epidemics.workbench.simulation.run_session import RunSession


@define
class Run:

    session_run: RunSession = field()
    model: Model = field()
    stop_criteria: dict = field()

    def run(self):
        pass
