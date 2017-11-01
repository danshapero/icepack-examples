
import numpy as np
import matplotlib.pyplot as plt
import icepack, icepack.plot

# Generate a mesh using `gmsh` and read it back in.
import make_mesh
length, width = 20.0e3, 20.0e3
make_mesh.main(length, width, "rectangle")


# The ice thickness decreases linearly from the inflow boundary to the calving
# front.
h0, dh = 500.0, 100.0
def thickness(x):
    return h0 - dh * x[0] / length


# Make the ice temperature jump by 5C in the middle of the domain.
temp = 254.15
def temperature(x):
    dtheta = 5.0
    inside = ((length/4 < x[0] < 3*length/4) and (width/4 < x[1] < 3*width/4))
    return temp + inside * dtheta


# The ice velocity is an exact solution for constant temperature and linear
# thickness. For the derivation, see the glacier mechanics book by Greve and
# Blatter.
def velocity(x):
    from icepack import rho_ice, rho_water, gravity, rate_factor
    u0 = 100.0
    rho = rho_ice * (1 - rho_ice / rho_water)
    A = (rho * gravity * h0 / 4)**3 * rate_factor(temp)
    q = 1 - (1 - (dh / h0) * (x[0] / length))**4
    return u0 + 0.25 * A * q * length * h0 / dh


# Read the mesh from a file, refine it a bit, and make a discretization.
mesh = icepack.read_msh("rectangle.msh")
mesh.refine_global(3)
discretization = icepack.make_discretization(mesh, 1)

# Interpolate all the exact data to the discretization we just made.
h = icepack.interpolate(discretization, thickness)
u0 = icepack.interpolate(discretization, velocity, lambda x: 0.0)
theta = icepack.interpolate(discretization, temperature)


# --- New stuff! ---

# The boundary segments of the mesh have different numeric IDs in order to help
# set where Dirichlet or Neumann boundary conditions apply. We can check what
# they are by plotting the mesh.
fig, ax = plt.subplots()
ax.set_aspect('equal')
icepack.plot.plot_mesh(ax, mesh)
plt.show(fig)

# From this figure we can see that boundary region 1 is where we want Dirichlet
# boundary conditions, and region 2 is where we want Neumann conditions.
dirichlet_boundary_ids = {1}

# Create a model object that stores these boundary conditions, along with all
# the silly configuration options for how to solve the nonlinear system.
ice_shelf = icepack.IceShelf(dirichlet_boundary_ids)

# Solve for the ice velocity!
u = ice_shelf.solve(h, theta, u0)

# Plot the result.
fig, ax = plt.subplots()
ax.set_aspect('equal')
icepack.plot.plot_field(ax, u)
plt.show(fig)

