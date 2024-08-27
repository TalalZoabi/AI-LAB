from .Crowding import Crowding


class DeterministicCrowding(Crowding):
    def apply_crowding(self, offspring, parents, fitness):
        new_population = []
        for o in offspring:
            similar_parent = min(parents, key=lambda p: self.distance_func(o, p))
            if fitness[o] > fitness[similar_parent]:
                new_population.append(o)
            else:
                new_population.append(similar_parent)
        return new_population

