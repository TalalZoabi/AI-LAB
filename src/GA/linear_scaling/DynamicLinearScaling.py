from .LinearScaling import LinearScaling

class DynamicLinearScaling(LinearScaling):
    def __init__(self, initial_k=2.0, increment=0.1, max_k=3.0):
        self.k = initial_k
        self.increment = increment
        self.max_k = max_k

    def scale(self, fitnesses):
        max_val = max(fitnesses)
        avg_val = sum(fitnesses) / len(fitnesses)
        if max_val == avg_val:
            return [1] * len(fitnesses)  # Avoid division by zero
        a = (self.k - 1) / (max_val - avg_val)
        b = 1 - a * avg_val
        self.k = min(self.k + self.increment, self.max_k)
        return [a * f + b for f in fitnesses]

