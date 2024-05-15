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

lattice = IntegerLattice(sage.GF(q), HNF)

print("Codeword: ", codeword)
print("Target Vector", target_vector)
print("Min Distance", lin_code.minimum_distance())
print("Is Codeword in Lattice?", codeword in lattice)
print("Closest Vector", lattice.closest_vector(target_vector))

