from attr import define, field

from complex_epidemics.workbench.simulation.run_session import RunSession


@define
class Simulation:
    name: str = field(init=False)
    description: str = field(init=False)
    model_parameters_batch: field(init=False)
    agents_parameters_batch: field(init=False)
    model_parameters: dict = field(init=False)
    agents_parameters: dict = field(init=False)
    iterations_per_run_session: int = field(init=False)
    run_sessions: list[RunSession] = field(init=False)

    def run(self, session: RunSession) -> None:
        pass

    def run_all(self) -> None:
        pass

    def get_session_run_data(self):
        pass

    def generate_sessions(self):
        pass

    def _create_runner(self):
        pass
