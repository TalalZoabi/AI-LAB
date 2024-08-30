import random
from .GPA import GPA
from .GPAFactory import GPAFactory
from .GPABloat import GPABloat

class GPAMutation:
    def __init__(self, optimizer: GPABloat):
        self.optimizer = optimizer

    def subtree_mutation(self, ind: GPA):
        node, depth = ind.select_random_node()
        new_subtree = GPAFactory.generate_individual('full', GPA.MAX_DEPTH - depth)
        if new_subtree is None:
            return

        node.value = new_subtree.value
        node.left = new_subtree.left
        node.right = new_subtree.right

    def point_mutation(self, ind: GPA):
        node, _ = ind.select_random_node()

        if node.is_operator():
            node.value = GPA.get_random_operator()
            node.extra = None  # Operators don't need the extra field
        
            if node.left is None:
                node.left = GPAFactory.generate_individual('full', GPA.MAX_DEPTH - 1)
            if node.right is None:
                node.right = GPAFactory.generate_individual('full', GPA.MAX_DEPTH - 1)

    def mutate(self, ind: GPA, *args, **kwargs):
        SUBTREE_MUTATION = 0
        POINT_MUTATION = 1

        subtree_prob = 0.5

        if random.random() < subtree_prob:
            mutation_type = SUBTREE_MUTATION
        else:
            mutation_type = POINT_MUTATION

        if mutation_type == SUBTREE_MUTATION:
            self.subtree_mutation(ind)
        elif mutation_type == POINT_MUTATION:
            self.point_mutation(ind)
        else:
            raise ValueError("Invalid mutation type")

        self.optimizer.optimize(ind)

        return ind
