import random
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import plotly.graph_objects as go

from .Problem import Problem


class BinPacking(Problem):
    def __init__(self, items, bin_capacity):
        self.items = items
        self.bin_capacity = bin_capacity

    def initialize_population(self, population_size):
        population = []
        for _ in range(population_size):
            individual = random.sample(self.items, len(self.items))
            population.append(individual)
        return population
    
    def distance(self, individual1, individual2):
        set1 = set(individual1)
        set2 = set(individual2)
        intersection = len(set1 & set2)
        union = len(set1 | set2)
        return 1 - intersection / union
    
    def distance_unit(self):
        return "Jaccard distance"

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



    def display_individual(self, individual):
        bins = self.pack_bins(individual)
        num_bins = len(bins)

        # Create a DataFrame to display the bin packing
        bin_data = []
        for i, bin in enumerate(bins):
            bin_str = ', '.join(str(item) for item in bin)
            fullness = sum(bin)
            bin_data.append([f'Bin {i+1}', bin_str, f'{fullness}/{self.bin_capacity}'])

        df = pd.DataFrame(bin_data, columns=['Bin', 'Items', 'Fullness'])

        # Plot the DataFrame as an interactive table using Plotly
        fig = go.Figure(data=[go.Table(
            header=dict(values=list(df.columns),
                        fill_color='paleturquoise',
                        align='left'),
            cells=dict(values=[df.Bin, df.Items, df.Fullness],
                       fill_color='lavender',
                       align='left'))
        ])

        fig.update_layout(title=f'Bin Packing Solution - {num_bins} Bins Used',
                          height=600,  # Adjust height as necessary for scrolling
                          margin=dict(l=0, r=0, t=40, b=0))

        fig.show()

