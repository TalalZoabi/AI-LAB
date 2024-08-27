import random

class CVRPMutation:
    def __init__(self, method):
        self.method = method

    def mutate(self, individual):
        if self.method == 'swap':
            return self.swap_mutation(individual)
        elif self.method == 'insertion':
            return self.insertion_mutation(individual)
        elif self.method == 'inversion':
            return self.inversion_mutation(individual)
        else:
            raise ValueError("Unsupported mutation method.")

    def swap_mutation(self, individual):
        idx1, idx2 = random.sample(range(1, len(individual) - 1), 2)  # Avoid depots
        individual[idx1], individual[idx2] = individual[idx2], individual[idx1]
        return individual

    def insertion_mutation(self, individual):
        idx1, idx2 = random.sample(range(1, len(individual) - 1), 2)  # Avoid depots
        gene = individual.pop(idx1)
        individual.insert(idx2, gene)
        return individual

    def inversion_mutation(self, individual):
        idx1, idx2 = sorted(random.sample(range(1, len(individual) - 1), 2))  # Avoid depots
        individual[idx1:idx2] = reversed(individual[idx1:idx2])
        return individual