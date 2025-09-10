import numpy as np
import matplotlib.pyplot as plt

# Given duck curve values (D)
D = np.array([10,9,8,7,6,6,7,8,9,10,5,4,3,3,4,5,8,12,15,18,16,14,12,11]) * 1000

# Parameters
N = 200  # Number of EVs
sigma_values = [0.25,0.5,1,1.5,2,3,5, 10]  # 8 sigma values
alpha = 0.5  # Step size
max_iter = 2000  # Maximum iterations
tolerance = 1e-7  # Convergence threshold
hours = np.arange(24)

# Create figure for subplots
plt.figure(figsize=(20, 10))
plt.suptitle('Duck Curve Flattening with Different Sigma Values', y=1.02, fontsize=16)

# Dictionary to store optimized loads for combined plot
optimized_loads = {}

for i, sigma in enumerate(sigma_values):
    # Initialize
    lambda_t = np.zeros_like(D, dtype=float)
    optimized_load = D.copy()
    
    # Gradient ascent optimization loop
    for k in range(max_iter):
        u_total = -lambda_t / (2 * sigma)
        optimized_load = D + u_total
        gradient = -lambda_t / 2 + D + u_total
        new_lambda = lambda_t + alpha * gradient
        
        if np.linalg.norm(new_lambda - lambda_t) < tolerance:
            break
        lambda_t = new_lambda

    # Final optimized load
    optimized_load = D - lambda_t / (2 * sigma)
    optimized_loads[sigma] = optimized_load

    # Create subplot (2 rows x 4 columns)
    plt.subplot(2, 4, i + 1)
    plt.plot(hours, D, 'b-', label='Original Load', linewidth=2)
    plt.plot(hours, optimized_load + 3500, 'r--', label=f'Optimized (σ={sigma})', linewidth=2)
    plt.xlabel('Hour of Day')
    plt.ylabel('Load')
    plt.title(f'σ = {sigma}')
    plt.grid(True)
    plt.xticks(hours)
    if i == 0:
        plt.legend()

plt.tight_layout()
plt.show()

# Combined comparison plot
plt.figure(figsize=(12, 6))
plt.plot(hours, D, 'k-', linewidth=3, label='Original Load')

for sigma, load in optimized_loads.items():
    plt.plot(hours, load + 3500, '--', linewidth=2, label=f'σ={sigma}')

plt.xlabel('Hour of Day')
plt.ylabel('Load')
plt.title('Comparison of Different Sigma Values (Optimized Duck Curve)')
plt.grid(True)
plt.xticks(hours)
plt.legend()
plt.tight_layout()
plt.show()