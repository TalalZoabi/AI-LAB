import random
from .GEP import GEP

class GEPFactory:

    def __init__(self, head_length: int):
        self.head_length = head_length

    @staticmethod
    def generate_random_chromosome(length: int) -> list[str]:
        return [random.choice(GEP.TERMINALS + GEP.FUNCTIONS) for _ in range(length)]

    @staticmethod
    def generate_random_tail(length: int) -> list[str]:
        return [random.choice(GEP.TERMINALS) for _ in range(length)]

    @staticmethod
    def generate_chromosome(head_length: int) -> list[str]:
        chromosome = []
        for _ in range(head_length):
            gene = random.choice(GEP.TERMINALS + GEP.FUNCTIONS)
            chromosome.append(gene)
        return chromosome
    
    @staticmethod
    def calc_needed_terminals(chromosome: list[str]) -> int:
        stack_size = 0
        missing = 0
        for gene in reversed(chromosome):
            if gene in GEP.TERMINALS:
                stack_size += 1
            else:
                stack_size -= 2
                if stack_size < 0:
                    missing += -stack_size
                    stack_size = 0
                stack_size += 1
        return missing
            
    @staticmethod
    def calc_size(chromosome: list[str]) -> int:
        size = 0
        for gene in reversed(chromosome):
            if gene in GEP.FUNCTIONS:
                size += 2
        return size

    @staticmethod
    def generate_tail(head: list[str]) -> list[str]:
        missing = GEPFactory.calc_needed_terminals(head)
        tail = GEPFactory.generate_random_tail(missing)
        return tail



    def generate_population(self, size: int) -> list[GEP]:
        return [GEP(GEPFactory.generate_chromosome(self.head_length)) for _ in range(size)]
