

from .GEP import GEP
from .GEPFactory import GEPFactory

class GEPFitness:
    def __init__(self, target_data: list, tail_attempts: int, size_factor: float):
        self.target_data = target_data
        self.tail_attempts = tail_attempts
        self.size_factor = size_factor

    def fitness(self, chromosome: list[str]) -> float:
        error = 0.0
        for x, y in self.target_data:
            y_pred = GEP.evaluate_exp(chromosome, x)
            error += abs(y - y_pred)
        size = GEPFactory.calc_size(chromosome)
        return -error - self.size_factor * size


    def evaluate(self, head: GEP) -> float:
        max_fitness = None
        best_tail = None
        for _ in range(self.tail_attempts):
            tail = GEPFactory.generate_tail(head.exp)
            full_chromosome = head.exp + tail
            ind_fitness = self.fitness(full_chromosome)
            if max_fitness is None or ind_fitness > max_fitness:
                max_fitness = ind_fitness
                best_tail = tail
        
        head.best_fitness = max_fitness
        head.best_tail = best_tail
        return max_fitness
