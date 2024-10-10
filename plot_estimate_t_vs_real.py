import csv
import ast
import sys
import matplotlib.pyplot as plt
from collections import defaultdict

def read_csv_with_arrays(file_path):
    """
    Reads a CSV file where arrays are stored as strings, converts them back to lists, 
    and averages the estimated and actual t values for each dimension n, across different k values.
    Also collects data for n = 12 and q = 17 for detailed plotting.
    
    :param file_path: Path to the CSV file.
    :return: Lists of n, average estimated t per n, average exact t per n, and data for n=12, q=17
    """
    n_values = defaultdict(list)  # Dictionary to store estimated t values for each n
    exact_t_values = defaultdict(list)  # Dictionary to store exact t values for each n

    # To collect data for n=12 and q=17
    k_values_for_n12_q17 = []
    estimated_d_for_n12_q17 = []
    exact_d_for_n12_q17 = []

    try:
        with open(file_path, mode='r') as file:
            csv_reader = csv.reader(file)
            header = next(csv_reader)  # Read the header row
            
            # Iterate through rows
            for row in csv_reader:
                # Extract basic columns
                n = int(row[0])
                k = int(row[1])
                q = int(row[2])

                # Convert string representations of arrays back to Python lists
                estimated_t_array = ast.literal_eval(row[3])
                exact_t_array = ast.literal_eval(row[4])

                # Calculate the averages of estimated t and exact t
                avg_estimated_t = sum(estimated_t_array) / len(estimated_t_array)
                avg_exact_t = sum(exact_t_array) / len(exact_t_array)

                # Store the averages in the dictionary for each n
                n_values[n].append(avg_estimated_t)
                exact_t_values[n].append(avg_exact_t)

                # If n=12 and q=17, collect the individual values for plotting
                if n == 12 and q == 17:
                    k_values_for_n12_q17.append(k)
                    estimated_d_for_n12_q17.append((2 * avg_estimated_t) + 1)  # Convert t to minimum distance
                    exact_d_for_n12_q17.append((2 * avg_exact_t) + 1)  # Convert t to minimum distance

        # Now average over all the k values for each n
        n_list = sorted(n_values.keys())
        avg_estimated_t_per_n = [sum(n_values[n]) / len(n_values[n]) for n in n_list]
        avg_exact_t_per_n = [sum(exact_t_values[n]) / len(exact_t_values[n]) for n in n_list]
        
        return n_list, avg_estimated_t_per_n, avg_exact_t_per_n, k_values_for_n12_q17, estimated_d_for_n12_q17, exact_d_for_n12_q17
    
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

def plot_avg_results(n_values, avg_estimated_t_values, avg_exact_t_values):
    """
    Plots the average estimated t and average exact t over the dimension n.
    
    :param n_values: List of unique n values (dimensions)
    :param avg_estimated_t_values: List of average estimated t values per n
    :param avg_exact_t_values: List of average exact t values per n (from exact minimum distances)
    """

    avg_estimated_d_values = [(2 * t) + 1 for t in avg_estimated_t_values]
    avg_exact_d_values = [(2 * t) + 1 for t in avg_exact_t_values]    
    plt.figure(figsize=(10, 6))
    
    # Plotting the average estimated t values
    plt.plot(n_values, avg_estimated_d_values , label="Estimated Minimum Distance", marker='o', linestyle='--', color='b')
    
    # Plotting the average exact t values
    plt.plot(n_values, avg_exact_d_values, label="Actual Minimum Distance", marker='x', linestyle='-', color='r')
    
    # Adding labels and title
    plt.xlabel("Dimension n", fontsize=14)
    plt.ylabel("Average Minimum Distance (d)", fontsize=14)
    plt.title("Estimated vs Actual Minimum Distance", fontsize=16)
    
    # Adjusting the limits (so it doesn't go below zero)
    plt.ylim(bottom=0)

    # Add gridlines for better readability
    plt.grid(True, which='both', linestyle='--', linewidth=0.7)

    # Adding a legend
    plt.legend(loc='upper left', fontsize=12)

    # Improve layout
    plt.tight_layout()
    
    # Show the plot
    plt.show()

def plot_n12_q17_results(k_values, estimated_d_values, exact_d_values):
    """
    Plots the estimated and actual minimum distances for n=12 and q=17 over different k values.
    
    :param k_values: List of k values for n=12 and q=17
    :param estimated_d_values: List of estimated minimum distances for n=12 and q=17
    :param exact_d_values: List of exact minimum distances for n=12 and q=17
    """
    plt.figure(figsize=(10, 6))

    # Plotting the estimated minimum distances
    plt.plot(k_values, estimated_d_values, label="Estimated Minimum Distance", marker='o', linestyle='--', color='b')

    # Plotting the exact minimum distances
    plt.plot(k_values, exact_d_values, label="Actual Minimum Distance", marker='x', linestyle='-', color='r')

    # Adding labels and title
    plt.xlabel("Dimension k", fontsize=14)
    plt.ylabel("Minimum Distance (d)", fontsize=14)
    plt.title("Minimum Distance vs Dimension k for n=12, q=17", fontsize=16)

    # Adjusting the limits (so it doesn't go below zero)
    plt.ylim(bottom=0)

    # Add gridlines for better readability
    plt.grid(True, which='both', linestyle='--', linewidth=0.7)

    # Adding a legend
    plt.legend(loc='upper left', fontsize=12)

    # Improve layout
    plt.tight_layout()

    # Show the plot
    plt.show()


if __name__ == "__main__":
    # Check if the file path is passed as an argument
    if len(sys.argv) != 2:
        print("Usage: python read_csv_and_plot_avg_by_n.py <path_to_csv_file>")
        sys.exit(1)
    
    # Get the CSV file path from the command-line arguments
    csv_file_path = sys.argv[1]
    
    # Call the function to read and process the CSV, get the data to plot
    n_list, avg_estimated_t_values, avg_exact_t_values, k_values_for_n12_q17, estimated_d_for_n12_q17, exact_d_for_n12_q17 = read_csv_with_arrays(csv_file_path)
    
    # Call the function to plot the average results
    plot_avg_results(n_list, avg_estimated_t_values, avg_exact_t_values)
    
    # Call the function to plot results for n=12 and q=17
    plot_n12_q17_results(k_values_for_n12_q17, estimated_d_for_n12_q17, exact_d_for_n12_q17)
