import random

A = 1
B = 2
AND = 3
OR = 4
NOT = 5

class GP:
    def __init__(self, value: int, left=None, right=None) -> None:
        self.value = value
        self.left = left
        self.right = right

    def size(self) -> int:
        if self.value == A or self.value == B:
            return 1
        else:
            return 1 + self.left.size() + self.right.size()

    def evaluate(self, a_value: bool, b_value: bool) -> bool:
        if self.value == A:
            return a_value
        elif self.value == B:
            return b_value
        elif self.value == AND:
            return self.left.evaluate(a_value, b_value) and self.right.evaluate(a_value, b_value)
        elif self.value == OR:
            return self.left.evaluate(a_value, b_value) or self.right.evaluate(a_value, b_value)
        elif self.value == NOT:
            return not self.left.evaluate(a_value, b_value)
        else:
            raise ValueError("Invalid node value")

def generate_full_tree(depth, max_depth):
    if depth == max_depth:
        return GP(random.choice([A, B]))
    else:
        operator = random.choice([AND, OR, NOT])
        if operator == NOT:
            return GP(operator, left=generate_full_tree(depth + 1, max_depth))
        else:
            return GP(operator, left=generate_full_tree(depth + 1, max_depth), right=generate_full_tree(depth + 1, max_depth))

def generate_grow_tree(depth, max_depth):
    if depth == max_depth or (depth > 0 and random.random() > 0.5):
        return GP(random.choice([A, B]))
    else:
        operator = random.choice([AND, OR, NOT])
        if operator == NOT:
            return GP(operator, left=generate_grow_tree(depth + 1, max_depth))
        else:
            return GP(operator, left=generate_grow_tree(depth + 1, max_depth), right=generate_grow_tree(depth + 1, max_depth))

def generate_individual(max_depth, method):
    if method == 'full':
        return generate_full_tree(0, max_depth)
    elif method == 'grow':
        return generate_grow_tree(0, max_depth)
    else:
        raise ValueError("Invalid method: choose 'full' or 'grow'")

def generate_initial_population(size, max_parse_tree_depth):
    population = []
    half_size = size // 2
    for _ in range(half_size):
        population.append(generate_individual(max_parse_tree_depth, 'full'))
    for _ in range(half_size, size):
        population.append(generate_individual(max_parse_tree_depth, 'grow'))
    return population

# Example usage
population_size = 10
max_tree_depth = 3
initial_population = generate_initial_population(population_size, max_tree_depth)

# Print the generated population for verification
for i, individual in enumerate(initial_population):
    print(f"Individual {i+1}: {individual.value} (size: {individual.size()})")
