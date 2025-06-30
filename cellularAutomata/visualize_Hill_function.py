import numpy as np
import matplotlib.pyplot as plt

def plot_function(S, S0, l, n):
    return (1 + l * (S / S0) ** n) / (1 + (S / S0) ** n)

# Define the range of S values
S_values = np.linspace(0.1, 100, 400)

# Define parameter sets for demonstration
parameter_sets = [
    # (S0, l, n)
    (5.0, 2.0, 2.0),  
    (10.0, 2.0, 2.0),
    (5.0, 0.0, 2.0),
    (5.0, 2.0, 5.0),
]

# Create subplots
fig, axs = plt.subplots(2, 2, figsize=(12, 10))
fig.suptitle('Effect of Changing Parameters on the Hill Function')

# Plot for each parameter set
for i, (S0, l, n) in enumerate(parameter_sets):
    ax = axs[i // 2, i % 2]
    f_S = plot_function(S_values, S0, l, n)
    ax.plot(S_values, f_S, label=f'S0={S0}, l={l}, n={n}')
    ax.set_xscale('log')
    ax.set_xlabel('S')
    ax.set_ylabel('f(S)')
    ax.set_title(f'Parameters: S0={S0}, l={l}, n={n}')
    ax.legend()
    ax.grid(True)

plt.tight_layout()
plt.show()
