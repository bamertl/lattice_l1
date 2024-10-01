import sys
import csv


def read_and_print_csv(file_path):
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        
        print(f"{'n':<5} {'k':<5} {'q':<5} {'avg_lattice_transform_time (ms)':<35} {'stv_lattice_transform_time (ms)':<35} {'avg_kannan_embedding_time (ms)':<35} {'stv_kannan_embedding_time (ms)':<35} {'avg_shortest_vector_time (ms)':<35} {'stv_shortest_vector_time (ms)':<35} {'all_time_min_distance':<25}")
        print("-" * 250)
        for row in reader:
            n = row['n']
            k = row['k']
            q = row['q']
            avg_lattice_transform_time = float(row['avg_lattice_transform_time']) / 1e6
            stv_lattice_transform_time = float(row['stv_lattice_transform_time']) / 1e6
            avg_kannan_embedding_time = float(row['avg_kannan_embedding_time']) / 1e6
            stv_kannan_embedding_time = float(row['stv_kannan_embedding_time']) / 1e6
            avg_shortest_vector_time = float(row['avg_shortest_vector_time']) / 1e6
            stv_shortest_vector_time = float(row['stv_shortest_vector_time']) / 1e6
            all_time_min_distance = row['all_time_min_distance']
            
            print(f"{n:<5} {k:<5} {q:<5} {avg_lattice_transform_time:<35.2f} {stv_lattice_transform_time:<35.2f} {avg_kannan_embedding_time:<35.2f} {stv_kannan_embedding_time:<35.2f} {avg_shortest_vector_time:<35.2f} {stv_shortest_vector_time:<35.2f} {all_time_min_distance:<25}")



if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python read_csv.py <csv_file_path>")
    else:
        csv_file_path = sys.argv[1]
        read_and_print_csv(csv_file_path)