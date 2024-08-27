import concurrent.futures
import time
import logging

from src.GA.CoevolutionaryAlgorithm import CoevolutionaryAlgorithm

# Function to run a single instance of the co-evolutionary algorithm
def run_instance(config):
    ce = CoevolutionaryAlgorithm(config)
    results = ce.evolve()

    # Ensure the result structure is as expected
    if not all(key in results for key in ['population_fitnesses', 'adversary_fitnesses', 'best_solution', 'performance']):
        raise ValueError("Results missing required keys")

    return results

# Function to run experiments concurrently
def run_experiments(configurations):
    results = []
    start_time = time.perf_counter()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {executor.submit(run_instance, config): idx for idx, config in enumerate(configurations)}

        for future in concurrent.futures.as_completed(futures):
            idx = futures[future]
            config = configurations[idx]
            
            result = future.result()
            results.append(result)
            # Log the result for this configuration
            # logging.info(f'Result for configuration {config["name"]}: {result}')
        
            elapsed_time = time.perf_counter() - start_time
            avg_time_per_config = elapsed_time / (len(results) + 1)
            remaining_time = avg_time_per_config * (len(configurations) - len(results))
            logging.info(f'Completed {len(results)}/{len(configurations)}. Estimated time remaining: {remaining_time:.2f} seconds')

    return results