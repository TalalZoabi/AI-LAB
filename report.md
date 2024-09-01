

## GP (logic tree representation)

### Indiovidual representtaion

To represent individuals we made a class name GP to hold the data (tree representation)
it is a typical binary tree stuucture implemented with python where each node has value and pointers (refrences) to left and right children

We also added constant values to the class to follow best practyices and allow for more understandible and readibel code.

``` python
class GP:
    MAX_DEPTH = 4
    A = 1
    B = 2
    AND = 3
    OR = 4
    NOT = 5

    TRUE=6
    FALSE=7
    NEGATION = 8


    def __init__(self, value: int, left=None, right=None) -> None:
        self.value = value
        self.left = left
        self.right = right
```

we defined the operators (AND, OR, NOT) and the terminals (A,B) (as well as true and false constant values which help with preventing bloat and optimization)

we also defined (MAX_DEPTH) to prevent unbounded growth of trees and to help with execution time.


### Individual generation

For random tree generation we defined a GPFactory class to handle the proccess of creation

``` python
import random
import logging

from .GP import GP

from .GPBloat import GPBloat

class GPFactory:
    @staticmethod
    def generate_full_tree(depth, max_depth):
        if max_depth < 0:
            logging.warning("Max depth is less than 0, ignoring generation")
            return
        if depth >= max_depth:
            return GP(random.choice([GP.A, GP.B]))
        else:
            operator = random.choice([GP.AND, GP.OR, GP.NOT])
            if operator == GP.NOT:
                return GP(operator, left=GPFactory.generate_full_tree(depth + 1, max_depth))
            else:
                return GP(operator, left=GPFactory.generate_full_tree(depth + 1, max_depth), right=GPFactory.generate_full_tree(depth + 1, max_depth))

    @staticmethod
    def generate_grow_tree(depth, max_depth):
        if depth == max_depth or (depth > 0 and random.random() > 0.5):
            return GP(random.choice([GP.A, GP.B]))
        else:
            operator = random.choice([GP.AND, GP.OR, GP.NOT])
            if operator == GP.NOT:
                return GP(operator, left=GPFactory.generate_grow_tree(depth + 1, max_depth))
            else:
                return GP(operator, left=GPFactory.generate_grow_tree(depth + 1, max_depth), right=GPFactory.generate_grow_tree(depth + 1, max_depth))

    @staticmethod
    def get_random_terminal():
        return random.choice([GP.A, GP.B])
    
    @staticmethod
    def get_random_operator():
        return random.choice([GP.AND, GP.OR, GP.NOT])

    @staticmethod
    def generate_individual(method, max_depth):
        if method == 'full':
            return GPFactory.generate_full_tree(1, max_depth)
        elif method == 'grow':
            return GPFactory.generate_grow_tree(1, max_depth)
        else:
            raise ValueError("Invalid method: choose 'full' or 'grow'")

    @staticmethod
    def generate_population(pop_size):
        optimizer = GPBloat()

        population = []
        for _ in range(pop_size//2):
            ind = GPFactory.generate_individual('full', GP.MAX_DEPTH)            
            optimizer.optimize(ind)
            population.append(ind)

            ind = GPFactory.generate_individual('grow', GP.MAX_DEPTH)
            optimizer.optimize(ind)
            population.append(ind)
        


        random.shuffle(population)
        return population

```

This follows teh lecture notes on 'full' tree generation and the 'grow' method.
And we use 'ramped half & half' to generate a population

Using these methods we can ensure that generated individuals never violate the max depth constraint and aree valid trees.

inner nodes are only operators and leaf nodes are only terminals.


### Fitness function
To meassure fitness of an individual, we need to compare its answers to that of the target function (for example: the xor function) and also penalize larger tree size.

We defined the GPFitness class to meassure the fitness:

``` python

class GPFitness(FitnessFunction):
    def __init__(self, lambda_penalty, opt_size, target_function):
        self.lambda_penalty = lambda_penalty
        self.opt_size = opt_size
        self.target_function = target_function

    def evaluate(self, individual) -> float:
        hits = 0
        for a in [True, False]:
            for b in [True, False]:
                if individual.evaluate(a, b) == self.target_function(a, b):
                    hits += 1

        return hits - self.lambda_penalty * abs(self.opt_size - individual.size())
```

