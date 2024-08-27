import random
from .CrossoverOperator import CrossoverOperator

class ArithmeticCrossover(CrossoverOperator):
    def __init__(self, alpha=0.5):
        """
        Initialize the ArithmeticCrossover with a given alpha.
        
        :param alpha: The weight for combining the parents' genes. Default is 0.5.
        """
        self.alpha = alpha

    def crossover(self, parent1, parent2):
        """
        Perform arithmetic crossover between two parents.
        
        :param parent1: The first parent individual.
        :param parent2: The second parent individual.
        :return: Two offspring resulting from the crossover.
        """
        # Ensure both parents are of the same length
        assert len(parent1) == len(parent2), "Parents must have the same length"

        child1 = [(self.alpha * p1 + (1 - self.alpha) * p2) for p1, p2 in zip(parent1, parent2)]
        child2 = [(self.alpha * p2 + (1 - self.alpha) * p1) for p1, p2 in zip(parent1, parent2)]
        
        return [child1, child2]
