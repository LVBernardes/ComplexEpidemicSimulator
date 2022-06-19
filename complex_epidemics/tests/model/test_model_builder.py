import enum

from mesa.time import BaseScheduler

from complex_epidemics.graph.graph_factory import GraphFactory
from complex_epidemics.model.model_builder import SimulationModelBuilder
from complex_epidemics.model.support_objects.clock import Clock


class TestModelBuilder:
    def test_class_instantiation(self):

        nem_builder = SimulationModelBuilder()

        assert isinstance(nem_builder, SimulationModelBuilder)

    def test_method_assemble_method(self):

        graph_factory = GraphFactory()
        new_graph = graph_factory.new_contact_graph()
        new_clock = Clock()
        new_builder = SimulationModelBuilder()

        recipe_enum = enum.Enum(
            "Recipe",
            {
                "clock": new_clock,
                "schedule": BaseScheduler(new_builder._model),
                "graph": new_graph,
            },
        )

        new_builder.assemble_element(recipe_enum.clock)
        new_builder.assemble_element(recipe_enum.schedule)
        new_builder.assemble_element(recipe_enum.graph)

        assert (
            isinstance(new_builder._model.clock, Clock)
            and isinstance(new_builder._model.schedule, BaseScheduler)
            and isinstance(new_builder._model.graph, type(new_graph))
        )
