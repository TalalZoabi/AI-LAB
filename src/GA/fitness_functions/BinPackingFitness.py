from .FitnessFunction import FitnessFunction


class BinPackingFitness(FitnessFunction):
    def __init__(self, bin_capacity, weight_bins_used=1.0, weight_total_waste=1.0, weight_load_balance=1.0):
        self.bin_capacity = bin_capacity
        self.weight_bins_used = weight_bins_used
        self.weight_total_waste = weight_total_waste
        self.weight_load_balance = weight_load_balance

    def evaluate(self, individual):
        bins = self.pack_bins(individual)
        num_bins_used = len(bins)
        total_waste = sum(self.bin_capacity - sum(bin) for bin in bins)
        bin_loads = [sum(bin) for bin in bins]
        load_balance = max(bin_loads) - min(bin_loads) if bin_loads else 0

        # Combine the factors into a single fitness score
        fitness = (self.weight_bins_used * num_bins_used +
                   self.weight_total_waste * total_waste +
                   self.weight_load_balance * load_balance)

        # Since we want to minimize these factors, return the negative fitness value for maximization
        return -fitness

    def pack_bins(self, individual):
        bins = []
        for item in individual:
            placed = False
            for bin in bins:
                if sum(bin) + item <= self.bin_capacity:
                    bin.append(item)
                    placed = True
                    break
            if not placed:
                bins.append([item])
        return bins
    
    def min_fitness(self, *args, **kwargs):
        # The worst-case fitness (max number of bins and maximum waste)
        items = kwargs.get('items', [])
        max_bins_used = len(items)  # Each item in its own bin
        max_total_waste = max_bins_used * self.bin_capacity - sum(items)
        return -(self.weight_bins_used * max_bins_used + self.weight_total_waste * max_total_waste + self.weight_load_balance * (self.bin_capacity - min(items)))

    def max_fitness(self, *args, **kwargs):
        # The best-case fitness (minimum number of bins and minimum waste)
        items = kwargs.get('items', [])
        min_bins_used = sum(items) // self.bin_capacity + (1 if sum(items) % self.bin_capacity > 0 else 0)
        min_total_waste = self.bin_capacity - min(items)
        return -(self.weight_bins_used * min_bins_used + self.weight_total_waste * min_total_waste + self.weight_load_balance * 0)



