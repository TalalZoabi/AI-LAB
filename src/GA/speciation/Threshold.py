
from .Speciation import Speciation

class Threshold(Speciation):
    def __init__(self, similarity_threshold, distance_func):
        super().__init__(distance_func)
        self.similarity_threshold = similarity_threshold

    def apply_speciation(self, population):
        species = []
        for i, ind_i in enumerate(population):
            placed = False
            for spec in species:
                if self.distance_func(ind_i, population[spec[0]]) < self.similarity_threshold:
                    spec.append(i)
                    placed = True
                    break
            if not placed:
                species.append([i])
        return species
