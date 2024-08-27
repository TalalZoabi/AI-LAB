import random

from .MutationOperator import MutationOperator

class InversionMutation(MutationOperator):
    def mutate(self, candidate):
        candidate = list(candidate)  # Convert string to list for mutability
        start, end = sorted(random.sample(range(len(candidate)), 2))
        candidate[start:end] = reversed(candidate[start:end])
        return ''.join(candidate)  # Convert back to string
