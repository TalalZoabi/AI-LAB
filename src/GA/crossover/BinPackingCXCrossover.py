from .CrossoverOperator import CrossoverOperator

class BinPackingCXCrossover(CrossoverOperator):
    def cycle_crossover(self, parent1, parent2):
        size = len(parent1)
        child = [None] * size
        cycles = [0] * size
        cycle_num = 1

        for i in range(size):
            if cycles[i] == 0:
                start = i
                while cycles[start] == 0:
                    cycles[start] = cycle_num
                    start_value = parent1[start]
                    if start_value in parent2:
                        start = parent2.index(start_value)
                    else:
                        break
                cycle_num += 1

        for i in range(size):
            if cycles[i] % 2 == 1:
                child[i] = parent1[i]
            else:
                child[i] = parent2[i]

        # Fill in any remaining None values with items from the other parent
        for i in range(size):
            if child[i] is None:
                if parent2[i] not in child:
                    child[i] = parent2[i]
                else:
                    child[i] = parent1[i]

        return child


    def crossover(self, parent1, parent2):
        offspring1 = self.cycle_crossover(parent1, parent2)
        offspring2 = self.cycle_crossover(parent2, parent1)
        return [offspring1, offspring2]
