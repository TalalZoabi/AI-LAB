import random
import logging

from .GP import GP

from .GPBloat import GPBloat

class GPFactory:
    @staticmethod
    def generate_full_tree(depth, max_depth):
        if max_depth < 0:
            logging.warning("Max depth is less than 0, ignoring generation")
            return
        if depth >= max_depth:
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
            return GPFactory.generate_full_tree(1, max_depth)
        elif method == 'grow':
            return GPFactory.generate_grow_tree(1, max_depth)
        else:
            raise ValueError("Invalid method: choose 'full' or 'grow'")

    @staticmethod
    def generate_population(pop_size):
        optimizer = GPBloat()

        population = []
        for _ in range(pop_size//2):
            ind = GPFactory.generate_individual('full', GP.MAX_DEPTH)            
            optimizer.optimize(ind)
            population.append(ind)

            ind = GPFactory.generate_individual('grow', GP.MAX_DEPTH)
            optimizer.optimize(ind)
            population.append(ind)
        


        random.shuffle(population)
        return population

