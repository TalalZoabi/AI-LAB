import random

from .MutationOperator import MutationOperator


class SudokuRowColumnSwapMutation(MutationOperator):
    def __init__(self, fixed_positions):
        self.fixed_positions = fixed_positions

    def mutate(self, candidate):
        candidate = list(candidate)  # Convert to list for mutability
        grid = self.convert_to_grid(candidate)
        
        if random.choice([True, False]):
            # Row swap within a band
            band = random.randint(0, 2) * 3
            row1, row2 = random.sample(range(band, band + 3), 2)
            if not self.is_row_fixed(row1) and not self.is_row_fixed(row2):
                grid[row1], grid[row2] = grid[row2], grid[row1]
        else:
            # Column swap within a stack
            stack = random.randint(0, 2) * 3
            col1, col2 = random.sample(range(stack, stack + 3), 2)
            if not self.is_column_fixed(col1) and not self.is_column_fixed(col2):
                for row in grid:
                    row[col1], row[col2] = row[col2], row[col1]
        
        return self.convert_to_list(grid)

    def convert_to_grid(self, candidate):
        return [candidate[i*9:(i+1)*9] for i in range(9)]

    def convert_to_list(self, grid):
        return [cell for row in grid for cell in row]

    def is_row_fixed(self, row):
        return any(self.fixed_positions[row])

    def is_column_fixed(self, col):
        return any(self.fixed_positions[row][col] for row in range(9))

