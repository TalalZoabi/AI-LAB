# Coevolution
As stated we needed to use coevolutionary algorithm to generate the sorting networks for numbers.

So we had to integrate the idea into our existing code base.

# Our implementation of coevolution
Because of the way we implemented GA in the previous assignments, we are able to set different and varying operators and methods for each component.

The coevolution differs from the old implementation because we need to manage two populations, which will interact with each other throughout the search.

# Representing the populations

## Introduction
As stated in the assignment doc, we would need to manage two populations:
- Individuals: the sorting networks
- Adversaries: the vectors (the parasites)

The individual population is what we seek to build, and the parasite or adversary population is made up of tests for the individuals.

This way we evolve new and better networks while also evolving harder and more complex challenges.

## Representations

### Individuals
A sorting network is represented as a list of comparison operations, where at every step we compare (and swap) the values in the given indices.

Example:

```python
[(1,2), (1,4)]
```

This network compares `arr[1]` and `arr[2]`. If `arr[1] > arr[2]`, then we swap the values; otherwise, we continue to the next comparison.

This allows for a compact and simple way of representing the network.

The implementation of creating an individual sorting network is as follows:

```python:src/problems/SortingNetworks.py
startLine: 0
endLine: 25
```

### Adversaries
An adversary (parasite) is represented via a fixed-size vector (array/list) that contains numbers.

This acts as a test array for a sorting network where we can examine a sorting network's correctness by running tests on it.

Example: `[1, 5, 4, -2, 10]`

This also allows for simple representation and creation of more 'tests'.

The implementation of creating an adversarial individual is as follows:

```python:src/problems/SortingNetworks.py
startLine: 0
endLine: 25
```

# Fitness Calculation

Since the two populations interact with each other, and the way we defined the two populations, the fitness calculation of one population will depend on the other population (or a sample of the other population).

## Individual Population Fitness
To calculate fitness, we needed to consider two things:
1. Sorting network size: prioritize finding smaller networks that sort the arrays.
2. Sorting network correctness: given an array, the sorting network can sort it successfully.

In order to create a balance/variance, we added alpha and beta parameters so we can choose what aspect to focus on more (higher alpha values mean that correctness has more weight, while higher beta values mean that network size has more weight).

We added two methods to measure fitness for population individual fitness:
1. Simple fitness: given a sample of the adversary parasite population, we run each test on the network and count the number of successes (i.e., the number of tests that result in a sorted array). We also consider the network size, and the final formula is:

```python
alpha * correct_count - beta * network_length
```

This way we can test out the different effects with varying values.

2. Complex fitness: given a sample of the adversary parasite population, we run each test on the network. We calculate the number of 'misses' (i.e., how far the result is from a sorted array).

The distance from a sorted array is calculated as the number of elements that make the array 'not sorted' (i.e., if `arr[i] > arr[i+1]`, then index `i` adds to the misses count). This allows us to use a deeper and better method to network for small improvements.

The final fitness is calculated as:

```python
alpha * hits_count - beta * network_length
```

where `hits_count = network_length - misses_count` (as explained before).

The implementation of the fitness functions is as follows:

```python:src/GA/fitness_functions/SortingNetworksFitness.py
startLine: 1
endLine: 144
```

## Adversary Population Fitness

To calculate adversary fitness, we need to consider only one thing:
1. Hardness: i.e., the number of sorting networks this test challenges (produces a wrong answer).

The more networks the test breaks, the better fitness it has (better test).

This made us add two methods to calculate adversary fitness (inspired by population fitness):

1. Simple fitness: i.e., the number of networks the adversary breaks (integer value).

We run each network from the sample on the test, and the more non-sorted results mean higher fitness.

2. Complex fitness: i.e., the number of misses the test causes a sorting network to have (refer to complex individual fitness for reference).

The implementation of the adversary fitness functions is as follows:

```python:src/GA/fitness_functions/SortingNetworksFitness.py
startLine: 1
endLine: 144
```

# Mutation Operators

Mutation operators are crucial in the genetic algorithm as they introduce variability into the population, helping to explore the search space more effectively. In our implementation, we used different mutation operators for the sorting networks and adversaries.

## Sorting Networks Mutation

The mutation operator for sorting networks is implemented in `SortingNetworksMutation.py`. This operator can add, remove, or modify comparisons in a sorting network.

```typescript:src/GA/mutation_operator/SortingNetworksMutation.py
startLine: 2
endLine: 30
```

- **Add Mutation**: Adds a new random comparison to the sorting network.
- **Remove Mutation**: Removes a random comparison from the sorting network.
- **Modify Mutation**: Modifies an existing comparison in the sorting network.

## Adversary Mutation

The mutation operator for adversaries is implemented in `SimpleMutation.py`. This operator can modify the values in the adversary vector.

```typescript:src/GA/mutation_operator/SimpleMutation.py
startLine: 1
endLine: 20
```

- **Modify Mutation**: Modifies the values in the adversary vector based on a mutation rate.

# Crossover Operators

Crossover operators are essential in the genetic algorithm as they combine the genetic information of two parents to produce new offspring. In our implementation, we used different crossover operators for the sorting networks and adversaries.

## Sorting Networks Crossover

The crossover operator for sorting networks is implemented in `SortingNetworksCrossover.py`. This operator can perform single-point or uniform crossover on the sorting networks.

```typescript:src/GA/crossover/SortingNetworksCrossover.py
startLine: 0
endLine: 39
```

