
# AI-Lab: Capacitated Vehicle Routing Problem (CVRP) and Ackley Function Optimization

## Overview
This project implements various heuristic and meta-heuristic algorithms to solve the Capacitated Vehicle Routing Problem (CVRP) and find the global minimum of the Ackley function. The algorithms included are:
- Iterated Local Search (ILS)
- Tabu Search (TS)
- Ant Colony Optimization (ACO)
- Simulated Annealing (SA)
- Genetic Algorithm (GA)
- Adaptive Large Neighborhood Search (ALNS)

## Requirements
To run the scripts, you will need:
- Python 3.10
- Required libraries (e.g., NumPy, Matplotlib)

You can install the required libraries using pip:
```bash
pip install -r requirements.txt
```

## Directory Structure
```
/AI-Lab
│
├── /src
│   ├── main.py                # Main script to run the algorithms
│   ├── algorithms.py          # Implementation of the algorithms
│   ├── utils.py               # Utility functions for data handling
│   └── ...
│
├── /data
│   ├── cvrp_data.txt          # Input data for CVRP
│   └── ackley_data.txt        # Input data for Ackley function
│
├── /results
│   └── results.txt            # Output results from the algorithms
│
└── README.md                  # This README file
```

## Running the Scripts

### 1. Prepare Input Data
Before running the algorithms, ensure that the input data files are correctly formatted. The input files should be placed in the `/data` directory.

- **CVRP Input Format**:
```
Vehicle Capacity: <capacity>
Number of Vehicles: <number>
Depot: (x,y)
Cities: [(x1, y1, demand1), (x2, y2, demand2), ...]
```

- **Ackley Function Input Format**:
```
Bounds: [(min1, max1), (min2, max2), ...]
```

### 2. Execute the Main Script
To run the algorithms, execute the `main.py` script. You can do this from the command line as follows:

```bash
python src/main.py
```

### 3. View Results
After running the script, the results will be saved in the `/results` directory in a file named `results.txt`. You can open this file to view the output of the algorithms, including the best solutions found and their corresponding fitness values.

### Example Command
Here’s an example command to run the script:

```bash
python src/main.py
```

## Customization
You can customize the parameters for each algorithm directly in the `main.py` script. Look for sections where the algorithms are instantiated and modify the parameters as needed.

## Conclusion
This project provides a comprehensive implementation of various optimization algorithms for solving the CVRP and the Ackley function. For any questions or issues, please refer to the documentation or contact the project maintainers.

# AI-LAB
# AI-LAB
