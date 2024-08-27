import random
import logging

from .CrossoverOperator import CrossoverOperator


class SortingNetworksCrossover(CrossoverOperator):
    def __init__(self):
        pass

    
    def crossover(self, parent1, parent2):
        # Allow for variable length crossover
        min_len = min(len(parent1), len(parent2))
        max_len = max(len(parent1), len(parent2))
        
        if min_len == 0:
            # If one parent has no comparisons, return the other parent
            return parent1, parent2

        crossover_type = random.choice(['single_point', 'uniform'])
        logging.debug(f"Applying {crossover_type} crossover")

        if crossover_type == 'single_point':
            point = random.randint(0, min_len - 1)
            child1 = parent1[:point] + parent2[point:]
            child2 = parent2[:point] + parent1[point:]
        
        elif crossover_type == 'uniform':
            child1 = [(random.choice([p1, p2])) for p1, p2 in zip(parent1, parent2)]
            child2 = [(random.choice([p1, p2])) for p1, p2 in zip(parent1, parent2)]
        
        # Adjust size randomly to explore different configurations
        if random.random() < 0.5:
            child1.extend(parent2[min_len:max_len])
        if random.random() < 0.5:
            child2.extend(parent1[min_len:max_len])

        

        # Return new sorting networks
        return child1, child2




