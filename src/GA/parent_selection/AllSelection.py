
from .ParentSelectionMethod import ParentSelectionMethod

class AllSelection(ParentSelectionMethod):
    def select(self, population, fitnesses, num_parents):
        return population

