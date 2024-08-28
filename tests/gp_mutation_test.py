

from src.GP.GP import GP
from src.GP.GPFactory import GPFactory
from src.GP.GPBloat import GPBloat

def mutate_individual(ind: GP):
    new_ind = ind.copy()
    node = new_ind.select_random_node()
    
    if node.is_terminal():
        node.value = GPFactory.get_random_terminal()
    
    else:
        node.value = GPFactory.get_random_operator()
        if node.left is not None:
            node.left = GPFactory.generate_full_tree(0, 2)
        if node.right is not None:
            node.right = GPFactory.generate_full_tree(0, 2)



