import numpy as np

class AckleyFunction:
    def __init__(self, dimension, a=20, b=0.2, c=2 * np.pi):
        self.dimension = dimension
        self.a = a
        self.b = b
        self.c = c

    def evaluate(self, x):
        d = len(x)
        sum1 = np.sum(x ** 2)
        sum2 = np.sum(np.cos(self.c * x))
        term1 = -self.a * np.exp(-self.b * np.sqrt(sum1 / d))
        term2 = -np.exp(sum2 / d)
        original_value = term1 + term2 + self.a + np.exp(1)
        return -original_value  # Return the negative of the original Ackley function value

    def max_fitness(self, *args, **kwargs):
        # The Ackley function has a global minimum at 0, so the maximum fitness is 0
        return 0

    def min_fitness(self, *args, **kwargs):
        # The Ackley function can have very large negative values, but we can set a reasonable lower bound
        return -20