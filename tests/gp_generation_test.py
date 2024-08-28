
from src.GP.GP import GP
from src.GP.GPFactory import GPFactory


gp_factory = GPFactory()

full_ind = gp_factory.generate_individual(GP.MAX_DEPTH, 'full')
grow_ind = gp_factory.generate_individual(GP.MAX_DEPTH, 'grow')


print("full individual:" + str(full_ind))
print("grow individual:" + str(grow_ind))








