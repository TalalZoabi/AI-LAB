import random

from .MutationOperator import MutationOperator




class SudokuInversionMutation(MutationOperator):
    def __init__(self, fixed_positions):
        self.fixed_positions = fixed_positions

    def mutate(self, candidate):
        candidate = list(candidate)  # Convert to list for mutability
        grid = self.convert_to_grid(candidate)
        
        if random.choice([True, False]):
            # Row inversion
            row = random.randint(0, 8)
            if self.can_mutate_row(row):
                start, end = sorted(random.sample(range(9), 2))
                grid[row][start:end] = self.reverse_except_fixed(grid[row][start:end], self.fixed_positions[row][start:end])
        else:
            # Column inversion
            col = random.randint(0, 8)
            if self.can_mutate_column(col):
                col_values = [grid[row][col] for row in range(9)]
                start, end = sorted(random.sample(range(9), 2))
                col_values[start:end] = self.reverse_except_fixed(col_values[start:end], [self.fixed_positions[row][col] for row in range(9)][start:end])
                for row in range(9):
                    grid[row][col] = col_values[row]

        return self.convert_to_list(grid)

    def convert_to_grid(self, candidate):
        return [candidate[i*9:(i+1)*9] for i in range(9)]

    def convert_to_list(self, grid):
        return [cell for row in grid for cell in row]

    def can_mutate_row(self, row):
        return sum(self.fixed_positions[row]) < 8

    def can_mutate_column(self, col):
        return sum(self.fixed_positions[row][col] for row in range(9)) < 8

    def reverse_except_fixed(self, values, fixed):
        non_fixed_values = [v for v, f in zip(values, fixed) if not f]
        non_fixed_values.reverse()
        result = []
        non_fixed_idx = 0
        for f in fixed:
            if f:
                result.append(values[fixed.index(f)])
            else:
                result.append(non_fixed_values[non_fixed_idx])
                non_fixed_idx += 1
        return result