given the expected optimal size the larger the difference in sizes the less fit the individual would be.
We added lambda penatly so we can control the effect the size has on the fitness.

we measdure hits as discreet 1/0 values because we are dealing with boolean values.
to test out equivelnance we check for every possible input. and because we only have 2 variables we need to run the tree 4 times and compare with the target function.

This function rewards hits and poenalizes size (need to set the lambda pentalty accordingly so we allow for larger size if it means more hits)


### Crossover 
Since we are working with trees, a simple crossover method wouyld be to select ranom nodes in teh two trees and do a swap operation (and thus creating 2 new individuals).

This means we need to consider two aspects:

#### node selection:
We woudnlt want to choose random uniform selection, since most nodes are leaves, thuis with a very high chance we will swap leaves an keep expanding teh tree indefitely.

that's why we need a non uniform selection method.

we aded to teh GP class, this method:

```python 
def select_random_node(self) -> tuple['GP', int]:
        candidate = None
        candidate_depth = 0

        def visit(node, depth=1):
            nonlocal candidate, candidate_depth
            if node is None:
                return

            if random.randint(1, depth) == 1:
                candidate = node
                candidate_depth = depth

            visit(node.left, depth+1)
            visit(node.right, depth+1)

        visit(self)
        return candidate, candidate_depth-1

```

This method has a higher chance to select nodes higher up in the tree than lower ones.
this balances out the selection so that leaf nodes are no overwhelmingly chosen.

this means that equal depth nodes have the same chance to be chosen.


we made a script nammed 'gp_random_node_select_test' that uses this method and plots out data baout the distubution of nodes. (and their depth)

(Add size distubution plots here)

to run this script sinply type 'python -m tests.gp_random_node_select_test'


#### Depth Constraint
We notice that when doing crososver operation the resulting tree may violate the max depth constraint.

Thats why we implemnetd a method to prune trees that exceed teh max depth and call it after the crossover operation.

``` python
def prune_to_max_depth(self):
        def prune(node, current_depth):
            if current_depth == GP.MAX_DEPTH:
                node.left = None
                node.right = None
                if node.is_operator():
                    node.value = GP.get_random_terminal()
            else:
                if node.left:
                    prune(node.left, current_depth + 1)
                if node.right:
                    prune(node.right, current_depth + 1)

        prune(self, 0)
```

this method removes the parst taht exceed the max dpeth and replaces then with terminals. (chosen at random)

This means that we can exusre the trees are valid and do not exceed teh max depth. (which helps with analysis and performance)



These cosniderations made us implement the following crossovber method:

``` python 

class GPCrossover:
    def __init__(self, optimizer: GPBloat):
        self.optimizer = optimizer

    def crossover(self, parent1: GP, parent2: GP):
        child1 = parent1.copy()
        child2 = parent2.copy()

        node1, _ = child1.select_random_node()
        node2, _ = child2.select_random_node()


        node1.value, node2.value = node2.value, node1.value
        node1.left, node2.left = node2.left, node1.left
        node1.right, node2.right = node2.right, node1.right



        child1.prune_to_max_depth()
        child2.prune_to_max_depth()

        self.optimizer.optimize(child1)
        self.optimizer.optimize(child2)        

        return child1, child2

```


We choose a node from each tree and do the crossover, and then prune the trees to ensure it complies with the max depth constraint.

Thus we ensure that genearted individuals and offpsring from individuals are both valid expressions and limited in size.


### Mutation

For muatating individuals, we also need to consider validity of teh resulting tree and teh size constraint.

We made two mutation types: point mutation and subtree mutation.

#### point mutation
the idea is that we select a random node and change teh value of it. 
We ensure that terminals can only replace terminals and operators can only replace operators.

A private case is when mutation to/from teh NOT operator, since in teh rest of the operators we need both children to be valid but in teh NOT operator we only consider teh left child.


(if a child is missing then we generate one using the generate method)

#### subtree mutation
the idea is that we select a ranodm node and replace its subtree with a new subtree.

Operators can be replaced with a terminal (subtree of size 1) and vice versa.



#### Implemenmattion

