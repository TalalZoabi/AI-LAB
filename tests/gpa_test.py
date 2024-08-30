import random




from src.GA.GeneticAlgorithm import GeneticAlgorithm
from src.GA.fitness_functions.GPAFitness import GPAFitness
from src.GA.parent_selection.ElitistSelection import ElitistSelection
from src.GA.survivor_selection.HybridSelection import HybridSelection
from src.GA.mutation_strategy.MutationStrategy import BasicMutation

from src.GPA.GPACrossover import GPACrossover
from src.GPA.GPABloat import GPABloat
from src.GPA.GPAMutation import GPAMutation
from src.GPA.GPAFactory import GPAFactory


fitness_lambda_penalty = 0.01

def target_function(x: float) -> float:
    return x*x + x + 1


error_range = 0.1
sample_size = 100

def check_correctness(individual) -> float:
    hits = 0
    for _ in range(sample_size):
        x = random.uniform(-1, 1)
        if abs(individual.evaluate(x) - target_function(x)) < error_range:
            hits += 1
    
    return hits/sample_size*100

if __name__ == '__main__':
    optimizer = GPABloat()


    config = {
        'name': 'test',
        'fitness_function': GPAFitness(fitness_lambda_penalty, opt_size=None, target_function=target_function, error_range=error_range, sample_size=sample_size),
        'population_size': 100,
        'num_generations': 100,
        'num_islands': 10,
        'migration_rate': 10,
        'parent_selection': ElitistSelection(),
        'crossover_operator': GPACrossover(optimizer),
        'mutation_operator': GPAMutation(optimizer),
        'survivor_selection': HybridSelection(0.8,0.2),
        'mutation_strategy': BasicMutation(0.3),
        'generate_population': GPAFactory.generate_population,
        'fitness_sharing': None
    }

    genetic_algorithm = GeneticAlgorithm(config)


    res = genetic_algorithm.evolve()

    best_individual = res['best_solution']
    best_solution_fitness = res['best_solution_fitness']

    print(f'Best individual: {best_individual}')
    print(f'Best solution fitness: {best_solution_fitness}')

    print(f'Correctness: {check_correctness(best_individual)}')


