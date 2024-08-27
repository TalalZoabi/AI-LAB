



# Fitness functions
from ..GA.fitness_functions.SortingNetworksFitness import SortingNetworksSimpleFitness, AdversarySimpleFitness, SortingNetworksComplexFitness, AdversaryComplexFitness


# Parent selection
from ..GA.parent_selection import TournamentSelection, ElitistSelection

# Crossover operators
from ..GA.crossover.SortingNetworksCrossover import SortingNetworksCrossover
from ..GA.crossover.SimpleCrossover import SimpleCrossover
from ..GA.crossover.UniformCrossover import UniformCrossover
from ..GA.crossover.SinglePointCrossover import SinglePointCrossover
from ..GA.crossover.TwoPointCrossover import TwoPointCrossover
from ..GA.crossover.ArithmeticCrossover import ArithmeticCrossover

# Mutation operators
from ..GA.mutation_operator.SimpleMutation import SimpleMutation
from ..GA.mutation_operator.SortingNetworksMutation import SortingNetworksMutation
from ..GA.mutation_operator.DecayMutation import DecayMutation

# Mutation strategies
from ..GA.mutation_strategy.MutationStrategy import BasicMutation

# Survivor selection
from ..GA.survivor_selection.ElitismSelection import ElitismSelection as SurvivorElitismSelection
from ..GA.survivor_selection.EliteTournamentSelection import EliteTournamentSelection
from ..GA.survivor_selection.HybridSelection import HybridSelection
from ..GA.survivor_selection.CrowdingSelection import CrowdingSelection

# Fitness sharing
from ..GA.fitness_sharing.BasicFitnessSharing import BasicFitnessSharing

# Sorting Networks problem
from src.problems.SortingNetworks import SortingNetworks

from ..utils.compare import compare_comparrisons


