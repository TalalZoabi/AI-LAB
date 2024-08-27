from .CrossoverOperator import CrossoverOperator


class SudokuCXCrossover(CrossoverOperator):
    def __init__(self, fixed_positions):
        self.fixed_positions = fixed_positions

    def cycle_crossover(self, parent1_genome, parent2_genome):
        size = len(parent1_genome)
        child_genome = [None] * size
        cycles = [0] * size
        cycle_num = 1
        
        # Loop through each gene to identify cycles
        for i in range(size):
            if cycles[i] == 0:
                start = i
                while cycles[start] == 0:
                    cycles[start] = cycle_num
                    start = parent1_genome.index(parent2_genome[start])
                cycle_num += 1
        
        # Fill the child genome using the identified cycles
        for i in range(size):
            if cycles[i] % 2 == 1:
                child_genome[i] = parent1_genome[i]
            else:
                child_genome[i] = parent2_genome[i]
        
        return child_genome
    
    
    def crossover(self, parent1, parent2):
        offspring1 = self.cycle_crossover(parent1, parent2)
        offspring2 = self.cycle_crossover(parent2, parent1)
        return [offspring1, offspring2]

    def convert_to_grid(self, candidate):
        return [candidate[i*9:(i+1)*9] for i in range(9)]

    def convert_to_list(self, grid):
        return [cell for row in grid for cell in row]

