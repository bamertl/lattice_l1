import pandas as pd
import matplotlib.pyplot as plt
import os

# Apply a scientific style for the plots
plt.style.use("seaborn-v0_8-whitegrid")

# Create the directory if it doesn't exist
os.makedirs("./figs/1distance", exist_ok=True)

def plot_distances():
    # Load data from CSV files
    lee_data = pd.read_csv("./data/distance/minimum_distance_estimations_lee.csv")
    hamming_data = pd.read_csv("./data/distance/minimum_distance_estimations_hamming.csv")

    # Get the unique values of q (primes) to plot each prime separately
    primes = lee_data['q'].unique()

    # Iterate over each prime and plot the data
    for q in primes:
        # Filter data for the current prime q
        lee_filtered = lee_data[lee_data['q'] == q]
        hamming_filtered = hamming_data[hamming_data['q'] == q]

        # Plot Lee distance vs. n
        plt.figure(figsize=(10, 6))
        plt.plot(lee_filtered['n'], lee_filtered['estimated_d'], label="Lee Distance", marker='o', markersize=6, linewidth=2, color='blue')
        
        # Plot Hamming distance vs. n
        plt.plot(hamming_filtered['n'], hamming_filtered['estimated_d'], label="Hamming Distance", marker='x', markersize=6, linewidth=2, color='red')

        # Labels and title with LaTeX formatting
        plt.xlabel(r"Dimension $n$", fontsize=14)
        plt.ylabel(r"Estimated Minimum Distance ($d$)", fontsize=14)
        plt.title(f"Estimated Minimum Distance ($d$) vs $n$ ($p$ = {q})", fontsize=16, weight='bold')
        
        # Add legend
        plt.legend(fontsize=12)

        # Add grid lines for better readability
        plt.grid(True, which='both', linestyle='--', linewidth=0.5)

        # Save plot to the figs/1distance folder
        plt.savefig(f"./figs/1distance/distance_vs_n_q{q}.png", dpi=300, bbox_inches='tight')
        plt.close()  # Close the plot to free memory

        print(f"Plot saved for q={q} as distance_vs_n_q{q}.png")

if __name__ == "__main__":
    plot_distances()
