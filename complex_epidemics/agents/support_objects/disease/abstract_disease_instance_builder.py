from abc import ABC, abstractmethod
from typing import Any


class IDiseaseInstanceBuilder(ABC):
    @abstractmethod
    def get_result(self):
        """Get built disease instance."""

    @abstractmethod
    def reset(self):
        """Reset builder pipeline."""

    @abstractmethod
    def build(self):
        """Execute production pipeline."""

    @abstractmethod
    def set_disease_instance_platform(self, disease: Any, host: Any):
        """Create new instance for Disease Instance class."""

    @abstractmethod
    def set_disease_recipe(self, recipe: Any):
        """Validate and store disease recipe.."""
