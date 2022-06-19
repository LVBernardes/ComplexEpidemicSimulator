from complex_epidemics.graph.graph_factory import GraphFactory
from complex_epidemics.graph.networkx_engine.networkx_bipartitegraph import (
    NetworkxBipartiteGraph,
)
from complex_epidemics.graph.networkx_engine.networkx_graph import NetworkxGraph


class TestGraphFactory:
    def test_instantiation(self):
        graph_factory = GraphFactory()

        assert isinstance(graph_factory, GraphFactory)

    def test_method_new_contact_graph(self):
        graph_factory = GraphFactory()

        new_contact_graph = graph_factory.new_contact_graph(engine="networkx")

        assert isinstance(new_contact_graph, NetworkxGraph)

    def test_method_new_space_graph(self):
        graph_factory = GraphFactory()

        new_contact_graph = graph_factory.new_space_graph(engine="networkx")

        assert isinstance(new_contact_graph, NetworkxBipartiteGraph)
