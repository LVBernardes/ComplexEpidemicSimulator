# -*- coding: utf-8 -*-
"""Graph type enumeration module.
"""

from enum import Enum


class GraphType(Enum):
    """Graph type enumeration.

    **GRAPH:** Non-directed graph.

    **BIPARTITEGRAPH:** Non-directed bipartite graph.
    """

    GRAPH = "Graph"
    BIPARTITEGRAPH = "BipartiteGraph"
