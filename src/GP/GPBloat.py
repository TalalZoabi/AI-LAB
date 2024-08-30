
from .GP import GP

class GPBloat:

    def remove_redundant_operators(self, ind: GP):
        if not ind.is_operator():
            return
        if ind.left is None:
            return
        if ind.right is None:
            return
        if not ind.left.is_terminal() or ind.left.value == ind.value:
            return
        if ind.left.value == ind.right.value:
            ind.value = ind.left.value
            ind.left = None
            ind.right = None
        
    def remove_duplicate_not(self, ind: GP | None):
        if ind is None: 
            return
        
        if ind.value == GP.NOT and ind.left.value == GP.NOT:
            ind.value = ind.left.left.value
            ind.right = ind.left.left.right
            ind.left = ind.left.left.left

    # uses the fact that (NOT A) and (NOT B) is equivalent to (NOT (A OR B)) which saves an extra node
    def reduce_not(self, ind: GP):
        if not ind.is_operator():
            return
        if ind.right is None:
            return
        if ind.left is None:
            return

        if ind.right.value == GP.NOT and ind.left.value == GP.NOT:
            new_value = GP.AND if ind.value == GP.OR else GP.OR
            new_node = GP(new_value, left=ind.left.left, right=ind.right.left)
            ind.value = GP.NOT
            ind.right = None
            ind.left = new_node
            
    def remove_redundant_not(self, ind: GP):
        if ind.value != GP.NOT:
            return        
        if ind.left is None:
            ind.left = ind.right
            ind.right = None

        if ind.left.value == GP.NOT:
            ind.value = ind.left.left.value
            ind.right = ind.left.left.right
            ind.left = ind.left.left.left
            return
        
        if ind.left.value == GP.TRUE:
            ind.value = GP.FALSE
            ind.left = None
            ind.right = None
            return

        if ind.left.value == GP.FALSE:
            ind.value = GP.TRUE
            ind.left = None
            ind.right = None
            return


        if ind.left.value == GP.NEGATION:
            ind.value = GP.NEGATION
            ind.left = None
            ind.right = None


    def remove_redundant_and(self, ind: GP):
        if ind.value != GP.AND:
            return
        

        # handles A and not A case. (always false)
        if (ind.left.value == GP.NOT and ind.right.is_terminal() and ind.right.value == ind.left.left.value) \
            or (ind.right.value == GP.NOT and ind.left.is_terminal() and ind.left.value == ind.right.left.value):
            ind.value = GP.FALSE
            ind.right = None
            ind.left = None
            return

        # handles if one of the chidlren is always false, then the whole expression is false
        if ind.left.value == GP.FALSE or ind.right.value == GP.FALSE:
            ind.value = GP.FALSE
            ind.right = None
            ind.left = None
            return 

        # handles if one of the children is always true, then the whole expression is the other child
        if ind.left.value == GP.TRUE or ind.left.value == GP.NEGATION:
            ind.value = ind.right.value
            ind.left = ind.right.left
            ind.right = ind.right.right
            return
        elif ind.right.value == GP.TRUE or ind.right.value == GP.NEGATION:
            ind.value = ind.left.value
            ind.right = ind.left.right
            ind.left = ind.left.left
            return

        if ind.left == ind.right:
            ind.value = ind.left.value
            ind.right = ind.left.right
            ind.left = ind.left.left


    
    def remove_redundant_or(self, ind: GP):
        try:
            if ind.value != GP.OR:
                return

            if (ind.left.value == GP.NOT and ind.right.is_terminal() and ind.right.value == ind.left.left.value) \
                or (ind.right.value == GP.NOT and ind.left.is_terminal() and ind.left.value == ind.right.left.value):
                ind.value = GP.TRUE
                ind.right = None
                ind.left = None
                return

            if ind.left.value == GP.TRUE or ind.right.value == GP.TRUE:
                ind.value = GP.TRUE
                ind.right = None
                ind.left = None
                return

            if ind.left.value == GP.FALSE or ind.left.value == GP.NEGATION:
                ind.value = ind.right.value
                ind.left = ind.right.left
                ind.right = ind.right.right
                return
            elif ind.right.value == GP.FALSE or ind.right.value == GP.NEGATION:
                ind.value = ind.left.value
                ind.right = ind.left.right
                ind.left = ind.left.left
                return

            if ind.left == ind.right:
                ind.value = ind.left.value
                ind.right = ind.left.right
                ind.left = ind.left.left
        except AttributeError as e:
            print(ind)
            print(ind.left)
            print(ind.right)
            raise e


    def check_warning(self, ind: GP):
        if ind.value == GP.AND and (ind.left is None or ind.right is None):
            print("Warning: AND operator with only one child")
            print(ind)
        
        if ind.value == GP.OR and (ind.left is None or ind.right is None):
            print("Warning: OR operator with only one child")
            print(ind)

        if ind.value == GP.NOT and ind.left is None:
            print("Warning: NOT operator with no child")
            print(ind)


    def handle_negation(self, ind: GP):
        if ind.value != GP.NEGATION:
            return
        
        ind.value = ind.get_random_terminal()
        ind.left = None
        ind.right = None

    def optimize(self, ind: GP | None) -> GP | None:
        if ind is None:
            return None
        self.optimize(ind.left)
        self.optimize(ind.right)

        self.check_warning(ind)
        
        self.remove_redundant_operators(ind)
        self.remove_duplicate_not(ind)
        self.reduce_not(ind)
        self.remove_redundant_and(ind)
        self.remove_redundant_or(ind)
        self.remove_redundant_not(ind)

        self.handle_negation(ind)


        return ind
    

    def check_negation(self, ind: GP) -> bool:
        if ind is None:
            return False
        if ind.value == GP.NEGATION:
            print("Warning: Negation operator found")
            return True
        
        return self.check_negation(ind.left) or self.check_negation(ind.right)

