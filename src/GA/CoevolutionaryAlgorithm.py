import random
import logging
import time
import numpy as np
from src.problems.CVRP import CVRP
import concurrent.futures

class CoevolutionaryAlgorithm:
    def __init__(self, config):

        # Configuration for the problem
        self.name = config['name']

        self.population_fitness_function = config['population_fitness_function']
        self.adversary_fitness_function = config['adversary_fitness_function']

        self.population_size = config['population_size']
        self.adversary_population_size = config['adversary_population_size']
        self.num_generations = config['num_generations']
        
        self.num_islands = config['num_islands']
        self.migration_rate = config['migration_rate']
        
        # Configuration for various methods
        self.population_parent_selection = config['population_parent_selection']
        self.adversary_parent_selection = config['adversary_parent_selection']

        self.population_crossover_operator = config['population_crossover_operator']
        self.adversary_crossover_operator = config['adversary_crossover_operator']

        self.population_mutation_operator = config['population_mutation_operator']
        self.adversary_mutation_operator = config['adversary_mutation_operator']
        
        self.population_survivor_selection = config['population_survivor_selection']
        self.adversary_survivor_selection = config['adversary_survivor_selection']
        
        self.population_mutation_strategy = config['population_mutation_strategy']
        self.adversary_mutation_strategy = config['adversary_mutation_strategy']

        self.population_sample_size = config['population_sample_size']
        self.adversary_sample_size = config['adversary_sample_size']

        # Create islands
        self.generate_population_individual = config['generate_individual']
        self.generate_adversary_individual = config['generate_adversary_individual']

        self.population_fitness_sharing = config['population_fitness_sharing']
        self.adversary_fitness_sharing = config['adversary_fitness_sharing']

        self.population_islands, self.adversary_islands = self.initialize_islands()
    
        # collect data for plotting
        self.population_fitnesses = []
        self.adversary_fitnesses = []





    def initialize_islands(self):
        pop_islands = []
        adv_islands = []
        for _ in range(self.num_islands):
            population = [self.generate_population_individual() for _ in range(self.population_size // self.num_islands)]
            pop_islands.append(population)

            adversary_population = [self.generate_adversary_individual() for _ in range(self.adversary_population_size // self.num_islands)]
            adv_islands.append(adversary_population)
        
        return pop_islands, adv_islands

    def population_selection(self, population, fitnesses, num_parents):
        return self.population_parent_selection.select(population, fitnesses, num_parents)

    def adversary_selection(self, population, fitnesses, num_parents):
        return self.adversary_parent_selection.select(population, fitnesses, num_parents)


    def population_mutation(self, individual, fitness, generation, num_generations):
        if self.population_mutation_strategy.should_mutate({'individual_fitness': fitness, 'generation': self.current_generation, 'best_fitness': self.best_pop_fitness}):
            return self.population_mutation_operator.mutate(individual, generation, num_generations)
        return individual
    
    def adversary_mutation(self, individual, fitness, generation, num_generations):
        if self.adversary_mutation_strategy.should_mutate({'individual_fitness': fitness, 'generation': self.current_generation, 'best_fitness': self.best_adv_fitness}):
            return self.adversary_mutation_operator.mutate(individual, generation, num_generations)
        return individual

    def population_migrate(self):
        for i in range(self.num_islands):
            if i < self.num_islands - 1:
                index = random.randint(0, len(self.population_islands[i]) - 1)
                migrant = self.population_islands[i].pop(index)
                self.population_islands[i + 1].append(migrant)
            else:
                index = random.randint(0, len(self.population_islands[i]) - 1)
                migrant = self.population_islands[i].pop(index)
                self.population_islands[0].append(migrant)

    def adversary_migrate(self):
        for i in range(self.num_islands):
            if i < self.num_islands - 1:
                index = random.randint(0, len(self.adversary_islands[i]) - 1)
                migrant = self.adversary_islands[i].pop(index)
                self.adversary_islands[i + 1].append(migrant)
            else:
                index = random.randint(0, len(self.adversary_islands[i]) - 1)
                migrant = self.adversary_islands[i].pop(index)
                self.adversary_islands[0].append(migrant)


    def population_evaluate_fitness(self, population, adv_population):
        # use parallelism
        with concurrent.futures.ThreadPoolExecutor() as executor:
            return list(executor.map(lambda x: self.population_fitness_function.evaluate(x, adv_population), population))


    def adversary_evaluate_fitness(self, adv_population, population):
        # use parallelism
        with concurrent.futures.ThreadPoolExecutor() as executor:
            return list(executor.map(lambda x: self.adversary_fitness_function.evaluate(x, population), adv_population))


    def population_crossover(self, parent1, parent2):
        offspring1, offspring2 = self.population_crossover_operator.crossover(parent1, parent2)
        return offspring1, offspring2
    
    def adversary_crossover(self, parent1, parent2):
        offspring1, offspring2 = self.adversary_crossover_operator.crossover(parent1, parent2)
        return offspring1, offspring2

    # parallelize this
    def evolve_population_island(self, island, generation):
        logging.info(f"Evolution on island of size {len(island)}")
        new_population = []
        new_population_fitnesses = []

        adversary_sample = self.sample_adversary_islands(self.adversary_sample_size)
        raw_fitnesses = self.population_evaluate_fitness(island, adversary_sample)

        if self.population_fitness_sharing is not None:
            shared_fitnesses = self.population_fitness_sharing.apply_sharing(island, raw_fitnesses)
        else:
            shared_fitnesses = raw_fitnesses
            
        island_len = self.population_size // self.num_islands
        parents = self.population_selection(island, shared_fitnesses, 2*island_len)
        parents = [(parents[i], parents[i+1]) for i in range(0, len(parents), 2)]

        # parrallelize crossover
        with concurrent.futures.ThreadPoolExecutor() as executor:
            offspring = executor.map(lambda x: self.population_crossover(x[0], x[1]), parents)
            offspring = list(offspring)
            for offspring1, offspring2 in offspring:
                offspring1_fitness = self.population_fitness_function.evaluate(offspring1, adversary_sample)
                offspring2_fitness = self.population_fitness_function.evaluate(offspring2, adversary_sample)

                offspring1 = self.population_mutation(offspring1, offspring1_fitness, generation, self.num_generations)
                offspring2 = self.population_mutation(offspring2, offspring2_fitness, generation, self.num_generations)
                new_population.extend([offspring1, offspring2])
                new_population_fitnesses.extend([offspring1_fitness, offspring2_fitness])

        

        new_population.extend(island)
        new_population_fitnesses.extend(raw_fitnesses)
        
        self.best_pop_fitness = max(self.best_pop_fitness, max(shared_fitnesses))
        new_island = self.population_survivor_selection.select(new_population, new_population_fitnesses, self.population_size // self.num_islands)

        if len(new_island) != island_len:
            logging.error(f"Island size mismatch: {len(new_island)} != {island_len}")

        return shared_fitnesses


    def population_evolve_islands(self, generation):
        total_fitnesses = []
        
        # run the evolution on each island in parallel
        with concurrent.futures.ThreadPoolExecutor() as executor:
            fitnesses = executor.map(lambda x: self.evolve_population_island(x, generation), self.population_islands)
            for f in fitnesses:
                total_fitnesses.extend(f)
        
        return total_fitnesses
        
    def adversary_evolve_island(self, island, generation):
        new_population = []
        new_population_fitnesses = []

        population_sample = self.sample_population_islands(self.population_sample_size)
        raw_fitnesses = self.adversary_evaluate_fitness(island, population_sample)

        if self.adversary_fitness_sharing is not None:
            shared_fitnesses = self.adversary_fitness_sharing.apply_sharing(island, raw_fitnesses)
        else:
            shared_fitnesses = raw_fitnesses

        parents = self.adversary_selection(island, shared_fitnesses, 2*len(island))
        for i in range(0, len(parents), 2):
            offspring1, offspring2 = self.adversary_crossover(parents[i], parents[i+1])
            offspring1_fitness = self.adversary_fitness_function.evaluate(offspring1, population_sample)
            offspring2_fitness = self.adversary_fitness_function.evaluate(offspring2, population_sample)

            offspring1 = self.adversary_mutation(offspring1, offspring1_fitness, generation, self.num_generations)
            offspring2 = self.adversary_mutation(offspring2, offspring2_fitness, generation, self.num_generations)
            new_population.extend([offspring1, offspring2])
            new_population_fitnesses.extend([offspring1_fitness, offspring2_fitness])

        self.best_adv_fitness = max(self.best_adv_fitness, max(shared_fitnesses))
        new_island = self.adversary_survivor_selection.select(new_population, new_population_fitnesses, self.adversary_population_size // self.num_islands)

        if len(new_island) != len(island):
            logging.error(f"Island size mismatch: {len(new_island)} != {len(island)}")

        return shared_fitnesses

    def adversary_evolve_islands(self, generation):
        total_fitnesses = []
        
        # run the evolution on each island in parallel
        with concurrent.futures.ThreadPoolExecutor() as executor:
            fitnesses = executor.map(lambda x: self.adversary_evolve_island(x, generation), self.adversary_islands)
            for f in fitnesses:
                total_fitnesses.extend(f)
            
        return total_fitnesses
    


    def evolve(self):
        self.current_generation = 0
        self.best_pop_fitness, self.best_adv_fitness = float('inf'), float('inf')
        self.start_time = time.time()
        for generation in range(self.num_generations):
            logging.info(f"Generation {generation}/{self.num_generations} - elapsed time: {time.time() - self.start_time}")
            self.current_generation = generation

            population_fitnesses = self.population_evolve_islands(generation)
            adversary_fitnesses = self.adversary_evolve_islands(generation)

            if generation % self.migration_rate == 0:
                self.population_migrate()
                self.adversary_migrate()

            self.population_fitnesses.append(population_fitnesses)
            self.adversary_fitnesses.append(adversary_fitnesses)

        entire_population = [ind for island in self.population_islands for ind in island]
        entire_adversary_population = [ind for island in self.adversary_islands for ind in island]

        population_fitnesses = self.population_evaluate_fitness(entire_population, entire_adversary_population)
        adversary_fitnesses = self.adversary_evaluate_fitness(entire_adversary_population, entire_population)

        pop_best_solution, pop_best_fitness = max(zip(entire_population, population_fitnesses), key=lambda x: x[1])
        adv_best_solution, adv_best_fitness = max(zip(entire_adversary_population, adversary_fitnesses), key=lambda x: x[1])

        _, perc = self.population_fitness_function.get_performance(pop_best_solution, entire_adversary_population)

        results = {
            'population_fitnesses': self.population_fitnesses,
            'adversary_fitnesses': self.adversary_fitnesses,
            'best_solution': pop_best_solution,
            'best_solution_fitness': pop_best_fitness,
            'best_adversary': adv_best_solution,
            'best_adversary_fitness': adv_best_fitness,
            'tests': entire_adversary_population,
            'performance': perc,
            'name': self.name
        }

        return results


    def sample_population_islands(self, num_samples):
        logging.debug(f"Sampling {num_samples} individuals from population islands")
        total_population = [ind for island in self.population_islands for ind in island]
        logging.debug(f"Total population size: {len(total_population)}")
        logging.debug(f"Some samples: {total_population[:5]}")
        samples = random.sample(total_population, num_samples)
        logging.debug(f"Sampled individuals: {samples}")
        return samples

    def sample_adversary_islands(self, num_samples):
        logging.debug(f"Sampling {num_samples} individuals from adversary islands")
        total_adversary_population = [ind for island in self.adversary_islands for ind in island]
        logging.debug(f"Total adversary population size: {len(total_adversary_population)}")
        logging.debug(f"Some samples: {total_adversary_population[:5]}")
        samples = random.sample(total_adversary_population, num_samples)
        logging.debug(f"Sampled individuals: {samples}")
        return samples


