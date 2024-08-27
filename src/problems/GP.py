import random



class GP:
    MAX_DEPTH = 3
    A = 1
    B = 2
    AND = 3
    OR = 4
    NOT = 5


    def __init__(self, value: int, left=None, right=None) -> None:
        self.value = value
        self.left = left
        self.right = right

    def size(self) -> int:
        if self.value == A or self.value == B:
            return 1
        else:
            left_size = self.left.size() if self.left else 0
            right_size = self.right.size() if self.right else 0
            return 1 + left_size + right_size

    def calc_max_depth(self) -> int:
        if self.value == GP.A or self.value == GP.B:
            return 1
        else:
            left_depth = self.left.max_depth() if self.left else 0
            right_depth = self.right.max_depth() if self.right else 0
            return 1 + max(left_depth, right_depth)

    def evaluate(self, a_value: bool, b_value: bool) -> bool:
        if self.value == GP.A:
            return a_value
        elif self.value == GP.B:
            return b_value
        elif self.value == GP.AND:
            return self.left.evaluate(a_value, b_value) and self.right.evaluate(a_value, b_value)
        elif self.value == GP.OR:
            return self.left.evaluate(a_value, b_value) or self.right.evaluate(a_value, b_value)
        elif self.value == GP.NOT:
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




def mutate(individual: GP) -> GP:
    # Select a random node in the tree for mutation
    mutation_point, parent, is_left_child = select_random_node(individual)

    # Calculate the current depth of the mutation point
    current_depth = mutation_point.calc_max_depth()

    # Ensure that the new subtree will not exceed the max depth
    remaining_depth = individual.MAX_DEPTH - current_depth

    if mutation_point.value in [GP.A, GP.B]:
        # If the mutation point is a terminal, replace it with another terminal
        mutation_point.value = random.choice([GP.A, GP.B])
    else:
        # Replace the subtree rooted at mutation_point with a new randomly generated subtree
        new_subtree = generate_grow_tree(0, remaining_depth)
        if parent:
            if is_left_child:
                parent.left = new_subtree
            else:
                parent.right = new_subtree
        else:
            # If mutation_point is the root
            individual.value = new_subtree.value
            individual.left = new_subtree.left
            individual.right = new_subtree.right

    return individual

def select_random_node(individual: GP):
    """
    Recursively selects a random node in the tree.
    Returns the selected node, its parent, and whether it is a left or right child.
    """
    if individual.left is None and individual.right is None:
        return individual, None, None

    if random.random() > 0.5:
        if individual.left:
            selected_node, parent, is_left_child = select_random_node(individual.left)
            if parent is None:
                return selected_node, individual, True
            else:
                return selected_node, parent, is_left_child
        elif individual.right:
            selected_node, parent, is_left_child = select_random_node(individual.right)
            if parent is None:
                return selected_node, individual, False
            else:
                return selected_node, parent, is_left_child
    else:
        if individual.right:
            selected_node, parent, is_left_child = select_random_node(individual.right)
            if parent is None:
                return selected_node, individual, False
            else:
                return selected_node, parent, is_left_child
        elif individual.left:
            selected_node, parent, is_left_child = select_random_node(individual.left)
            if parent is None:
                return selected_node, individual, True
            else:
                return selected_node, parent, is_left_child

    # Default return for the root node
    return individual, None, None



