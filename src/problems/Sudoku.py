import random
import numpy as np
import matplotlib.pyplot as plt

from .Problem import Problem


class Sudoku(Problem):
    def __init__(self, initial_board):
        self.initial_board = initial_board
        self.fixed_positions = self.create_fixed_positions(initial_board)

    def create_fixed_positions(self, board):
        fixed_positions = [[bool(cell) for cell in row] for row in board]
        return fixed_positions



    def initialize_population(self, population_size):
        population = []
        for _ in range(population_size):
            individual = [self.initial_board[row][col] if self.fixed_positions[row][col] else random.randint(1, 9)
                          for row in range(9) for col in range(9)]
            population.append(individual)
        return population
    
    def distance(self, individual1, individual2):
        return sum(c1 != c2 for c1, c2 in zip(individual1, individual2))
    
    def distance_unit(self):
        return "mismatches"
    

    def convert_to_grid(self, individual):
        return [individual[i*9:(i+1)*9] for i in range(9)]


    def display_individual(self, individual):
        grid = self.convert_to_grid(individual)
        conflicts_grid = np.zeros((9, 9), dtype=int)

        # Mark conflicts in rows, columns, and subgrids
        for i in range(9):
            for j in range(9):
                if grid[i][j] in grid[i][:j] + grid[i][j+1:] or grid[i][j] in [grid[x][j] for x in range(9) if x != i]:
                    conflicts_grid[i][j] = 1

        for row in range(0, 9, 3):
            for col in range(0, 9, 3):
                subgrid = [grid[r][c] for r in range(row, row + 3) for c in range(col, col + 3)]
                for i in range(3):
                    for j in range(3):
                        if subgrid[i*3+j] in subgrid[:i*3+j] + subgrid[i*3+j+1:]:
                            conflicts_grid[row+i][col+j] = 1

        fig, ax = plt.subplots()
        for i in range(9):
            for j in range(9):
                color = 'grey' if self.fixed_positions[i][j] else 'red' if conflicts_grid[i][j] else 'black'
                ax.text(j + 0.5, 8.5 - i, grid[i][j], ha='center', va='center', color=color, fontsize=12, bbox=dict(facecolor='white', edgecolor='none', boxstyle='round,pad=0.5'))

        ax.set_xlim(0, 9)
        ax.set_ylim(0, 9)
        ax.set_xticks(np.arange(0.5, 9.5, step=1))
        ax.set_yticks(np.arange(0.5, 9.5, step=1))
        ax.set_xticklabels(range(1, 10))
        ax.set_yticklabels(range(9, 0, -1))
        ax.grid(True)
        plt.title("Sudoku Display")
        plt.show()