
class Crowding:
    def __init__(self, distance_func):
        self.distance_func = distance_func

    def apply_crowding(self, offspring, parents, fitness):
        raise NotImplementedError("This method should be implemented by subclasses.")
