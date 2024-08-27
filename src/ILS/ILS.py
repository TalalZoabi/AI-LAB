import random
import math
from src.problems.CVRP import CVRP
from src.problems.Ackley import Ackley
import numpy as np

class ILS:
    def __init__(self, problem, max_iterations, perturbation_method, local_search_method, acceptance_criterion):
        self.problem = problem
        self.max_iterations = max_iterations
        self.perturbation_method = self.get_method(perturbation_method, self.perturbation_methods())
        self.local_search_method = self.get_method(local_search_method, self.local_search_methods())
        self.acceptance_criterion = self.get_method(acceptance_criterion, self.acceptance_criteria())

    def solve(self):
        # Step 1: Generate an initial solution
        current_solution = self.problem.generate_initial_solution()
        current_fitness = self.problem.evaluate_fitness(current_solution)

        best_solution = current_solution
        best_fitness = current_fitness

        for iteration in range(self.max_iterations):
            # Step 2: Apply local search
            improved_solution = self.local_search(current_solution)
            improved_fitness = self.problem.evaluate_fitness(improved_solution)

            # Step 3: Apply perturbation
            perturbed_solution = self.perturb(improved_solution)
            perturbed_fitness = self.problem.evaluate_fitness(perturbed_solution)

            # Step 4: Apply acceptance criterion
            if self.acceptance_criterion(perturbed_fitness, current_fitness):
                current_solution = perturbed_solution
                current_fitness = perturbed_fitness

                if current_fitness < best_fitness:
                    best_solution = current_solution
                    best_fitness = current_fitness

        return best_solution, best_fitness

    def local_search(self, solution):
        # Implement a local search method (e.g., 2-opt)
        return self.local_search_method(solution, self.problem)

    def perturb(self, solution):
        # Implement a perturbation method (e.g., swap, insertion)
        return self.perturbation_method(solution)

    def acceptance_criterion(self, new_fitness, current_fitness):
        # Implement an acceptance criterion (e.g., always accept if better)
        return self.acceptance_criterion(new_fitness, current_fitness)

    def get_method(self, method_name, methods_dict):
        if method_name in methods_dict:
            return methods_dict[method_name]
        else:
            raise ValueError(f"Unsupported method: {method_name}")

    def perturbation_methods(self):
        return {
            'swap': self.swap,
            'insertion': self.insertion,
            'inversion': self.inversion,
            'scramble': self.scramble
        }

    def local_search_methods(self):
        return {
            'one_opt': self.one_opt,
            'two_opt': self.two_opt
        }

    def acceptance_criteria(self):
        return {
            'better': lambda new, current: new < current
        }

    def swap(self, solution):
        # Implement the swap perturbation method
        idx1, idx2 = random.sample(range(1, len(solution) - 1), 2)
        solution[idx1], solution[idx2] = solution[idx2], solution[idx1]
        return solution

    def insertion(self, solution):
        # Implement the insertion perturbation method
        idx1, idx2 = random.sample(range(1, len(solution) - 1), 2)
        gene = solution.pop(idx1)
        solution.insert(idx2, gene)
        return solution

    def inversion(self, solution):
        # Implement the inversion perturbation method
        idx1, idx2 = sorted(random.sample(range(1, len(solution) - 1), 2))
        solution[idx1:idx2] = reversed(solution[idx1:idx2])
        return solution

    def scramble(self, solution):
        # Implement the scramble perturbation method
        idx1, idx2 = sorted(random.sample(range(1, len(solution) - 1), 2))
        segment = solution[idx1:idx2]
        random.shuffle(segment)
        solution[idx1:idx2] = segment
        return solution

    def one_opt(self, solution, problem):
        # Implement the 1-opt local search method
        for i in range(1, len(solution) - 1):
            for j in range(i + 1, len(solution) - 1):
                new_solution = solution[:i] + [solution[j]] + solution[i:j] + solution[j+1:]
                if problem.evaluate_fitness(new_solution) < problem.evaluate_fitness(solution):
                    solution = new_solution
        return solution

    def two_opt(self, solution, problem):
        if isinstance(solution, np.ndarray):
            solution = solution.tolist()
        
        best_solution = solution[:]
        best_fitness = problem.evaluate_fitness(solution)
        for i in range(1, len(solution) - 1):
            for j in range(i + 1, len(solution)):
                # Ensure slices are correctly concatenated
                new_solution = solution[:i] + solution[i:j][::-1] + solution[j:]
                new_fitness = problem.evaluate_fitness(new_solution)
                if new_fitness < best_fitness:
                    best_solution = new_solution[:]
                    best_fitness = new_fitness
        return best_solution