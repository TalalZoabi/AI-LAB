import random
import numpy as np

from .MutationOperator import MutationOperator

class DecayMutation(MutationOperator):
    def __init__(self, mutation_strength):
        self.mutation_strength = mutation_strength

    def mutate(self, individual, current_generation, max_generations, *args, **kwargs):
        adaptive_strength = self.mutation_strength * (1 - current_generation / max_generations)
        for i in range(len(individual)):
            if random.random() < adaptive_strength:
                mutation_value = np.random.normal(0, adaptive_strength)
                if random.random() < 0.5:
                    individual[i] += mutation_value
                else:
                    individual[i] -= mutation_value
        return individual


