import numpy as np
from .Problem import Problem

class Ackley(Problem):
    def __init__(self, dimension, a=20, b=0.2, c=2 * np.pi):
        self.dimension = dimension
        self.a = a
        self.b = b
        self.c = c

    def evaluate(self, individual):
        individual = np.array(individual)  # Convert the individual to a NumPy array
        part1 = -self.a * np.exp(-self.b * np.sqrt(np.sum(individual**2) / self.dimension))
        part2 = -np.exp(np.sum(np.cos(self.c * individual)) / self.dimension)
        return part1 + part2 + self.a + np.exp(1)

    def generate_initial_solution(self, method='random'):
        if method == 'random':
            return self.generate_random_solution()
        else:
            raise ValueError(f"Unsupported method: {method}")

    def generate_random_solution(self):
        return np.random.uniform(-32.768, 32.768, size=(self.dimension,))

    def display_individual(self, individual):
        # For simplicity, we will just print the individual and its fitness
        fitness = self.evaluate(individual)
        print(f"Individual: {individual}, Fitness: {fitness}")

    def evaluate_fitness(self, individual):
        """
        Evaluates the fitness of an individual solution.
        :param individual: A list of floats representing the solution.
        :return: The fitness score of the individual.
        """
        return 1 / (self.evaluate(individual) + 1)  # +1 to avoid division by zero