import numpy as np
import matplotlib.pyplot as plt

 
# Define the basis vectors
basis_vectors = np.array([[1, 2], [0, 5]])

# Define the field size
p = 5

# Generate all points in the lattice over the field Fp_5
lattice_points = []
for i in range(p):
    for j in range(p):
        point = (i * basis_vectors[0] + j * basis_vectors[1]) % p
        lattice_points.append(point)

# Convert the list of lattice points to a numpy array for plotting
lattice_points = np.array(lattice_points)

# Plot the lattice points
plt.figure(figsize=(8, 8))
plt.scatter(lattice_points[:, 0], lattice_points[:, 1], color='blue')

# Set plot limits
plt.xlim(-1, p)
plt.ylim(-1, p)

# Set labels and title
plt.xlabel('x')
plt.ylabel('y')
plt.title('2D Lattice over the Finite Field Fp_5')

# Show grid
plt.grid(True)

# Display the plot
plt.show()
