import random

from .MutationOperator import MutationOperator


class BinPackingInversionMutation(MutationOperator):
    def mutate(self, candidate):
        candidate = list(candidate)  # Convert to list for mutability
        start, end = sorted(random.sample(range(len(candidate)), 2))
        candidate[start:end] = reversed(candidate[start:end])
        return candidate
