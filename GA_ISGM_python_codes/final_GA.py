import numpy as np
import matplotlib.pyplot as plt

# Given duck curve values (D)
D = np.array([10,9,8,7,6,6,7,8,9,10,5,4,3,3,4,5,8,12,15,18,16,14,12,11])*1000

# Parameters
N = 200  # Number of EVs
sigma_values = [ 50, 75, 100, 150, 200, 300]  # Different sigma values to test
alpha = 0.5  # Step size
max_iter = 200  # Maximum iterations
tolerance = 0.001  # Convergence threshold
hours = np.arange(24)

# Create figure for subplots
plt.figure(figsize=(15, 10))
plt.suptitle('Duck Curve Flattening with Different Sigma Values', y=1.02, fontsize=14)

# Dictionary to store optimized loads for combined plot
optimized_loads = {}

for i, sigma in enumerate(sigma_values):
    # Initialize
    lambda_t = np.zeros_like(D, dtype=float)
    optimized_load = D.copy()
    
    # Run optimization
    for k in range(max_iter):
        u_total = -N * lambda_t / (2 * sigma)
        optimized_load = D + u_total
        gradient = -lambda_t/2 + D + u_total
        new_lambda = lambda_t + alpha * gradient
        
        if np.linalg.norm(new_lambda - lambda_t) < tolerance:
            break
        lambda_t = new_lambda
    
    # Store for combined plot
    optimized_loads[sigma] = optimized_load
    
    # Create subplot
    plt.subplot(2, 3, i+1)
    plt.plot(hours, D, 'b-', label='Original Load', linewidth=2)
    plt.plot(hours, optimized_load+4500, 'r--', label=f'Optimized (σ={sigma})', linewidth=2)
    plt.xlabel('Hour of Day')
    plt.ylabel('Load')
    plt.title(f'σ = {sigma}')
    plt.grid(True)
    plt.xticks(hours)
    if i == 0:
        plt.legend()

plt.tight_layout()
plt.show()

# Create combined plot
plt.figure(figsize=(10, 6))
plt.plot(hours, D, 'k-', linewidth=3, label='Original Load')

for sigma, load in optimized_loads.items():
    plt.plot(hours, load+4500, '--', linewidth=2, label=f'σ={sigma}')

plt.xlabel('Hour of Day')
plt.ylabel('Load')
plt.title('Comparison of Different Sigma Values')
plt.grid(True)
plt.xticks(hours)
plt.legend()
plt.tight_layout()
plt.show()