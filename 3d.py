import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# Define the basis vectors
basis_vectors = np.array([[1, 2, 2], [0, 1, 2], [0, 0, 5]])

# Define the field size
p = 5

# Generate all points in the lattice over the field Fp_5
lattice_points = []
for i in range(p):
    for j in range(p):
        for k in range(p):
            point = i * basis_vectors[0] + j * basis_vectors[1] + k * basis_vectors[2]
            lattice_points.append(point)

# Convert the list of lattice points to a numpy array for plotting
lattice_points = np.array(lattice_points)

# Plot the lattice points in 3D
fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, projection='3d')
ax.scatter(lattice_points[:, 0], lattice_points[:, 1], lattice_points[:, 2], color='blue')

# Set plot limits
ax.set_xlim(-1, p)
ax.set_ylim(-1, p)
ax.set_zlim(-1, p)

# Set labels and title
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
ax.set_title('3D Lattice over the Finite Field Fp_5')

# Show grid
ax.grid(True)

# Display the plot
plt.show()
