from .FitnessFunction import FitnessFunction

class MatchFitness(FitnessFunction):
    def __init__(self, target_string):
        self.target_string = target_string

    def evaluate(self, individual):
        if len(individual) != len(self.target_string):
            raise ValueError("Individual length must match target string length.")
        
        matches = sum(1 for i, j in zip(individual, self.target_string) if i == j)
        return matches
    
    def max_fitness(self, *args, **kwargs):
        return len(self.target_string)
    
    def min_fitness(self, *args, **kwargs):
        return 0
    
