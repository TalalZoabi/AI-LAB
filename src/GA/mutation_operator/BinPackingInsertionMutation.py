import random

from .MutationOperator import MutationOperator




class BinPackingInsertionMutation(MutationOperator):
    def mutate(self, candidate):
        candidate = list(candidate)  # Convert to list for mutability
        idx1, idx2 = random.sample(range(len(candidate)), 2)
        item = candidate.pop(idx1)
        candidate.insert(idx2, item)
        return candidate