``` python

class GPMutation:
    def __init__(self, optimizer: GPBloat):
        self.optimizer = optimizer

    def subtree_mutation(self, ind: GP):
        node, depth = ind.select_random_node()
        new_subtree = GPFactory.generate_individual('full', GP.MAX_DEPTH - depth)
        if new_subtree is None:
            return

        node.value = new_subtree.value
        node.left = new_subtree.left
        node.right = new_subtree.right


    def point_mutation(self, ind: GP):
        node, depth = ind.select_random_node()

        if node.is_terminal():
            node.value = GPFactory.get_random_terminal()
        else:
            node.value = GPFactory.get_random_operator()
            if node.value == GP.NOT:
                node.right = None
            if node.right is None:
                node.right = GPFactory.generate_individual('full', GP.MAX_DEPTH - depth - 1)
            if node.left is None:
                node.left = GPFactory.generate_individual('full', GP.MAX_DEPTH - depth - 1)



    def mutate(self, ind: GP, *args, **kwargs):
        SUBTREE_MUTATION = 0
        POINT_MUTATION = 1

        subtree_prob = 0.5


        if random.random() < subtree_prob:
            mutation_type = SUBTREE_MUTATION
        else:
            mutation_type = POINT_MUTATION

        if mutation_type == SUBTREE_MUTATION:
            self.subtree_mutation(ind)
        elif mutation_type == POINT_MUTATION:
            self.point_mutation(ind)
        else:
            raise ValueError("Invalid mutation type")

        self.optimizer.optimize(ind)

        return ind 
```


This way we ensure that in both cases the resulting mutated tree is valid and does not violate the depth constraint.



### Anti Bloating

To furthe rprevent bloating and achive better results, we defined a method to optimize given while preservinf the logic.

this is simple optimizationm techniques taht rely on teh tree structure and some binary logic tricks and identities.

Like how the expression (A and not A) is always false and (A and A) is equivelent to A.

This allows us to minimize tree size while maintainibng the same logic.

This is applied after mutation and crossover to ensure that when evaluating a tree and its fitness we have a smaller minimal equivelant for it. (faster running time and simpler results)

To acheive this we implemneted  a class named GPBloat (which doe sthe opposiet of bloating)

``` python

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

```

Here we do some simple optimization tricks, like double not removal, de morgan law and equivelance check.
(Note that this may alter a subtree to just be a set constant True/False)

This obviously assume sthat the original tree is valid but then results in a valid tree.


### More tests

#### XOR test

```python


from src.GA.GeneticAlgorithm import GeneticAlgorithm
from src.GA.fitness_functions.GPFitness import GPFitness
from src.GA.parent_selection.ElitistSelection import ElitistSelection
from src.GA.survivor_selection.HybridSelection import HybridSelection
from src.GA.mutation_strategy.MutationStrategy import BasicMutation

from src.GP.GPCrossover import GPCrossover
from src.GP.GPBloat import GPBloat
from src.GP.GPMutation import GPMutation
from src.GP.GPFactory import GPFactory


fitness_lambda_penalty = 0.7

def target_function(a, b):
    return a ^ b


def check_correctness(individual):
    for a in [True, False]:
        for b in [True, False]:
            if individual.evaluate(a, b) != target_function(a, b):
                print(f'Error for {a} and {b}')
                return False
    return True

optimizer = GPBloat()


config = {
    'name': 'gp_xor',
    'fitness_function': GPFitness(fitness_lambda_penalty, 7, target_function),
    'population_size': 200,
    'num_generations': 200,
    'num_islands': 10,
    'migration_rate': 10,
    'parent_selection': ElitistSelection(),
    'crossover_operator': GPCrossover(optimizer),
    'mutation_operator': GPMutation(optimizer),
    'survivor_selection': HybridSelection(0.8,0.2),
    'mutation_strategy': BasicMutation(0.1),
    'generate_population': GPFactory.generate_population,
    'fitness_sharing': None
}

if __name__ == '__main__':
    genetic_algorithm = GeneticAlgorithm(config)

    res = genetic_algorithm.evolve()

    best_individual = res['best_solution']

    genetic_algorithm.plot_fitness(True)

    print(f'Best individual: {best_individual}')

    print(f'Correctness: {check_correctness(best_individual)}')


```

