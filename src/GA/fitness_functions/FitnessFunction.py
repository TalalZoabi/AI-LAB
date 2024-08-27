from abc import ABC, abstractmethod

class FitnessFunction(ABC):
    @abstractmethod
    def evaluate(self, individual):
        """
        Abstract method to evaluate the fitness of an individual.
        
        :param individual: The individual solution to evaluate.
        :return: The fitness score of the individual.
        """
        pass
    
    @abstractmethod
    def max_fitness(self, *args, **kwargs):
        """
        Abstract method to return the maximum possible fitness score.
        
        :return: The maximum possible fitness score.
        """
        pass

    @abstractmethod
    def min_fitness(self, *args, **kwargs):
        """
        Abstract method to return the minimum possible fitness score.
        
        :return: The minimum possible fitness score.
        """
        pass



