import random
import numpy as np
from ..problems.Ackley import Ackley
from ..problems.CVRP import CVRP

class ACO:
    def __init__(self, problem, num_ants, num_iterations, alpha, beta, rho, q, construct_method, evaluate_method, update_method, pheromone_init_method):
        self.problem = problem
        self.num_ants = num_ants
        self.num_iterations = num_iterations
        self.alpha = alpha
        self.beta = beta
        self.rho = rho
        self.q = q

        # Map method names to functions
        self.construct_methods = {
            'default': self.construct_solution_default,
            'greedy': self.construct_solution_greedy,
            'randomized': self.construct_solution_randomized,
        }
        self.evaluate_methods = {
            'default': self.evaluate_solution_default,
            'time_based': self.evaluate_solution_time_based,
            'cost_based': self.evaluate_solution_cost_based,
        }
        self.update_methods = {
            'default': self.update_pheromones_default,
            'rank_based': self.update_pheromones_rank_based,
            'elitist': self.update_pheromones_elitist,
        }
        self.pheromone_init_methods = {
            'default': self.initialize_pheromone_default,
            'uniform': self.initialize_pheromone_uniform,
            'random': self.initialize_pheromone_random,
        }

        # Select methods based on input strings
        self.construct_solution = self.construct_methods[construct_method]
        self.evaluate_solution = self.evaluate_methods[evaluate_method]
        self.update_pheromones = self.update_methods[update_method]
        self.initialize_pheromone = self.pheromone_init_methods[pheromone_init_method]

        # Initialize pheromone levels
        self.pheromone = self.initialize_pheromone()

    def initialize_pheromone_default(self):
        if isinstance(self.problem, CVRP):
            num_nodes = len(self.problem.customer_locations) + 1  # +1 for the depot
        elif isinstance(self.problem, Ackley):
            num_nodes = self.problem.dimension
        initial_pheromone = 1.0  # Initial pheromone level
        pheromone_matrix = np.full((num_nodes, num_nodes), initial_pheromone)
        return pheromone_matrix

    def initialize_pheromone_uniform(self):
        if isinstance(self.problem, CVRP):
            num_nodes = len(self.problem.customer_locations) + 1  # +1 for the depot
        elif isinstance(self.problem, Ackley):
            num_nodes = self.problem.dimension
        initial_pheromone = 0.5  # Different initial pheromone level
        pheromone_matrix = np.full((num_nodes, num_nodes), initial_pheromone)
        return pheromone_matrix

    def initialize_pheromone_random(self):
        if isinstance(self.problem, CVRP):
            num_nodes = len(self.problem.customer_locations) + 1  # +1 for the depot
        elif isinstance(self.problem, Ackley):
            num_nodes = self.problem.dimension
        pheromone_matrix = np.random.rand(num_nodes, num_nodes)
        return pheromone_matrix

    def construct_solution_default(self):
        if isinstance(self.problem, CVRP):
            return self.construct_solution_cvrp()
        elif isinstance(self.problem, Ackley):
            return self.construct_solution_ackley()

    def construct_solution_greedy(self):
        if isinstance(self.problem, CVRP):
            return self.construct_solution_greedy_cvrp()
        elif isinstance(self.problem, Ackley):
            return self.construct_solution_greedy_ackley()

    def construct_solution_randomized(self):
        if isinstance(self.problem, CVRP):
            return self.construct_solution_randomized_cvrp()
        elif isinstance(self.problem, Ackley):
            return self.construct_solution_randomized_ackley()

    def construct_solution_cvrp(self):
        solution = [0]  # Start with the depot
        visited = set()
        current_node = 0
        current_load = 0  # Track the current load of the vehicle
        num_customers = len(self.problem.customer_locations)
        
        while len(visited) < num_customers:
            probabilities = self.calculate_probabilities(current_node, visited)
            if not probabilities:
                # If no valid probabilities, return to depot and start a new route
                solution.append(0)
                current_node = 0
                current_load = 0
                continue
            
            next_node = self.select_next_node(probabilities)
            
            if next_node == 0:
                # If the next node is the depot, check if we need to start a new route
                if current_node == 0:
                    # If we are already at the depot and can't find a valid next node, break the loop
                    break
                else:
                    # Return to depot and start a new route
                    solution.append(0)
                    current_node = 0
                    current_load = 0
                    continue
            
            # Validate the next node
            if next_node < 0 or next_node > num_customers:
                continue
            
            next_demand = self.problem.customer_demands[next_node - 1]
            if current_load + next_demand > self.problem.vehicle_capacity:
                # Return to depot and start a new route
                solution.append(0)
                current_node = 0
                current_load = 0
                continue
            
            solution.append(next_node)
            visited.add(next_node)
            current_load += next_demand
            current_node = next_node
        
        solution.append(0)  # End with the depot
        return solution

    def construct_solution_greedy_cvrp(self):
        solution = []
        visited = set()
        current_node = 0  # Start from the depot
        current_load = 0  # Track the current load of the vehicle
        solution.append(current_node)
        visited.add(current_node)

        while len(visited) < len(self.problem.customer_locations) + 1:
            next_node = self.select_next_node_greedy(current_node, visited)
            
            if next_node == 0 or len(visited) == len(self.problem.customer_locations) or current_load + self.problem.customer_demands[next_node - 1] > self.problem.vehicle_capacity:
                solution.append(0)  # End the current vehicle's route at the depot
                current_load = 0  # Reset the load for the new vehicle
                if len(visited) < len(self.problem.customer_locations):
                    current_node = 0  # Start a new vehicle's route from the depot
                else:
                    break
            else:
                solution.append(next_node)
                visited.add(next_node)
                current_load += self.problem.customer_demands[next_node - 1]
                current_node = next_node

        # Ensure the solution ends at the depot
        if solution[-1] != 0:
            solution.append(0)

        return solution

    def construct_solution_randomized_cvrp(self):
        solution = []
        visited = set()
        current_node = 0  # Start from the depot
        current_load = 0  # Track the current load of the vehicle
        solution.append(current_node)
        visited.add(current_node)

        while len(visited) < len(self.problem.customer_locations) + 1:
            probabilities = self.calculate_probabilities(current_node, visited)
            next_node = self.select_next_node_randomized(probabilities)
            
            if next_node == 0 or len(visited) == len(self.problem.customer_locations) or current_load + self.problem.customer_demands[next_node - 1] > self.problem.vehicle_capacity:
                solution.append(0)  # End the current vehicle's route at the depot
                current_load = 0  # Reset the load for the new vehicle
                if len(visited) < len(self.problem.customer_locations):
                    current_node = 0  # Start a new vehicle's route from the depot
                else:
                    break
            else:
                solution.append(next_node)
                visited.add(next_node)
                current_load += self.problem.customer_demands[next_node - 1]
                current_node = next_node

        # Ensure the solution ends at the depot
        if solution[-1] != 0:
            solution.append(0)

        return solution

    def construct_solution_ackley(self):
        solution = []
        for _ in range(self.problem.dimension):
            solution.append(random.uniform(-32.768, 32.768))
        return solution

    def construct_solution_greedy_ackley(self):
        solution = []
        for _ in range(self.problem.dimension):
            solution.append(0)  # Greedy approach for Ackley problem
        return solution

    def construct_solution_randomized_ackley(self):
        solution = []
        for _ in range(self.problem.dimension):
            solution.append(random.uniform(-32.768, 32.768))
        return solution

    def calculate_probabilities(self, current_node, visited):
        probabilities = []
        total = 0
        num_nodes = len(self.problem.customer_locations)  # Corrected range

        for node in range(num_nodes):  # +1 for the depot
            if node not in visited and node <= num_nodes:  # Ensure node is within valid range
                if current_node == 0:
                    current_coords = self.problem.depot_location
                else:
                    current_coords = self.problem.customer_locations[current_node - 1]

                if node == 0:
                    next_coords = self.problem.depot_location
                else:
                    next_coords = self.problem.customer_locations[node - 1]

                pheromone = self.pheromone[current_node][node] ** self.alpha
                distance = self.problem.distance(current_coords, next_coords)
                if distance == 0:
                    heuristic = float('inf')  # Handle division by zero
                else:
                    heuristic = (1.0 / distance) ** self.beta

                probability = pheromone * heuristic
                probabilities.append((node, probability))
                total += probability

        if total == 0 or np.isnan(total) or np.isinf(total):
            probabilities = [(node, 1.0) for node, _ in probabilities]  # Handle zero or invalid total probability
            total = len(probabilities)


        return [(node, prob / total) for node, prob in probabilities]

    def select_next_node(self, probabilities):
        if not probabilities:
            return 0  # Return to depot if no valid probabilities
        
        nodes, probs = zip(*probabilities)
        if any(np.isnan(probs)) or any(np.isinf(probs)):
            raise ValueError("Probabilities contain NaN or inf values")
        
        
        next_node = random.choices(nodes, probs)[0]
                
        return next_node

    def select_next_node_greedy(self, current_node, visited):
        best_node = None
        best_value = float('-inf')
        num_nodes = len(self.problem.customer_locations)

        for node in range(num_nodes):
            if node not in visited:
                if current_node == 0:
                    current_coords = self.problem.depot_location
                else:
                    current_coords = self.problem.customer_locations[current_node - 1]

                if node == 0:
                    next_coords = self.problem.depot_location
                else:
                    next_coords = self.problem.customer_locations[node - 1]

                value = 1.0 / self.problem.distance(current_coords, next_coords)

                if value > best_value:
                    best_value = value
                    best_node = node

        return best_node

    def select_next_node_randomized(self, probabilities):
        if not probabilities:
            return 0  # Return to depot if no valid probabilities
        
        nodes, probs = zip(*probabilities)
        return random.choices(nodes, probs)[0]

    def evaluate_solution_default(self, solution):
        return self.problem.evaluate(solution)

    def evaluate_solution_time_based(self, solution):
        if isinstance(self.problem, CVRP):
            return self.evaluate_solution_time_based_cvrp(solution)
        elif isinstance(self.problem, Ackley):
            return self.evaluate_solution_ackley(solution)

    def evaluate_solution_cost_based(self, solution):
        if isinstance(self.problem, CVRP):
            return self.evaluate_solution_cost_based_cvrp(solution)
        elif isinstance(self.problem, Ackley):
            return self.evaluate_solution_ackley(solution)

    def evaluate_solution_time_based_cvrp(self, solution):
        total_time = 0
        current_coords = self.problem.depot_location

        for i in range(1, len(solution)):
            if solution[i] == 0:
                next_coords = self.problem.depot_location
            else:
                next_coords = self.problem.customer_locations[solution[i] - 1]

            total_time += self.problem.distance(current_coords, next_coords) / self.problem.vehicle_speed
            current_coords = next_coords

        return total_time

    def evaluate_solution_cost_based_cvrp(self, solution):
        total_cost = 0
        current_coords = self.problem.depot_location

        for i in range(1, len(solution)):
            if solution[i] == 0:
                next_coords = self.problem.depot_location
            else:
                next_coords = self.problem.customer_locations[solution[i] - 1]

            total_cost += self.problem.distance(current_coords, next_coords) * self.problem.cost_per_distance
            current_coords = next_coords

        return total_cost

    def update_pheromones_default(self, solutions):
        if isinstance(self.problem, CVRP):
            num_nodes = len(self.problem.customer_locations) + 1
            for i in range(num_nodes):
                for j in range(num_nodes):
                    self.pheromone[i][j] *= (1 - self.rho)

            for solution in solutions:
                fitness = self.evaluate_solution(solution)
                pheromone_deposit = self.q / fitness
                for i in range(len(solution) - 1):
                    self.pheromone[solution[i]][solution[i + 1]] += pheromone_deposit
                self.pheromone[solution[-1]][solution[0]] += pheromone_deposit  # Return to start
        elif isinstance(self.problem, Ackley):
            self.pheromone *= (1 - self.rho)
            best_solution = min(solutions, key=lambda s: self.evaluate_solution(s))
            fitness = self.evaluate_solution(best_solution)
            pheromone_deposit = self.q / fitness
            self.pheromone += pheromone_deposit

    def update_pheromones_rank_based(self, solutions):
        if isinstance(self.problem, CVRP):
            num_nodes = len(self.problem.customer_locations) + 1
            for i in range(num_nodes):
                for j in range(num_nodes):
                    self.pheromone[i][j] *= (1 - self.rho)

            ranked_solutions = sorted(solutions, key=lambda s: self.evaluate_solution(s))
            for rank, solution in enumerate(ranked_solutions):
                fitness = self.evaluate_solution(solution)
                pheromone_deposit = (self.q / fitness) * (len(ranked_solutions) - rank)
                for i in range(len(solution) - 1):
                    self.pheromone[solution[i]][solution[i + 1]] += pheromone_deposit
                self.pheromone[solution[-1]][solution[0]] += pheromone_deposit  # Return to start
        elif isinstance(self.problem, Ackley):
            self.pheromone *= (1 - self.rho)
            ranked_solutions = sorted(solutions, key=lambda s: self.evaluate_solution(s))
            for rank, solution in enumerate(ranked_solutions):
                fitness = self.evaluate_solution(solution)
                pheromone_deposit = (self.q / fitness) * (len(ranked_solutions) - rank)
                self.pheromone += pheromone_deposit

    def update_pheromones_elitist(self, solutions):
        if isinstance(self.problem, CVRP):
            num_nodes = len(self.problem.customer_locations) + 1
            for i in range(num_nodes):
                for j in range(num_nodes):
                    self.pheromone[i][j] *= (1 - self.rho)

            best_solution = min(solutions, key=lambda s: self.evaluate_solution(s))
            fitness = self.evaluate_solution(best_solution)
            pheromone_deposit = self.q / fitness
            for i in range(len(best_solution) - 1):
                self.pheromone[best_solution[i]][best_solution[i + 1]] += pheromone_deposit
            self.pheromone[best_solution[-1]][best_solution[0]] += pheromone_deposit  # Return to start
        elif isinstance(self.problem, Ackley):
            self.pheromone *= (1 - self.rho)
            best_solution = min(solutions, key=lambda s: self.evaluate_solution(s))
            fitness = self.evaluate_solution(best_solution)
            pheromone_deposit = self.q / fitness
            self.pheromone += pheromone_deposit

    def solve(self):
        best_solution = None
        best_fitness = float('inf')
        for _ in range(self.num_iterations):
            solutions = [self.construct_solution() for _ in range(self.num_ants)]
            for solution in solutions:
                fitness = self.evaluate_solution(solution)
                if fitness < best_fitness:
                    best_fitness = fitness
                    best_solution = solution
            self.update_pheromones(solutions)
        return best_solution, best_fitness