import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
import sys


from src.simulation import SimulationStats
from src.analysis.csv_utils import read_csv_to_stats
import matplotlib.pyplot as plt

def plot_simulation_stats(stats: SimulationStats, figsavename=None):
   
    grouped_data = {}
    for obj in stats:
        if obj.q not in grouped_data:
            grouped_data[obj.q] = []
        grouped_data[obj.q].append(obj)

    for q, group in grouped_data.items():
        n_values = [obj.n for obj in group]
        min_l1_norm_failed_values = [obj.min_l1_norm_failed for obj in group]
        max_l1_norm_good_values = [obj.max_l1_norm_good for obj in group]
        estimated_t_values = [obj.estimated_t for obj in group]
        percentage_good_values = [
            (int(obj.num_good) / (int(obj.num_good) + int(obj.num_failed)) * 100) if (int(obj.num_good) + int(obj.num_failed)) > 0 else 0
            for obj in group
        ]
        fig, ax1 = plt.subplots(figsize=(10, 6))
        
        ax1.plot(n_values, min_l1_norm_failed_values, label='Min L1 Norm Failed', marker='o', color='b')
        ax1.plot(n_values, max_l1_norm_good_values, label='Max L1 Norm Good', marker='x', color='g')
        
        ax1.set_xlabel('n')
        ax1.set_ylabel('Norm Values')
        ax1.legend(loc='upper left')
        ax1.grid(True)
        
        ax2 = ax1.twinx()
        ax2.plot(n_values, estimated_t_values, label='Estimated t', marker='^', color='r')
        ax2.set_ylabel('Estimated t')
        ax2.legend(loc='upper right')

        ax3 = ax1.twinx()
        ax3.spines['right'].set_position(('outward', 60))
        ax3.plot(n_values, percentage_good_values, label='Percentage Good', marker='s', color='purple')
        ax3.set_ylabel('Percentage Good')
        ax3.legend(loc='lower right')
        
        plt.title(f'Plot for q={q}')

        if not figsavename:
            plt.show()
        else:
            plt.savefig(f"./figs/{figsavename}_prime{q}.png")
            plt.close()



if __name__ == "__main__":
    # get command line argument 1 as the csv file name
    filename = sys.argv[1]

    if len(sys.argv) > 2:
        figsavename = sys.argv[2]
    else:
        figsavename = None
    if not filename:
        print("Please provide a filename as a command line argument")
        sys.exit(1)

    stats = read_csv_to_stats(filename)
    plot_simulation_stats(stats, figsavename)