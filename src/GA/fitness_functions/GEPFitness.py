
from .FitnessFunction import FitnessFunction

class GEPFitness(FitnessFunction):
    def __init__(self, target):
        self.target = target

    def evaluate(self, genome):
        return self.target - genome.evaluate()