def get_k6_configurations():
    MAX_INDEX = 6  # Number of inputs to the sorting network (k=6)
    sn = SortingNetworks(MAX_INDEX, 2, 100, -100, 100)


    # Basic template for configurations
    base_config = {
        'population_size': 1000,
        'adversary_population_size': 200,
        'num_generations': 1000,
        'num_islands': 10,
        'migration_rate': 10,  # Set a reasonable migration rate to avoid division by zero
        'population_mutation_strategy': BasicMutation(0.4),
        'adversary_mutation_strategy': BasicMutation(0.3),
        'generate_individual': sn.create_individual,
        'generate_adversary_individual': sn.create_adversarial_individual,
        'population_parent_selection': TournamentSelection(5, 0.3),
        'adversary_parent_selection': ElitistSelection(),
        'population_fitness_sharing': None,
        'adversary_fitness_sharing': None
    }
    
    configurations = []

    # 1. SimpleFitness with SimpleMutation and SortingNetworksMutation (Baseline)
    configurations.append({
        **base_config,
        'name': 'SimpleFitness_SimpleMutation_SortingNetworksMutation',
        'population_fitness_function': SortingNetworksSimpleFitness(100.0, 0.1),
        'adversary_fitness_function': AdversarySimpleFitness(),
        'population_mutation_operator': SortingNetworksMutation(MAX_INDEX),
        'adversary_mutation_operator': DecayMutation(20.0),
        'population_crossover_operator': SortingNetworksCrossover(),
        'adversary_crossover_operator': SimpleCrossover(),
        'population_survivor_selection': EliteTournamentSelection(10, 50),
        'adversary_survivor_selection': SurvivorElitismSelection(),
        'population_sample_size': 3,
        'adversary_sample_size': 3,
    })

    # 2. Large Population Size vs Small Adversary Population Size
    configurations.append({
        **base_config,
        'name': 'LargePop_SmallAdvPop',
        'population_fitness_function': SortingNetworksComplexFitness(3.0, 1.0),
        'adversary_fitness_function': AdversaryComplexFitness(),
        'population_size': 1500,  # Larger population size
        'adversary_population_size': 100,  # Smaller adversary population size
        'population_mutation_operator': SortingNetworksMutation(MAX_INDEX),
        'adversary_mutation_operator': SimpleMutation(20.0),
        'population_crossover_operator': SinglePointCrossover(),
        'adversary_crossover_operator': SimpleCrossover(),
        'population_survivor_selection': HybridSelection(0.3, 0.6),
        'adversary_survivor_selection': SurvivorElitismSelection(),
        'population_sample_size': 5,
        'adversary_sample_size': 3,
    })

    # 3. Similar Population Size vs Adversary Population Size
    configurations.append({
        **base_config,
        'name': 'SimilarPopSize',
        'population_fitness_function': SortingNetworksComplexFitness(3.0, 1.0),
        'adversary_fitness_function': AdversaryComplexFitness(),
        'population_size': 500,  # Population size similar to adversary
        'adversary_population_size': 500,  # Equal population size
        'population_mutation_operator': SortingNetworksMutation(MAX_INDEX),
        'adversary_mutation_operator': SimpleMutation(0.7),
        'population_crossover_operator': TwoPointCrossover(),
        'adversary_crossover_operator': ArithmeticCrossover(),
        'population_survivor_selection': HybridSelection(0.5, 0.5),
        'adversary_survivor_selection': SurvivorElitismSelection(),
        'population_sample_size': 3,
        'adversary_sample_size': 3,
    })

    # 4. Small Population Size vs Large Adversary Population Size
    configurations.append({
        **base_config,
        'name': 'SmallPop_LargeAdvPop',
        'population_fitness_function': SortingNetworksComplexFitness(3.0, 1.0),
        'adversary_fitness_function': AdversaryComplexFitness(),
        'population_size': 100,  # Smaller population size
        'adversary_population_size': 1500,  # Larger adversary population size
        'population_mutation_operator': SortingNetworksMutation(MAX_INDEX),
        'adversary_mutation_operator': SimpleMutation(20.0),
        'population_crossover_operator': SortingNetworksCrossover(),
        'adversary_crossover_operator': SimpleCrossover(),
        'population_survivor_selection': EliteTournamentSelection(5, 5),
        'adversary_survivor_selection': SurvivorElitismSelection(),
        'population_sample_size': 3,
        'adversary_sample_size': 5,
    })

    # 5. Impact of Large Sample Sizes
    configurations.append({
        **base_config,
        'name': 'LargeSampleSizes',
        'population_fitness_function': SortingNetworksSimpleFitness(100.0, 0.1),
        'adversary_fitness_function': AdversarySimpleFitness(),
        'population_size': 1000,
        'adversary_population_size': 1000,
        'population_mutation_operator': SortingNetworksMutation(MAX_INDEX),
        'adversary_mutation_operator': SimpleMutation(20.0),
        'population_crossover_operator': TwoPointCrossover(),
        'adversary_crossover_operator': SimpleCrossover(),
        'population_survivor_selection': EliteTournamentSelection(5, 5),
        'adversary_survivor_selection': SurvivorElitismSelection(),
        'population_sample_size': 50,
        'adversary_sample_size': 50,
    })

    # 6. Impact of Small Sample Sizes
    configurations.append({
        **base_config,
        'name': 'SmallSampleSizes',
        'population_fitness_function': SortingNetworksComplexFitness(3.0, 1.0),
        'adversary_fitness_function': AdversaryComplexFitness(),
        'population_size': 1000,
        'adversary_population_size': 1000,
        'population_mutation_operator': SortingNetworksMutation(MAX_INDEX),
        'adversary_mutation_operator': SimpleMutation(20.0),
        'population_crossover_operator': SortingNetworksCrossover(),
        'adversary_crossover_operator': SimpleCrossover(),
        'population_survivor_selection': CrowdingSelection(tournament_size=5, distance_func=lambda x, y: sum(a != b for a, b in zip(x, y))),
        'adversary_survivor_selection': SurvivorElitismSelection(),
        'population_sample_size': 3,
        'adversary_sample_size': 3,
    })

    return configurations



