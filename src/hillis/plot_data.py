import os
import json
import logging
import numpy as np
import matplotlib.pyplot as plt

def plot_comparison(all_data, plot_dir='plots'):
    if not os.path.exists(plot_dir):
        os.makedirs(plot_dir)

    plt.figure(figsize=(18, 10))
    plt.suptitle('Comparison of Average Fitness Across Configurations')

    for data in all_data:
        if len(data['avg_population_fitness']) > 0:
            plt.plot(data['avg_population_fitness'], label=f'{data["label"]} - Pop')
        if len(data['avg_adversary_fitness']) > 0:
            plt.plot(data['avg_adversary_fitness'], linestyle='--', label=f'{data["label"]} - Adv')
    
    plt.xlabel('Generations')
    plt.ylabel('Average Fitness')
    plt.legend()
    plt.tight_layout()
    plt.savefig(f'{plot_dir}/comparison_avg_fitness.png')
    plt.close()

    plt.figure(figsize=(18, 10))
    plt.suptitle('Comparison of Best Fitness Across Configurations')

    for data in all_data:
        if len(data['best_population_fitness']) > 0:
            plt.plot(data['best_population_fitness'], label=f'{data["label"]} - Best Pop')
        if len(data['best_adversary_fitness']) > 0:
            plt.plot(data['best_adversary_fitness'], linestyle='--', label=f'{data["label"]} - Best Adv')
    
    plt.xlabel('Generations')
    plt.ylabel('Best Fitness')
    plt.legend()
    plt.tight_layout()
    plt.savefig(f'{plot_dir}/comparison_best_fitness.png')
    plt.close()

    plt.figure(figsize=(18, 10))
    plt.suptitle('Comparison of Fitness Variance Across Configurations')

    for data in all_data:
        if len(data['var_population_fitness']) > 0:
            plt.plot(data['var_population_fitness'], label=f'{data["label"]} - Pop Variance')
        if len(data['var_adversary_fitness']) > 0:
            plt.plot(data['var_adversary_fitness'], linestyle='--', label=f'{data["label"]} - Adv Variance')
    
    plt.xlabel('Generations')
    plt.ylabel('Fitness Variance')
    plt.legend()
    plt.tight_layout()
    plt.savefig(f'{plot_dir}/comparison_fitness_variance.png')
    plt.close()

    plt.figure(figsize=(12, 6))
    plt.bar([data['label'] for data in all_data], [data['best_individual_length'] for data in all_data], alpha=0.7, label='Best Individual Length')
    plt.ylabel('Length')
    plt.title('Best Individual Length Across Configurations')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.savefig(f'{plot_dir}/best_individual_length.png')
    plt.close()

    plt.figure(figsize=(12, 6))
    plt.bar([data['label'] for data in all_data], [data['performance_percentage'] for data in all_data], alpha=0.7, color='orange', label='Performance Percentage')
    plt.ylabel('Performance (%)')
    plt.title('Performance Percentage of Best Individuals Across Configurations')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.savefig(f'{plot_dir}/performance_percentage.png')
    plt.close()