Here we set the target function as xor and run for 200 generations

(add plots here)


#### NAND test

``` python



from src.GA.GeneticAlgorithm import GeneticAlgorithm
from src.GA.fitness_functions.GPFitness import GPFitness
from src.GA.parent_selection.ElitistSelection import ElitistSelection
from src.GA.survivor_selection.HybridSelection import HybridSelection
from src.GA.mutation_strategy.MutationStrategy import BasicMutation

from src.GP.GPCrossover import GPCrossover
from src.GP.GPBloat import GPBloat
from src.GP.GPMutation import GPMutation
from src.GP.GPFactory import GPFactory


fitness_lambda_penalty = 0.7

def target_function(a, b):
    return not (a and b)


def check_correctness(individual):
    for a in [True, False]:
        for b in [True, False]:
            if individual.evaluate(a, b) != target_function(a, b):
                print(f'Error for {a} and {b}')
                return False
    return True

optimizer = GPBloat()


config = {
    'name': 'test',
    'fitness_function': GPFitness(fitness_lambda_penalty, 7, target_function),
    'population_size': 200,
    'num_generations': 200,
    'num_islands': 10,
    'migration_rate': 10,
    'parent_selection': ElitistSelection(),
    'crossover_operator': GPCrossover(optimizer),
    'mutation_operator': GPMutation(optimizer),
    'survivor_selection': HybridSelection(0.8,0.2),
    'mutation_strategy': BasicMutation(0.1),
    'generate_population': GPFactory.generate_population,
    'fitness_sharing': None
}

genetic_algorithm = GeneticAlgorithm(config)


res = genetic_algorithm.evolve()

best_individual = res['best_solution']


print(f'Best individual before optimization: {best_individual}')

optimizer.optimize(best_individual)

print(f'Best individual after optimization: {best_individual}')

print(f'Correctness: {check_correctness(best_individual)}')



```


here we chose teh nand function


#### Third tests (custom function)

``` python 



from src.GA.GeneticAlgorithm import GeneticAlgorithm
from src.GA.fitness_functions.GPFitness import GPFitness
from src.GA.parent_selection.ElitistSelection import ElitistSelection
from src.GA.survivor_selection.HybridSelection import HybridSelection
from src.GA.mutation_strategy.MutationStrategy import BasicMutation

from src.GP.GPCrossover import GPCrossover
from src.GP.GPBloat import GPBloat
from src.GP.GPMutation import GPMutation
from src.GP.GPFactory import GPFactory


fitness_lambda_penalty = 0.7

def target_function(a: bool, b: bool) -> bool:
    return (a and b) or (not a and not b)


def check_correctness(individual):
    for a in [True, False]:
        for b in [True, False]:
            if individual.evaluate(a, b) != target_function(a, b):
                print(f'Error for {a} and {b}')
                return False
    return True

optimizer = GPBloat()


config = {
    'name': 'test',
    'fitness_function': GPFitness(fitness_lambda_penalty, 7, target_function),
    'population_size': 200,
    'num_generations': 200,
    'num_islands': 10,
    'migration_rate': 10,
    'parent_selection': ElitistSelection(),
    'crossover_operator': GPCrossover(optimizer),
    'mutation_operator': GPMutation(optimizer),
    'survivor_selection': HybridSelection(0.8,0.2),
    'mutation_strategy': BasicMutation(0.1),
    'generate_population': GPFactory.generate_population,
    'fitness_sharing': None
}

genetic_algorithm = GeneticAlgorithm(config)


res = genetic_algorithm.evolve()

best_individual = res['best_solution']


print(f'Best individual before optimization: {best_individual}')

optimizer.optimize(best_individual)

print(f'Best individual after optimization: {best_individual}')

print(f'Correctness: {check_correctness(best_individual)}')

```


Here we chose a custom function


#### Forth test (another custom function)

