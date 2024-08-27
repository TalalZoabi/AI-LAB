import random
from src.problems.CVRP import CVRP
from src.problems.Ackley import Ackley

class ALNS:
    def __init__(self, problem, num_iterations, destruction_rate, repair_rate, initial_solution_method='greedy', destruction_method='random', repair_method='greedy'):
        self.problem = problem
        self.num_iterations = num_iterations
        self.destruction_rate = destruction_rate
        self.repair_rate = repair_rate
        self.initial_solution_method = initial_solution_method
        self.destruction_method = destruction_method
        self.repair_method = repair_method
        self.operators = self.initialize_operators()
        self.operator_scores = {op: 1 for op in list(self.operators['destruction'].values()) + list(self.operators['repair'].values())}
        self.operator_probabilities = {op: 1 / len(self.operator_scores) for op in self.operator_scores}

    def initialize_operators(self):
        # Initialize destruction and repair operators
        return {
            'destruction': {
                'random': self.destroy_random,
                'worst': self.destroy_worst,
                'cluster': self.destroy_cluster
            },
            'repair': {
                'greedy': self.repair_greedy,
                'random': self.repair_random,
                'nearest': self.repair_nearest
            }
        }

    def destroy_random(self, solution):
        num_to_remove = int(len(solution) * self.destruction_rate)
        if isinstance(self.problem, CVRP):
            customers = [c for c in solution if c != 0]
        elif isinstance(self.problem, Ackley):
            customers = solution
        customers = list(customers)  # Ensure customers is a list
        removed_customers = random.sample(customers, num_to_remove)
        new_solution = [c for c in solution if c not in removed_customers]
        return new_solution, removed_customers

    def destroy_worst(self, solution):
        num_to_remove = int(len(solution) * self.destruction_rate)
        if isinstance(self.problem, CVRP):
            customers = [c for c in solution if c != 0]
            customer_contributions = [(c, self.problem.evaluate_fitness([c])) for c in customers]
        elif isinstance(self.problem, Ackley):
            customers = solution
            customer_contributions = [(c, self.problem.evaluate([c])) for c in customers]
        customer_contributions.sort(key=lambda x: x[1], reverse=True)
        removed_customers = [c[0] for c in customer_contributions[:num_to_remove]]
        new_solution = [c for c in solution if c not in removed_customers]
        return new_solution, removed_customers

    def destroy_cluster(self, solution):
        num_to_remove = int(len(solution) * self.destruction_rate)
        if isinstance(self.problem, CVRP):
            customers = [c for c in solution if c != 0]
            cluster_center = random.choice(customers)
            cluster_center_location = self.problem.customer_locations[cluster_center]
            distances = [(c, self.problem.distance(cluster_center_location, self.problem.customer_locations[c])) for c in customers]
        elif isinstance(self.problem, Ackley):
            customers = solution
            cluster_center = random.choice(customers)
            distances = [(c, abs(cluster_center - c)) for c in customers]
        distances.sort(key=lambda x: x[1])
        removed_customers = [c[0] for c in distances[:num_to_remove]]
        new_solution = [c for c in solution if c not in removed_customers]
        return new_solution, removed_customers

    def repair_greedy(self, solution, removed_customers):
        for customer in removed_customers:
            best_position = None
            best_increase = float('inf')
            for i in range(1, len(solution)):
                new_solution = solution[:i] + [customer] + solution[i:]
                if isinstance(self.problem, CVRP):
                    increase = self.problem.evaluate_fitness(new_solution) - self.problem.evaluate_fitness(solution)
                elif isinstance(self.problem, Ackley):
                    increase = self.problem.evaluate(new_solution) - self.problem.evaluate(solution)
                if increase < best_increase:
                    best_increase = increase
                    best_position = i
            solution.insert(best_position, customer)
        return solution

    def repair_random(self, solution, removed_customers):
        for customer in removed_customers:
            position = random.randint(1, len(solution) - 1)
            solution.insert(position, customer)
        return solution

    def repair_nearest(self, solution, removed_customers):
        for customer in removed_customers:
            best_position = None
            best_increase = float('inf')
            for i in range(1, len(solution)):
                if isinstance(self.problem, CVRP):
                    prev_location = self.problem.customer_locations[solution[i-1]]
                    next_location = self.problem.customer_locations[solution[i]]
                    customer_location = self.problem.customer_locations[customer]
                    increase = (
                        self.problem.distance(prev_location, customer_location) +
                        self.problem.distance(customer_location, next_location) -
                        self.problem.distance(prev_location, next_location)
                    )
                elif isinstance(self.problem, Ackley):
                    increase = abs(solution[i-1] - customer) + abs(customer - solution[i]) - abs(solution[i-1] - solution[i])
                if increase < best_increase:
                    best_increase = increase
                    best_position = i
            solution.insert(best_position, customer)
        return solution

    def adapt_operators(self):
        # Update operator probabilities based on their scores
        total_score = sum(self.operator_scores.values())
        if total_score > 0:
            for op in self.operator_scores:
                self.operator_probabilities[op] = self.operator_scores[op] / total_score
        else:
            # Handle the case where total_score is zero
            for op in self.operator_scores:
                self.operator_probabilities[op] = 1 / len(self.operator_scores)  # Distribute probabilities evenly

    def select_operator(self, operators):
        # Select an operator based on its probability
        return random.choices(list(operators.values()), weights=[self.operator_probabilities[op] for op in operators.values()])[0]

    def solve(self):
        current_solution = self.problem.generate_initial_solution(self.initial_solution_method)
        best_solution = current_solution
        if isinstance(self.problem, CVRP):
            best_fitness = self.problem.evaluate_fitness(current_solution)
        elif isinstance(self.problem, Ackley):
            best_fitness = self.problem.evaluate(current_solution)

        for iteration in range(self.num_iterations):
            destruction_operator = self.operators['destruction'][self.destruction_method]
            repair_operator = self.operators['repair'][self.repair_method]

            destroyed_solution, removed_customers = destruction_operator(current_solution)
            repaired_solution = repair_operator(destroyed_solution, removed_customers)
            if isinstance(self.problem, CVRP):
                repaired_fitness = self.problem.evaluate_fitness(repaired_solution)
            elif isinstance(self.problem, Ackley):
                repaired_fitness = self.problem.evaluate(repaired_solution)

            if repaired_fitness < best_fitness:
                best_solution = repaired_solution
                best_fitness = repaired_fitness
                self.operator_scores[destruction_operator] += 1
                self.operator_scores[repair_operator] += 1
            else:
                self.operator_scores[destruction_operator] -= 1
                self.operator_scores[repair_operator] -= 1

            current_solution = repaired_solution
            self.adapt_operators()

        return best_solution, best_fitness