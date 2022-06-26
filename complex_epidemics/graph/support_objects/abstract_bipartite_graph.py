# -*- coding: utf-8 -*-
"""Abstract bipartite graph module.
"""

from abc import ABC, abstractmethod


class AbstractBipartiteGraph(ABC):
    """Bipartite graph abstract class.

    Used to uncouple graph engines from its use during modeling.
    """

    @abstractmethod
    def add_node_to_component_zero(self, *args, **kwargs):
        pass

    @abstractmethod
    def get_nodes_from_component_zero(self, *args, **kwargs):
        pass

    @abstractmethod
    def add_node_to_component_one(self, *args, **kwargs):
        pass

    @abstractmethod
    def get_nodes_from_component_one(self, *args, **kwargs):
        pass

    @abstractmethod
    def get_node_component(self, *args, **kwargs):
        pass
