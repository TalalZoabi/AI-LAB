import random
from .ParentSelectionMethod import ParentSelectionMethod


class SUSLinearScaling(ParentSelectionMethod):
    def __init__(self, scaling_strategy):
        self.scaling_strategy = scaling_strategy

    def select(self, population, fitnesses, num_parents):
        scaled_fitnesses = self.scaling_strategy.scale(fitnesses)
        total_fitness = sum(scaled_fitnesses)
        selection_probs = [f / total_fitness for f in scaled_fitnesses]
        
        pointers = [(i + random.random()) / num_parents for i in range(num_parents)]
        selected_parents = []
        cumulative_sum = 0
        j = 0
        for i, individual in enumerate(population):
            cumulative_sum += selection_probs[i]
            while j < num_parents and cumulative_sum > pointers[j]:
                selected_parents.append(individual)
                j += 1
        return selected_parents

