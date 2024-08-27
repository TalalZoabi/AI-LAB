import random
from .ParentSelectionMethod import ParentSelectionMethod


class RWSRankingSelection(ParentSelectionMethod):
    def __init__(self, scaling_strategy):
        self.scaling_strategy = scaling_strategy

    def select(self, population, fitnesses, num_parents):
        # Rank the individuals based on fitness
        sorted_population = [x for _, x in sorted(zip(fitnesses, population), reverse=True)]
        ranks = list(range(1, len(population) + 1))
        
        # Apply linear scaling to ranks
        scaled_ranks = self.scaling_strategy.scale(ranks)
        total_rank = sum(scaled_ranks)
        selection_probs = [rank / total_rank for rank in scaled_ranks]
        
        # Select parents based on scaled ranks
        selected_parents = random.choices(sorted_population, weights=selection_probs, k=num_parents)
        return selected_parents

