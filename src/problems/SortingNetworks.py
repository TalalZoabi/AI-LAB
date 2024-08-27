import random
import numpy as np
import matplotlib.pyplot as plt

from .Problem import Problem

class SortingNetworks(Problem):
    def __init__(self, max_index, min_comparisons, max_comparisons, lower_bound, upper_bound):
        self.max_index = max_index
        self.min_comparisons = min_comparisons
        self.max_comparisons = max_comparisons

        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

    def create_individual(self):
        # Randomly determine the number of comparisons for this network
        num_comparisons = random.randint(self.min_comparisons, self.max_comparisons)

        # Generate a list of random comparisons (pairs of indices)
        comparisons = [random.sample(range(self.max_index), 2) for _ in range(num_comparisons)]
        return comparisons

    
    def create_adversarial_individual(self):
        return [random.randint(self.lower_bound, self.upper_bound) for _ in range(self.max_index)]

    