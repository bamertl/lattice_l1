import numpy as np
import matplotlib.pyplot as plt
import os

# Set p value
p = 7

# Define the range from -p//2 to p (for visualization)
x_values = np.arange(-p // 2, p + 1)

# Calculate Lee weights: for negative values, we use the same Lee metric as for positive |x|
lee_weights = [min(abs(x), p - abs(x)) for x in x_values]

# Set the style
plt.style.use("seaborn-v0_8-whitegrid")

# Create the plot
plt.figure(figsize=(10, 6))
plt.plot(x_values, lee_weights, marker='o', linestyle='-', color='b', label='Lee Weight')

# Draw vertical red lines at -p/2 and p/2 (without rounding)
plt.axvline(-p / 2, color='r', linestyle='--', linewidth=1.5, label='$-p/2$')
plt.axvline(p / 2, color='r', linestyle='--', linewidth=1.5, label='$p/2$')

# Labeling the axes with updated labels
plt.xlabel('Values (v)', fontsize=14)
plt.ylabel('Lee Weight', fontsize=14)

# Title and legend with specified fontsizes
plt.title('Lee Weights from $-\\frac{p}{2}$ to $p$ in $\\mathbb{Z}_7$', fontsize=16)
plt.legend(fontsize=12)

# Adding grid
plt.grid(True)

# Define the directory to save the figure
output_dir = './figs/'
os.makedirs(output_dir, exist_ok=True)  # Create the directory if it doesn't exist

# Save the figure
output_path = os.path.join(output_dir, "lee_weights_z7_plot.png")
plt.savefig(output_path, dpi=300)

# Close the plot
plt.close()