``` python





from src.GA.GeneticAlgorithm import GeneticAlgorithm
from src.GA.fitness_functions.GPFitness import GPFitness
from src.GA.parent_selection.ElitistSelection import ElitistSelection
from src.GA.survivor_selection.HybridSelection import HybridSelection
from src.GA.mutation_strategy.MutationStrategy import BasicMutation

from src.GP.GPCrossover import GPCrossover
from src.GP.GPBloat import GPBloat
from src.GP.GPMutation import GPMutation
from src.GP.GPFactory import GPFactory


fitness_lambda_penalty = 0.7

def target_function(a: bool, b: bool) -> bool:
    return (a and b) ^ (a or b)


def check_correctness(individual):
    for a in [True, False]:
        for b in [True, False]:
            if individual.evaluate(a, b) != target_function(a, b):
                print(f'Error for {a} and {b}')
                return False
    return True

optimizer = GPBloat()


config = {
    'name': 'test',
    'fitness_function': GPFitness(fitness_lambda_penalty, 7, target_function),
    'population_size': 200,
    'num_generations': 200,
    'num_islands': 10,
    'migration_rate': 10,
    'parent_selection': ElitistSelection(),
    'crossover_operator': GPCrossover(optimizer),
    'mutation_operator': GPMutation(optimizer),
    'survivor_selection': HybridSelection(0.8,0.2),
    'mutation_strategy': BasicMutation(0.1),
    'generate_population': GPFactory.generate_population,
    'fitness_sharing': None
}

genetic_algorithm = GeneticAlgorithm(config)


res = genetic_algorithm.evolve()

best_individual = res['best_solution']


print(f'Best individual before optimization: {best_individual}')

optimizer.optimize(best_individual)

print(f'Best individual after optimization: {best_individual}')

print(f'Correctness: {check_correctness(best_individual)}')

```




## GPA

In this section we will tackle teh univariate polynomial function finding 

GPA is for Genetic Programming - Arithmatic, since we will deal with arithmetic operations instead of boolean logic ones.


### Repreentation
We represent an individual as a tree liek with GP but in this case we only have 1 terminal and the operators are +,-,*,/.

``` python

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

```


``` python


class GPAFactory:
    @staticmethod
    def generate_full_tree(depth, max_depth):
        if max_depth < 0:
            logging.warning("Max depth is less than 0, ignoring generation")
            return None
        if depth >= max_depth:
            terminal_value = GPA.get_random_terminal()
            return GPA(terminal_value, left=None, right=None)
        else:
            operator = GPA.get_random_operator()
            return GPA(
                operator,
                left=GPAFactory.generate_full_tree(depth + 1, max_depth),
                right=GPAFactory.generate_full_tree(depth + 1, max_depth)
            )

    @staticmethod
    def generate_grow_tree(depth, max_depth):
        if depth == max_depth or (depth > 0 and random.random() > 0.5):
            terminal_value = GPA.get_random_terminal()
            return GPA(terminal_value, left=None, right=None)
        else:
            operator = GPA.get_random_operator()
            return GPA(
                operator,
                left=GPAFactory.generate_grow_tree(depth + 1, max_depth),
                right=GPAFactory.generate_grow_tree(depth + 1, max_depth)
            )

    @staticmethod
    def generate_individual(method, max_depth):
        if method == 'full':
            return GPAFactory.generate_full_tree(1, max_depth)
        elif method == 'grow':
            return GPAFactory.generate_grow_tree(1, max_depth)
        else:
            raise ValueError("Invalid method: choose 'full' or 'grow'")

    @staticmethod
    def generate_population(pop_size):
        optimizer = GPABloat()

        population = []
        for _ in range(pop_size // 2):
            ind = GPAFactory.generate_individual('full', GPA.MAX_DEPTH)
            optimizer.optimize(ind)
            population.append(ind)

            ind = GPAFactory.generate_individual('grow', GPA.MAX_DEPTH)
            optimizer.optimize(ind)
            population.append(ind)

        random.shuffle(population)
        return population

```

### Depth constraint

We use dteh same method as in GP, that is pruning the tree to ensure it fits the limit.

### Evaluation
Since we are delaing with arithmetic operators and values the evaluation process is different

``` python

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

```

here we use arithmatic expressions (and assume division by 0 yields 1 for simplicity)


We do not handle constants, instead we only deal with arithmatic operations on teh valeu of x.

### Fitness 

