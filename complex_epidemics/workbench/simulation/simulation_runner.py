class SimulationRunner:
    def __init__(self, run_session_list: list):
        self.run_session_list = run_session_list
        self._execution_queue = None

    def execute_run(self):
        pass

    def execute_run_session(self):
        pass

    def register_run_in_execution_queue(self):
        pass

    def remove_run_from_execution_queue(self):
        pass
