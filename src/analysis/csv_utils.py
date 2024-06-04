from src.simulation import SimulationStats
from dataclasses import asdict
import csv

def write_single_stat_to_csv(stat: SimulationStats, filename: str):
    # Open the file in append mode to avoid overwriting existing content
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        
        # Write the header only once if the file is empty
        if file.tell() == 0:
            writer.writerow(SimulationStats.__annotations__.keys())
        
        stat_dict = asdict(stat)
        # Write the data
        writer.writerow(stat_dict.values())


def read_csv_to_stats(filename: str):
    stats = []
    with open(filename, mode='r') as file:
        reader = csv.reader(file)
        header = next(reader)
        for row in reader:
            stats.append(SimulationStats(*row))
    return stats 

