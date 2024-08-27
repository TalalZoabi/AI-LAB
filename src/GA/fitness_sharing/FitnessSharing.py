
class FitnessSharing:
    def __init__(self, sigma_share, distance_func, alpha=1.0):
        self.sigma_share = sigma_share
        self.alpha = alpha
        self.distance_func = distance_func

    def apply_sharing(self, population, raw_fitness):
        raise NotImplementedError("This method should be implemented by subclasses.")


