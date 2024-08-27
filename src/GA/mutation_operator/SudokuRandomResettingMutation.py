import random

from .MutationOperator import MutationOperator



class SudokuRandomResettingMutation(MutationOperator):
    def __init__(self, fixed_positions):
        self.fixed_positions = fixed_positions

    def mutate(self, candidate):
        candidate = list(candidate)  # Convert to list for mutability
        grid = self.convert_to_grid(candidate)
        
        while True:
            row, col = random.randint(0, 8), random.randint(0, 8)
            if not self.fixed_positions[row][col]:
                grid[row][col] = random.randint(1, 9)
                break

        return self.convert_to_list(grid)

    def convert_to_grid(self, candidate):
        return [candidate[i*9:(i+1)*9] for i in range(9)]

    def convert_to_list(self, grid):
        return [cell for row in grid for cell in row]

