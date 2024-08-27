import random
from .CrossoverOperator import CrossoverOperator

class TwoPointCrossover(CrossoverOperator):
    def crossover(self, parent1, parent2):
        # Ensure parents have enough length for crossover
        if len(parent1) < 3 or len(parent2) < 3:
            return [parent1, parent2]  # No crossover possible, return original parents
        
        # Select two crossover points
        point1, point2 = sorted(random.sample(range(1, min(len(parent1), len(parent2))), 2))
        
        # Create offspring by swapping segments between the two crossover points
        offspring1 = parent1[:point1] + parent2[point1:point2] + parent1[point2:]
        offspring2 = parent2[:point1] + parent1[point1:point2] + parent2[point2:]
        
        return [offspring1, offspring2]
