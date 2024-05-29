import sage.all as sage
from sage.modules.free_module_integer import IntegerLattice

n = 5
k = 2
q = 7
G = sage.matrix(sage.ZZ, [[1,0,1,1,0], [0,1,1,0,1]]).T

Gene = G.change_ring(sage.GF(q))
lin_code = sage.codes.LinearCode(Gene.T)

message = sage.vector(sage.GF(q), [1, 2])

codeword = G * message
error = sage.vector(sage.GF(q), [0, 0, 1,0,0])
target_vector = codeword + error
print("G:\n",G)
augmentation = sage.identity_matrix(sage.ZZ, n) * q
G_Augmented = G.augment(augmentation)
print("G_Augmented:\n",G_Augmented)

HNF = G_Augmented.T.hermite_form(include_zero_rows=False) # 
print("HNF:\n",HNF.T)

lattice = IntegerLattice(HNF)

print("Codeword: ", codeword)
print("Target Vector", target_vector)
print("Min Distance", lin_code.minimum_distance())
print("Is Codeword in Lattice?", codeword in lattice)


codewords = list(lin_code)

def hamming_distance(u, v):
    return sum(u[i] != v[i] for i in range(len(u)))

closest_codeword = None
min_distance = float('inf')

for codeword in codewords:
    distance = hamming_distance(codeword, target_vector)
    if distance < min_distance:
        min_distance = distance
        closest_codeword = codeword
print(f"The closest codeword to the vector {target_vector} is: {closest_codeword}")
print(f"The Hamming distance between them is: {min_distance}")

target_vector = target_vector.change_ring(sage.ZZ)
print("Closest Vector", lattice.closest_vector(target_vector))

