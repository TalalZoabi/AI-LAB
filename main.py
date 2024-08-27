import os
import logging
import json
import pandas as pd



from src.hillis.configs import get_k16_configurations,   get_k6_configurations
from src.hillis.collect_data import analyze_results
from src.hillis.plot_data import plot_comparison
from src.hillis.multi_run import run_experiments


# Setup logging
logging.basicConfig(
    level=logging.ERROR,  # Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Format of the logs
)


def save_best_solutions(results, num_elements, plot_dir='plots'):
    if not os.path.exists(plot_dir):
        os.makedirs(plot_dir)

    best = []

    for result in results:
        best_individual = result['best_solution']
        performance_percentage = result['performance']
        
        best.append({'individual': best_individual, 'performance': performance_percentage, 'label': result['name']})

    # Save to json file
    with open(f'{plot_dir}/best_solutions.json', 'w') as f:
        json.dump(best, f, indent=4)

def save_full_data(all_data, filename='experiment_results.csv'):
    # Flatten the data and save it to a CSV file
    flat_data = []
    for data in all_data:
        for i in range(len(data['avg_population_fitness'])):
            flat_data.append({
                'label': data['label'],
                'generation': i,
                'avg_population_fitness': data['avg_population_fitness'][i],
                'avg_adversary_fitness': data['avg_adversary_fitness'][i],
                'best_population_fitness': data['best_population_fitness'][i],
                'best_adversary_fitness': data['best_adversary_fitness'][i],
                'var_population_fitness': data['var_population_fitness'][i],
                'var_adversary_fitness': data['var_adversary_fitness'][i],
                'convergence_rate_population': data['pop_convergence_rate'][i],
                'convergence_rate_adversary': data['adv_convergence_rate'][i],
                'best_individual_length': data['best_individual_length'],
                'performance_percentage': data['performance_percentage']
            })

    df = pd.DataFrame(flat_data)
    df.to_csv(filename, index=False)
    logging.info(f"Full data saved to {filename}")



def main():


    k_6_configurations = get_k6_configurations()
    k_16_configurations = get_k16_configurations()

    print("Number of K=6 configurations to run:", len(k_6_configurations))
    print("Number of K=16 configurations to run:", len(k_16_configurations))

    # Run experiments for each configuration    
    k_6_results = run_experiments(k_6_configurations)
    k_16_results = run_experiments(k_16_configurations)

    # Save results to JSON file
    with open('results_6.json', 'w') as f:
        json.dump(k_6_results, f, indent=4)
    
    with open('results_16.json', 'w') as f:
        json.dump(k_16_results, f, indent=4)


    # Analyze results and plot data
    k_6_all_data = analyze_results(k_6_results, 'plots_6', configurations=k_6_configurations)
    k_16_all_data = analyze_results(k_16_results, 'plots_16', configurations=k_16_configurations)

    plot_comparison(k_6_all_data, 'plots_6')
    plot_comparison(k_16_all_data, 'plots_16')

    # Save best solutions
    save_best_solutions(k_6_results, 6, 'plots_6')
    save_best_solutions(k_16_results, 16, 'plots_16')


    # Save full data
    save_full_data(k_6_all_data, 'experiment_results_6.csv')
    save_full_data(k_16_all_data, 'experiment_results_16.csv')

if __name__ == '__main__':
    main()