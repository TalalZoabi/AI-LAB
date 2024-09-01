import random
import logging
import time
import matplotlib.pyplot as plt
from concurrent.futures import ProcessPoolExecutor
import numpy as np

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

        # Data structure to store fitness history (numpy array) of size (num_islands, num_generations, population_size)
        self.island_fitness_history = np.zeros((self.num_islands, self.num_generations, self.population_size // self.num_islands))

    
        # Track the best fitness observed
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

    def _select_survivors(self, population, fitnesses, num_survivors):
        return self.survivor_selection.select(population, fitnesses, num_survivors)

    def _evaluate_fitness(self, population):
        fitnesses = []
        for individual in population:
            fitnesses.append(self.fitness_function.evaluate(individual))
        return fitnesses

    def _crossover(self, parents):
        offspring = []
        for parent1, parent2 in parents:
            child1, child2 = self.crossover_operator.crossover(parent1, parent2)
            offspring.append(child1)
            offspring.append(child2)
        return offspring

    def _evolve_island(self, island, generation):
        raw_fitnesses = self._evaluate_fitness(island)        

        if self.fitness_sharing is not None:
            fitnesses = self._apply_fitness_sharing(raw_fitnesses)
        else:
            fitnesses = raw_fitnesses

        parents = self._parent_selection(island, fitnesses, 2 * len(island))
        parents = [(parents[i], parents[i + 1]) for i in range(0, len(parents), 2)]

        offspring = self._crossover(parents)

        # Flatten offspring
        offspring = [self._offspring_mutation(ind, generation) for ind in offspring]

        offspring_fitnesses = self._evaluate_fitness(offspring)
        total_population = island + offspring
        total_fitnesses = fitnesses + offspring_fitnesses
        survivors = self._select_survivors(total_population, total_fitnesses, len(island))

        return survivors, raw_fitnesses

    def evolve_generation(self, generation):
        logging.info(f'Generation {generation}')

        with ProcessPoolExecutor() as executor:
            futures = [executor.submit(self._evolve_island, self.islands[i], generation) for i in range(len(self.islands))]
            res = [future.result() for future in futures]

        for i, (survivors, raw_fitnesses) in enumerate(res):
            self.islands[i] = survivors
            self.island_fitness_history[i][generation] = raw_fitnesses

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


    def plot_fitness(self, save=False):
        num_generations = self.num_generations
        avg_fitness_per_gen = []
        fitness_variance_per_gen = []
        best_fitness_per_gen = []
        
        for gen in range(num_generations):
            fitnesses_across_islands = [self.island_fitness_history[i][gen] for i in range(self.num_islands)]
            
            # Flatten the list of fitnesses across islands for this generation
            all_fitnesses = [fitness for island_fitness in fitnesses_across_islands for fitness in island_fitness]
            
            avg_fitness_per_gen.append(np.mean(all_fitnesses))
            fitness_variance_per_gen.append(np.var(all_fitnesses))
            best_fitness_per_gen.append(max(all_fitnesses))

        # Create a single figure with multiple subplots
        fig, axs = plt.subplots(2, 2, figsize=(14, 10))
        
        # Plot Average Fitness per Generation
        axs[0, 0].plot(avg_fitness_per_gen, label='Average Fitness', color='blue')
        axs[0, 0].set_title('Average Fitness per Generation')
        axs[0, 0].set_xlabel('Generation')
        axs[0, 0].set_ylabel('Average Fitness')
        axs[0, 0].legend()
        axs[0, 0].grid(True)

        # Plot Fitness Variance per Generation
        axs[0, 1].plot(fitness_variance_per_gen, label='Fitness Variance', color='orange')
        axs[0, 1].set_title('Fitness Variance per Generation')
        axs[0, 1].set_xlabel('Generation')
        axs[0, 1].set_ylabel('Fitness Variance')
        axs[0, 1].legend()
        axs[0, 1].grid(True)

        # Plot Best Fitness per Generation
        axs[1, 0].plot(best_fitness_per_gen, label='Best Fitness', color='green')
        axs[1, 0].set_title('Best Fitness per Generation')
        axs[1, 0].set_xlabel('Generation')
        axs[1, 0].set_ylabel('Best Fitness')
        axs[1, 0].legend()
        axs[1, 0].grid(True)

        # Hide the fourth subplot (bottom-right) as it's not needed
        axs[1, 1].axis('off')

        # Adjust layout
        plt.tight_layout()
        
        # Show the plot
        plt.show()

        if save:
            fig.savefig(f'{self.name}_fitness_summary_plot.png')

