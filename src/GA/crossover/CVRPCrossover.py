import random
import logging
from .CrossoverOperator import CrossoverOperator

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class CVRPCrossover(CrossoverOperator):
    def __init__(self, method: str):
        self.method = method

    def crossover(self, parent1, parent2):
        
        if self.method == 'OX':
            child1 = self.order_crossover(parent1, parent2)
            child2 = self.order_crossover(parent2, parent1)
        elif self.method == 'PMX':
            child1 = self.partially_mapped_crossover(parent1, parent2)
            child2 = self.partially_mapped_crossover(parent2, parent1)
        elif self.method == 'CX':
            child1 = self.cycle_crossover(parent1, parent2)
            child2 = self.cycle_crossover(parent2, parent1)
        else:
            raise ValueError("Unsupported crossover method.")
        
        # Validate children
        if not self.validate_child(child1) or not self.validate_child(child2):
            return [parent1, parent2]
        
        return [child1, child2]

    # Order Crossover (OX)
    def order_crossover(self, parent1, parent2):
        size1 = len(parent1)
        size2 = len(parent2)
        size = min(size1, size2)  # Use the smaller size to avoid index out of range errors
        start, end = sorted(random.sample(range(1, size - 1), 2))  # Ensure we don't crossover the depot
        
        
        child = [None] * size1
        child[start:end] = parent1[start:end]
        
        
        parent2_idx = 1
        for i in range(1, size1 - 1):
            if child[i] is None:
                while parent2_idx < size2 and (parent2[parent2_idx] in child or parent2[parent2_idx] == 0):
                    parent2_idx += 1
                    if parent2_idx >= size2:
                        break
                if parent2_idx < size2:
                    child[i] = parent2[parent2_idx]
                    parent2_idx += 1

        # Fill remaining None values with elements from parent1 or parent2
        remaining_elements = [x for x in parent1 if x not in child and x != 0] + \
                             [x for x in parent2 if x not in child and x != 0]
        remaining_idx = 0
        for i in range(1, size1 - 1):
            if child[i] is None and remaining_idx < len(remaining_elements):
                child[i] = remaining_elements[remaining_idx]
                remaining_idx += 1

        # Ensure the child has valid routes with depots at correct positions
        child[0] = 0
        child[-1] = 0


        return child

    # Partially Mapped Crossover (PMX)
    def partially_mapped_crossover(self, parent1, parent2):
        size = len(parent1)
        start, end = sorted(random.sample(range(1, size - 1), 2))  # Ensure we don't crossover the depot
        
        
        child = [None] * size
        child[start:end] = parent1[start:end]
        
        mapping = {parent1[i]: parent2[i] for i in range(start, end)}
        
        for i in range(size):
            if i >= start and i < end:
                continue
            candidate = parent2[i]
            while candidate in mapping:
                candidate = mapping[candidate]
            child[i] = candidate
        
        # Ensure the child has valid routes with depots at correct positions
        child[0] = 0
        child[-1] = 0


        return child

    # Cycle Crossover (CX)
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
                    start = parent1.index(parent2[start])
                cycle_num += 1
        
        for i in range(size):
            if cycles[i] % 2 == 1:
                child[i] = parent1[i]
            else:
                child[i] = parent2[i]
        
        # Ensure the child has valid routes with depots at correct positions
        child[0] = 0
        child[-1] = 0


        return child

    def validate_child(self, child):
        # Ensure no None values in the child
        if None in child:
            return False
        # Ensure the child starts and ends with the depot
        if child[0] != 0 or child[-1] != 0:
            return False
        return True