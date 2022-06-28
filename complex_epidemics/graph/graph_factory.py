# -*- coding: utf-8 -*-
"""Graph factory module.
Component of factory pattern used for graph provisioning.
"""
import importlib

from complex_epidemics.graph.support_objects.abstract_bipartite_graph import (
    AbstractBipartiteGraph,
)
from complex_epidemics.graph.support_objects.abstract_graph import AbstractGraph
from complex_epidemics.graph.graph_engine import GraphEngine
from complex_epidemics.graph.graph_type import GraphType


class GraphFactory:
    def __init__(self):
        pass

    @staticmethod
    def new_space_graph(engine: str = "networkx") -> AbstractGraph:
        """Creates a new bipartite graph instance based on defined engine.

        Parameters
        ----------
        engine: {'networkx', 'igraph'}
            Graph engine to be used for graph instantiation.

        Returns
        -------
        graph:
            Returns a new implementation of `AbstractBipartiteGraph` using
            the `engine` defined in parameters.
        """
        for enum in GraphEngine:
            engine_name = enum.value
            engine_name_lowercase = engine_name.lower()
            if engine_name_lowercase == engine.lower():
                factory_module = importlib.import_module(
                    f"complex_epidemics.graph."
                    f"{engine_name_lowercase}_engine."
                    f"{engine_name_lowercase}_factory"
                )
                graph_class = getattr(factory_module, f"{engine_name}Factory")
                new_factory = graph_class()
                graph = new_factory.create_graph(graph_type=GraphType.BIPARTITEGRAPH)
                return graph

    @staticmethod
    def new_contact_graph(engine: str = "networkx") -> AbstractBipartiteGraph:
        """Creates a new graph instance based on defined engine.

        Parameters
        ----------
        engine: {'networkx', 'igraph'}
            Graph engine to be used for graph instantiation.

        Returns
        -------
        graph:
            Returns a new implementation of `AbstractGraph` using
            the `engine` defined in parameters.
        """
        for enum in GraphEngine:
            engine_name = enum.value
            engine_name_lowercase = engine_name.lower()
            if engine_name_lowercase == engine.lower():
                factory_module = importlib.import_module(
                    f"complex_epidemics.graph."
                    f"{engine_name_lowercase}_engine."
                    f"{engine_name_lowercase}_factory"
                )
                graph_class = getattr(factory_module, f"{engine_name}Factory")
                new_factory = graph_class()
                graph = new_factory.create_graph(graph_type=GraphType.GRAPH)
                return graph


if __name__ == "__main__":
    graphfactory = GraphFactory()
    spacegraph = graphfactory.new_space_graph()
    print(spacegraph.__class__)
    contactgraph = graphfactory.new_contact_graph()
    print(contactgraph.__class__)
