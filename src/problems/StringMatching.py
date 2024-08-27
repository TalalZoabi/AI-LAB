import random
import numpy as np
import matplotlib.pyplot as plt

from .Problem import Problem

class StringMatching(Problem):
    def __init__(self, target_string):
        self.target_string = target_string

    def initialize_population(self, population_size):
        population = []
        for _ in range(population_size):
            individual = ''.join(random.choices(self.target_string, k=len(self.target_string)))
            population.append(individual)
        return population
    
    def distance(self, individual1, individual2):
        return sum(c1 != c2 for c1, c2 in zip(individual1, individual2))
    
    def distance_unit(self):
        return "mismatches"
    
    def display_individual(self, individual, title):
        fig, ax = plt.subplots()
        for i, char in enumerate(individual):
            color = 'green' if char == self.target_string[i] else 'red'
            ax.text(i + 0.5, 0.5, char, ha='center', va='center', color=color, fontsize=12, bbox=dict(facecolor='white', edgecolor='none', boxstyle='round,pad=0.5'))

        ax.set_xlim(0, len(individual))
        ax.set_ylim(0, 1)
        ax.set_xticks(np.arange(0.5, len(individual), step=1))
        ax.set_yticks([])
        ax.set_xticklabels(range(len(individual)))
        ax.grid(True)
        plt.title(title)
        plt.show()

