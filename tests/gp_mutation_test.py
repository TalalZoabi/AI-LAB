import random

from src.GP.GP import GP
from src.GP.GPFactory import GPFactory
from src.GP.GPMutation import GPMutation



def test_subtree_mutation():
    factory = GPFactory()
    ind = factory.generate_individual('full', GP.MAX_DEPTH)    
    mutate = GPMutation()

    tries = 10

    print("Original individual:")
    print(ind)
    print("original individual max depth: ", ind.calc_max_depth())

    for i in range(tries):
        print("Max depth: ", ind.calc_max_depth())

        print(f"Mutation {i+1}:")
        mutate.mutate(ind)
        print(ind)

    




    

test_subtree_mutation()

