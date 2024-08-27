from .ParentSelectionMethod import ParentSelectionMethod


class ElitistSelection(ParentSelectionMethod):
    def __init__(self):
        pass

    def select(self, population, fitnesses, num_parents):
        sorted_population = [x for _, x in sorted(zip(fitnesses, population), key=lambda x: x[0], reverse=True)]
        selected_parents = sorted_population[:num_parents]
        return selected_parents

