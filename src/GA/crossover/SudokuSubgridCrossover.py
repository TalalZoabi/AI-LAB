import random
from .CrossoverOperator import CrossoverOperator

class SudokuSubgridCrossover(CrossoverOperator):
    def __init__(self, fixed_positions):
        self.fixed_positions = fixed_positions

    def crossover(self, parent1, parent2):
        grid1 = self.convert_to_grid(parent1)
        grid2 = self.convert_to_grid(parent2)
        offspring1 = [row[:] for row in grid1]
        offspring2 = [row[:] for row in grid2]

        subgrid_idx = random.randint(0, 8)
        row_start = (subgrid_idx // 3) * 3
        col_start = (subgrid_idx % 3) * 3

        for i in range(3):
            for j in range(3):
                if not self.fixed_positions[row_start + i][col_start + j]:
                    offspring1[row_start + i][col_start + j] = grid2[row_start + i][col_start + j]
                    offspring2[row_start + i][col_start + j] = grid1[row_start + i][col_start + j]

        return [self.convert_to_list(offspring1), self.convert_to_list(offspring2)]

    def convert_to_grid(self, candidate):
        return [candidate[i*9:(i+1)*9] for i in range(9)]

    def convert_to_list(self, grid):
        return [cell for row in grid for cell in row]



