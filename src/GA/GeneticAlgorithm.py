import random
import logging
import time
import concurrent.futures
from concurrent.futures import ProcessPoolExecutor



class GeneticAlgorithm:
    def __init__(self, config):
        # Configuration for the problem
        self.name = config['name']

        self.fitness_function = config['fitness_function']
        self.population_size = config['population_size']
        self.num_generations = config['num_generations']
        self.num_islands = config['num_islands']
        self.migration_rate = config['migration_rate']
        
        # Configuration for various methods
        self.parent_selection = config['parent_selection']
        
        self.crossover_operator = config['crossover_operator']
        self.mutation_operator = config['mutation_operator']
        self.survivor_selection = config['survivor_selection']
        self.mutation_strategy = config['mutation_strategy']

        # Create islands
        self.generate_population = config['generate_population'] 
        self.fitness_sharing = config['fitness_sharing']
        
        self.islands = self._initialize_islands()
    
        # collect data for plotting
        self.population_fitnesses = []
        self.best_fitness = float('-inf')


    def _initialize_islands(self):
        pop_islands = []
        for _ in range(self.num_islands):
            population = self.generate_population(self.population_size // self.num_islands)
            pop_islands.append(population)

        return pop_islands

    def _parent_selection(self, population, fitnesses, num_parents):
        return self.parent_selection.select(population, fitnesses, num_parents)


    def _offspring_mutation(self, individual, generation, fitness=None):
        if self.mutation_strategy.should_mutate({'individual_fitness': fitness, 'generation': generation, 'best_fitness': self.best_fitness}):
            return self.mutation_operator.mutate(individual, generation, self.num_generations)
        return individual
    
    def _migrate(self):
        for i in range(self.num_islands):
            target_island = (i + 1) % self.num_islands
            index = random.randint(0, len(self.islands[i]) - 1)
            migrant = self.islands[i].pop(index)
            self.islands[target_island].append(migrant)

    def _select_surviors(self, population, fitnesses, num_survivors):
        return self.survivor_selection.select(population, fitnesses, num_survivors)


    def _evaluate_fitness(self, population):
        # use parallelism
        fitnesses = []
        for individual in population:
            fitnesses.append(self.fitness_function.evaluate(individual))
        return fitnesses

    def _crossover(self, parents):
        offspring = []
        for parent1, parent2 in parents:
            children =  self.crossover_operator.crossover(parent1, parent2)
            offspring.append(children)
        return offspring

    def _evolve_island(self, island, generation):
        raw_fitnesses = self._evaluate_fitness(island)

        if self.fitness_sharing is not None:
            fitnesses = self._apply_fitness_sharing(raw_fitnesses)
        else:
            fitnesses = raw_fitnesses

        parents = self._parent_selection(island, fitnesses, 2*len(island))
        parents = [(parents[i], parents[i+1]) for i in range(0, len(parents), 2)]

        offspring = self._crossover(parents)

        # flatten offspring
        offspring = [ind for pair in offspring for ind in pair]
        offspring = [self._offspring_mutation(ind, generation) for ind in offspring]

        offspring_fitnesses = self._evaluate_fitness(offspring)
        total_population = island + offspring
        total_fitnesses = fitnesses + offspring_fitnesses
        survivors = self._select_surviors(total_population, total_fitnesses, len(island))

        return survivors



    def evolve_generation(self, generation):
        logging.info(f'Generation {generation}')

        with ProcessPoolExecutor() as executor:
            futures = [executor.submit(self._evolve_island, island, generation) for island in self.islands]
            self.islands = [future.result() for future in futures]

        if generation % self.migration_rate == 0:
            self._migrate()

    def evolve(self):
        self.current_generation = 0
        self.best_pop_fitness = float('inf')
        self.start_time = time.time()
        
        print("Starting run")
        for generation in range(self.num_generations):
            print(f"Generation {generation} - {generation/self.num_generations*100:.2f}% complete")
            self.evolve_generation(generation)

        print("Finished run")
        print("Time taken: ", time.time() - self.start_time)


        entire_population = [ind for island in self.islands for ind in island]
        population_fitnesses = self._evaluate_fitness(entire_population)
        best_solution, best_fitness = max(zip(entire_population, population_fitnesses), key=lambda x: x[1])


        results = {
            'population_fitnesses': population_fitnesses,
            'best_solution': best_solution,
            'best_solution_fitness': best_fitness,
            'name': self.name
        }

        return results



