from src.simulation import SimulationStats
import sys
from src.analysis.csv_utils import read_csv_to_stats
import matplotlib.pyplot as plt

def plot_simulation_stats(stats: SimulationStats, figsavename=None):
    n_values = [int(stat.n) for stat in stats]
    q_values = [int(stat.q) for stat in stats]
    num_good_values = [int(stat.num_good) for stat in stats]
    

    print(n_values)
    print(num_good_values)
    # Plotting num_good vs combined n and q
    plt.figure(figsize=(10, 5))
    
    # Plot with different markers or colors
    plt.scatter(n_values, num_good_values, c='blue', label='num_good vs n', marker='o')
    plt.scatter(q_values, num_good_values, c='red', label='num_good vs q', marker='x')
    
    plt.xlabel('n and q values')
    plt.ylabel('num_decoded from 1000')
    plt.title('num_good vs n and q')
    plt.legend()
    plt.grid(True)

    if not figsavename:
        plt.show()
    else:
        plt.savefig("./figs/"+ figsavename)
        plt.close()



if __name__ == "__main__":
    # get command line argument 1 as the csv file name
    filename = sys.argv[1]

    figsavename = sys.argv[2]
    if not filename:
        print("Please provide a filename as a command line argument")
        sys.exit(1)

    stats = read_csv_to_stats(filename)
    plot_simulation_stats(stats, figsavename)