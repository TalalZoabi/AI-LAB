import os
import logging
import numpy as np
import matplotlib.pyplot as plt


def analyze_results(results, plot_dir='plots', configurations=[]):
    if not os.path.exists(plot_dir):
        os.makedirs(plot_dir)
    
    all_data = []
    
    for result in results:
        # Debugging: Check the content of the result
        logging.info(f"Analyzing results for {result['name']}: {result}")
        
        population_fitness_matrix = np.array(result['population_fitnesses'])
        adversary_fitness_matrix = np.array(result['adversary_fitnesses'])

        # Log matrices shapes and first few elements for debugging
        logging.info(f"Population fitness matrix shape: {population_fitness_matrix.shape}")
        logging.info(f"Adversary fitness matrix shape: {adversary_fitness_matrix.shape}")
        logging.info(f"Population fitness matrix (first few elements): {population_fitness_matrix[:2, :5]}")
        logging.info(f"Adversary fitness matrix (first few elements): {adversary_fitness_matrix[:2, :5]}")
        
        # Calculate metrics
        avg_population_fitness = np.mean(population_fitness_matrix, axis=1)
        avg_adversary_fitness = np.mean(adversary_fitness_matrix, axis=1)
        best_population_fitness = np.max(population_fitness_matrix, axis=1)
        best_adversary_fitness = np.max(adversary_fitness_matrix, axis=1)
        var_population_fitness = np.var(population_fitness_matrix, axis=1)
        var_adversary_fitness = np.var(adversary_fitness_matrix, axis=1)

        best_individual_length = len(result['best_solution'])
        performance_percentage = result['performance']

        # Calculate gradients if array length is sufficient
        if len(avg_population_fitness) > 1:
            pop_convergence_rate = np.gradient(avg_population_fitness)
        else:
            pop_convergence_rate = [0] * len(avg_population_fitness)
        
        if len(avg_adversary_fitness) > 1:
            adv_convergence_rate = np.gradient(avg_adversary_fitness)
        else:
            adv_convergence_rate = [0] * len(avg_adversary_fitness)

        # Store data for comparison and saving
        run_data = {
            'label': result['name'],
            'avg_population_fitness': avg_population_fitness,
            'avg_adversary_fitness': avg_adversary_fitness,
            'best_population_fitness': best_population_fitness,
            'best_adversary_fitness': best_adversary_fitness,
            'var_population_fitness': var_population_fitness,
            'var_adversary_fitness': var_adversary_fitness,
            'best_individual_length': best_individual_length,
            'performance_percentage': performance_percentage,
            'pop_convergence_rate': pop_convergence_rate,
            'adv_convergence_rate': adv_convergence_rate
        }

        all_data.append(run_data)

        # Plot results for this configuration in a tight layout
        plt.figure(figsize=(18, 10))
        
        # Average Fitness Plot
        plt.subplot(2, 2, 1)
        if len(avg_population_fitness) > 0:
            plt.plot(avg_population_fitness, label='Population')
        if len(avg_adversary_fitness) > 0:
            plt.plot(avg_adversary_fitness, label='Adversary', linestyle='--')
        plt.xlabel('Generations')
        plt.ylabel('Average Fitness')
        plt.title(f'Average Fitness Over Generations - {result["name"]}')
        plt.legend()

        # Best Fitness Plot
        plt.subplot(2, 2, 2)
        if len(best_population_fitness) > 0:
            plt.plot(best_population_fitness, label='Best Population')
        if len(best_adversary_fitness) > 0:
            plt.plot(best_adversary_fitness, label='Best Adversary', linestyle='--')
        plt.xlabel('Generations')
        plt.ylabel('Best Fitness')
        plt.title(f'Best Fitness Over Generations - {result["name"]}')
        plt.legend()

        # Variance Plot
        plt.subplot(2, 2, 3)
        if len(var_population_fitness) > 0:
            plt.plot(var_population_fitness, label='Population Variance')
        if len(var_adversary_fitness) > 0:
            plt.plot(var_adversary_fitness, label='Adversary Variance', linestyle='--')
        plt.xlabel('Generations')
        plt.ylabel('Fitness Variance')
        plt.title(f'Fitness Variance Over Generations - {result["name"]}')
        plt.legend()

        # Convergence Rate Plot
        plt.subplot(2, 2, 4)
        if len(pop_convergence_rate) > 0:
            plt.plot(pop_convergence_rate, label='Population Convergence Rate')
        if len(adv_convergence_rate) > 0:
            plt.plot(adv_convergence_rate, label='Adversary Convergence Rate', linestyle='--')
        plt.xlabel('Generations')
        plt.ylabel('Convergence Rate')
        plt.title(f'Convergence Rate Over Generations - {result["name"]}')
        plt.legend()

        plt.tight_layout()
        plt.savefig(f"{plot_dir}/{result['name']}_fitness_plots.png")
        plt.close()

    return all_data
