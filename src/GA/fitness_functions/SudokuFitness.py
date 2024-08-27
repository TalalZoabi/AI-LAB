from .FitnessFunction import FitnessFunction


class SudokuFitness(FitnessFunction):
    def __init__(self):
        pass

    def evaluate(self, individual):
        grid = self.convert_to_grid(individual)
        row_conflicts = self.count_row_conflicts(grid)
        column_conflicts = self.count_column_conflicts(grid)
        subgrid_conflicts = self.count_subgrid_conflicts(grid)
        
        total_conflicts = row_conflicts + column_conflicts + subgrid_conflicts
        max_conflicts = 3 * 9 * (9 - 1)  # Maximum possible conflicts
        
        fitness = max_conflicts - total_conflicts
        return fitness

    def convert_to_grid(self, individual):
        return [individual[i*9:(i+1)*9] for i in range(9)]

    def count_row_conflicts(self, grid):
        conflicts = 0
        for row in grid:
            conflicts += len(row) - len(set(row))
        return conflicts

    def count_column_conflicts(self, grid):
        conflicts = 0
        for col in range(9):
            column = [grid[row][col] for row in range(9)]
            conflicts += len(column) - len(set(column))
        return conflicts

    def count_subgrid_conflicts(self, grid):
        conflicts = 0
        for row in range(0, 9, 3):
            for col in range(0, 9, 3):
                subgrid = [grid[r][c] for r in range(row, row + 3) for c in range(col, col + 3)]
                conflicts += len(subgrid) - len(set(subgrid))
        return conflicts
    
    def max_fitness(self, *args, **kwargs):
        return 3 * 9 * (9 - 1)
    
    def min_fitness(self, *args, **kwargs):
        return 0