``` python 

class GPAFitness(FitnessFunction):
    def __init__(self, lambda_penalty: float, opt_size: int, target_function: callable, error_range: float, sample_size: int):
        self.lambda_penalty = lambda_penalty
        self.opt_size = opt_size
        self.target_function = target_function
        self.error_range = error_range
        self.sample_size = sample_size

    def evaluate(self, individual) -> float:
        hits = 0
        parity = 0

        for _ in range(self.sample_size):
            x = random.uniform(-1, 1)
            val = individual.evaluate(x)     
            diff = abs(val - self.target_function(x))  
            parity += diff
            if val < self.error_range:
                hits += 1



        if self.opt_size is None:
            return hits - self.lambda_penalty * individual.size() - parity
        else: 
            return hits - self.lambda_penalty * (individual.size() - self.opt_size) - parity

```

we chose to not only measure hits if teh disatnce from teh target is withtin teh threshold, we also penalzie larger parities from the target.

And we made the opt_size optional, since initially we do not knwo teh size o fteh optimal tree.

### Crossovber
Crossover is exactklyt like in GP, where we choose nodes, do teh crossover and pruen the trees to maintain teh max depth constraint.


``` python

from .GPA import GPA
from .GPABloat import GPABloat

class GPACrossover:
    def __init__(self, optimizer: GPABloat):
        self.optimizer = optimizer

    def crossover(self, parent1: GPA, parent2: GPA):
        child1 = parent1.copy()
        child2 = parent2.copy()

        # Select random nodes from both parents
        node1, _ = child1.select_random_node()
        node2, _ = child2.select_random_node()

        # Swap the selected nodes
        node1.value, node2.value = node2.value, node1.value
        node1.left, node2.left = node2.left, node1.left
        node1.right, node2.right = node2.right, node1.right

        # Prune trees to ensure they don't exceed the maximum depth
        child1.prune_to_max_depth()
        child2.prune_to_max_depth()

        # Optimize the trees to remove redundant operations and simplify the expressions
        self.optimizer.optimize(child1)
        self.optimizer.optimize(child2)        

        return child1, child2
```


### Mutation
Similiar to the GP boolean logic mutation, we have two mutation types, point muttaion and subtree mutation

``` python


class GPAMutation:
    def __init__(self, optimizer: GPABloat):
        self.optimizer = optimizer

    def subtree_mutation(self, ind: GPA):
        node, depth = ind.select_random_node()
        new_subtree = GPAFactory.generate_individual('full', GPA.MAX_DEPTH - depth)
        if new_subtree is None:
            return

        node.value = new_subtree.value
        node.left = new_subtree.left
        node.right = new_subtree.right

    def point_mutation(self, ind: GPA):
        node, _ = ind.select_random_node()

        if node.is_operator():
            node.value = GPA.get_random_operator()
            node.extra = None  # Operators don't need the extra field
        
            if node.left is None:
                node.left = GPAFactory.generate_individual('full', GPA.MAX_DEPTH - 1)
            if node.right is None:
                node.right = GPAFactory.generate_individual('full', GPA.MAX_DEPTH - 1)

    def mutate(self, ind: GPA, *args, **kwargs):
        SUBTREE_MUTATION = 0
        POINT_MUTATION = 1

        subtree_prob = 0.5

        if random.random() < subtree_prob:
            mutation_type = SUBTREE_MUTATION
        else:
            mutation_type = POINT_MUTATION

        if mutation_type == SUBTREE_MUTATION:
            self.subtree_mutation(ind)
        elif mutation_type == POINT_MUTATION:
            self.point_mutation(ind)
        else:
            raise ValueError("Invalid mutation type")

        self.optimizer.optimize(ind)

        return ind
```




## GEP

### Representtaion
in GEP we have the head and the tail.
The tail is an extention to make the head valid.

To represnt an individual we only save the head which is set to a fixed size (say 20)

and all individuals have a fixed head size.


``` python


class GEP:
    TERMINALS = ['x', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    FUNCTIONS = ['+', '-', '*', '/']

    def __init__(self, exp: list[str]):
        self.exp = exp
        self.best_fitness = None
        self.best_tail = None


```

### evaluation

to evaluate a GEP expression we need a stack based code, to evaluate teh exression

``` python

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

```

notice that this requires teh expression to be valid.


