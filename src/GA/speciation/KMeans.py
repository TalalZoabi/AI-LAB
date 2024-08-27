import numpy as np
from sklearn.cluster import KMeans

from .Speciation import Speciation

class KMeansSpeciation(Speciation):
    def __init__(self, num_clusters, distance_func):
        super().__init__(distance_func)
        self.num_clusters = num_clusters

    def apply_speciation(self, population):
        # Calculate the distance matrix
        distance_matrix = np.array([[self.distance_func(ind_i, ind_j) for ind_j in population] for ind_i in population])
        
        # Use KMeans clustering
        kmeans = KMeans(n_clusters=self.num_clusters)
        labels = kmeans.fit_predict(distance_matrix)
        
        # Group individuals into species based on labels
        species = [[] for _ in range(self.num_clusters)]
        for i, label in enumerate(labels):
            species[label].append(i)
        
        return species
