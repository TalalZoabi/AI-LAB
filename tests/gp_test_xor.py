
from src.GA.GeneticAlgorithm import GeneticAlgorithm
from src.GA.fitness_functions.GPFitness import GPFitness
from src.GA.parent_selection.ElitistSelection import ElitistSelection
from src.GA.survivor_selection.HybridSelection import HybridSelection
from src.GA.mutation_strategy.MutationStrategy import BasicMutation

from src.GP.GPCrossover import GPCrossover
from src.GP.GPBloat import GPBloat
from src.GP.GPMutation import GPMutation
from src.GP.GPFactory import GPFactory


fitness_lambda_penalty = 0.7

def target_function(a, b):
    return a ^ b


def check_correctness(individual):
    for a in [True, False]:
        for b in [True, False]:
            if individual.evaluate(a, b) != target_function(a, b):
                print(f'Error for {a} and {b}')
                return False
    return True

optimizer = GPBloat()


config = {
    'name': 'gp_xor',
    'fitness_function': GPFitness(fitness_lambda_penalty, 7, target_function),
    'population_size': 200,
    'num_generations': 200,
    'num_islands': 10,
    'migration_rate': 10,
    'parent_selection': ElitistSelection(),
    'crossover_operator': GPCrossover(optimizer),
    'mutation_operator': GPMutation(optimizer),
    'survivor_selection': HybridSelection(0.8,0.2),
    'mutation_strategy': BasicMutation(0.1),
    'generate_population': GPFactory.generate_population,
    'fitness_sharing': None
}

if __name__ == '__main__':
    genetic_algorithm = GeneticAlgorithm(config)

    res = genetic_algorithm.evolve()

    best_individual = res['best_solution']

    genetic_algorithm.plot_fitness(True)

    print(f'Best individual: {best_individual}')

    print(f'Correctness: {check_correctness(best_individual)}')


