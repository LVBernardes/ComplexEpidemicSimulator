import copy
from collections import Counter
from multiprocessing import Pool
from typing import Any

from attrs import define, field
from tqdm import tqdm

from complex_epidemics.workbench.simulation.run import Run
from complex_epidemics.workbench.support_objects.state import State


@define
class RunSession:

    session_model_parameters: dict = field(init=False)
    session_agent_parameters: dict = field(init=False)
    simulation_parameters: dict = field(init=False)
    iterations_per_run_session: int = field(init=False)
    state: State = field(default=State.CREATED)
    runs: list[Run] = field(init=False)
    run_template: Run = field(init=False)
    number_processes: int = field(default=1)
    display_progress_bar: bool = field(default=True)

    def generate_run_template(self):
        pass

    def executable_run(self):
        run_object = copy.deepcopy(self.run_template)
        run_object.execute()
        self.runs.append(run_object)

    def play(self):

        run_counter = count()

        results: list[dict[str, Any]] = []

        with tqdm(
            self.iterations_per_run_session, disable=not self.display_progress_bar
        ) as pbar:
            if self.number_processes == 1:
                for iterator in range(self.iterations_per_run_session):
                    self.executable_run()
                    pbar.update()
            else:
                with Pool(self.number_processes) as p:
                    for iterator, _ in p.imap_unordered(
                        self.executable_run, range(self.iterations_per_run_session)
                    ):
                        next(iterator)
                        pbar.update()
