# -*- coding: utf-8 -*-
"""Networkx engine graph factory module.
"""

import logging
from typing import Any

from complex_epidemics.graph.support_objects.abstract_graph_factory import AbstractGraphFactory
from complex_epidemics.graph.graph_type import GraphType
from complex_epidemics.graph.networkx_engine.networkx_bipartitegraph import (
    NetworkxBipartiteGraph,
)
from complex_epidemics.graph.networkx_engine.networkx_graph import NetworkxGraph
from complex_epidemics.utils.exceptions import InvalidTypeError

LOG = logging.getLogger(__name__)


class NetworkxFactory(AbstractGraphFactory):
    """Networkx graph factory.

    Implements new graphs based on requested type which can be:

    **BIPARTITEGRAPH:** NetworkxBipartiteGraph

    **GRAPH:** NetworksGraph
    """

    def __init__(self):
        pass

    @staticmethod
    def create_graph(graph_type: GraphType) -> Any:
        """Creates a new graph.

        Parameters
        ----------
        graph_type : `GraphType`

        Returns
        -------
        new_graph: `NetworkxGraph` | `NetworkxBipartiteGraph`

        """
        if type(graph_type) is not GraphType:
            LOG.error("Type informed is not of GraphType. Type: %s.", type(graph_type))
            raise InvalidTypeError(
                "Type informed is not of GraphType. Type: %s.", type(graph_type)
            )

        if graph_type.name is GraphType.BIPARTITEGRAPH.name:
            try:
                new_graph = NetworkxBipartiteGraph()
            except Exception as err:
                LOG.exception("Exception %s", err)
            else:
                LOG.debug("New Networkx %s created.", GraphType.BIPARTITEGRAPH)
                return new_graph
        elif graph_type.name is GraphType.GRAPH.name:
            try:
                new_graph = NetworkxGraph()
            except Exception as err:
                LOG.exception("Exception %s", err)
            else:
                LOG.debug("New Networkx %s created.", GraphType.GRAPH)
                return new_graph
        else:
            LOG.error("Graph type enumeration element %s not implement.", graph_type)
            raise ValueError(
                "Graph type enumeration element %s not implement.", graph_type
            )
