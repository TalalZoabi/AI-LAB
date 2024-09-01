import random


class GEP:
    TERMINALS = ['x', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    FUNCTIONS = ['+', '-', '*', '/']

    def __init__(self, exp: list[str]):
        self.exp = exp
        self.best_fitness = None
        self.best_tail = None

    @staticmethod
    def is_terminal(gene: str) -> bool:
        return gene in GEP.TERMINALS
    
    @staticmethod
    def is_function(gene: str) -> bool:
        return gene in GEP.FUNCTIONS

    @staticmethod
    def evaluate_exp(chromosome: list[str], x_value: float) -> int:
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

    def __len__(self):
        return len(self.exp)

    def __str__(self):
        return str(self.exp + self.best_tail)
    
