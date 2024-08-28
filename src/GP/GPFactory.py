import random

from .GP import GP


class GPFactory:

    def __init__(self, max_depth: int) -> None:
        self.max_depth = max_depth

    def generate_full_tree(self, depth):
        if depth == self.max_depth:
            return GP(random.choice([GP.A, GP.B]))
        else:
            operator = random.choice([GP.AND, GP.OR, GP.NOT])
            if operator == GP.NOT:
                return GP(operator, left=self.generate_full_tree(depth + 1))
            else:
                return GP(operator, left=self.generate_full_tree(depth + 1), right=self.generate_full_tree(depth + 1))

    def generate_grow_tree(self, depth):
        if depth == self.max_depth or (depth > 0 and random.random() > 0.5):
            return GP(random.choice([GP.A, GP.B]))
        else:
            operator = random.choice([GP.AND, GP.OR, GP.NOT])
            if operator == GP.NOT:
                return GP(operator, left=self.generate_grow_tree(depth + 1))
            else:
                return GP(operator, left=self.generate_grow_tree(depth + 1), right=self.generate_grow_tree(depth + 1))

    def get_random_terminal(self):
        return random.choice([GP.A, GP.B])
    
    def get_random_operator(self):
        return random.choice([GP.AND, GP.OR, GP.NOT])

    def generate_individual(self, method):
        if method == 'full':
            return self.generate_full_tree(0)
        elif method == 'grow':
            return self.generate_grow_tree(0)
        else:
            raise ValueError("Invalid method: choose 'full' or 'grow'")