def get_k16_configurations():
    MAX_INDEX = 16  # Number of inputs to the sorting network (k=16)
    sn = SortingNetworks(MAX_INDEX, 2, 100, -100, 100)


    # Basic template for configurations
    base_config = {
        'population_size': 1000,
        'adversary_population_size': 200,
        'num_generations': 1000,
        'num_islands': 10,
        'migration_rate': 10,  # Set a reasonable migration rate to avoid division by zero
        'population_mutation_strategy': BasicMutation(0.4),
        'adversary_mutation_strategy': BasicMutation(0.3),
        'generate_individual': sn.create_individual,
        'generate_adversary_individual': sn.create_adversarial_individual,
        'population_parent_selection': TournamentSelection(15, 0.3),
        'adversary_parent_selection': ElitistSelection(),
        'population_fitness_sharing': None,
        'adversary_fitness_sharing': None
    }
    
    configurations = []

    # 1. SimpleFitness with SimpleMutation and SortingNetworksMutation (Baseline)
    configurations.append({
        **base_config,
        'name': 'SimpleFitness_SimpleMutation_SortingNetworksMutation_k16',
        'population_fitness_function': SortingNetworksSimpleFitness(100.0, 0.1),
        'adversary_fitness_function': AdversarySimpleFitness(),
        'population_mutation_operator': SortingNetworksMutation(MAX_INDEX),
        'adversary_mutation_operator': SimpleMutation(20.0),
        'population_crossover_operator': SortingNetworksCrossover(),
        'adversary_crossover_operator': SimpleCrossover(),
        'population_survivor_selection': EliteTournamentSelection(10, 50),
        'adversary_survivor_selection': SurvivorElitismSelection(),
        'population_sample_size': 3,
        'adversary_sample_size': 3,
    })

    # 2. Large Population Size vs Small Adversary Population Size
    configurations.append({
        **base_config,
        'name': 'LargePop_SmallAdvPop_k16',
        'population_fitness_function': SortingNetworksComplexFitness(3.0, 1.0),
        'adversary_fitness_function': AdversaryComplexFitness(),
        'population_size': 1500,  # Larger population size
        'adversary_population_size': 100,  # Smaller adversary population size
        'population_mutation_operator': SortingNetworksMutation(MAX_INDEX),
        'adversary_mutation_operator': SimpleMutation(20.0),
        'population_crossover_operator': SinglePointCrossover(),
        'adversary_crossover_operator': SimpleCrossover(),
        'population_survivor_selection': HybridSelection(0.7, 0.3),
        'adversary_survivor_selection': SurvivorElitismSelection(),
        'population_sample_size': 5,
        'adversary_sample_size': 3,
    })

    # 3. Similar Population Size vs Adversary Population Size
    configurations.append({
        **base_config,
        'name': 'SimilarPopSize_k16',
        'population_fitness_function': SortingNetworksComplexFitness(3.0, 1.0),
        'adversary_fitness_function': AdversaryComplexFitness(),
        'population_size': 500,  # Population size similar to adversary
        'adversary_population_size': 500,  # Equal population size
        'population_mutation_operator': SortingNetworksMutation(MAX_INDEX),
        'adversary_mutation_operator': SimpleMutation(20.0),
        'population_crossover_operator': TwoPointCrossover(),
        'adversary_crossover_operator': ArithmeticCrossover(),
        'population_survivor_selection': CrowdingSelection(tournament_size=5, distance_func=lambda x, y: sum(a != b for a, b in zip(x, y))),
        'adversary_survivor_selection': SurvivorElitismSelection(),
        'population_sample_size': 3,
        'adversary_sample_size': 3,
    })

    # 4. Small Population Size vs Large Adversary Population Size
    configurations.append({
        **base_config,
        'name': 'SmallPop_LargeAdvPop_k16',
        'population_fitness_function': SortingNetworksComplexFitness(3.0, 1.0),
        'adversary_fitness_function': AdversaryComplexFitness(),
        'population_size': 100,  # Smaller population size
        'adversary_population_size': 1500,  # Larger adversary population size
        'population_mutation_operator': SortingNetworksMutation(MAX_INDEX),
        'adversary_mutation_operator': SimpleMutation(20.0),
        'population_crossover_operator': SortingNetworksCrossover(),
        'adversary_crossover_operator': SimpleCrossover(),
        'population_survivor_selection': EliteTournamentSelection(15, 50),
        'adversary_survivor_selection': SurvivorElitismSelection(),
        'population_sample_size': 3,
        'adversary_sample_size': 5,
    })

    # 5. Impact of Large Sample Sizes
    configurations.append({
        **base_config,
        'name': 'LargeSampleSizes_k16',
        'population_fitness_function': SortingNetworksSimpleFitness(100.0, 0.1),
        'adversary_fitness_function': AdversarySimpleFitness(),
        'population_size': 1000,
        'adversary_population_size': 1000,
        'population_mutation_operator': SortingNetworksMutation(MAX_INDEX),
        'adversary_mutation_operator': SimpleMutation(20.0),
        'population_crossover_operator': SortingNetworksCrossover(),
        'adversary_crossover_operator': SimpleCrossover(),
        'population_survivor_selection': EliteTournamentSelection(15, 50),
        'adversary_survivor_selection': SurvivorElitismSelection(),
        'population_sample_size': 50,
        'adversary_sample_size': 50,
    })

    # 6. Impact of Small Sample Sizes
    configurations.append({
        **base_config,
        'name': 'SmallSampleSizes_k16',
        'population_fitness_function': SortingNetworksComplexFitness(3.0, 1.0),
        'adversary_fitness_function': AdversaryComplexFitness(),
        'population_size': 1000,
        'adversary_population_size': 1000,
        'population_mutation_operator': SortingNetworksMutation(MAX_INDEX),
        'adversary_mutation_operator': SimpleMutation(20.0),
        'population_crossover_operator': SortingNetworksCrossover(),
        'adversary_crossover_operator': SimpleCrossover(),
        'population_survivor_selection': CrowdingSelection(tournament_size=5, distance_func=lambda x, y: sum(a != b for a, b in zip(x, y))),
        'adversary_survivor_selection': SurvivorElitismSelection(),
        'population_sample_size': 10,
        'adversary_sample_size': 10,
    })

    return configurations




