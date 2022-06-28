# -*- coding: utf-8 -*-
"""Networkx engine bipartite graph module.
"""
import logging
from typing import Union

import networkx as nx

from complex_epidemics.graph.support_objects.abstract_bipartite_graph import (
    AbstractBipartiteGraph,
)
from complex_epidemics.graph.networkx_engine.networkx_graph import NetworkxGraph
from complex_epidemics.utils.log_messages import LogMessage

LOG = logging.getLogger(__name__)


class NetworkxBipartiteGraph(AbstractBipartiteGraph, NetworkxGraph):
    def __init__(self):
        super().__init__()

    def add_node_to_component_zero(self, node_id: Union[int, str]) -> bool:
        if not self.has_node(node_id):
            try:
                self.add_node(node_id, bipartite=0)
            except Exception as err:
                LOG.exception(
                    "Unable to add node with %s to graph component ZERO. \
                    Exception: %s",
                    node_id,
                    err.__class__,
                )
                raise
            else:
                LOG.debug("Node %s added to graph component ZERO.", node_id)
                return True
        else:
            LOG.debug("Node %s ALREADY exists in graph.", node_id)
            return False

    def get_nodes_from_component_zero(self) -> list:
        try:
            return [
                n
                for n, attr in self.get_nodes(attrs_data=True)
                if attr["bipartite"] == 0
            ]
        except Exception as err:
            LOG.exception(LogMessage.UNEXPECTEDEXCEPTION)

    def add_node_to_component_one(self, node_id: Union[int, str]) -> bool:
        if not self.has_node(node_id):
            try:
                self.add_node(node_id, bipartite=1)
            except Exception as err:
                LOG.exception(
                    "Unable to add node with %s to graph component ONE. \
                    Exception: %s",
                    node_id,
                    err.__class__,
                )
                raise
            else:
                LOG.debug("Node %s added to graph component ONE.", node_id)
                return True
        else:
            LOG.debug("Node %s ALREADY exists in graph.", node_id)
            return False

    def get_nodes_from_component_one(self) -> list:
        try:
            return [
                n
                for n, attr in self.get_nodes(attrs_data=True)
                if attr["bipartite"] == 1
            ]
        except Exception as err:
            LOG.exception(LogMessage.UNEXPECTEDEXCEPTION)

    def get_node_component(self, node_id: Union[int, str]):
        if self.has_node(node_id):
            try:
                component = nx.get_node_attributes(self._graph, "bipartite")
            except Exception as err:
                LOG.exception(
                    f"Unable to retrieve attribute 'bipartite' from graph. "
                    f"Exception: {err.__class__}"
                )
                raise
            else:
                try:
                    component[node_id]
                except KeyError:
                    LOG.debug("Agent %s has NO attribute 'bipartite'.", node_id)
                    return None
                else:
                    LOG.debug(
                        "Agent %s component attribute retrieved is: \
                        %s.",
                        node_id,
                        component[node_id],
                    )
                    return component[node_id]
        else:
            LOG.error("Agent %s does NOT exist in graph.", node_id)
            return None
