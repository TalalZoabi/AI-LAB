
from .FitnessFunction import FitnessFunction


class GPFitness(FitnessFunction):
    def __init__(self, lambda_penalty):
        self.lambda_penalty = lambda_penalty

    def fitness(self, individual):
        hits = 0

        for a in [True, False]:
            for b in [True, False]:
                if individual.evaluate(a, b) == (a ^ b):
                    hits += 1

        OPT_SIZE = 9 # Optimal tree size for this problem
        return hits + self.lambda_penalty * abs(OPT_SIZE - individual.size())

    def max_fitness(self):
        return 4
    
    def min_fitness(self):
        return 0