### ensuring validity
we cannot ensure that a random genartted head is valid thus we need to genrate a tail to turn this non valid expre4ssion to a valid one.

an exprerssion cannot be evaluated if teh stack is missing elements when attempting to call an operator.
thus if we add enough terminals to teh expression the expresison should become valid.
menaing that the tail only needs to be made of of a certain number of terminals.

To calculatethe needed number of terminals we made a method to chedk and see when we are missing elements in teh stack.

``` python

@staticmethod
    def calc_needed_terminals(chromosome: list[str]) -> int:
        stack_size = 0
        missing = 0
        for gene in reversed(chromosome):
            if gene in GEP.TERMINALS:
                stack_size += 1
            else:
                stack_size -= 2
                if stack_size < 0:
                    missing += -stack_size
                    stack_size = 0
                stack_size += 1
        return missing

```

This simulates a stack and returns teh needed number of terminals.

Note that in the head there may be extra terminals that will never be used.


the size of teh tail can be at most the size of the head (properties of binary trees) thus by limiting teh head size we by extension also limit teh size of the tail (and thus the entire expression size is bounded).

This is the size control mechanism.

### Fitness evaluation

we said taht an individual is only made up of teh head (and thus isnt neccesarly a valid expression) thus to evaluate the fitness of an individual, we set a number of tail attempts that we geenarte random tails and take the clocest reuslts (with teh best tail)

``` python

class GEPFitness:
    def __init__(self, target_data: list, tail_attempts: int, size_factor: float):
        self.target_data = target_data
        self.tail_attempts = tail_attempts
        self.size_factor = size_factor

    def fitness(self, chromosome: list[str]) -> float:
        error = 0.0
        for x, y in self.target_data:
            y_pred = GEP.evaluate_exp(chromosome, x)
            error += abs(y - y_pred)
        size = GEPFactory.calc_size(chromosome)
        return -error - self.size_factor * size


    def evaluate(self, head: GEP) -> float:
        max_fitness = None
        best_tail = None
        for _ in range(self.tail_attempts):
            tail = GEPFactory.generate_tail(head.exp)
            full_chromosome = head.exp + tail
            ind_fitness = self.fitness(full_chromosome)
            if max_fitness is None or ind_fitness > max_fitness:
                max_fitness = ind_fitness
                best_tail = tail
        
        head.best_fitness = max_fitness
        head.best_tail = best_tail
        return max_fitness

```


### Muttaion
Since we dealing with a string (array of symbols) we chose to have a mutaton rate and with a success chance of mutation rate mutate each symbol in teh head. (muttaions are only applied to teh head)

since we do not assume valdity for teh head,and we have valdity with a genearted tail, thsu mutation does not affect validity.
same for size.


``` python

class GEPMutation:
    def __init__(self, mutation_rate: float):
        self.mutation_rate = mutation_rate

    def mutate(self, chromosome: GEP, *args, **kwargs) -> GEP:
        new_chromosome = []
        for gene in chromosome.exp:
            if random.random() < self.mutation_rate:
                new_gene = random.choice(GEP.TERMINALS + GEP.FUNCTIONS)
                new_chromosome.append(new_gene)
            else:
                new_chromosome.append(gene)
        return GEP(new_chromosome)

```

### Crossover
For crossover, (we assumed that heads are a fixed length string) thus we can do a simpel signel point crossover.

``` python

class GEPCrossover:
    def crossover(self, parent1: GEP, parent2: GEP):
        # Ensure both parents are of the same length
        assert len(parent1) == len(parent2), "Parents must have the same length"
        
        # Randomly select a crossover point
        crossover_point = random.randint(1, len(parent1) - 1)
        


        # Perform crossover
        child1 = parent1.exp[:crossover_point] + parent2.exp[crossover_point:]
        child2 = parent2.exp[:crossover_point] + parent1.exp[crossover_point:]

        child1 = GEP(child1)
        child2 = GEP(child2)

        return [child1, child2]


```




script for GEP

