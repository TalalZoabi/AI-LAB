from abc import ABC, abstractmethod
import random

class CrossoverOperator(ABC):
    @abstractmethod
    def crossover(self, parent1, parent2):
        """
        Abstract method to crossover two parents to produce offspring.
        :param parent1: The first parent individual.
        :param parent2: The second parent individual.
        :return: A list of offspring individuals.
        """
        pass