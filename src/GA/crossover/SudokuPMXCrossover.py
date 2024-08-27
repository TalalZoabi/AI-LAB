from .CrossoverOperator import CrossoverOperator




class SudokuPMXCrossover(CrossoverOperator):
    def __init__(self, fixed_positions):
        self.fixed_positions = fixed_positions

    def pmx_crossover(self, parent1_genome, parent2_genome):
        import random
        size = len(parent1_genome)
        child_genome = [None] * size
        start, end = sorted(random.sample(range(size), 2))

        for i in range(start, end):
            if not self.fixed_positions[i // 9][i % 9]:
                child_genome[i] = parent1_genome[i]

        for i in range(start, end):
            if not self.fixed_positions[i // 9][i % 9]:
                if parent2_genome[i] not in child_genome[start:end]:
                    pos = i
                    while start <= pos < end:
                        pos = parent1_genome.index(parent2_genome[pos])
                    child_genome[pos] = parent2_genome[i]

        for i in range(size):
            if child_genome[i] is None:
                child_genome[i] = parent2_genome[i]

        return child_genome
    
    def crossover(self, parent1, parent2):
        offspring1 = self.pmx_crossover(parent1, parent2)
        offspring2 = self.pmx_crossover(parent2, parent1)
        return [offspring1, offspring2]

    def convert_to_grid(self, candidate):
        return [candidate[i*9:(i+1)*9] for i in range(9)]

    def convert_to_list(self, grid):
        return [cell for row in grid for cell in row]



