from abc import ABC, abstractmethod
import random

class SurvivorSelectionMethod(ABC):
    @abstractmethod
    def select(self, population, fitnesses, num_survivors):
        """
        Abstract method to select survivors from the population based on their fitness.
        
        :param population: The current population of individuals.
        :param fitnesses: A list of fitness values corresponding to the population.
        :param num_survivors: The number of survivors to select.
        :return: A list of selected survivors.
        """
        pass



