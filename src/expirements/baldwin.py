import random
import numpy as np
import matplotlib.pyplot as plt

class BaldwinExperiment:
    def __init__(self, target_length, population_size=1000, generations=50, learning_attempts=1000, mutation_rate=0.01, print_terminal=False):
        self.target_length = target_length
        self.population_size = population_size
        self.generations = generations
        self.learning_attempts = learning_attempts
        self.mutation_rate = mutation_rate
        self.print_terminal = print_terminal
        self.target = self.generate_target()
        self.population = self.initialize_population()
        self.data = {'incorrect': [], 'correct': [], 'learned': [], 'fitness': []}

    def generate_target(self):
        return [random.choice([0, 1, '?']) for _ in range(self.target_length)]

    def initialize_population(self):
        population = []
        for _ in range(self.population_size):
            individual = self.create_individual()
            population.append(individual)
        return population

    def create_individual(self):
        individual = ['?'] * self.target_length
        indices = list(range(self.target_length))
        random.shuffle(indices)

        # Set 50% random bits
        random_bits_indices = indices[:self.target_length // 2]
        for idx in random_bits_indices:
            individual[idx] = random.choice([0, 1])

        # Set 25% correct bits
        correct_bits_indices = indices[self.target_length // 2:self.target_length // 2 + self.target_length // 4]
        for idx in correct_bits_indices:
            if self.target[idx] != '?':
                individual[idx] = self.target[idx]
            else:
                individual[idx] = random.choice([0, 1])

        # Set 25% incorrect bits
        incorrect_bits_indices = indices[self.target_length // 2 + self.target_length // 4:]
        for idx in incorrect_bits_indices:
            if self.target[idx] != '?':
                individual[idx] = 1 - self.target[idx]
            else:
                individual[idx] = random.choice([0, 1])

        return individual

    def fitness(self, individual):
        correct = 0
        for i in range(self.target_length):
            if self.target[i] != '?' and individual[i] == self.target[i]:
                correct += 1
        return correct

    def local_search(self, individual):
        total_learnable_bits = individual.count('?')
        correct_learned_bits = 0

        for attempt in range(self.learning_attempts):
            candidate = individual[:]
            for i in range(self.target_length):
                if candidate[i] == '?':
                    candidate[i] = random.choice([0, 1])

            fitness_value = self.fitness(candidate)
            if fitness_value == self.target_length:
                unused_attempts = self.learning_attempts - attempt
                correct_learned_bits = sum(1 for i in range(self.target_length) if candidate[i] == self.target[i] and self.target[i] != '?')
                return candidate, unused_attempts, correct_learned_bits, total_learnable_bits

        correct_learned_bits = sum(1 for i in range(self.target_length) if individual[i] == self.target[i] and self.target[i] != '?')
        return individual, 0, correct_learned_bits, total_learnable_bits

    def fitness_with_learning(self, individual):
        _, unused_attempts, correct_learned_bits, total_learnable_bits = self.local_search(individual)
        fitness = 1 + (19 * unused_attempts / self.learning_attempts)
        return fitness, correct_learned_bits, total_learnable_bits

    def mutate(self, individual):
        for i in range(self.target_length):
            if random.random() < self.mutation_rate:
                individual[i] = random.choice([0, 1, '?'])  # Flip bit to 0, 1, or ?
        return individual

    def crossover(self, parent1, parent2):
        crossover_point = random.randint(0, self.target_length - 1)
        child1 = parent1[:crossover_point] + parent2[crossover_point:]
        child2 = parent2[:crossover_point] + parent1[crossover_point:]
        return child1, child2

    def selection(self, population, fitnesses):
        selected = random.choices(population, weights=fitnesses, k=self.population_size)
        return selected

    def run_experiment(self, with_learning=True):
        for generation in range(self.generations):
            new_population = []
            fitnesses = []
            total_correct_learned_bits = 0
            total_learnable_bits = 0

            for individual in self.population:
                if with_learning:
                    fitness, correct_learned_bits, learnable_bits = self.fitness_with_learning(individual)
                    total_correct_learned_bits += correct_learned_bits
                    total_learnable_bits += learnable_bits
                else:
                    fitness = self.fitness(individual)
                fitnesses.append(fitness)
                new_population.append(individual)

            self.population = self.selection(new_population, fitnesses)
            offspring = []
            for i in range(0, self.population_size, 2):
                parent1, parent2 = self.population[i], self.population[(i + 1) % self.population_size]
                child1, child2 = self.crossover(parent1, parent2)
                offspring.append(self.mutate(child1))
                offspring.append(self.mutate(child2))

            self.population = offspring[:self.population_size]
            self.collect_data(generation, total_correct_learned_bits, total_learnable_bits, fitnesses)
            if self.print_terminal:
                self.print_generation_stats(generation)

    def collect_data(self, generation, total_correct_learned_bits, total_learnable_bits, fitnesses):
        incorrect_positions = 0
        correct_positions = 0
        for individual in self.population:
            for i in range(self.target_length):
                if self.target[i] == '?':
                    continue
                if individual[i] == self.target[i]:
                    correct_positions += 1
                else:
                    incorrect_positions += 1

        total_positions = self.population_size * self.target_length
        self.data['incorrect'].append((incorrect_positions / total_positions) * 100)
        self.data['correct'].append((correct_positions / total_positions) * 100)
        if total_learnable_bits > 0:
            learned_bits_percentage = (total_correct_learned_bits / (total_learnable_bits * self.population_size)) * 100
        else:
            learned_bits_percentage = 0
        self.data['learned'].append(learned_bits_percentage)
        self.data['fitness'].append(np.mean(fitnesses))

    def print_generation_stats(self, generation):
        print(f"Generation {generation}:")
        print(f"  Incorrect Positions (%): {self.data['incorrect'][-1]}")
        print(f"  Correct Positions (%): {self.data['correct'][-1]}")
        print(f"  Learned Bits (%): {self.data['learned'][-1]}")
        print(f"  Average Fitness: {self.data['fitness'][-1]}")

    def plot_results(self, title):
        generations = range(self.generations)
        fig, ax = plt.subplots(4, 1, figsize=(12, 20))

        ax[0].plot(generations, self.data['incorrect'], label='Incorrect Positions (%)')
        ax[0].set_xlabel('Generations')
        ax[0].set_ylabel('Percentage')
        ax[0].set_title('Incorrect Positions Over Generations')
        ax[0].legend()

        ax[1].plot(generations, self.data['correct'], label='Correct Positions (%)')
        ax[1].set_xlabel('Generations')
        ax[1].set_ylabel('Percentage')
        ax[1].set_title('Correct Positions Over Generations')
        ax[1].legend()

        ax[2].plot(generations, self.data['learned'], label='Learned Bits (%)')
        ax[2].set_xlabel('Generations')
        ax[2].set_ylabel('Percentage')
        ax[2].set_title('Learned Bits Over Generations')
        ax[2].legend()

        ax[3].plot(generations, self.data['fitness'], label='Average Fitness')
        ax[3].set_xlabel('Generations')
        ax[3].set_ylabel('Fitness')
        ax[3].set_title('Average Fitness Over Generations')
        ax[3].legend()

        plt.suptitle(title)
        plt.tight_layout(rect=[0, 0, 1, 0.97])
        plt.savefig(f"{title.replace(' ', '_')}.png")
        plt.show()



# Run a sanity check to ensure everything works as expected
def sanity_check():
    experiment = BaldwinExperiment(target_length=20, population_size=1000, generations=50, learning_attempts=1000, mutation_rate=0.05, print_terminal=True)
    print("Running experiment with learning phase...")
    experiment.run_experiment(with_learning=True)
    experiment.plot_results("Results with Learning")

    # Print final results for verification
    print("\nFinal Results with Learning Phase:")
    print("Average Incorrect Positions:", np.mean(experiment.data['incorrect']))
    print("Average Correct Positions:", np.mean(experiment.data['correct']))
    print("Average Learned Bits:", np.mean(experiment.data['learned']))
    print("Average Fitness:", np.mean(experiment.data['fitness']))




    # Reset the experiment for the run without learning
    experiment.data = {'incorrect': [], 'correct': [], 'learned': [], 'fitness': []}
    experiment.population = experiment.initialize_population()

    print("Running experiment without learning phase...")
    experiment.run_experiment(with_learning=False)
    experiment.plot_results("Results without Learning")

    print("\nFinal Results without Learning Phase:")
    print("Average Incorrect Positions:", np.mean(experiment.data['incorrect']))
    print("Average Correct Positions:", np.mean(experiment.data['correct']))
    print("Average Learned Bits:", np.mean(experiment.data['learned']))
    print("Average Fitness:", np.mean(experiment.data['fitness']))

# Run the sanity check
sanity_check()
