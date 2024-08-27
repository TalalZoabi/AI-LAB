import random

from .SurvivorSelectionMethod import SurvivorSelectionMethod



class EliteTournamentSelection(SurvivorSelectionMethod):
    def __init__(self, tournament_size, elite_size):
        self.tournament_size = tournament_size
        self.elite_size = elite_size


    def select(self, population, fitnesses, num_survivors):
        selected_survivors = []

        elitist = sorted(zip(population, fitnesses), key=lambda x: x[1], reverse=True)
        
        elite = [x[0] for x in elitist[:self.elite_size]]
        
        selected_survivors.extend(elite)
        for _ in range(num_survivors - self.elite_size):
            tournament = random.sample(list(zip(population, fitnesses)), self.tournament_size)
            winner = max(tournament, key=lambda x: x[1])[0]
            selected_survivors.append(winner)
        return selected_survivors

