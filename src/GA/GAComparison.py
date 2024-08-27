import time
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable
import numpy as np

from .GeneticAlgorithm import GeneticAlgorithm


class GAComparison:
    def __init__(self, configurations):
        self.configurations = configurations
        self.results = {}
    
    def run(self):
        for config in self.configurations:
            ga = GeneticAlgorithm(config)
            ga.run()
            self.results[config['name']] = ga.get_results()



    def plot_results(self):
        plt.figure(figsize=(18, 12))
        colors = plt.cm.viridis(np.linspace(0, 1, len(self.configurations)))
        
        # Plot best fitnesses
        plt.subplot(3, 3, 1)
        for color, (config_name, data) in zip(colors, self.results.items()):
            generations = range(len(data['best_fitnesses']))
            plt.plot(generations, data['best_fitnesses'], color=color, label=config_name)
        plt.title('Best Fitness over Generations')
        plt.xlabel('Generation')
        plt.ylabel('Best Fitness')
        plt.legend()
        
        # Plot average fitnesses
        plt.subplot(3, 3, 2)
        for color, (config_name, data) in zip(colors, self.results.items()):
            generations = range(len(data['avg_fitnesses']))
            plt.plot(generations, data['avg_fitnesses'], color=color, label=config_name)
        plt.title('Average Fitness over Generations')
        plt.xlabel('Generation')
        plt.ylabel('Average Fitness')
        plt.legend()
        
        # Plot scaled average fitnesses
        plt.subplot(3, 3, 3)
        for color, (config_name, data) in zip(colors, self.results.items()):
            generations = range(len(data['scaled_avg_fitnesses']))
            plt.plot(generations, data['scaled_avg_fitnesses'], color=color, label=config_name)
        plt.title('Scaled Average Fitness over Generations')
        plt.xlabel('Generation')
        plt.ylabel('Scaled Average Fitness')
        plt.legend()
        
        # Plot standard deviations
        plt.subplot(3, 3, 4)
        for color, (config_name, data) in zip(colors, self.results.items()):
            generations = range(len(data['std_devs']))
            plt.plot(generations, data['std_devs'], color=color, label=config_name)
        plt.title('Standard Deviation of Fitness over Generations')
        plt.xlabel('Generation')
        plt.ylabel('Standard Deviation')
        plt.legend()
        
        # Plot runtime per generation
        plt.subplot(3, 3, 5)
        for color, (config_name, data) in zip(colors, self.results.items()):
            generations = range(len(data['runtimes']))
            plt.plot(generations, data['runtimes'], color=color, label=config_name)
        plt.title('Runtime per Generation')
        plt.xlabel('Generation')
        plt.ylabel('Runtime (seconds)')
        plt.legend()
        
        # Plot diversities
        plt.subplot(3, 3, 6)
        for color, (config_name, data) in zip(colors, self.results.items()):
            generations = range(len(data['diversities']))
            plt.plot(generations, data['diversities'], color=color, label=config_name)
        plt.title('Diversity over Generations')
        plt.xlabel('Generation')
        plt.ylabel('Diversity')
        plt.legend()
        
        # Plot convergence generations
        plt.subplot(3, 3, 7)
        convergence_generations = [data['convergence_generation'] for data in self.results.values()]
        plt.bar(self.results.keys(), convergence_generations, color=colors)
        plt.title('Convergence Generation')
        plt.xlabel('Configuration')
        plt.ylabel('Generation of Convergence')
        
        plt.tight_layout()
        plt.show()





