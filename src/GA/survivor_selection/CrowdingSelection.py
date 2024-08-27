from .SurvivorSelectionMethod import SurvivorSelectionMethod

class CrowdingSelection(SurvivorSelectionMethod):
    def __init__(self, tournament_size, distance_func):
        self.tournament_size = tournament_size
        self.distance_func = distance_func

    def select(self, population, fitnesses, num_survivors):
        crowding_distances = []
        for i in range(len(population)):
            distances = []
            for j in range(len(population)):
                if i == j:
                    continue
                distances.append(self.distance_func(population[i], population[j]))
            distances = sorted(distances)
            crowding_distances.append(distances[self.tournament_size - 1])

        combined_scores = [(fitness, distance) for fitness, distance in zip(fitnesses, crowding_distances)]
        sorted_pop = sorted(zip(population, combined_scores), key=lambda x: (x[1][0], -x[1][1]), reverse=True)
        return [ind for ind, _ in sorted_pop[:num_survivors]]
