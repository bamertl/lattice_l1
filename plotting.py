import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from itertools import product, combinations
from matplotlib.lines import Line2D

# Parameters
n = 3
Pn = 10
radius_Sn = 2
num_public_key_points = 5  # Number of public key points to generate

# Prepare figure
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
ax.set_aspect("auto")

# Plot Bn (cube)
r = [-Pn, Pn]
for s, e in combinations(np.array(list(product(r, r, r))), 2):
    if np.sum(np.abs(np.array(s)-np.array(e))) == r[1]-r[0]:
        ax.plot3D(*zip(s, e), color="blue")

# Sphere (Sn)
phi, theta = np.mgrid[0.0:np.pi:20j, 0.0:2.0*np.pi:20j]
x = radius_Sn * np.sin(phi) * np.cos(theta)
y = radius_Sn * np.sin(phi) * np.sin(theta)
z = radius_Sn * np.cos(phi)
ax.plot_surface(x, y, z, color='red', alpha=0.5)

# Vector u (private key)
u = np.array([1, 1, 1])
u = radius_Sn * u / np.linalg.norm(u)  # Normalize and scale
ax.quiver(0, 0, 0, u[0], u[1], u[2], color='green', arrow_length_ratio=0.1, label='Vector u')

# Generate public key points within Bn
public_key_points = np.random.uniform(-Pn, Pn, (num_public_key_points, 3))
ax.scatter(public_key_points[:, 0], public_key_points[:, 1], public_key_points[:, 2], color='black', label='Public Key Points')

# Assume v is one of the public key points with a small perturbation
v = public_key_points[0] + np.array([0.5, 0.5, 0.5])  # Simplified perturbation
ax.quiver(*public_key_points[0], *v, color='purple', arrow_length_ratio=0.1, label='Vector v')

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# Adjusting legend to include all elements
ax.legend()

plt.title('Visualization of Bn, Sn, Vector u, Public Key Points, and Vector v')
plt.show()
