
from src.problems.GP import GP, generate_individual, A, B, AND, OR, NOT


full_ind = generate_individual(GP.MAX_DEPTH, 'full')
grow_ind = generate_individual(GP.MAX_DEPTH, 'grow')






def print_gp(individual):
    if individual.value == GP.A:
        return 'A'
    elif individual.value == GP.B:
        return 'B'
    elif individual.value == GP.AND:
        return f'( {print_gp(individual.left)} AND {print_gp(individual.right)})'
    elif individual.value == GP.OR:
        return f'({print_gp(individual.left)} OR {print_gp(individual.right)})'
    elif individual.value == GP.NOT:
        return f'(NOT {print_gp(individual.left)})'
    else:
        raise ValueError("Invalid node value")



print("full individual:" + print_gp(full_ind))
print("grow individual:" + print_gp(grow_ind))





