from src.construction_a import FiniteField, ConstructionA
from src.lattice import Lattice

dimension = 5
prime = 13
k = 5
finite_field = FiniteField(dimension, prime)
construction_a = ConstructionA(finite_field, 5, 4)


construction_a.linear_code.generate_all_codewords()

lattice = Lattice(construction_a.lattice_bases)
lattice.print_stats()

