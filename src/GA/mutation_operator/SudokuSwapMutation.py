import random

from .MutationOperator import MutationOperator



class SudokuSwapMutation(MutationOperator):
    def __init__(self, fixed_positions):
        self.fixed_positions = fixed_positions

    def mutate(self, candidate):
        candidate = list(candidate)  # Convert to list for mutability
        grid = self.convert_to_grid(candidate)
        
        subgrid_idx = random.randint(0, 8)
        subgrid = self.get_subgrid(grid, subgrid_idx)
        fixed_subgrid_positions = self.get_fixed_subgrid_positions(subgrid_idx)
        
        if len(fixed_subgrid_positions) < 2:
            return candidate  # No mutation if less than two mutable positions
        
        while True:
            idx1, idx2 = random.sample(range(9), 2)
            if not fixed_subgrid_positions[idx1] and not fixed_subgrid_positions[idx2]:
                subgrid[idx1], subgrid[idx2] = subgrid[idx2], subgrid[idx1]
                break
        
        self.set_subgrid(grid, subgrid_idx, subgrid)
        return self.convert_to_list(grid)

    def convert_to_grid(self, candidate):
        return [candidate[i*9:(i+1)*9] for i in range(9)]

    def convert_to_list(self, grid):
        return [cell for row in grid for cell in row]

    def get_subgrid(self, grid, subgrid_idx):
        row_start = (subgrid_idx // 3) * 3
        col_start = (subgrid_idx % 3) * 3
        subgrid = []
        for i in range(3):
            subgrid.extend(grid[row_start + i][col_start:col_start + 3])
        return subgrid

    def set_subgrid(self, grid, subgrid_idx, subgrid):
        row_start = (subgrid_idx // 3) * 3
        col_start = (subgrid_idx % 3) * 3
        idx = 0
        for i in range(3):
            for j in range(3):
                grid[row_start + i][col_start + j] = subgrid[idx]
                idx += 1
    
    def get_fixed_subgrid_positions(self, subgrid_idx):
        row_start = (subgrid_idx // 3) * 3
        col_start = (subgrid_idx % 3) * 3
        fixed_subgrid_positions = []
        for i in range(3):
            for j in range(3):
                fixed_subgrid_positions.append(self.fixed_positions[row_start + i][col_start + j])
        return fixed_subgrid_positions
