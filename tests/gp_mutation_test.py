import random

from src.GP.GP import GP
from src.GP.GPFactory import GPFactory
from src.GP.GPBloat import GPBloat

def subtree_mutation(ind: GP):
    node, depth = ind.select_random_node()
    new_subtree = GPFactory.generate_full_tree(0, GP.MAX_DEPTH - depth)
    node.value = new_subtree.value
    node.left = new_subtree.left
    node.right = new_subtree.right


def point_mutation(ind: GP):
    node, depth = ind.select_random_node()

    if node.is_terminal():
        node.value = GPFactory.get_random_terminal()
    else:
        node.value = GPFactory.get_random_operator()
        if node.value == GP.NOT:
            node.right = None
        elif node.right is None:
            node.right = GPFactory.generate_full_tree(0, GP.MAX_DEPTH - depth)



def mutate_individual(ind: GP):
    SUBTREE_MUTATION = 0
    POINT_MUTATION = 1

    mutation_type = random.choice([SUBTREE_MUTATION, POINT_MUTATION])
    if mutation_type == SUBTREE_MUTATION:
        subtree_mutation(ind)
    elif mutation_type == POINT_MUTATION:
        point_mutation(ind)
    else:
        raise ValueError("Invalid mutation type")



def test_subtree_mutation():
    factory = GPFactory()
    ind = factory.generate_individual('full', GP.MAX_DEPTH)    

    tries = 10

    print("Original individual:")
    print(ind)

    for i in range(tries):
        print(f"Mutation {i+1}:")
        mutate_individual(ind)
        print(ind)

    




    

test_subtree_mutation()

