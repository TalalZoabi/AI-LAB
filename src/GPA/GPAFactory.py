import random
import logging
from .GPA import GPA
from .GPABloat import GPABloat

class GPAFactory:
    @staticmethod
    def generate_full_tree(depth, max_depth):
        if max_depth < 0:
            logging.warning("Max depth is less than 0, ignoring generation")
            return None
        if depth >= max_depth:
            terminal_value = GPA.get_random_terminal()
            return GPA(terminal_value, left=None, right=None)
        else:
            operator = GPA.get_random_operator()
            return GPA(
                operator,
                left=GPAFactory.generate_full_tree(depth + 1, max_depth),
                right=GPAFactory.generate_full_tree(depth + 1, max_depth)
            )

    @staticmethod
    def generate_grow_tree(depth, max_depth):
        if depth == max_depth or (depth > 0 and random.random() > 0.5):
            terminal_value = GPA.get_random_terminal()
            return GPA(terminal_value, left=None, right=None)
        else:
            operator = GPA.get_random_operator()
            return GPA(
                operator,
                left=GPAFactory.generate_grow_tree(depth + 1, max_depth),
                right=GPAFactory.generate_grow_tree(depth + 1, max_depth)
            )

    @staticmethod
    def generate_individual(method, max_depth):
        if method == 'full':
            return GPAFactory.generate_full_tree(1, max_depth)
        elif method == 'grow':
            return GPAFactory.generate_grow_tree(1, max_depth)
        else:
            raise ValueError("Invalid method: choose 'full' or 'grow'")

    @staticmethod
    def generate_population(pop_size):
        optimizer = GPABloat()

        population = []
        for _ in range(pop_size // 2):
            ind = GPAFactory.generate_individual('full', GPA.MAX_DEPTH)
            optimizer.optimize(ind)
            population.append(ind)

            ind = GPAFactory.generate_individual('grow', GPA.MAX_DEPTH)
            optimizer.optimize(ind)
            population.append(ind)

        random.shuffle(population)
        return population
