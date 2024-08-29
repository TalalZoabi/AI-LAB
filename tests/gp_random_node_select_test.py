from src.GP.GP import GP
from src.GP.GPFactory import GPFactory
import numpy as np
import matplotlib.pyplot as plt

gp_factory = GPFactory()

test_size = 1000

sizes = []
depths = []

for i in range(test_size):
    gp = gp_factory.generate_individual('full', GP.MAX_DEPTH)
    node, _ = gp.select_random_node()
    sizes.append(node.size())
    depths.append(node.calc_max_depth())

# Calculate average size, depth, and variance
avg_size = sum(sizes) / test_size
avg_depth = sum(depths) / test_size
size_variance = np.var(sizes)
depth_variance = np.var(depths)

print(f'Max size: {max(sizes)}')
print(f'Min size: {min(sizes)}')
print(f'Max depth: {max(depths)}')
print(f'Min depth: {min(depths)}')
print(f'Variance size: {size_variance}')
print(f'Variance depth: {depth_variance}')

# Plotting size distribution
plt.figure(figsize=(10, 6))
plt.hist(sizes, bins=20, color='skyblue', edgecolor='black', alpha=0.7)
plt.title('Size Distribution of Selected Nodes', fontsize=16)
plt.xlabel('Size of Selected Node', fontsize=14)
plt.ylabel('Frequency', fontsize=14)
plt.grid(True)
plt.tight_layout()
plt.show()

# Plotting depth distribution
plt.figure(figsize=(10, 6))
plt.hist(depths, bins=20, color='lightcoral', edgecolor='black', alpha=0.7)
plt.title('Depth Distribution of Selected Nodes', fontsize=16)
plt.xlabel('Depth of Selected Node', fontsize=14)
plt.ylabel('Frequency', fontsize=14)
plt.grid(True)
plt.tight_layout()
plt.show()

print(f'Average size: {avg_size}')
print(f'Average depth: {avg_depth}')
