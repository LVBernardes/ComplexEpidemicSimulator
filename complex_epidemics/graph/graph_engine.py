# -*- coding: utf-8 -*-
"""Graph engine enumeration module.
"""

from enum import Enum


class GraphEngine(Enum):
    """Graph engine enumeration.

    **NETWORKX:** `Networkx`_ graph engine backend.

    .. _Networkx:
        https://networkx.org/
    """

    NETWORKX = "Networkx"
