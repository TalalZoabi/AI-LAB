from .SurvivorSelectionMethod import SurvivorSelectionMethod


class AgingSelection(SurvivorSelectionMethod):
    def __init__(self, max_age):
        self.max_age = max_age

    def select(self, population, fitnesses, num_survivors, ages):
        # Separate individuals into young and adult groups
        young_individuals = [(pop, fit, age) for pop, fit, age in zip(population, fitnesses, ages) if age == 0]
        adult_individuals = [(pop, fit, age) for pop, fit, age in zip(population, fitnesses, ages) if 0 < age <= self.max_age]

        # Sort adults by fitness in descending order
        adult_individuals.sort(key=lambda x: x[1], reverse=True)
        
        # Initialize survivors with all young individuals
        survivors = young_individuals
        
        # Add adult individuals until reaching the desired number of survivors
        survivors += adult_individuals[:num_survivors - len(survivors)]
        
        # Extract the selected population and update ages
        selected_population = [x[0] for x in survivors[:num_survivors]]
        new_ages = [age + 1 for pop, age in zip(population, ages)]

        return selected_population, new_ages

