import random

from .MutationOperator import MutationOperator


class BinPackingScrambleMutation(MutationOperator):
    def mutate(self, candidate):
        candidate = list(candidate)  # Convert to list for mutability
        start, end = sorted(random.sample(range(len(candidate)), 2))
        sublist = candidate[start:end]
        random.shuffle(sublist)
        candidate[start:end] = sublist
        return candidate


