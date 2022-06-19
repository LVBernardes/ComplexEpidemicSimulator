from abc import ABC, abstractmethod


class IModelStepper(ABC):
    @abstractmethod
    def step(self):
        pass
