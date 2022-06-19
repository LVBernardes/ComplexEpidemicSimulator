import importlib

import complex_epidemics.graph.graph_engine as cxe_graph_engine


class TestBipartiteGraph:
    def test_graph_instantiation(self):

        for engine in cxe_graph_engine.GraphEngine:
            engine_name = engine.value
            engine_name_lowercase = engine_name.lower()
            graph_module = importlib.import_module(
                f"complex_epidemics.graph."
                f"{engine_name_lowercase}_engine."
                f"{engine_name_lowercase}_bipartitegraph"
            )
            graph_class = getattr(graph_module, f"{engine_name}BipartiteGraph")
            graph_instance = graph_class()
            assert isinstance(graph_instance, graph_class)

    def test_graph_method_add_node_to_component_zero(self):
        for engine in cxe_graph_engine.GraphEngine:
            engine_name = engine.value
            engine_name_lowercase = engine_name.lower()
            graph_module = importlib.import_module(
                f"complex_epidemics.graph."
                f"{engine_name_lowercase}_engine."
                f"{engine_name_lowercase}_bipartitegraph"
            )
            graph_class = getattr(graph_module, f"{engine_name}BipartiteGraph")
            graph_instance = graph_class()

            graph_instance.add_node_to_component_zero(1)

            assert graph_instance.get_node_component(1) == 0

    def test_graph_method_add_node_to_component_one(self):
        for engine in cxe_graph_engine.GraphEngine:
            engine_name = engine.value
            engine_name_lowercase = engine_name.lower()
            graph_module = importlib.import_module(
                f"complex_epidemics.graph."
                f"{engine_name_lowercase}_engine."
                f"{engine_name_lowercase}_bipartitegraph"
            )
            graph_class = getattr(graph_module, f"{engine_name}BipartiteGraph")
            graph_instance = graph_class()

            graph_instance.add_node_to_component_one(1)

            assert graph_instance.get_node_component(1) == 1
