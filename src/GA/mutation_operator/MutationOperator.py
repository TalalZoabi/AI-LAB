from abc import ABC, abstractmethod
import string
import random

class MutationOperator(ABC):
    @abstractmethod
    def mutate(self, candidate, *args, **kwargs):
        """
        Abstract method to mutate a given candidate.
        :param candidate: An individual solution to be mutated.
        :return: A mutated individual solution.
        """
        pass



