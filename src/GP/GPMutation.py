import random

from .GP import GP
from .GPFactory import GPFactory
from .GPBloat import GPBloat


class GPMutation:
    def __init__(self, optimizer: GPBloat):
        self.optimizer = optimizer

    def subtree_mutation(self, ind: GP):
        node, depth = ind.select_random_node()
        new_subtree = GPFactory.generate_individual('full', GP.MAX_DEPTH - depth)
        if new_subtree is None:
            return

        node.value = new_subtree.value
        node.left = new_subtree.left
        node.right = new_subtree.right


    def point_mutation(self, ind: GP):
        node, depth = ind.select_random_node()

        if node.is_terminal():
            node.value = GPFactory.get_random_terminal()
        else:
            node.value = GPFactory.get_random_operator()
            if node.value == GP.NOT:
                node.right = None
            if node.right is None:
                node.right = GPFactory.generate_individual('full', GP.MAX_DEPTH - depth - 1)
            if node.left is None:
                node.left = GPFactory.generate_individual('full', GP.MAX_DEPTH - depth - 1)



    def mutate(self, ind: GP, *args, **kwargs):
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