from src.construction_a import FiniteField, ConstructionA

dimension = 3
prime = 7
finite_field = FiniteField(dimension, prime)
construction_a = ConstructionA(finite_field, 3, 2)


construction_a.linear_code.generate_all_codewords()

