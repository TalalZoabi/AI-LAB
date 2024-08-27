import random
import math
from src.problems.CVRP import CVRP
from src.problems.Ackley import Ackley

class SA:
    def __init__(self, problem, initial_temperature, cooling_rate, num_iterations, perturbation_method='swap', acceptance_method='default', initial_solution_method='greedy'):
        self.problem = problem
        self.initial_temperature = initial_temperature
        self.cooling_rate = cooling_rate
        self.num_iterations = num_iterations
        self.perturbation_method = self.get_method(perturbation_method, self.perturbation_methods())
        self.acceptance_method = self.get_method(acceptance_method, self.acceptance_methods())
        self.initial_solution_method = initial_solution_method

    def get_method(self, method_name, methods_dict):
        if method_name in methods_dict:
            return methods_dict[method_name]
        else:
            raise ValueError(f"Unsupported method: {method_name}")

    def perturbation_methods(self):
        return {
            'swap': self.perturb_swap,
            'insertion': self.perturb_insertion,
            'reverse': self.perturb_reverse,
            'scramble': self.perturb_scramble,
            'two_opt': self.perturb_two_opt
        }

    def acceptance_methods(self):
        return {
            'default': self.acceptance_probability_default,
            'threshold': self.acceptance_probability_threshold,
            'boltzmann': self.acceptance_probability_boltzmann,
            'metropolis': self.acceptance_probability_metropolis
        }

    def solve(self):
        current_solution = self.problem.generate_initial_solution(self.initial_solution_method)
        current_fitness = self.problem.evaluate_fitness(current_solution)
        best_solution = current_solution
        best_fitness = current_fitness
        temperature = self.initial_temperature

        for iteration in range(self.num_iterations):
            new_solution = self.perturbation_method(current_solution)
            new_fitness = self.problem.evaluate_fitness(new_solution)
            if self.acceptance_method(current_fitness, new_fitness, temperature) > random.random():
                current_solution = new_solution
                current_fitness = new_fitness
                if new_fitness > best_fitness:
                    best_solution = new_solution
                    best_fitness = new_fitness
            temperature *= self.cooling_rate

        return best_solution, best_fitness

    def perturb_swap(self, solution):
        idx1, idx2 = random.sample(range(1, len(solution) - 1), 2)
        if isinstance(self.problem, CVRP) and (solution[idx1] == 0 or solution[idx2] == 0):
            return solution  # Skip if depot is involved
        solution[idx1], solution[idx2] = solution[idx2], solution[idx1]
        return solution

    def perturb_insertion(self, solution):
        idx1, idx2 = random.sample(range(1, len(solution) - 1), 2)
        if isinstance(self.problem, CVRP) and (solution[idx1] == 0 or solution[idx2] == 0):
            return solution  # Skip if depot is involved
        customer = solution.pop(idx1)
        solution.insert(idx2, customer)
        return solution

    def perturb_reverse(self, solution):
        idx1, idx2 = sorted(random.sample(range(1, len(solution) - 1), 2))
        if isinstance(self.problem, CVRP) and 0 in solution[idx1:idx2]:
            return solution  # Skip if depot is involved
        solution[idx1:idx2] = reversed(solution[idx1:idx2])
        return solution

    def perturb_scramble(self, solution):
        idx1, idx2 = sorted(random.sample(range(1, len(solution) - 1), 2))
        if isinstance(self.problem, CVRP) and 0 in solution[idx1:idx2]:
            return solution  # Skip if depot is involved
        subset = solution[idx1:idx2]
        random.shuffle(subset)
        solution[idx1:idx2] = subset
        return solution

    def perturb_two_opt(self, solution):
        idx1, idx2 = sorted(random.sample(range(1, len(solution) - 1), 2))
        if isinstance(self.problem, CVRP) and 0 in solution[idx1:idx2]:
            return solution  # Skip if depot is involved
        solution[idx1:idx2] = solution[idx1:idx2][::-1]
        return solution

    def acceptance_probability_default(self, current_fitness, new_fitness, temperature):
        if new_fitness > current_fitness:
            return 1.0
        else:
            return math.exp((new_fitness - current_fitness) / temperature)

    def acceptance_probability_threshold(self, current_fitness, new_fitness, temperature, threshold=0.1):
        if new_fitness > current_fitness:
            return 1.0
        elif new_fitness > current_fitness * (1 - threshold):
            return 0.5
        else:
            return math.exp((new_fitness - current_fitness) / temperature)

    def acceptance_probability_boltzmann(self, current_fitness, new_fitness, temperature):
        if new_fitness > current_fitness:
            return 1.0
        else:
            return 1 / (1 + math.exp((current_fitness - new_fitness) / temperature))

    def acceptance_probability_metropolis(self, current_fitness, new_fitness, temperature):
        if new_fitness > current_fitness:
            return 1.0
        else:
            return math.exp((new_fitness - current_fitness) / temperature)