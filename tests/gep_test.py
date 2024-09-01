import random

TERMINALS = ['x'] + [str(i) for i in range(10)]
FUNCTIONS = ['+', '-', '*', '/']


target_values =[(1,5), (2,17), (3,43), (4,85), (5,145)]
size_factor = 0.1

tail_attempts = 20

def fitness(chromosome: list[str]) -> float:
    error = 0.0
    for x, y in target_values:
        y_pred = evaluate(chromosome, x)
        error += abs(y - y_pred)
    size = calc_size(chromosome)
    return -error - size_factor * size

def head_fitness(chromosome: list[str]) -> tuple[float, list[str]]:
    max_fitness = None
    best_tail = None
    for _ in range(tail_attempts):
        tail = generate_tail(chromosome)
        full_chromosome = chromosome + tail
        ind_fitness = fitness(full_chromosome)
        if max_fitness is None or ind_fitness > max_fitness:
            max_fitness = ind_fitness
            best_tail = tail
    return max_fitness, best_tail



def generate_random_chromosome(length: int) -> list[str]:
    return [random.choice(TERMINALS + FUNCTIONS) for _ in range(length)]

def generate_random_tail(length: int) -> list[str]:
    return [random.choice(TERMINALS) for _ in range(length)]


def crossover(head1: list[str], head2: list[str]) -> tuple[list[str], list[str]]:
    # do single point crossover (asume heads are opf teh same size )
    point = random.randint(1, len(head1) - 1)
    new_head1 = head1[:point] + head2[point:]
    new_head2 = head2[:point] + head1[point:]

    return new_head1, new_head2

def mutate(head: list[str], mutation_rate: float) -> list[str]:
    new_chromosome = []
    for gene in head:
        if random.random() < mutation_rate:
            new_gene = random.choice(TERMINALS + FUNCTIONS)
            new_chromosome.append(new_gene)
        else:
            new_chromosome.append(gene)
    return new_chromosome


def calc_needed_terminals(chromosome: list[str]) -> int:
    stack_size = 0
    missing = 0
    for gene in reversed(chromosome):
        if gene in TERMINALS:
            stack_size += 1
        else:
            stack_size -= 2
            if stack_size < 0:
                missing += -stack_size
                stack_size = 0
            stack_size += 1
    return missing
            

def calc_size(chromosome: list[str]) -> int:
    size = 0
    for gene in reversed(chromosome):
        if gene in FUNCTIONS:
            size += 2
    return size

def generate_tail(head: list[str]) -> list[str]:
    missing = calc_needed_terminals(head)
    tail = generate_random_tail(missing)
    return tail



def evaluate(chromosome: list[str], x_value: float) -> int:
    stack = []
    res = None
    for gene in reversed(chromosome):
        if gene == 'x':
            if res is None:
                res = x_value
            stack.append(x_value)
        elif gene == '+':
            arg1 = stack.pop()
            arg2 = stack.pop()
            res = arg1 + arg2
            stack.append(res)
        elif gene == '-':
            arg1 = stack.pop()
            arg2 = stack.pop()
            res = arg1 - arg2
            stack.append(res)
        elif gene == '*':
            arg1 = stack.pop()
            arg2 = stack.pop()
            res = arg1 * arg2
            stack.append(res)
        elif gene == '/':
            arg1 = stack.pop()
            arg2 = stack.pop()
            res = arg1 / arg2 if arg2 != 0 else 1
            stack.append(res)
        else:
            if res is None:
                res = float(gene)
            stack.append(float(gene))
    return res



def gep():
    population_size = 200
    head_length = 10
    mutation_rate = 0.1
    generations = 100
    elitism = 80

    population = [generate_random_chromosome(head_length) for _ in range(population_size)]
    for _ in range(generations):
        fitnesses = [head_fitness(chromosome) for chromosome in population]
        data = list(zip(population, fitnesses))
        data.sort(key=lambda x: x[1][0], reverse=True)

        # select the best (elitism)
        data = data[:elitism]
        while len(data) < population_size:
            parent1, _ = random.choice(data)
            parent2, _ = random.choice(data)
            child1, child2 = crossover(parent1, parent2)
            child1 = mutate(child1, mutation_rate)
            child2 = mutate(child2, mutation_rate)
            data.append((child1, head_fitness(child1)))
            data.append((child2, head_fitness(child2)))

        population = [x[0] for x in data]
    
    # find best chromosome and best tail and return it
    best_individual = max(data, key=lambda x: x[1][0])
    return best_individual[0], best_individual[1][1], best_individual[1][0]



if __name__ == '__main__':
    best_chromosome, best_tail, best_fitness = gep()
    print('Best chromosome:', best_chromosome)
    print('Best tail:', best_tail)
    print('Best fitness:', best_fitness)
    print('Size:', calc_size(best_chromosome))
    for x, y in target_values:
        print(f'x={x}, y={y}, y_pred={evaluate(best_chromosome + best_tail, x)}')


