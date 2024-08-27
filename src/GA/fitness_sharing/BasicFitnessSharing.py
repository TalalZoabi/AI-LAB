from .FitnessSharing import FitnessSharing

class BasicFitnessSharing(FitnessSharing):
    def apply_sharing(self, population, raw_fitness):
        shared_fitness = [0] * len(population)
        for i, ind_i in enumerate(population):
            sharing_sum = sum(self.sharing_function(ind_i, ind_j) for ind_j in population)
            shared_fitness[i] = raw_fitness[i] / sharing_sum
        return shared_fitness

    def sharing_function(self, ind_i, ind_j):
        distance = self.distance_func(ind_i, ind_j)
        if distance < self.sigma_share:
            return 1 - (distance / self.sigma_share) ** self.alpha
        return 0



