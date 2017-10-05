
import icepack
import matplotlib.pyplot as plt
import numpy as np

# First we'll call a helper script to generate a simple example mesh. This is
# in the script `make_mesh.py` in this folder.
import make_mesh
length, width = 20.0e3, 20.0e3
make_mesh.main(length, width, "rectangle.geo")

# This function reads in an unstructured mesh from a file stored in the gmsh
# `.msh` format.
mesh = icepack.read_msh("rectangle.msh")

# The `mesh` object is a python wrapper around a data structure from the
# library deal.II, which provides all of the underlying finite element
# modelling tools that icepack is built on.
print("Data type of mesh objects: {}".format(type(mesh)))

# Mesh objects have several operations for querying their size and contents.
print("Number of vertices: {}".format(mesh.n_vertices()))
print("Number of cells:    {}".format(mesh.n_active_cells()))

# We can access the vertex locations too. We can make a scatter plot of all the
# vertex locations as a sanity check.
X = [x[0] for x in mesh.get_vertices()]
Y = [x[1] for x in mesh.get_vertices()]

fig, ax = plt.subplots()
ax.scatter(X, Y)
plt.show(fig)

# This mesh is too coarse. We can refine all the cells for better resolution.
mesh.refine_global(4)
print("Number of vertices, cells: {0} {1}"
      .format(mesh.n_vertices(), mesh.n_active_cells()))

# To represent fields defined over this domain, we first need to create a
# finite element discretization. The second argument is the polynomial degree.
discretization = icepack.make_discretization(mesh, 1)

# To test this out, we'll make a random Fourier series.
def f(x):
    k1 = (2.0, 3.0)
    k2 = (-5.0, 1.0)
    phi1 = 2 * np.pi * (k1[0] * x[0] / length + k1[1] * x[1] / width)
    phi2 = 2 * np.pi * (k2[0] * x[0] / length + k2[1] * x[1] / width)
    return np.sin(phi1) + np.sin(phi2)

# We'll be using this function a lot. It takes an analytically defined field
# `f` and interpolates it to a finite element discretization. The fields we'll
# be interpolating are input data, either defined by hand or from observations.
u = icepack.interpolate(discretization, f)

# Finally, to make sure it's all working right, we can plot it.
import icepack.plot
fig, ax = plt.subplots()
icepack.plot.plot_field(ax, u)
plt.show(fig)

