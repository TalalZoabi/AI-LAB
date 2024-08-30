from .GPA import GPA
from .GPABloat import GPABloat

class GPACrossover:
    def __init__(self, optimizer: GPABloat):
        self.optimizer = optimizer

    def crossover(self, parent1: GPA, parent2: GPA):
        child1 = parent1.copy()
        child2 = parent2.copy()

        # Select random nodes from both parents
        node1, _ = child1.select_random_node()
        node2, _ = child2.select_random_node()

        # Swap the selected nodes
        node1.value, node2.value = node2.value, node1.value
        node1.left, node2.left = node2.left, node1.left
        node1.right, node2.right = node2.right, node1.right

        # Prune trees to ensure they don't exceed the maximum depth
        child1.prune_to_max_depth()
        child2.prune_to_max_depth()

        # Optimize the trees to remove redundant operations and simplify the expressions
        self.optimizer.optimize(child1)
        self.optimizer.optimize(child2)        

        return child1, child2
