import re
import numpy as np
import matplotlib.pyplot as plt
import random
from .Problem import Problem

class CVRP(Problem):
    def __init__(self, vehicle_capacity, customer_demands, customer_locations, depot_location, vehicle_speed=1.0, cost_per_distance=1.0):
        self.vehicle_capacity = vehicle_capacity
        self.customer_demands = customer_demands
        self.customer_locations = customer_locations
        self.depot_location = depot_location
        self.vehicle_speed = vehicle_speed
        self.cost_per_distance = cost_per_distance


    @staticmethod
    def from_file(file_path):
        with open(file_path, 'r') as file:
            lines = file.readlines()

        data = {
            'NAME': '',
            'COMMENT': '',
            'TYPE': '',
            'DIMENSION': 0,
            'EDGE_WEIGHT_TYPE': '',
            'CAPACITY': 0,
            'NODE_COORD_SECTION': {},
            'DEMAND_SECTION': {},
            'NODE_DATA': []
        }

        section = None

        for line in lines:
            line = line.strip()
            if line == 'NODE_COORD_SECTION':
                section = 'NODE_COORD_SECTION'
                continue
            elif line == 'DEMAND_SECTION':
                section = 'DEMAND_SECTION'
                continue
            elif line == 'DEPOT_SECTION':
                section = 'DEPOT_SECTION'
                continue
            elif line == 'EOF':
                break

            if section is None:
                if ':' in line:
                    parts = line.split(':', 1)
                    key, value = parts[0].strip(), parts[1].strip()
                    if key in data:
                        if key in ['DIMENSION', 'CAPACITY']:
                            data[key] = int(value)
                        else:
                            data[key] = value
            else:
                if section == 'NODE_COORD_SECTION':
                    parts = re.split(r'\s+', line)
                    node_id = int(parts[0])
                    x_coord = float(parts[1])
                    y_coord = float(parts[2])
                    data[section][node_id] = (x_coord, y_coord)
                elif section == 'DEMAND_SECTION':
                    parts = re.split(r'\s+', line)
                    node_id = int(parts[0])
                    demand = int(parts[1])
                    data[section][node_id] = demand

        # Combine NODE_COORD_SECTION and DEMAND_SECTION into NODE_DATA
        customer_demands = [0]  # Depot demand is 0
        customer_locations = [(0, 0)]  # Depot location is (0, 0)

        for node_id in range(1, data['DIMENSION'] + 1):
            if node_id in data['NODE_COORD_SECTION']:
                customer_locations.append(data['NODE_COORD_SECTION'][node_id])
            if node_id in data['DEMAND_SECTION']:
                customer_demands.append(data['DEMAND_SECTION'][node_id])

        return CVRP(
            vehicle_capacity=data['CAPACITY'],
            customer_demands=customer_demands,
            customer_locations=customer_locations,
            depot_location=(0, 0)  # Explicitly set depot location to (0, 0)
        )


    def generate_initial_solution(self, method='greedy'):
        if method == 'greedy':
            return self.generate_greedy_solution()
        elif method == 'random':
            return self.generate_random_solution()
        else:
            raise ValueError(f"Unsupported method: {method}")

    def generate_greedy_solution(self):
        num_customers = len(self.customer_demands)
        unvisited = set(range(1, num_customers))
        solution = [0]  # Start at the depot
        current_load = 0

        while unvisited:
            current_location = solution[-1]
            nearest_customer = None
            nearest_distance = float('inf')

            for customer in unvisited:
                distance = self.distance(self.customer_locations[current_location], self.customer_locations[customer])
                if distance < nearest_distance and current_load + self.customer_demands[customer] <= self.vehicle_capacity:
                    nearest_customer = customer
                    nearest_distance = distance

            if nearest_customer is None:
                # Return to the depot and start a new route
                solution.append(0)
                current_load = 0
            else:
                # Visit the nearest customer
                solution.append(nearest_customer)
                current_load += self.customer_demands[nearest_customer]
                unvisited.remove(nearest_customer)

        solution.append(0)  # Return to the depot at the end
        return solution

    def generate_random_solution(self):
        customers = list(range(1, len(self.customer_demands)))
        random.shuffle(customers)
        routes = []
        current_route = []
        current_load = 0

        for customer in customers:
            if current_load + self.customer_demands[customer] <= self.vehicle_capacity:
                current_route.append(customer)
                current_load += self.customer_demands[customer]
            else:
                routes.append(current_route)
                current_route = [customer]
                current_load = self.customer_demands[customer]

        if current_route:
            routes.append(current_route)

        # Convert routes to a single list with depots
        solution = []
        for route in routes:
            if route:
                solution.append(0)
                solution.extend(route)
        solution.append(0)
        return solution

    def calculate_distance_matrix(self):
        num_customers = len(self.customer_locations)
        distance_matrix = [[0] * num_customers for _ in range(num_customers)]

        for i in range(num_customers):
            for j in range(num_customers):
                distance_matrix[i][j] = self.distance(self.customer_locations[i], self.customer_locations[j])

        return distance_matrix


    def calculate_route_distance(self, route):
        distance = 0
        if len(route) == 0:
            return distance
        distance += self.distance((0, 0), self.customer_locations[route[0]])
        for i in range(len(route) - 1):
            distance += self.distance(self.customer_locations[route[i]], self.customer_locations[route[i + 1]])
        distance += self.distance(self.customer_locations[route[-1]], (0, 0))
        return distance

    def distance(self, point1, point2):
        return np.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

    def display_individual(self, individual):
        plt.figure()
        current_route = []
        for node in individual:
            if node == 0:
                if current_route:
                    route_coords = [(0, 0)] + [self.customer_locations[customer] for customer in current_route] + [(0, 0)]
                    x_coords = [coord[0] for coord in route_coords]
                    y_coords = [coord[1] for coord in route_coords]
                    plt.plot(x_coords, y_coords, marker='o')
                    current_route = []
            else:
                current_route.append(node)
        
        plt.scatter(0, 0, color='red', label='Depot')
        for i, location in enumerate(self.customer_locations):
            plt.annotate(i, location)
        plt.legend()
        plt.show()

    def evaluate_fitness(self, individual):
        """
        Evaluates the fitness of an individual solution.
        :param individual: A list of integers where segments between 0s represent routes.
        :return: The fitness score of the individual.
        """
        total_distance = 0
        capacity_penalty = 0
        route = []

        for customer in individual:
            if customer == 0:
                if route:
                    route_load = sum(self.customer_demands[customer] for customer in route)
                    if route_load > self.vehicle_capacity:
                        capacity_penalty += (route_load - self.vehicle_capacity) * 1000  # Apply a penalty for exceeding vehicle capacity

                    route_distance = self.calculate_route_distance(route)
                    total_distance += route_distance

                    route = []
            else:
                route.append(customer)

        fitness = 1 / (total_distance + capacity_penalty + 1)  # +1 to avoid division by zero

        return fitness
    


    def evaluate(self, individual):
        """
        Evaluates the fitness of an individual solution.
        :param individual: A list of integers where segments between 0s represent routes.
        :return: The fitness score of the individual.
        """
        total_distance = 0
        capacity_penalty = 0
        route = []

        for customer in individual:
            if customer == 0:
                if route:
                    # Validate customer IDs
                    for customer in route:
                        if customer >= len(self.customer_demands) or customer < 0:
                            raise ValueError(f"Invalid customer ID {customer} in route: {route}")

                    route_load = sum(self.customer_demands[customer] for customer in route)
                    if route_load > self.vehicle_capacity:
                        capacity_penalty += (route_load - self.vehicle_capacity) * 1000  # Apply a penalty for exceeding vehicle capacity

                    route_distance = self.calculate_route_distance(route)
                    total_distance += route_distance

                    route = []
            else:
                route.append(customer)

        fitness = 1 / (total_distance + capacity_penalty + 1)  # +1 to avoid division by zero

        return fitness
    
    


    def evaluate_solution_time_based(self, solution):
        total_time = 0
        current_coords = self.depot_location

        for i in range(1, len(solution)):
            if solution[i] == 0:
                next_coords = self.depot_location
            else:
                next_coords = self.customer_locations[solution[i] - 1]

            total_time += self.distance(current_coords, next_coords) / self.vehicle_speed
            current_coords = next_coords

        return total_time

    def evaluate_solution_cost_based(self, solution):
        total_cost = 0
        current_coords = self.depot_location

        for i in range(1, len(solution)):
            if solution[i] == 0:
                next_coords = self.depot_location
            else:
                next_coords = self.customer_locations[solution[i] - 1]

            total_cost += self.distance(current_coords, next_coords) * self.cost_per_distance
            current_coords = next_coords

        return total_cost