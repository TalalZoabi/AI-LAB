from .FitnessFunction import FitnessFunction
import numpy as np

class CVRPFitness(FitnessFunction):
    def __init__(self, distances, vehicle_capacity, customer_demands):
        """
        Initializes the CVRP Fitness Function.
        
        :param distances: A 2D list (or array) of distances between customers and between customers and the depot.
        :param vehicle_capacity: The maximum capacity of each vehicle.
        :param customer_demands: A list of demands for each customer.
        """
        self.distances = distances
        self.vehicle_capacity = vehicle_capacity
        self.customer_demands = customer_demands

    def evaluate(self, individual):
        """
        Evaluates the fitness of an individual solution.
        :param individual: A list of routes, where each route is a list of customer indices.
        :return: The fitness score of the individual.
        """
        total_distance = 0
        capacity_penalty = 0
        visited_customers = set()

        for route in individual:
            if not route:
                continue

            route_load = sum(self.customer_demands[customer] for customer in route)
            if route_load > self.vehicle_capacity:
                capacity_penalty += (route_load - self.vehicle_capacity) * 1000  # Apply a penalty for exceeding vehicle capacity

            route_distance = self.distances[0][route[0]]  # Distance from depot to first customer
            for i in range(len(route) - 1):
                route_distance += self.distances[route[i]][route[i + 1]]
            route_distance += self.distances[route[-1]][0]  # Return to depot
            total_distance += route_distance

            visited_customers.update(route)

        # Penalize for not visiting all customers
        missing_customers = set(range(1, len(self.customer_demands) + 1)) - visited_customers
        missing_customers_penalty = len(missing_customers) * 1000  # Arbitrary large penalty for each missing customer

        # Fitness calculation
        fitness = 1 / (total_distance + capacity_penalty + missing_customers_penalty + 1)  # +1 to avoid division by zero

        return fitness

    def max_fitness(self):
        """
        Returns the maximum possible fitness score.
        
        :return: The maximum possible fitness score.
        """
        return float('inf')  # Theoretically, the best fitness but impractical to achieve

    def min_fitness(self):
        """
        Returns the minimum possible fitness score.
        
        :return: The minimum possible fitness score.
        """
        return 0  # Worst-case scenario where routes are infinitely long