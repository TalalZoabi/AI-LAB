from abc import ABC, abstractmethod
import random

class ParentSelectionMethod(ABC):
    @abstractmethod
    def select(self, population, fitnesses, num_parents):
        """
        Abstract method to select parents from the population based on their fitness.
        
        :param population: The current population of individuals.
        :param fitnesses: A list of fitness values corresponding to the population.
        :param num_parents: The number of parents to select.
        :return: A list of selected parents.
        """
        pass