- **Single-Point Crossover**: A single crossover point is selected, and the segments before and after this point are swapped between the two parents.
- **Uniform Crossover**: Each gene is chosen randomly from one of the two parents.

## Adversary Crossover

The crossover operator for adversaries is implemented in `SimpleCrossover.py`. This operator can perform single-point crossover on the adversary vectors.

```typescript:src/GA/crossover/SimpleCrossover.py
startLine: 0
endLine: 30
```

- **Single-Point Crossover**: A single crossover point is selected, and the segments before and after this point are swapped between the two parents.

# Results

## Visualization of Sorting Networks

The results of the coevolutionary algorithm were visualized to understand the performance of the evolved sorting networks. The following plots were generated:

### Best Fitness over Generations

![Best Fitness over Generations](plots_16/comparison_best_fitness.png)

### Average Fitness over Generations

![Average Fitness over Generations](plots_16/comparison_avg_fitness.png)

### Scaled Average Fitness over Generations

![Scaled Average Fitness over Generations](plots_16/comparison_scaled_avg_fitness.png)

### Standard Deviation of Fitness over Generations

![Standard Deviation of Fitness over Generations](plots_16/comparison_std_dev_fitness.png)

### Runtime per Generation

![Runtime per Generation](plots_16/comparison_runtime.png)

### Diversity over Generations

![Diversity over Generations](plots_16/comparison_diversity.png)

### Convergence Generation

![Convergence Generation](plots_16/comparison_convergence_generation.png)

## Performance Analysis

The performance of the evolved sorting networks was analyzed based on the fitness metrics over generations. The following metrics were considered:
- Best Fitness
- Average Fitness
- Scaled Average Fitness
- Standard Deviation of Fitness
- Runtime per Generation
- Diversity
- Convergence Generation

## Comparison with QuickSort

The evolved sorting networks were compared with QuickSort to evaluate their efficiency and correctness. The comparison was based on the number of comparisons and the time taken to sort arrays of different sizes.

# Discussion

## Interpretation of Results

The results indicate that the coevolutionary algorithm was effective in evolving sorting networks that can sort arrays efficiently. The best fitness values improved over generations, and the diversity of the population was maintained, preventing premature convergence.

## Evolutionary Challenges

Several challenges were encountered during the evolutionary process, including population drift, trivial solutions, and system forgetting. These challenges were addressed by using appropriate selection, crossover, and mutation strategies.

## Bitonic Networks

Some of the evolved networks resembled bitonic networks, which are known for their efficiency in sorting. The presence of bitonic networks in the evolved solutions indicates that the algorithm was able to discover efficient sorting patterns.

# Conclusion

## Summary of Findings

The coevolutionary algorithm successfully evolved sorting networks that can sort arrays efficiently. The evolved networks were compared with QuickSort, and the results showed that the coevolutionary approach is effective in discovering efficient sorting patterns.

## Future Work




## Results

### Visualization of Sorting Networks
The results of the coevolutionary algorithm were visualized to understand the performance of the evolved sorting networks.

#### Best Fitness over Generations
![Best Fitness over Generations](plots_16/comparison_best_fitness.png)

#### Average Fitness over Generations
![Average Fitness over Generations](plots_16/comparison_avg_fitness.png)

#### Scaled Average Fitness over Generations
![Scaled Average Fitness over Generations](plots_16/comparison_scaled_avg_fitness.png)

#### Standard Deviation of Fitness over Generations
![Standard Deviation of Fitness over Generations](plots_16/comparison_std_dev_fitness.png)

#### Runtime per Generation
![Runtime per Generation](plots_16/comparison_runtime.png)

#### Diversity over Generations
![Diversity over Generations](plots_16/comparison_diversity.png)

#### Convergence Generation
![Convergence Generation](plots_16/comparison_convergence_generation.png)

## Performance Analysis
The performance of the evolved sorting networks was analyzed based on the fitness metrics over generations. The following metrics were considered:
- Best Fitness
- Average Fitness
- Scaled Average Fitness
- Standard Deviation of Fitness
- Runtime per Generation
- Diversity
- Convergence Generation

## Comparison with QuickSort
The evolved sorting networks were compared with QuickSort to evaluate their efficiency and correctness. The comparison was based on the number of comparisons and the time taken to sort arrays of different sizes.

## Discussion

### Interpretation of Results
The results indicate that the coevolutionary algorithm was effective in evolving sorting networks that can sort arrays efficiently. The best fitness values improved over generations, and the diversity of the population was maintained, preventing premature convergence.

### Evolutionary Challenges
Several challenges were encountered during the evolutionary process, including population drift, trivial solutions, and system forgetting. These challenges were addressed by using appropriate selection, crossover, and mutation strategies.

### Bitonic Networks
Some of the evolved networks resembled bitonic networks, which are known for their efficiency in sorting. The presence of bitonic networks in the evolved solutions indicates that the algorithm was able to discover efficient sorting patterns.

## Conclusion

### Summary of Findings
The coevolutionary algorithm successfully evolved sorting networks that can sort arrays efficiently. The evolved networks were compared with QuickSort, and the results showed that the coevolutionary approach is effective in discovering efficient sorting patterns.

### Future Work
Future work could focus on improving the mutation and crossover operators to further enhance the performance of the evolved sorting networks. Additionally, exploring different fitness functions and selection strategies could lead to the discovery of even more efficient sorting networks.

## References
- Cite any references used during the project.

## Appendix

### Source Code
Include the full source code with comments.

### Raw Data
Include raw data files like CSV or JSON.

