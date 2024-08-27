import random
import matplotlib.pyplot as plt
from ..problems.CVRP import CVRP
from ..problems.Ackley import Ackley
import numpy as np

class TabuList:
    def __init__(self, size):
        self.size = size
        self.list = []

    def add(self, move):
        self.list.append(move)
        if len(self.list) > self.size:
            self.list.pop(0)

    def contains(self, move):
        return move in self.list

class TS:
    def __init__(self, problem, num_iterations, tabu_tenure, neighborhood_method='default', aspiration_method='default'):
        self.problem = problem
        self.num_iterations = num_iterations
        self.tabu_tenure = tabu_tenure
        self.tabu_list = TabuList(tabu_tenure)
        self.current_solution = problem.generate_initial_solution()
        self.best_solution = self.current_solution
        self.neighborhood_method = self.get_method(neighborhood_method, self.neighborhood_methods())
        self.aspiration_method = self.get_method(aspiration_method, self.aspiration_methods())

    def get_method(self, method_name, methods_dict):
        if method_name in methods_dict:
            return methods_dict[method_name]
        else:
            raise ValueError(f"Unsupported method: {method_name}")

    def neighborhood_methods(self):
        return {
            'default': self.generate_neighborhood_default,
            'alternative': self.generate_neighborhood_alternative,
            'insertion': self.generate_neighborhood_insertion,
            'reverse_subsequence': self.generate_neighborhood_reverse_subsequence
        }

    def aspiration_methods(self):
        return {
            'default': self.aspiration_criteria_default,
            'alternative': self.aspiration_criteria_alternative,
            'threshold': self.aspiration_criteria_threshold,
            'improvement': self.aspiration_criteria_improvement
        }

    def generate_neighborhood_default(self, solution):
        if isinstance(solution, np.ndarray):
            solution = solution.tolist()
        
        neighborhood = []

        # Swap operation
        for i in range(1, len(solution)):
            for j in range(i + 1, len(solution)):
                if isinstance(self.problem, CVRP) and (solution[i] == 0 or solution[j] == 0):
                    continue
                new_solution = solution[:]
                new_solution[i], new_solution[j] = new_solution[j], new_solution[i]
                neighborhood.append(new_solution)

        # Relocate operation
        for i in range(1, len(solution)):
            for j in range(1, len(solution)):
                if i != j and (not isinstance(self.problem, CVRP) or solution[i] != 0):
                    new_solution = solution[:]
                    customer = new_solution.pop(i)
                    new_solution.insert(j, customer)
                    neighborhood.append(new_solution)

        # 2-opt operation
        for i in range(1, len(solution)):
            for j in range(i + 1, len(solution)):
                if isinstance(self.problem, CVRP) and (solution[i] == 0 or solution[j] == 0):
                    continue
                new_solution = solution[:]
                new_solution[i:j] = reversed(new_solution[i:j])
                neighborhood.append(new_solution)

        # Add Vehicle operation (only for CVRP)
        if isinstance(self.problem, CVRP):
            for i in range(1, len(solution)):
                if solution[i] != 0:
                    new_solution = solution[:]
                    new_solution.insert(i, 0)
                    neighborhood.append(new_solution)

        # Remove Vehicle operation (only for CVRP)
        if isinstance(self.problem, CVRP) and solution.count(0) - 1 > 1:
            for i in range(1, len(solution)):
                if solution[i] == 0:
                    new_solution = solution[:]
                    new_solution.pop(i)
                    neighborhood.append(new_solution)

        # Cross-Exchange operation (only for CVRP)
        if isinstance(self.problem, CVRP):
            for i in range(1, len(solution)):
                for j in range(i + 1, len(solution)):
                    if solution[i] == 0 or solution[j] == 0:
                        continue
                    for k in range(j + 1, len(solution)):
                        if solution[k] == 0:
                            break
                        new_solution = solution[:]
                        new_solution[i:j], new_solution[j:k] = new_solution[j:k], new_solution[i:j]
                        neighborhood.append(new_solution)

        # Validate and filter neighborhood
        valid_neighborhood = [neighbor for neighbor in neighborhood if self.validate_solution(neighbor)]

        return valid_neighborhood

    def generate_neighborhood_alternative(self, solution):
        # Implement an alternative neighborhood generation method
        neighborhood = []
        for i in range(1, len(solution) - 1):
            for j in range(i + 1, len(solution)):
                new_solution = solution[:]
                new_solution[i], new_solution[j] = new_solution[j], new_solution[i]
                neighborhood.append(new_solution)
        valid_neighborhood = [neighbor for neighbor in neighborhood if self.validate_solution(neighbor)]
        return valid_neighborhood

    def generate_neighborhood_insertion(self, solution):
        neighborhood = []
        for i in range(1, len(solution)):
            for j in range(1, len(solution)):
                if i != j and (not isinstance(self.problem, CVRP) or solution[i] != 0):
                    new_solution = solution[:]
                    customer = new_solution.pop(i)
                    new_solution.insert(j, customer)
                    neighborhood.append(new_solution)
        valid_neighborhood = [neighbor for neighbor in neighborhood if self.validate_solution(neighbor)]
        return valid_neighborhood

    def generate_neighborhood_reverse_subsequence(self, solution):
        neighborhood = []
        for i in range(1, len(solution)):
            for j in range(i + 1, len(solution)):
                if isinstance(self.problem, CVRP) and (solution[i] == 0 or solution[j] == 0):
                    continue
                new_solution = solution[:]
                new_solution[i:j] = reversed(new_solution[i:j])
                neighborhood.append(new_solution)
        valid_neighborhood = [neighbor for neighbor in neighborhood if self.validate_solution(neighbor)]
        return valid_neighborhood

    def validate_solution(self, solution):
        if isinstance(self.problem, CVRP):
            visited = set()
            current_load = 0

            for customer in solution:
                if customer == 0:
                    if current_load > self.problem.vehicle_capacity:
                        return False
                    current_load = 0
                else:
                    if customer in visited:
                        return False
                    visited.add(customer)
                    current_load += self.problem.customer_demands[customer]

            # Check if all customers are visited
            if len(visited) != len(self.problem.customer_demands):
                return False

            return True
        elif isinstance(self.problem, Ackley):
            # For Ackley, we assume all solutions are valid
            return True

    def aspiration_criteria_default(self, neighbor):
        return self.problem.evaluate_fitness(neighbor) < self.problem.evaluate_fitness(self.best_solution)

    def aspiration_criteria_alternative(self, neighbor):
        # Implement an alternative aspiration criteria method
        return self.problem.evaluate_fitness(neighbor) < self.problem.evaluate_fitness(self.current_solution)

    def aspiration_criteria_threshold(self, neighbor, threshold=0.9):
        return self.problem.evaluate_fitness(neighbor) < threshold

    def aspiration_criteria_improvement(self, neighbor, improvement_percentage=0.05):
        current_fitness = self.problem.evaluate_fitness(self.current_solution)
        neighbor_fitness = self.problem.evaluate_fitness(neighbor)
        return neighbor_fitness < current_fitness * (1 - improvement_percentage)

    def tabu_search(self):
        for iteration in range(self.num_iterations):
            neighborhood = self.neighborhood_method(self.current_solution)
            best_neighbor = None
            best_neighbor_cost = float('inf')

            for neighbor in neighborhood:
                if not self.tabu_list.contains(neighbor) or self.aspiration_method(neighbor):
                    cost = self.problem.evaluate_fitness(neighbor)
                    if cost < best_neighbor_cost:
                        best_neighbor = neighbor
                        best_neighbor_cost = cost

            if best_neighbor is not None:
                self.current_solution = best_neighbor
                self.tabu_list.add(self.current_solution)
                if self.problem.evaluate_fitness(self.current_solution) < self.problem.evaluate_fitness(self.best_solution):
                    self.best_solution = self.current_solution
            else:
                # Handle the case where no valid neighbor is found
                print(f"Iteration {iteration}: No valid neighbor found, keeping the current best solution.")

        return self.best_solution

    def print_solution_details(self, solution):
        if isinstance(self.problem, CVRP):
            current_load = 0
            total_distance = 0
            vehicle_index = 1
            route_distance = 0

            print(f"Vehicle {vehicle_index} route: ", end="")
            for i in range(len(solution) - 1):
                from_node = solution[i]
                to_node = solution[i + 1]
                if from_node == 0:
                    if i != 0:
                        print(f"Load: {current_load}, Distance: {route_distance:.2f}")
                        vehicle_index += 1
                        print(f"Vehicle {vehicle_index} route: ", end="")
                    current_load = 0
                    route_distance = 0
                else:
                    current_load += self.problem.customer_demands[from_node]
                route_distance += self.calculate_distance(from_node, to_node)
                total_distance += self.calculate_distance(from_node, to_node)
                print(f"{from_node} -> ", end="")
            print(f"Load: {current_load}, Distance: {route_distance:.2f}")
            print(f"Total distance traveled: {total_distance:.2f}")

    def calculate_distance(self, from_node, to_node):
        if isinstance(self.problem, CVRP):
            from_location = self.problem.customer_locations[from_node] if from_node != 0 else (0, 0)
            to_location = self.problem.customer_locations[to_node] if to_node != 0 else (0, 0)
            return ((from_location[0] - to_location[0]) ** 2 + (from_location[1] - to_location[1]) ** 2) ** 0.5
        elif isinstance(self.problem, Ackley):
            # For Ackley, we don't need to calculate distances
            return 0

    def plot_solution(self, solution):
        if isinstance(self.problem, CVRP):
            colors = plt.cm.tab10.colors
            vehicle_routes = []
            current_route = []
            visited_customers = set()

            for customer in solution:
                if customer == 0:
                    if current_route:
                        vehicle_routes.append(current_route)
                        current_route = []
                else:
                    current_route.append(customer)
                    visited_customers.add(customer)
            if current_route:
                vehicle_routes.append(current_route)

            num_vehicles = len(vehicle_routes)
            fig, axes = plt.subplots(num_vehicles, 1, figsize=(10, 5 * num_vehicles), tight_layout=True)

            if num_vehicles == 1:
                axes = [axes]

            for i, route in enumerate(vehicle_routes):
                ax = axes[i]
                ax.set_title(f"Vehicle {i + 1} Route")
                ax.set_xlabel("X Coordinate")
                ax.set_ylabel("Y Coordinate")

                route_distance = 0
                route_load = 0
                previous_location = (0, 0)

                for customer in route:
                    current_location = self.problem.customer_locations[customer]
                    ax.plot([previous_location[0], current_location[0]], [previous_location[1], current_location[1]], color=colors[i % len(colors)])
                    previous_location = current_location
                    route_load += self.problem.customer_demands[customer]
                    route_distance += self.calculate_distance(previous_location, current_location)

                ax.plot([previous_location[0], 0], [previous_location[1], 0], color=colors[i % len(colors)])
                ax.text(0, 0, 'Depot', fontsize=12, ha='right')
                ax.text(previous_location[0], previous_location[1], f'Load: {route_load}, Distance: {route_distance:.2f}', fontsize=12, ha='right')

            plt.show()