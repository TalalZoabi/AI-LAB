import random

from .MutationOperator import MutationOperator





class SudokuDisplacementMutation(MutationOperator):
    def __init__(self, fixed_positions):
        self.fixed_positions = fixed_positions

    def mutate(self, candidate):
        candidate = list(candidate)  # Convert to list for mutability
        grid = self.convert_to_grid(candidate)

        if random.choice([True, False]):
            # Row displacement
            row = random.randint(0, 8)
            if self.can_mutate_row(row):
                start, end = sorted(random.sample(range(9), 2))
                segment = grid[row][start:end]
                grid[row][start:end] = [0] * (end - start)
                new_pos = random.randint(0, 9 - len(segment))
                grid[row][new_pos:new_pos] = segment
        else:
            # Column displacement
            col = random.randint(0, 8)
            if self.can_mutate_column(col):
                start, end = sorted(random.sample(range(9), 2))
                segment = [grid[row][col] for row in range(start, end)]
                for row in range(start, end):
                    grid[row][col] = 0
                new_pos = random.randint(0, 9 - len(segment))
                for i in range(len(segment)):
                    grid[new_pos + i][col] = segment[i]

        return self.convert_to_list(grid)

    def convert_to_grid(self, candidate):
        return [candidate[i*9:(i+1)*9] for i in range(9)]

    def convert_to_list(self, grid):
        return [cell for row in grid for cell in row]

    def can_mutate_row(self, row):
        return sum(self.fixed_positions[row]) < 8

    def can_mutate_column(self, col):
        return sum(self.fixed_positions[row][col] for row in range(9)) < 8

