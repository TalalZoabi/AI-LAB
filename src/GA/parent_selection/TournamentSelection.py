
import random
import logging
from .ParentSelectionMethod import ParentSelectionMethod


class TournamentSelection(ParentSelectionMethod):
    def __init__(self, tournament_size, probability_best=1.0):
        self.tournament_size = tournament_size
        self.probability_best = probability_best

    def select(self, population, fitnesses, num_parents):
        logger = logging.getLogger(__name__)
        selected_parents = []

        for i in range(num_parents):
            logger.debug(f"Selecting parent {i + 1}/{num_parents}")
            tournament = random.sample(list(zip(population, fitnesses)), self.tournament_size)
            tournament.sort(key=lambda x: x[1], reverse=True)
            
            if random.random() < self.probability_best:
                selected_parents.append(tournament[0][0])
            else:
                selected_parents.append(tournament[random.randint(1, self.tournament_size - 1)][0])
        return selected_parents
