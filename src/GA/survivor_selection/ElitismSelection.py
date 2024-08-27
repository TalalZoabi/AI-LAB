from  .SurvivorSelectionMethod import SurvivorSelectionMethod

class ElitismSelection(SurvivorSelectionMethod):
    def select(self, population, fitnesses, num_survivors, ages=None):
        sorted_population = [x for _, x in sorted(zip(fitnesses, population), key=lambda x: x[0], reverse=True)]
        return sorted_population[:num_survivors]
