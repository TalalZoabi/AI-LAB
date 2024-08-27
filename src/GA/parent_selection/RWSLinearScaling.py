import random
from .ParentSelectionMethod import ParentSelectionMethod


class RWSLinearScaling(ParentSelectionMethod):
    def __init__(self, scaling_strategy):
        self.scaling_strategy = scaling_strategy

    def select(self, population, fitnesses, num_parents):
        scaled_fitnesses = self.scaling_strategy.scale(fitnesses)
        total_fitness = sum(scaled_fitnesses)
        selection_probs = [f / total_fitness for f in scaled_fitnesses]
        
        selected_parents = random.choices(population, weights=selection_probs, k=num_parents)
        return selected_parents


