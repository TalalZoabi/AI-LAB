
from .FitnessFunction import FitnessFunction

class BaseSortingNetworksFitness(FitnessFunction):
    def __init__(self, alpha, beta) -> None:
        self.alpha = alpha
        self.beta = beta

    def get_performance(self, individual, adversaries):
        hits = 0
        for adv in adversaries:
            arr = self.run_adversary(individual, adv)
            hits += 1 if all(arr[i] <= arr[i + 1] for i in range(len(arr) - 1)) else 0
        
        hit_percentage = hits / len(adversaries) * 100
        return hits, hit_percentage

    def run_adversary(self, individual, adversary):
        arr = [i for i in adversary]
        for i, j in individual:
            i = min(i, j)
            j = max(i, j)
            if arr[i] > arr[j]:
                arr[i], arr[j] = arr[j], arr[i]
        return arr



class SortingNetworksComplexFitness(BaseSortingNetworksFitness):
    def __init__(self, alpha, beta):
        super().__init__(alpha, beta)

    def evaluate(self, individual, adversaries):
        fitness = 0
        for adversary in adversaries:
            fitness += self.evaluate_adversary(individual, adversary)

        return fitness

    def evaluate_adversary(self, individual, adversary):
        arr = self.run_adversary(individual, adversary)
        
        misses = 0
        for i in range(len(arr) - 1):
            if arr[i] > arr[i + 1]:
                misses += 1
        

        correct = len(arr) - misses
        
        # Fitness is the number of correct comparisons minus the number of incorrect comparisons
        # We favor individuals that have more correct comparisons and smaller size
        return self.alpha * correct - self.beta * len(individual) 

    

    def max_fitness(self, array_size, adv_num):
        return array_size * adv_num
    
    def min_fitness(self, *args, **kwargs):
        return 0
    

class SortingNetworksSimpleFitness(BaseSortingNetworksFitness):
    def __init__(self, alpha, beta):
        super().__init__(alpha, beta)

    def evaluate(self, individual, adversaries):
        fitness = 0
        for adversary in adversaries:
            fitness += self.evaluate_adversary(individual, adversary)

        return fitness
    
    

    def evaluate_adversary(self, individual, adversary):
        arr = self.run_adversary(individual, adversary)

        correct = 1 if all(arr[i] <= arr[i + 1] for i in range(len(arr) - 1)) else 0 
        return self.alpha * correct - self.beta * len(individual)
    

    def max_fitness(self, array_size, adv_num):
        return self.alpha * adv_num
    
    def min_fitness(self, *args, **kwargs):
        return 0
    


class AdversarySimpleFitness(BaseSortingNetworksFitness):
    def __init__(self):
        pass
    # Fitness is the number of sorting networks the adversary can break
    def evaluate(self, adv, population):
        fitness = 0
        for ind in population:
            fitness += self.evaluate_individual(adv, ind)
        return fitness
    
    def evaluate_individual(self, adv, ind):
        arr = self.run_adversary(ind, adv)
        # Fitness is 1 if the sorting network fails to sort the array, 0 otherwise
        return 0 if all(arr[i] <= arr[i + 1] for i in range(len(arr) - 1)) else 1
    
    def max_fitness(self, array_size, adv_num):
        return adv_num
    
    def min_fitness(self, *args, **kwargs):
        return 0

class AdversaryComplexFitness(BaseSortingNetworksFitness):
    def __init__(self):
        pass

    # Fitness is the sum of mismatches the adversary can cause to the sorting networks
    def evaluate(self, adv, population):
        fitness = 0
        for ind in population:
            fitness += self.evaluate_individual(adv, ind)
        return fitness
    
    # Evaluate the number of mismatches the adversary can cause to a single sorting network
    # More mismatches means a higher fitness (i.e. the adversary is more effective)
    def evaluate_individual(self, adv, ind):
        arr = self.run_adversary(ind, adv)

        misses = 0
        for i in range(len(arr) - 1):
            if arr[i] > arr[i + 1]:
                misses += 1
        
        return misses

    def max_fitness(self, array_size, adv_num):
        return array_size * adv_num
    
    def min_fitness(self, *args, **kwargs):
        return 0












