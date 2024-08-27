from .CrossoverOperator import CrossoverOperator

class SinglePointCrossover(CrossoverOperator):
    def crossover(self, parent1, parent2):
        import random

        if len(parent1) < 2 or len(parent2) < 2:
            offspring1 = parent1 + parent2
            offspring2 = parent2 + parent1
            return [offspring1, offspring2]
        
        # Ensure the crossover point is within bounds
        point = random.randint(1, min(len(parent1), len(parent2)) - 1)
        
        # Generate offspring by combining parents at the crossover point
        offspring1 = parent1[:point] + parent2[point:]
        offspring2 = parent2[:point] + parent1[point:]
        
        return [offspring1, offspring2]
