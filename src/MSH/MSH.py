import random
import time

from ..ACO.ACO import ACO
from ..SA.SA import SA
from ..ILS.ILS import ILS
from ..problems.CVRP import CVRP

class MultiStageHeuristic:
    def __init__(self, cvrp_problem, sa_config, ils_config, aco_config):
        self.cvrp_problem = cvrp_problem
        self.sa_config = sa_config
        self.ils_config = ils_config
        self.aco_config = aco_config

    def initialize_solution(self):
        # Use the greedy method to generate an initial solution
        initial_solution = self.cvrp_problem.generate_initial_solution('greedy')
        # Apply local search (e.g., 2-opt) to improve the initial solution
        improved_solution = self.local_search(initial_solution)
        return improved_solution

    def local_search(self, solution):
        # Implement a local search method (e.g., 2-opt)
        return self.two_opt(solution)

    def two_opt(self, solution):
        # Implement the 2-opt local search method
        best = solution
        improved = True
        while improved:
            improved = False
            for i in range(1, len(solution) - 2):
                for j in range(i + 1, len(solution)):
                    if j - i == 1: continue
                    new_solution = solution[:]
                    new_solution[i:j] = solution[j - 1:i - 1:-1]
                    if self.cvrp_problem.evaluate_fitness(new_solution) < self.cvrp_problem.evaluate_fitness(best):
                        best = new_solution
                        improved = True
            solution = best
        return best

    def run_sa(self, solution):
        # Use Simulated Annealing to explore the solution space
        sa = SA(
            problem=self.cvrp_problem,
            initial_temperature=self.sa_config['initial_temperature'],
            cooling_rate=self.sa_config['cooling_rate'],
            num_iterations=self.sa_config['num_iterations'],
            perturbation_method='swap',
            acceptance_method='default',
            initial_solution_method='random'
        )
        best_solution, best_fitness = sa.solve()
        return best_solution

    def run_ils(self, solution):
        # Use Iterated Local Search to intensify the search
        ils = ILS(
            problem=self.cvrp_problem,
            max_iterations=self.ils_config['max_iterations'],
            perturbation_method='swap',
            local_search_method='two_opt',
            acceptance_criterion='better'
        )
        best_solution, best_fitness = ils.solve()
        return best_solution

    def run_aco(self):
        # Use Ant Colony Optimization to optimize the best solutions
        aco = ACO(
            problem=self.cvrp_problem,
            num_ants=self.aco_config['num_ants'],
            num_iterations=self.aco_config['num_iterations'],
            alpha=self.aco_config['alpha'],
            beta=self.aco_config['beta'],
            rho=self.aco_config['rho'],
            q=self.aco_config['q'],
            construct_method='default',
            evaluate_method='default',
            update_method='default',
            pheromone_init_method='default'
        )
        best_solution, best_fitness = aco.solve()
        return best_solution

    def solve(self):
        # Initialization Stage
        initial_solution = self.initialize_solution()

        # Exploration Stage
        sa_solution = self.run_sa(initial_solution)

        # Exploitation Stage
        ils_solution = self.run_ils(sa_solution)

        # Optimization Stage
        best_solution = self.run_aco()

        return best_solution