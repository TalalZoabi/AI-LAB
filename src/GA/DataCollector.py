import matplotlib.pyplot as plt
import numpy as np

class DataCollector:
    def __init__(self, global_min_fitness, global_max_fitness,
                  distance_method, 
                  distance_unit,
                  convergence_threshold=0.01, convergence_window=10):
        self.global_min_fitness = global_min_fitness
        self.global_max_fitness = global_max_fitness
        
        self.distance_method = distance_method
        self.distance_unit = distance_unit

        self.fitness_matrix = []
        self.runtimes = []
        self.diversities = []
        self.convergence_threshold = convergence_threshold
        self.convergence_window = convergence_window
        self.convergence_generation = None

    def collect(self, fitnesses, runtime, population):
        self.fitness_matrix.append(fitnesses)
        self.runtimes.append(runtime)
        self.diversities.append(self.calculate_diversity(population))
        if self.convergence_generation is None:
            self.check_convergence()

    def calculate_statistics(self):
        self.avg_fitnesses = [sum(gen) / len(gen) for gen in self.fitness_matrix]
        self.scaled_avg_fitnesses = [self.scale_fitness(sum(gen) / len(gen)) for gen in self.fitness_matrix]
        self.std_devs = [(sum((x - avg) ** 2 for x in gen) / len(gen)) ** 0.5 for gen, avg in zip(self.fitness_matrix, self.avg_fitnesses)]
        self.best_fitnesses = [max(gen) for gen in self.fitness_matrix]

    def scale_fitness(self, fitness):
        return (fitness - self.global_min_fitness) * 100 / (self.global_max_fitness - self.global_min_fitness)

    def calculate_diversity(self, population):
        distances = []
        for i in range(len(population)):
            for j in range(i + 1, len(population)):
                distances.append(self.distance_method(population[i], population[j]))
        if distances:
            return sum(distances) / len(distances)
        else:
            return 0

    def check_convergence(self):
        if len(self.fitness_matrix) >= self.convergence_window:
            recent_avg_fitnesses = [sum(gen) / len(gen) for gen in self.fitness_matrix[-self.convergence_window:]]
            fitness_improvement = max(recent_avg_fitnesses) - min(recent_avg_fitnesses)
            if fitness_improvement < self.convergence_threshold:
                self.convergence_generation = len(self.fitness_matrix) - self.convergence_window

    def get_data(self):
        self.calculate_statistics()
        if not self.convergence_generation:
            self.convergence_generation = len(self.fitness_matrix)
        return {
            'avg_fitnesses': self.avg_fitnesses,
            'scaled_avg_fitnesses': self.scaled_avg_fitnesses,
            'std_devs': self.std_devs,
            'best_fitnesses': self.best_fitnesses,
            'runtimes': self.runtimes,
            'diversities': self.diversities,
            'convergence_generation': self.convergence_generation
        }


    def plot(self):
        self.calculate_statistics()
        generations = range(len(self.avg_fitnesses))

        plt.figure(figsize=(14, 7))

        # Average Fitness
        plt.subplot(2, 2, 1)
        plt.plot(generations, self.scaled_avg_fitnesses, label='Average Fitness')
        plt.xlabel('Generation')
        plt.ylabel('Fitness')
        plt.title('Average Fitness per Generation')
        plt.legend()

        # Best Fitness
        plt.subplot(2, 2, 2)
        plt.plot(generations, self.best_fitnesses, label='Best Fitness', color='green')
        plt.xlabel('Generation')
        plt.ylabel('Fitness')
        plt.title('Best Fitness per Generation')
        plt.legend()

        # Standard Deviation
        plt.subplot(2, 2, 3)
        plt.plot(generations, self.std_devs, label='Standard Deviation', color='red')
        plt.xlabel('Generation')
        plt.ylabel('Standard Deviation')
        plt.title('Standard Deviation of Fitness per Generation')
        plt.legend()

        # Average Runtime
        plt.subplot(2, 2, 4)
        plt.plot(generations, self.runtimes, label='Average Runtime', color='purple')
        plt.xlabel('Generation')
        plt.ylabel('Runtime (seconds)')
        plt.title('Average Runtime per Generation')
        plt.legend()

        plt.tight_layout()
        plt.show()

        plt.figure(figsize=(14, 7))

        # Genetic Diversity
        plt.subplot(1, 1, 1)
        plt.plot(generations, self.diversities, label='Genetic Diversity', color='blue')
        plt.xlabel('Generation')
        plt.ylabel(f'Diversity ({self.distance_unit}) ')
        plt.title('Genetic Diversity per Generation')
        plt.legend()

        plt.tight_layout()
        plt.show()

        if self.convergence_generation is not None:
            print(f"Convergence occurred at generation {self.convergence_generation}")



