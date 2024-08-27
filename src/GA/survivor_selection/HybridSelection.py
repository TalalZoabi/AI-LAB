import random
import logging
from .SurvivorSelectionMethod import SurvivorSelectionMethod


class HybridSelection(SurvivorSelectionMethod):
    def __init__(self, elitism_rate, random_rate):
        self.elitism_rate = elitism_rate
        self.random_rate = random_rate

    def select(self, population, fitnesses, num_survivors):
        logger = logging.getLogger(__name__)

        # Sort the population based on fitness (descending order)
        sorted_pop = sorted(zip(population, fitnesses), key=lambda x: x[1], reverse=True)
        
        # Determine the number of elites to select
        num_elites = int(self.elitism_rate * num_survivors)
        elites = [ind for ind, _ in sorted_pop[:num_elites]]
        
        # Prepare the remaining population
        remaining_pop = [ind for ind, _ in sorted_pop[num_elites:]]
        
        # Determine the number of random selections needed
        num_random = num_survivors - len(elites)

        if num_random < 0:
            logger.error(f"Elitism rate: {self.elitism_rate}")
            raise ValueError("Elitism rate too high")
        
        # Ensure we don't sample more than the available population
        if num_random > len(remaining_pop):
            num_random = len(remaining_pop)
        
        # Randomly select the remaining survivors
        random_selection = random.sample(remaining_pop, num_random)
        
        return elites + random_selection
