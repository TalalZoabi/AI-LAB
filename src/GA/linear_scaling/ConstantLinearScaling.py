from .LinearScaling import LinearScaling


class ConstantLinearScaling(LinearScaling):
    def __init__(self, k=2.0):
        self.k = k

    def scale(self, fitnesses):
        max_val = max(fitnesses)
        avg_val = sum(fitnesses) / len(fitnesses)
        if max_val == avg_val:
            return [1] * len(fitnesses)  # Avoid division by zero
        a = (self.k - 1) / (max_val - avg_val)
        b = 1 - a * avg_val
        return [a * f + b for f in fitnesses]
