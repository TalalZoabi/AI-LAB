import random
import logging
from .MutationOperator import MutationOperator

from ...utils.compare import compare_comparrisons

class SortingNetworksMutation(MutationOperator):
    def __init__(self, max_index) -> None:
        self.max_index = max_index
    
    def mutate(self, candidate, *args, **kwargs):
        mutation_type = random.choice(['add', 'remove', 'modify', 'flip', 'subsequence', 'reinsert', 'simplify'])
        logging.debug(f"Applying {mutation_type} mutation")

        if mutation_type == 'add':
            self.add_mutation(candidate)
        
        elif mutation_type == 'remove':
            self.remove_mutation(candidate)
        
        elif mutation_type == 'modify':
            self.modify_mutation(candidate)
        
        elif mutation_type == 'flip':
            self.flip_mutation(candidate)

        elif mutation_type == 'subsequence':
            self.subsequence_mutation(candidate)

        elif mutation_type == 'reinsert':
            self.reinsert_mutation(candidate)

        elif mutation_type == 'simplify':
            self.simplify_mutation(candidate)

        return candidate
    
    def add_mutation(self, candidate):
        i, j = random.sample(range(self.max_index), 2)
        candidate.append((i, j))
    
    def remove_mutation(self, candidate):
        if candidate:
            candidate.pop(random.randint(0, len(candidate) - 1))

    def modify_mutation(self, candidate):
        if candidate:
            index = random.randint(0, len(candidate) - 1)
            i, j = random.sample(range(self.max_index), 2)
            candidate[index] = (i, j)
    
    def flip_mutation(self, candidate):
        if candidate:
            index = random.randint(0, len(candidate) - 1)
            i, j = candidate[index]
            candidate[index] = (j, i)
    
    def subsequence_mutation(self, candidate):
        if len(candidate) > 1:
            start = random.randint(0, len(candidate) - 2)
            end = random.randint(start + 1, len(candidate) - 1)
            subsequence = candidate[start:end + 1]
            random.shuffle(subsequence)
            candidate[start:end + 1] = subsequence
    
    def reinsert_mutation(self, candidate):
        if len(candidate) > 1:
            index = random.randint(0, len(candidate) - 1)
            operation = candidate.pop(index)
            insert_position = random.randint(0, len(candidate))
            candidate.insert(insert_position, operation)

    def simplify_mutation(self, candidate):
        # Attempt to reduce complexity by removing redundant or unnecessary comparisons
        if len(candidate) > 1:
            candidate = self.remove_redundant_comparisons(candidate)

    def remove_redundant_comparisons(self, candidate):
        # remove consecutive comparisons that are redundant
        # if 2 consecutive comparisons are the same, remove one of them
        # example candidate [(1,0), (2,3), (2,3)] -> [(1,0), (2,3)]
        i = 0
        while i < len(candidate) - 1:
            if compare_comparrisons(candidate[i], candidate[i + 1]):
                candidate.pop(i)
            else:
                i += 1
