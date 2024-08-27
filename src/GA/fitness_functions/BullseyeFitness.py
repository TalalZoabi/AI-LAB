from .FitnessFunction import FitnessFunction

class BullseyeFitness(FitnessFunction):
    def __init__(self, target_string, bonus=100):
        self.target_string = target_string
        self.bonus = bonus

    def evaluate(self, individual):
        if len(individual) != len(self.target_string):
            raise ValueError("Individual length must match target string length.")
        
        if individual == self.target_string:
            return len(self.target_string) + self.bonus

        target_chars = list(self.target_string)
        matches = 0
        for char in individual:
            if char in target_chars:
                matches += 1
                target_chars.remove(char)
        
        return matches
    
    def max_fitness(self, *args, **kwargs):
        return len(self.target_string) + self.bonus
    
    def min_fitness(self, *args, **kwargs):
        return 0

