import random
from .CrossoverOperator import CrossoverOperator

class SudokuRowColumnCrossover(CrossoverOperator):
    def crossover(self, parent1, parent2):
        grid1 = self.convert_to_grid(parent1)
        grid2 = self.convert_to_grid(parent2)
        offspring1 = [row[:] for row in grid1]
        offspring2 = [row[:] for row in grid2]

        if random.choice([True, False]):
            # Row crossover
            row_idx = random.randint(0, 8)
            for col in range(9):
                if not self.fixed_positions[row_idx][col]:
                    offspring1[row_idx][col] = grid2[row_idx][col]
                    offspring2[row_idx][col] = grid1[row_idx][col]
        else:
            # Column crossover
            col_idx = random.randint(0, 8)
            for row in range(9):
                if not self.fixed_positions[row][col_idx]:
                    offspring1[row][col_idx] = grid2[row][col_idx]
                    offspring2[row][col_idx] = grid1[row][col_idx]

        return [self.convert_to_list(offspring1), self.convert_to_list(offspring2)]

    def convert_to_grid(self, candidate):
        return [candidate[i*9:(i+1)*9] for i in range(9)]

    def convert_to_list(self, grid):
        return [cell for row in grid for cell in row]

