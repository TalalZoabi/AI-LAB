
from .GP import GP
from .GPBloat import GPBloat

class GPCrossover:
    def __init__(self, optimizer: GPBloat):
        self.optimizer = optimizer

    def crossover(self, parent1: GP, parent2: GP):
        child1 = parent1.copy()
        child2 = parent2.copy()

        node1, _ = child1.select_random_node()
        node2, _ = child2.select_random_node()


        node1.value, node2.value = node2.value, node1.value
        node1.left, node2.left = node2.left, node1.left
        node1.right, node2.right = node2.right, node1.right



        child1.prune_to_max_depth()
        child2.prune_to_max_depth()

        self.optimizer.optimize(child1)
        self.optimizer.optimize(child2)        

        return child1, child2



