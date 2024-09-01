import random 


class MutationStrategy:
    def should_mutate(self, mutation_config):
        raise NotImplementedError("Mutation strategy must implement the should_mutate method.")

class AllMutation(MutationStrategy):
    def should_mutate(self, mutation_config):
        return True

class BasicMutation(MutationStrategy):
    def __init__(self, mutation_prob):
        self.mutation_prob = mutation_prob

    def should_mutate(self, mutation_config):
        return random.random() < self.mutation_prob


class NonUniformMutation(MutationStrategy):
    def __init__(self, initial_prob, decay_rate):
        self.initial_prob = initial_prob
        self.decay_rate = decay_rate

    def should_mutate(self, mutation_config):
        mutation_prob = self.initial_prob * (1 - self.decay_rate * mutation_config['generation'])
        return random.random() < mutation_prob


class TriggeredHyperMutation(MutationStrategy):
    def __init__(self, base_prob, threshold, max_prob):
        self.base_prob = base_prob
        self.threshold = threshold
        self.max_prob = max_prob
        self.hyper_mutation = False
        self.prev_best_fitness = None

    def should_mutate(self, mutation_config):
        if self.prev_best_fitness is None:
            self.prev_best_fitness = mutation_config['best_fitness']
            return False
        if not self.hyper_mutation:
            # Check for stagnation
            if mutation_config['best_fitness'] - self.prev_best_fitness < self.threshold:
                self.hyper_mutation = True
                self.current_prob = self.max_prob
            else:
                self.current_prob = self.base_prob
        else:
            # Check if significant improvement has been made
            if mutation_config['best_fitness'] - self.prev_best_fitness >= self.threshold:
                self.hyper_mutation = False
                self.current_prob = self.base_prob

        self.prev_best_fitness = mutation_config['best_fitness']

        return random.random() < self.current_prob


class AdaptiveMutation(MutationStrategy):
    def __init__(self, base_prob):
        self.base_prob = base_prob

    def should_mutate(self, mutation_config):
        mutation_prob = self.base_prob * (1 - (mutation_config['individual_fitness'] / mutation_config['best_fitness']))
        return random.random() < mutation_prob


