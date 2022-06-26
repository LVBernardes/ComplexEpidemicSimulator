# -*- coding: utf-8 -*-
"""Networkx engine graph module.
"""

import logging
from typing import Any

import networkx as nx

from complex_epidemics.graph.support_objects.abstract_graph import AbstractGraph
from complex_epidemics.utils.log_messages import LogMessage

LOG = logging.getLogger(__name__)


class NetworkxGraph(AbstractGraph):
    """Networkx standard graph."""

    def __init__(self):

        super().__init__()
        self._graph = nx.Graph()

    def add_graph_attributes(self, attrs: dict) -> None:
        try:
            for key, value in attrs.items():
                self._graph[key] = value
        except BaseException as err:
            LOG.exception(LogMessage.UNEXPECTEDEXCEPTION)

    def add_node(self, node_id: int | str, **node_attrs) -> None:
        try:
            self._graph.add_node(node_for_adding=node_id, **node_attrs)
        except BaseException as err:
            LOG.exception(LogMessage.UNEXPECTEDEXCEPTION)

    def get_node(self, node_id: int | str) -> Any:
        try:
            return self._graph.nodes[node_id]
        except BaseException as err:
            LOG.exception(LogMessage.UNEXPECTEDEXCEPTION)

    def remove_node(self, node_id: int | str):
        try:
            self._graph.remove_node(n=node_id)
        except BaseException as err:
            LOG.exception(LogMessage.UNEXPECTEDEXCEPTION)

    def add_node_attributes(self, node_id: int | str, node_attrs: dict) -> None:
        try:
            for key, value in node_attrs.items():
                self._graph.nodes[node_id][key] = value
        except BaseException as err:
            LOG.exception(LogMessage.UNEXPECTEDEXCEPTION)

    def get_node_attributes(self, node_id: int | str) -> dict:
        try:
            return self._graph.nodes[node_id]
        except BaseException as err:
            LOG.exception(LogMessage.UNEXPECTEDEXCEPTION)

    def has_node(self, node_id: int | str) -> bool:
        return self._graph.has_node(n=node_id)

    def get_nodes(
        self, attrs_data: str | bool = False
    ) -> list[tuple] | list[str | int]:
        try:
            return list(self._graph.nodes(data=attrs_data))
        except BaseException as err:
            LOG.exception(LogMessage.UNEXPECTEDEXCEPTION)

    def get_node_neighbours(self, node_id: int | str) -> list:
        try:
            return self._graph.neighbors(n=node_id)
        except BaseException as err:
            LOG.exception(LogMessage.UNEXPECTEDEXCEPTION)

    def add_edge(
        self, node_u_id: int | str, node_v_id: int | str, **edge_attrs
    ) -> None:
        try:
            self._graph.add_edge(u_of_edge=node_u_id, v_of_edge=node_v_id, **edge_attrs)
        except BaseException as err:
            LOG.exception(LogMessage.UNEXPECTEDEXCEPTION)

    def get_edges(self, node_id: int | str = None) -> list:
        try:
            return list(self._graph.edges(nbunch=node_id))
        except BaseException as err:
            LOG.exception(LogMessage.UNEXPECTEDEXCEPTION)

    def remove_edge(self, node_u_id: int | str, node_v_id: int | str) -> None:
        try:
            self._graph.remove_edge(u=node_u_id, v=node_v_id)
        except BaseException as err:
            LOG.exception(LogMessage.UNEXPECTEDEXCEPTION)

    def add_edge_attributes(
        self, node_u_id: int | str, node_v_id: int | str, edge_attrs: dict
    ) -> None:
        try:
            for key, value in edge_attrs.items():
                self._graph.edges[node_u_id, node_v_id][key] = value
        except BaseException as err:
            LOG.exception(LogMessage.UNEXPECTEDEXCEPTION)

    def get_edge_attributes(self, node_u_id: int | str, node_v_id: int | str) -> dict:
        try:
            return self._graph.edges[node_u_id, node_v_id]
        except BaseException as err:
            LOG.exception(LogMessage.UNEXPECTEDEXCEPTION)

    def has_edge(self, node_u_id: int | str, node_v_id: int | str) -> bool:
        return self._graph.has_edge(u=node_u_id, v=node_v_id)
