
from src.GP.GP import GP
from src.GP.GPFactory import GPFactory
from src.GP.GPBloat import GPBloat


gp_factory = GPFactory()
gp_bloat = GPBloat()

full_ind = gp_factory.generate_individual(GP.MAX_DEPTH, 'full')
grow_ind = gp_factory.generate_individual(GP.MAX_DEPTH, 'grow')

# bloat test

print("full individual:" + str(full_ind))
print("grow individual:" + str(grow_ind))

gp_bloat.optimize(full_ind)
gp_bloat.optimize(grow_ind)


print("full individual after bloat:" + str(full_ind))
print("grow individual after bloat:" + str(grow_ind)
)

