import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import os

# Check if the folder path is provided as a command line argument
if len(sys.argv) != 2:
    print("Usage: python plot_timings_analysis.py <folder_path>")
    sys.exit(1)

folder_path = sys.argv[1]
file_path = os.path.join(folder_path, 'result_times_ns.csv')

# Load the CSV file
data = pd.read_csv(file_path)

# Convert avg_shortest_vector_time from ns to seconds
data['avg_shortest_vector_time'] = data['avg_shortest_vector_time'] / 1e9

# Set up the plotting style
sns.set(style="whitegrid")

# Plotting avg_shortest_vector_time vs block_size for different dimensions (n)
plt.figure(figsize=(10, 6))
sns.lineplot(data=data, x='block_size', y='avg_shortest_vector_time', hue='n', marker='o')
plt.title('Average Shortest Vector Time vs BKZ Block Size', fontsize=16, weight='bold')
plt.xlabel('BKZ Block Size',fontsize=14)
plt.ylabel('Average Shortest Vector Time (s)', fontsize=14)
plt.legend(title='Dimension (n)')
plt.tight_layout()

# Save the plot
os.makedirs('./figs/bkz_block_size/', exist_ok=True)
plt.savefig('./figs/bkz_block_size/avg_shortest_vector_time_vs_block_size.png')

plt.show()
