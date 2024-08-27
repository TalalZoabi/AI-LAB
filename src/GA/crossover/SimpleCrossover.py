import random
import numpy as np

class SimpleCrossover:
    def __init__(self, alpha=0.5):
        self.alpha = alpha

    def crossover(self, parent1, parent2):
        child1 = [i for i in parent1]
        child2 = [i for i in parent2]
        for i in range(len(parent1)):
            gamma = (1 + 2 * self.alpha) * random.random() - self.alpha
            child1[i] = (1 - gamma) * parent1[i] + gamma * parent2[i]
            child2[i] = gamma * parent1[i] + (1 - gamma) * parent2[i]
        return [child1, child2]
    
    