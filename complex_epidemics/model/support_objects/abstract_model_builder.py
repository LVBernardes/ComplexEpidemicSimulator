from abc import ABC, abstractmethod


class IModelBuilder(ABC):
    @abstractmethod
    def get_result(self):
        """Get built model."""

    @abstractmethod
    def reset(self):
        """Reset builder pipeline."""

    @abstractmethod
    def assemble_element(self, element):
        """Assembler"""
