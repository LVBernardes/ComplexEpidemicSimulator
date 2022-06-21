from abc import ABC, abstractmethod


class IModelStepper(ABC):
    @abstractmethod
    def step(self):
        pass


class IModelAdvancer(ABC):
    @abstractmethod
    def advance(self):
        pass
