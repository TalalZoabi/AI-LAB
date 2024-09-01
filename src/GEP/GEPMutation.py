import random
from .GEP import GEP

class GEPMutation:
    def __init__(self, mutation_rate: float):
        self.mutation_rate = mutation_rate

    def mutate(self, chromosome: GEP, *args, **kwargs) -> GEP:
        new_chromosome = []
        for gene in chromosome.exp:
            if random.random() < self.mutation_rate:
                new_gene = random.choice(GEP.TERMINALS + GEP.FUNCTIONS)
                new_chromosome.append(new_gene)
            else:
                new_chromosome.append(gene)
        return GEP(new_chromosome)