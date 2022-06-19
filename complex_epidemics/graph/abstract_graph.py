# -*- coding: utf-8 -*-
"""Abstract graph module.
"""

from abc import ABC, abstractmethod


class AbstractGraph(ABC):
    """Standard graph abstract class.

    Used to uncouple graph engines from its use during modeling.
    """

    @abstractmethod
    def add_graph_attributes(self, *args, **kwargs):
        pass

    @abstractmethod
    def add_node(self, *args, **kwargs):
        pass

    @abstractmethod
    def get_node(self, *args, **kwargs):
        pass

    @abstractmethod
    def remove_node(self, *args, **kwargs):
        pass

    @abstractmethod
    def add_node_attributes(self, *args, **kwargs):
        pass

    @abstractmethod
    def get_node_attributes(self, *args, **kwargs):
        pass

    @abstractmethod
    def has_node(self, *args, **kwargs):
        pass

    @abstractmethod
    def get_nodes(self, *args, **kwargs):
        pass

    @abstractmethod
    def get_node_neighbours(self, *args, **kwargs):
        pass

    @abstractmethod
    def add_edge(self, *args, **kwargs):
        pass

    @abstractmethod
    def get_edges(self, *args, **kwargs):
        pass

    @abstractmethod
    def remove_edge(self, *args, **kwargs):
        pass

    @abstractmethod
    def add_edge_attributes(self, *args, **kwargs):
        pass

    @abstractmethod
    def get_edge_attributes(self, *args, **kwargs):
        pass

    @abstractmethod
    def has_edge(self, *args, **kwargs):
        pass
