import random


from .GP import GP


class GPFactory:
    @staticmethod
    def generate_full_tree(depth, max_depth):
        if depth == max_depth:
            return GP(random.choice([GP.A, GP.B]))
        else:
            operator = random.choice([GP.AND, GP.OR, GP.NOT])
            if operator == GP.NOT:
                return GP(operator, left=GPFactory.generate_full_tree(depth + 1, max_depth))
            else:
                return GP(operator, left=GPFactory.generate_full_tree(depth + 1, max_depth), right=GPFactory.generate_full_tree(depth + 1, max_depth))

    @staticmethod
    def generate_grow_tree(depth, max_depth):
        if depth == max_depth or (depth > 0 and random.random() > 0.5):
            return GP(random.choice([GP.A, GP.B]))
        else:
            operator = random.choice([GP.AND, GP.OR, GP.NOT])
            if operator == GP.NOT:
                return GP(operator, left=GPFactory.generate_grow_tree(depth + 1, max_depth))
            else:
                return GP(operator, left=GPFactory.generate_grow_tree(depth + 1, max_depth), right=GPFactory.generate_grow_tree(depth + 1, max_depth))

    @staticmethod
    def get_random_terminal():
        return random.choice([GP.A, GP.B])
    
    @staticmethod
    def get_random_operator():
        return random.choice([GP.AND, GP.OR, GP.NOT])

    @staticmethod
    def generate_individual(method, max_depth):
        if method == 'full':
            return GPFactory.generate_full_tree(0, max_depth)
        elif method == 'grow':
            return GPFactory.generate_grow_tree(0, max_depth)
        else:
            raise ValueError("Invalid method: choose 'full' or 'grow'")



