
from .FitnessFunction import FitnessFunction


class GPFitness(FitnessFunction):
    def __init__(self, lambda_penalty, opt_size, target_function):
        self.lambda_penalty = lambda_penalty
        self.opt_size = opt_size
        self.target_function = target_function

    def fitness(self, individual) -> float:
        hits = 0
        for a in [True, False]:
            for b in [True, False]:
                if individual.evaluate(a, b) == self.target_function(a, b):
                    hits += 1

        return hits + self.lambda_penalty * abs(self.opt_size - individual.size())

    def max_fitness(self):
        return 4
    
    def min_fitness(self):
        return 0
