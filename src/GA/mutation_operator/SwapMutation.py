import random

from .MutationOperator import MutationOperator


class SwapMutation(MutationOperator):
    def mutate(self, candidate):
        candidate = list(candidate)  # Convert string to list for mutability
        idx1, idx2 = random.sample(range(len(candidate)), 2)
        candidate[idx1], candidate[idx2] = candidate[idx2], candidate[idx1]
        return ''.join(candidate)  # Convert back to string
