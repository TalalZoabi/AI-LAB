import random

from .FitnessFunction import FitnessFunction


class GPAFitness(FitnessFunction):
    def __init__(self, lambda_penalty: float, opt_size: int, target_function: callable, error_range: float, sample_size: int):
        self.lambda_penalty = lambda_penalty
        self.opt_size = opt_size
        self.target_function = target_function
        self.error_range = error_range
        self.sample_size = sample_size

    def evaluate(self, individual) -> float:
        hits = 0
        parity = 0

        for _ in range(self.sample_size):
            x = random.uniform(-1, 1)
            val = individual.evaluate(x)     
            diff = abs(val - self.target_function(x))  
            parity += diff
            if val < self.error_range:
                hits += 1



        if self.opt_size is None:
            return hits - self.lambda_penalty * individual.size() - parity
        else: 
            return hits - self.lambda_penalty * (individual.size() - self.opt_size) - parity

    def max_fitness(self):
        return self.sample_size
    
    def min_fitness(self):
        return -self.sample_size
