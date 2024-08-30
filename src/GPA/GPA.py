import random

class GPA:
    MAX_DEPTH = 10
    X = 1
    ADD = 2
    SUB = 3
    MUL = 4
    DIV = 5

    def __init__(self, value: int, left=None, right=None) -> None:
        self.value = value
        self.left = left
        self.right = right


    def is_operator(self) -> bool:
        return self.value in [GPA.ADD, GPA.SUB, GPA.MUL, GPA.DIV]
    
    def is_terminal(self) -> bool:
        return self.value == GPA.X

    def size(self) -> int:
        if self.is_terminal():
            return 1
        else:
            left_size = self.left.size() if self.left else 0
            right_size = self.right.size() if self.right else 0
            return 1 + left_size + right_size

    def calc_max_depth(self) -> int:
        if self.is_terminal():
            return 1
        else:
            left_depth = self.left.calc_max_depth() if self.left else 0
            right_depth = self.right.calc_max_depth() if self.right else 0
            return 1 + max(left_depth, right_depth)

    def evaluate(self, x_value: float) -> float:
        if self.value == GPA.X:
            return x_value
        elif self.value == GPA.ADD:
            return self.left.evaluate(x_value) + self.right.evaluate(x_value)
        elif self.value == GPA.SUB:
            return self.left.evaluate(x_value) - self.right.evaluate(x_value)
        elif self.value == GPA.MUL:
            return self.left.evaluate(x_value) * self.right.evaluate(x_value)
        elif self.value == GPA.DIV:
            right_value = self.right.evaluate(x_value)
            return self.left.evaluate(x_value) / right_value if right_value != 0 else 1 # assume 1 for division by zero
        else:
            raise ValueError("Invalid node value")

    def __str__(self) -> str:
        if self.value == GPA.X:
            return 'X'
        elif self.value == GPA.ADD:
            return f'({self.left} + {self.right})'
        elif self.value == GPA.SUB:
            return f'({self.left} - {self.right})'
        elif self.value == GPA.MUL:
            return f'({self.left} * {self.right})'
        elif self.value == GPA.DIV:
            return f'({self.left} / {self.right})'
        else:
            raise ValueError("Invalid node value")

    def select_random_node(self) -> tuple['GPA', int]:
        candidate = None
        candidate_depth = 0

        def visit(node, depth=1):
            nonlocal candidate, candidate_depth
            if node is None:
                return

            if random.randint(1, depth) == 1:
                candidate = node
                candidate_depth = depth

            visit(node.left, depth + 1)
            visit(node.right, depth + 1)

        visit(self)
        return candidate, candidate_depth - 1

    def copy(self):
        left_copy = self.left.copy() if self.left is not None else None
        right_copy = self.right.copy() if self.right is not None else None
        return GPA(self.value, left=left_copy, right=right_copy)

    def __eq__(self, other):
        if other is None:
            return False
        
        if self.value != other.value:
            return False
        
        if self.left != other.left and self.left != other.right:
            return False

        if self.right != other.right and self.right != other.left:
            return False
        
        return True

    def prune_to_max_depth(self):
        def prune(node, current_depth):
            if current_depth == GPA.MAX_DEPTH:
                node.left = None
                node.right = None
                if node.is_operator():
                    node.value = GPA.get_random_terminal()
            else:
                if node.left:
                    prune(node.left, current_depth + 1)
                if node.right:
                    prune(node.right, current_depth + 1)

        prune(self, 0)


    @staticmethod
    def get_random_terminal():
        return GPA.X


    @staticmethod
    def get_random_operator():
        return random.choice([GPA.ADD, GPA.SUB, GPA.MUL, GPA.DIV])
