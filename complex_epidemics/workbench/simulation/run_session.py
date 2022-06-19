from attrs import define, field

from complex_epidemics.workbench.simulation.run import Run
from complex_epidemics.workbench.simulation.state import State


@define
class RunSession:

    session_model_parameters: dict = field(init=False)
    session_agent_parameters: dict = field(init=False)
    iterations_per_run_session: int = field(init=False)
    state: State = field(default=State.CREATED)
    runs: list[Run] = field(init=False)

    def play(self):
        pass
