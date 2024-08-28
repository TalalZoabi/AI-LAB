import random



class GP:
    MAX_DEPTH = 3
    A = 1
    B = 2
    AND = 3
    OR = 4
    NOT = 5

    TRUE=6
    FALSE=7


    def __init__(self, value: int, left=None, right=None) -> None:
        self.value = value
        self.left = left
        self.right = right


    def is_operator(self) -> bool:
        return self.value == GP.AND or self.value == GP.OR or self.value == GP.NOT
    
    def is_terminal(self) -> bool:
        return self.value == GP.A or self.value == GP.B

    def size(self) -> int:
        if self.is_terminal():
            return 1
        else:
            left_size = self.left.size() if self.left else 0
            right_size = self.right.size() if self.right else 0
            return 1 + left_size + right_size

    def calc_max_depth(self) -> int:
        if self.value == GP.A or self.value == GP.B:
            return 1
        else:
            left_depth = self.left.calc_max_depth() if self.left else 0
            right_depth = self.right.calc_max_depth() if self.right else 0
            return 1 + max(left_depth, right_depth)

    def evaluate(self, a_value: bool, b_value: bool) -> bool:
        if self.value == GP.TRUE:
            return True
        elif self.value == GP.FALSE:
            return False
        elif self.value == GP.A:
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

    def __str__(self) -> str:
        if self.value == GP.TRUE:
            return 'TRUE'
        elif self.value == GP.FALSE:
            return 'FALSE'
        elif self.value == GP.A:
            return 'A'
        elif self.value == GP.B:
            return 'B'
        elif self.value == GP.AND:
            return f'({self.left} AND {self.right})'
        elif self.value == GP.OR:
            return f'({self.left} OR {self.right})'
        elif self.value == GP.NOT:
            if self.left is None:
                return f'(NOT {self.right})'
            elif self.right is None:
                return f'(NOT {self.left})'
        else:
            raise ValueError("Invalid node value")


    def select_random_node(self):
        candidate = None
        count = 0

        def visit(node, depth=1):
            nonlocal count, candidate
            if node is None:
                return

            if random.randint(1, depth) == 1:
                candidate = node

            visit(node.left, depth+1)
            visit(node.right, depth+1)

        visit(self)
        return candidate


    def copy(self):
        if self.value == GP.A or self.value == GP.B:
            return GP(self.value)
        else:
            return GP(self.value, self.left.copy(), self.right.copy())

    def __eq__(self, other):
        if other is None:
            return self is None
        
        
        if self.value != other.value:
            return False
        
        if self.left != other.left and self.left != other.right:
            return False

        if self.right != other.right and self.right != other.left:
            return False
        
        return True










