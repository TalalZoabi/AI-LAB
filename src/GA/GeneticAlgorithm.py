import random
import logging
import numpy as np
from src.problems.CVRP import CVRP

class GeneticAlgorithm:
    def __init__(self, config):
        self.fitness_function = config['fitness_function']
        self.population_size = config['population_size']
        self.num_generations = config['num_generations']
        self.crossover_rate = config['crossover_rate']
        self.mutation_rate = config['mutation_rate']
        self.num_islands = config['num_islands']
        self.migration_rate = config['migration_rate']
        self.generate_initial_solution = config['generate_initial_solution']
        self.islands = self.initialize_islands()
        
        # Configuration for various methods
        self.parent_selection = config['parent_selection']
        self.crossover_operator = config['crossover_operator']
        self.mutation_operator = config['mutation_operator']
        self.survivor_selection = config['survivor_selection']
        self.mutation_strategy = config['mutation_strategy']

    def initialize_islands(self):
        islands = []
        for _ in range(self.num_islands):
            population = [self.generate_initial_solution() for _ in range(self.population_size // self.num_islands)]
            islands.append(population)
        return islands

    def selection(self, population, fitnesses, num_parents):
        return self.parent_selection.select(population, fitnesses, num_parents)

    def crossover(self, parent1, parent2):
        offspring = self.crossover_operator.crossover(parent1, parent2)
        # Check if any of the offspring is None
        if offspring is None or any(child is None for child in offspring):
            logging.warning("Crossover resulted in None child, using parents as offspring.")
            return [parent1, parent2]
        return offspring

    def mutation(self, individual):
        if self.mutation_strategy.should_mutate({'generation': self.current_generation, 'best_fitness': self.best_fitness}):
            return self.mutation_operator.mutate(individual)
        return individual

    def migrate(self):
        for i in range(self.num_islands):
            if i < self.num_islands - 1:
                index = random.randint(0, len(self.islands[i]) - 1)
                migrant = self.islands[i].pop(index)
                self.islands[i + 1].append(migrant)
            else:
                index = random.randint(0, len(self.islands[i]) - 1)
                migrant = self.islands[i].pop(index)
                self.islands[0].append(migrant)

    def evaluate_fitness(self, population):
        return [self.fitness_function.evaluate(individual) for individual in population]

    def evolve(self):
        self.current_generation = 0
        self.best_fitness = float('inf')
        for generation in range(self.num_generations):
            self.current_generation = generation
            for island in self.islands:
                new_population = []
                fitnesses = self.evaluate_fitness(island)
                for _ in range(len(island) // 2):
                    parent1, parent2 = self.selection(island, fitnesses, 2)
                    if random.random() < self.crossover_rate:
                        offspring1, offspring2 = self.crossover(parent1, parent2)
                    else:
                        offspring1, offspring2 = parent1, parent2
                    if random.random() < self.mutation_rate:
                        offspring1 = self.mutation(offspring1)
                    if random.random() < self.mutation_rate:
                        offspring2 = self.mutation(offspring2)
                    new_population.extend([offspring1, offspring2])
                island[:] = new_population
            if generation % self.migration_rate == 0:
                self.migrate()
        best_solution = min((ind for island in self.islands for ind in island), key=self.fitness_function.evaluate)
        return best_solution, self.fitness_function.evaluate(best_solution)

    def generate_initial_solution(self):
        """
        Generates an initial solution for the CVRP problem.
        :return: A list of integers representing the initial solution.
        """
        num_customers = len(self.fitness_function.customer_demands) - 1  # Exclude the depot
        customers = list(range(1, num_customers + 1))
        random.shuffle(customers)
        solution = [0]  # Start with the depot
        for customer in customers:
            solution.append(customer)
            if random.random() < 0.1:  # Randomly decide to return to the depot
                solution.append(0)
        solution.append(0)  # End with the depot
        return solution