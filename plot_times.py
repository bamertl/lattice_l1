import csv
import sys
from collections import defaultdict
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style="whitegrid")
# Function to read CSV and calculate averages over n
def process_csv(file_path, scale_factor):
    data = defaultdict(lambda: {"count": 0, "avg_lattice_transform_time": 0, "avg_kannan_embedding_time": 0, "avg_shortest_vector_time": 0})
    
    with open(file_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            n = int(row['n'])
            data[n]["avg_lattice_transform_time"] += float(row['avg_lattice_transform_time']) * scale_factor
            data[n]["avg_kannan_embedding_time"] += float(row['avg_kannan_embedding_time']) * scale_factor
            data[n]["avg_shortest_vector_time"] += float(row['avg_shortest_vector_time']) * scale_factor
            data[n]["count"] += 1

    # Calculate averages
    averages = {}
    for n, values in data.items():
        avg_lattice_transform_time = values["avg_lattice_transform_time"] / values["count"]
        avg_kannan_embedding_time = values["avg_kannan_embedding_time"] / values["count"]
        avg_shortest_vector_time = values["avg_shortest_vector_time"] / values["count"]
        averages[n] = {
            "avg_lattice_transform_time": avg_lattice_transform_time,
            "avg_kannan_embedding_time": avg_kannan_embedding_time,
            "avg_shortest_vector_time": avg_shortest_vector_time
        }
    
    return averages

# Function to plot the results
def plot_averages(averages, unit_label):
    n_values = sorted(averages.keys())
    avg_lattice_transform_time = [averages[n]["avg_lattice_transform_time"] for n in n_values]
    avg_kannan_embedding_time = [averages[n]["avg_kannan_embedding_time"] for n in n_values]
    avg_shortest_vector_time = [averages[n]["avg_shortest_vector_time"] for n in n_values]

    plt.plot(n_values, avg_lattice_transform_time, label='Lattice Transform Time', marker='o')
    plt.plot(n_values, avg_kannan_embedding_time, label='Kannan Embedding Time', marker='o')
    plt.plot(n_values, avg_shortest_vector_time, label='Shortest Vector Time', marker='o')

    plt.xlabel('n')
    plt.ylabel(f'Time ({unit_label})')
    plt.title(f'{label} Timings',fontsize=16, weight='bold')
    plt.tight_layout()
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <file_path>")
    else:
        file_path = sys.argv[1]

        # Set the scale factor for time units (1 = ns, 1e-3 = µs, 1e-6 = ms, 1e-9 = s)
        scale_factor = 1e-6  # For milliseconds
        unit_label = 'ms'  # You can change this to 's' for seconds or other as needed
        label = "BKZ" 
        averages = process_csv(file_path, scale_factor)
        plot_averages(averages, unit_label)
