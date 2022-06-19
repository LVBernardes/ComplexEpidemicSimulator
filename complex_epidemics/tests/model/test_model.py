from complex_epidemics.model.simulation_model import SimulationModel


class TestSimulationModel:
    def test_class_instantiation(self):

        new_model = SimulationModel()

        assert isinstance(new_model, SimulationModel)

    def test_class_attributes_required(self):

        nem_model = SimulationModel()

        assert (
            hasattr(nem_model, "step")
            and hasattr(nem_model, "clock")
            and hasattr(nem_model, "graph")
            and hasattr(nem_model, "schedule")
        )
