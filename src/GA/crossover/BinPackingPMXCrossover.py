from .CrossoverOperator import CrossoverOperator


class BinPackingPMXCrossover(CrossoverOperator):
    def pmx_crossover(self, parent1, parent2):
        import random
        size = len(parent1)
        child = [None] * size
        start, end = sorted(random.sample(range(size), 2))

        # Copy the segment from parent1 to child
        for i in range(start, end):
            child[i] = parent1[i]

        # Map the rest of the positions from parent2 to child
        for i in range(start, end):
            if parent2[i] not in child[start:end]:
                pos = i
                while start <= pos < end:
                    pos = parent1.index(parent2[pos])
                child[pos] = parent2[i]

        # Fill in the remaining positions from parent2
        for i in range(size):
            if child[i] is None:
                child[i] = parent2[i]

        return child

    def crossover(self, parent1, parent2):
        offspring1 = self.pmx_crossover(parent1, parent2)
        offspring2 = self.pmx_crossover(parent2, parent1)
        return [offspring1, offspring2]
