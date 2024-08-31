import random

TERMINALS = ['x'] + [str(i) for i in range(10)]
FUNCTIONS = ['+', '-', '*', '/']



def generate_random_chromosome(length: int) -> list[str]:
    return [random.choice(TERMINALS + FUNCTIONS) for _ in range(length)]

def generate_random_tail(length: int) -> list[str]:
    return [random.choice(TERMINALS) for _ in range(length)]

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


ch1_head = generate_random_chromosome(5)
print(ch1_head)

ch1_tail = generate_tail(ch1_head)
print(ch1_tail)

ch1 = ch1_head + ch1_tail

print(ch1)

print(evaluate(ch1, 2.0))


