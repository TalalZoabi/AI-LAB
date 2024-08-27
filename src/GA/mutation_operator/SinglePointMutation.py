import random
import string

from .MutationOperator import MutationOperator


class SinglePointMutation(MutationOperator):
    def mutate(self, candidate, *args, **kwargs):
        candidate = list(candidate)  # Convert string to list for mutability
        idx = random.randint(0, len(candidate) - 1)
        candidate[idx] = random.choice(string.printable)
        return ''.join(candidate)  # Convert back to string


