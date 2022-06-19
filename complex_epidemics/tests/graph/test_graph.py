import importlib

import complex_epidemics.graph.graph_engine as cxe_graph_engine


class TestStandardGraph:
    def test_graph_instantiation(self):

        for engine in cxe_graph_engine.GraphEngine:
            engine_name = engine.value
            engine_name_lowercase = engine_name.lower()
            graph_module = importlib.import_module(
                f"complex_epidemics.graph."
                f"{engine_name_lowercase}_engine."
                f"{engine_name_lowercase}_graph"
            )
            graph_class = getattr(graph_module, f"{engine_name}Graph")
            graph_instance = graph_class()
            assert isinstance(graph_instance, graph_class)

    def test_graph_method_add_node(self):

        for engine in cxe_graph_engine.GraphEngine:
            engine_name = engine.value
            engine_name_lowercase = engine_name.lower()
            graph_module = importlib.import_module(
                f"complex_epidemics.graph."
                f"{engine_name_lowercase}_engine."
                f"{engine_name_lowercase}_graph"
            )
            graph_class = getattr(graph_module, f"{engine_name}Graph")
            graph_instance = graph_class()

            graph_instance.add_node(1)

            assert graph_instance.has_node(1)

    def test_graph_method_add_node_attributes(self):

        for engine in cxe_graph_engine.GraphEngine:
            engine_name = engine.value
            engine_name_lowercase = engine_name.lower()
            graph_module = importlib.import_module(
                f"complex_epidemics.graph."
                f"{engine_name_lowercase}_engine."
                f"{engine_name_lowercase}_graph"
            )
            graph_class = getattr(graph_module, f"{engine_name}Graph")
            graph_instance = graph_class()

            node_attrs = {"attr1": "value1", "attr2": "value2"}
            graph_instance.add_node(1)
            graph_instance.add_node_attributes(1, node_attrs)

            assert graph_instance.get_node(1) == node_attrs

    def test_graph_method_get_nodes(self):

        for engine in cxe_graph_engine.GraphEngine:
            engine_name = engine.value
            engine_name_lowercase = engine_name.lower()
            graph_module = importlib.import_module(
                f"complex_epidemics.graph."
                f"{engine_name_lowercase}_engine."
                f"{engine_name_lowercase}_graph"
            )
            graph_class = getattr(graph_module, f"{engine_name}Graph")
            graph_instance = graph_class()

            node_list = range(10)

            for node in node_list:
                graph_instance.add_node(node)

            assert graph_instance.get_nodes() == list(node_list)
