# -*- coding: utf-8 -*-
"""Abstract graph factory module.
"""

from abc import ABC, abstractmethod


class AbstractGraphFactory(ABC):
    """Graph Factory abstract class.

    Interface for graph factory implementation.
    """

    @staticmethod
    @abstractmethod
    def create_graph(**kwargs):
        pass
