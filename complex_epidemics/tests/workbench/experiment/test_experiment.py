from complex_epidemics.workbench.experiment.experiment import Experiment


class TestExperiment:
    def test_instantiation(self):

        new_experiment = Experiment()

        assert isinstance(new_experiment, Experiment)