``` python

import random

from src.GA.GeneticAlgorithm import GeneticAlgorithm
from src.GA.parent_selection.ElitistSelection import ElitistSelection
from src.GA.survivor_selection.HybridSelection import HybridSelection
from src.GA.mutation_strategy.MutationStrategy import AllMutation

from src.GEP.GEP import GEP
from src.GEP.GEPCrossover import GEPCrossover
from src.GEP.GEPMutation import GEPMutation
from src.GEP.GEPFitness import GEPFitness
from src.GEP.GEPFactory import GEPFactory

fitness_size_factor = 0.01

target_data = [(1,5), (2,17), (3, 43), (4, 85), (5, 145)]
tail_attempts = 20
mutation_rate = 0.2
head_length = 10
error = 0.1

def check_correctness(individual: GEP) -> bool:
    for x, y in target_data:
        y_pred = GEP.evaluate_exp(individual.exp + individual.best_tail, x)
        if abs(y - y_pred) > error:
            return False
    return True


if __name__ == '__main__':

    factory = GEPFactory(head_length)

    config = {
        'name': 'gep',
        'fitness_function': GEPFitness(target_data, tail_attempts, fitness_size_factor),
        'population_size': 200,
        'num_generations': 100,
        'num_islands': 10,
        'migration_rate': 10,
        'parent_selection': ElitistSelection(),
        'crossover_operator': GEPCrossover(),
        'mutation_operator': GEPMutation(mutation_rate),
        'survivor_selection': HybridSelection(0.8,0.2),
        'mutation_strategy': AllMutation(),
        'generate_population': factory.generate_population,
        'fitness_sharing': None
    }

    genetic_algorithm = GeneticAlgorithm(config)


    res = genetic_algorithm.evolve()

    genetic_algorithm.plot_fitness(True)

    # prin the fitness history
    best_individual = res['best_solution']
    best_solution_fitness = res['best_solution_fitness']

    print(f'Best individual: {best_individual}')
    print(f'Best solution fitness: {best_solution_fitness}')

    for x, y in target_data:
        y_pred = GEP.evaluate_exp(best_individual.exp + best_individual.best_tail, x)
        print(f'x: {x}, y: {y}, y_pred: {y_pred}')


    genetic_algorithm.plot_fitness(True)


```


here we have the GEPFactory class

``` python 

import random
from .GEP import GEP

class GEPFactory:

    def __init__(self, head_length: int):
        self.head_length = head_length

    @staticmethod
    def generate_random_chromosome(length: int) -> list[str]:
        return [random.choice(GEP.TERMINALS + GEP.FUNCTIONS) for _ in range(length)]

    @staticmethod
    def generate_random_tail(length: int) -> list[str]:
        return [random.choice(GEP.TERMINALS) for _ in range(length)]

    @staticmethod
    def generate_chromosome(head_length: int) -> list[str]:
        chromosome = []
        for _ in range(head_length):
            gene = random.choice(GEP.TERMINALS + GEP.FUNCTIONS)
            chromosome.append(gene)
        return chromosome
    
    @staticmethod
    def calc_needed_terminals(chromosome: list[str]) -> int:
        stack_size = 0
        missing = 0
        for gene in reversed(chromosome):
            if gene in GEP.TERMINALS:
                stack_size += 1
            else:
                stack_size -= 2
                if stack_size < 0:
                    missing += -stack_size
                    stack_size = 0
                stack_size += 1
        return missing
            
    @staticmethod
    def calc_size(chromosome: list[str]) -> int:
        size = 0
        for gene in reversed(chromosome):
            if gene in GEP.FUNCTIONS:
                size += 2
        return size

    @staticmethod
    def generate_tail(head: list[str]) -> list[str]:
        missing = GEPFactory.calc_needed_terminals(head)
        tail = GEPFactory.generate_random_tail(missing)
        return tail



    def generate_population(self, size: int) -> list[GEP]:
        return [GEP(GEPFactory.generate_chromosome(self.head_length)) for _ in range(size)]

```


terminal result for nand GP: 'nand_res.png'
terminal result for gpa: 'gpa_res.png'
terminal result for gep: 'gep_res.png'

fitness data plot for GP xor: 'gp_xor_fitness_summary_plot.png'
gpa fitness data: 'gpa_fitness_summary_plot.png'
gep fitness: 'gep_fitness_summary_plot.png'


size of sleected nodes plot: 'size_distribution.png'
depth of selected nodes plot: 'size_distribution-2.png'
