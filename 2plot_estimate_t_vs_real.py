import matplotlib.pyplot as plt
import csv
import sys
import numpy as np
import os

plt.style.use("seaborn-v0_8-whitegrid")


def plot_csv_file(file_path):
    try:
        # Read the CSV file into lists
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            header = next(reader)
            data = {column: [] for column in header}
            
            for row in reader:
                for i, value in enumerate(row):
                    try:
                        if '[' in value and ']' in value:
                            # Convert list strings to actual lists and calculate the average
                            list_values = [float(x) for x in value.strip('[]').split(',')]
                            average_value = np.mean(list_values)
                            data[header[i]].append(average_value)
                        else:
                            data[header[i]].append(float(value))
                    except ValueError:
                        print(f"Warning: Non-numeric data '{value}' found in column '{header[i]}', row {reader.line_num}. Skipping this value.")
                        data[header[i]].append(None)
        
        # Extract 'n', 'Estimated t list', and 'Exact t list' columns
        if 'n' not in data or 'Estimated t list' not in data or 'Exact t list' not in data or 'q' not in data:
            print("Error: Required columns 'n', 'Estimated t list', 'Exact t list', and 'q' not found in CSV file.")
            return
        
        n_values = [val for val in data['n'] if val is not None]
        estimated_t_values = [val for val in data['Estimated t list'] if val is not None]
        exact_t_values = [val for val in data['Exact t list'] if val is not None]
        q_value = data['q'][0] if data['q'] else 'Unknown'
        
        # Plot 'Estimated t' and 'Exact t' against 'n'
        plt.figure(figsize=(10, 6))
        plt.plot(n_values, estimated_t_values, marker='o', label='Estimated $t$')
        plt.plot(n_values, exact_t_values, marker='o', label='Exact $t$')
        
        plt.xlabel('Dimension $n$',fontsize=14)
        plt.ylabel('Lee Distance', fontsize=14)
        plt.title(f'Estimated $t$ and Exact t vs Dimension $n$ for $p$ = {int(q_value)}', fontsize=16)
        plt.legend(fontsize=12)
        plt.grid(True)
        
        # Create directory if it doesn't exist
        output_dir = './figs/2distance/'
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, 'plot_estimated_vs_exact.png')
        plt.savefig(output_path)
        plt.close()
        print(f"Plot saved to {output_path}")
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python plot_csv_file.py <path_to_csv>")
    else:
        plot_csv_file(sys.argv[1])

