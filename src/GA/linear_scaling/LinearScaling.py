from abc import ABC, abstractmethod

class LinearScaling(ABC):
    @abstractmethod
    def scale(self, fitnesses):
        pass


