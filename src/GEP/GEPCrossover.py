import random
from .GEP import GEP

class GEPCrossover:
    def crossover(self, parent1: GEP, parent2: GEP):
        # Ensure both parents are of the same length
        assert len(parent1) == len(parent2), "Parents must have the same length"
        
        # Randomly select a crossover point
        crossover_point = random.randint(1, len(parent1) - 1)
        


        # Perform crossover
        child1 = parent1.exp[:crossover_point] + parent2.exp[crossover_point:]
        child2 = parent2.exp[:crossover_point] + parent1.exp[crossover_point:]

        child1 = GEP(child1)
        child2 = GEP(child2)

        return [child1, child2]


