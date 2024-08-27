import random
from .CrossoverOperator import CrossoverOperator



class UniformCrossover(CrossoverOperator):
    def crossover(self, parent1, parent2):
        offspring1 = []
        offspring2 = []

        assert len(parent1) == len(parent2), "Parents must have the same length"

        for i in range(len(parent1)):
            if random.random() > 0.5:
                offspring1.append(parent1[i])
                offspring2.append(parent2[i])
            else:
                offspring1.append(parent2[i])
                offspring2.append(parent1[i])
        return [''.join(offspring1), ''.join(offspring2)]





