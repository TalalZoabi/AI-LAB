import random
import numpy as np

class SimpleMutation:
    def __init__(self, mutation_strength=0.1):
        self.mutation_strength = mutation_strength

    def mutate(self, individual, *args, **kwargs):
        for i in range(len(individual)):
            if random.random() < self.mutation_strength:  # Mutation probability
                mutation_value = np.random.normal(0, self.mutation_strength)
                if random.random() < 0.5:
                    individual[i] += mutation_value
                else:
                    individual[i] -= mutation_value
        return individual
