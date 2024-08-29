
from src.GP.GP import GP
from src.GP.GPFactory import GPFactory
from src.GP.GPCrossover import GPCrossover
from src.GP.GPBloat import GPBloat


optimizer = GPBloat()

gp_crossover = GPCrossover(optimizer=optimizer)

factory = GPFactory()

ind1 = factory.generate_individual('full', GP.MAX_DEPTH)
ind2 = factory.generate_individual('full', GP.MAX_DEPTH)

print("Individual 1:")
print(ind1)

print("Individual 2:")
print(ind2)

print("Individual 1 max depth: ", ind1.calc_max_depth())
print("Individual 2 max depth: ", ind2.calc_max_depth())

print("Crossover:")
new_ind1, new_ind2 = gp_crossover.crossover(ind1, ind2)

print("New individual 1:")
print(new_ind1)
print("New individual 1 max depth: ", new_ind1.calc_max_depth())

print("New individual 2:")
print(new_ind2)
print("New individual 2 max depth: ", new_ind2.calc_max_depth())

