import os
import csv
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict

def plot_minimum_distances(csv_file):
    # Initialize data structures to store values
    data = defaultdict(lambda: defaultdict(list))

    # Read CSV file
    with open(csv_file, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            n = int(row['n'])
            k = int(row['k'])
            q = int(row['q'])
            estimated_d = int(row['estimated_d'])
            # Only store values where n >= k
            if n >= k:
                data[n][q].append((k, estimated_d))
    
    # Set plot style
    sns.set(style="whitegrid")

    # Create directory for saving figures if it doesn't exist
    figs_path = os.path.join(".", "figs", "d_estimates")
    os.makedirs(figs_path, exist_ok=True)

    # Only plot for specific q values
    selected_qs = {5, 17, 211, 521}

    # Plot heatmap for each fixed q in selected_qs
    for q in selected_qs:
        if q not in set(q for q_dict in data.values() for q in q_dict):
            continue  # Skip if the q value is not found in the data

        plt.figure(figsize=(14, 10))

        # Prepare data for heatmap
        ks = sorted({k for n_dict in data.values() for k, _ in n_dict.get(q, [])})
        ns = sorted(data.keys())
        
        # Filter ks and ns to every 10th value and ensure n >= k
        ks = [k for k in ks if k % 10 == 1]  # e.g., 11, 21, 31, ...
        ns = [n for n in ns if n % 10 == 1]  # e.g., 11, 21, 31, ...

        heatmap_data = []

        # Populate the heatmap data only where n >= k
        for k in ks:
            row = []
            for n in ns:
                if k <= n and q in data[n]:  # Only include values where n >= k
                    # Find the estimated distance for the given (n, k, q)
                    d_val = next((val for k_val, val in data[n][q] if k_val == k), 0)
                    row.append(d_val)
                else:
                    row.append(0)
            heatmap_data.append(row)

        # Rotate x labels for readability
        ax = sns.heatmap(heatmap_data, annot=True, fmt=".0f", cmap="YlGnBu",
                         xticklabels=ns, yticklabels=ks, cbar_kws={'label': 'Estimated d'},
                         annot_kws={"size": 7}, linewidths=.5)
        plt.xticks(rotation=45, fontsize=10)
        plt.yticks(rotation=0, fontsize=10)
        plt.title(f'Heatmap of Estimated Minimum Distance for q={q}')
        plt.xlabel('n')
        plt.ylabel('k')
        plt.tight_layout()
        
        # Save the plot in the specified folder
        plot_filename = f"heatmap_q{q}.png"
        plot_filepath = os.path.join(figs_path, plot_filename)
        plt.savefig(plot_filepath)
        plt.close()

def main():
    # Read the CSV and generate plots
    csv_file = './data/minimum_distance_estimations.csv'
    plot_minimum_distances(csv_file)

if __name__ == "__main__":
    main()
