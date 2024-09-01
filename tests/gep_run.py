import random

from src.GA.GeneticAlgorithm import GeneticAlgorithm
from src.GA.parent_selection.ElitistSelection import ElitistSelection
from src.GA.survivor_selection.HybridSelection import HybridSelection
from src.GA.mutation_strategy.MutationStrategy import AllMutation

from src.GEP.GEP import GEP
from src.GEP.GEPCrossover import GEPCrossover
from src.GEP.GEPMutation import GEPMutation
from src.GEP.GEPFitness import GEPFitness
from src.GEP.GEPFactory import GEPFactory

fitness_size_factor = 0.01

target_data = [(1,5), (2,17), (3, 43), (4, 85), (5, 145)]
tail_attempts = 20
mutation_rate = 0.2
head_length = 10
error = 0.1

def check_correctness(individual: GEP) -> bool:
    for x, y in target_data:
        y_pred = GEP.evaluate_exp(individual.exp + individual.best_tail, x)
        if abs(y - y_pred) > error:
            return False
    return True


if __name__ == '__main__':

    factory = GEPFactory(head_length)

    config = {
        'name': 'gep',
        'fitness_function': GEPFitness(target_data, tail_attempts, fitness_size_factor),
        'population_size': 200,
        'num_generations': 100,
        'num_islands': 10,
        'migration_rate': 10,
        'parent_selection': ElitistSelection(),
        'crossover_operator': GEPCrossover(),
        'mutation_operator': GEPMutation(mutation_rate),
        'survivor_selection': HybridSelection(0.8,0.2),
        'mutation_strategy': AllMutation(),
        'generate_population': factory.generate_population,
        'fitness_sharing': None
    }

    genetic_algorithm = GeneticAlgorithm(config)


    res = genetic_algorithm.evolve()

    genetic_algorithm.plot_fitness(True)

    # prin the fitness history
    best_individual = res['best_solution']
    best_solution_fitness = res['best_solution_fitness']

    print(f'Best individual: {best_individual}')
    print(f'Best solution fitness: {best_solution_fitness}')

    for x, y in target_data:
        y_pred = GEP.evaluate_exp(best_individual.exp + best_individual.best_tail, x)
        print(f'x: {x}, y: {y}, y_pred: {y_pred}')


    genetic_algorithm.plot_fitness(True)
