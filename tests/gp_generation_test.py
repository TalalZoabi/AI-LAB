
from src.GP.GP import GP
from src.GP.GPFactory import GPFactory


gp_factory = GPFactory()

full_ind = gp_factory.generate_individual('full',GP.MAX_DEPTH)
grow_ind = gp_factory.generate_individual('grow',GP.MAX_DEPTH)


print("full individual:" + str(full_ind))
print("grow individual:" + str(grow_ind))

print("full individual max depth: ", full_ind.calc_max_depth())
print("grow individual max depth: ", grow_ind.calc_max_depth())







