import random

from .SurvivorSelectionMethod import SurvivorSelectionMethod



class TournamentSelection(SurvivorSelectionMethod):
    def __init__(self, tournament_size):
        self.tournament_size = tournament_size

    def select(self, population, fitnesses, num_survivors):
        selected_survivors = []
        for _ in range(num_survivors):
            tournament = random.sample(list(zip(population, fitnesses)), self.tournament_size)
            winner = max(tournament, key=lambda x: x[1])[0]
            selected_survivors.append(winner)
        return selected_survivors

