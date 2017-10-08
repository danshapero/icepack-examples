
import numpy as np
import matplotlib.pyplot as plt
import icepack, icepack.plot
from icepack import rho_ice, rho_water, gravity, rate_factor

# This is all the same as example 1, with the addition of an accumulation rate.

import make_mesh
length, width = 20.0e3, 20.0e3
make_mesh.main(length, width, "rectangle")

h0, dh = 500.0, 100.0
temp = 254.15

def thickness(x):
    return h0 - dh * x[0] / length

rho = rho_ice * (1 - rho_ice / rho_water)
A = (rho * gravity * h0 / 4)**3 * rate_factor(temp)

def velocity(x):
    u0 = 100.0
    q = 1 - (1 - (dh / h0) * (x[0] / length))**4
    return u0 + 0.25 * A * q * length * h0 / dh

def strain(x):
    q = 1 - (dh / h0) * (x[0] / length)
    return A * q**3

def accumulation(x):
    return 3.0

mesh = icepack.read_msh("rectangle.msh")
mesh.refine_global(3)
discretization = icepack.make_discretization(mesh, 1)

h_in = icepack.interpolate(discretization, thickness)
u0 = icepack.interpolate(discretization, velocity, lambda x: 0.0)
theta = icepack.interpolate(discretization, lambda x: temp)
a = icepack.interpolate(discretization, accumulation)


# --- New stuff! ---

# In example 1, we only cared about where to impose Dirichlet boundary
# conditions when solving for the ice velocity. But when solving for the ice
# thickness as well, we need to distinguish between parts of the boundary
# where ice is actively flowing into the domain as well.
fig, ax = plt.subplots()
ax.set_aspect('equal')
icepack.plot.plot_mesh(ax, mesh)
plt.show(fig)

dirichlet_boundary_ids = {1, 2}
inflow_boundary_ids = {2}
ice_shelf = icepack.IceShelf(dirichlet_boundary_ids)

# This class is used to update the ice thickness, much like how `IceShelf` is
# used to solve for the ice velocity.
mass_transport = icepack.MassTransport(inflow_boundary_ids)

# Next we need to pick a timestep. The prognostic equation for updating the ice
# thickness is hyperbolic, so we need to be careful about choosing a timestep
# that gives a reasonable Courant number for the mesh and velocity field.
courant_number = 0.5
dt = min(1.0/12, icepack.compute_timestep(courant_number, u0))

# Run the simulation for 1 model year.
T = 1.0
N = int(T / dt)

# Initialize the thickness and velocity.
h = icepack.interpolate(discretization, thickness)
u = icepack.interpolate(discretization, velocity, lambda x: 0.0)

# Loop over each timestep...
for k in range(N):
    # solving for the ice thickness and velocity in lockstep.
    h = mass_transport.solve(dt, h, a, u, h_in)
    u = ice_shelf.solve(h, theta, u0)

    # Plot the results as we go!
    fig, axes = plt.subplots(ncols=2)
    for ax in axes:
        ax.set_aspect('equal')
    ctr_h = icepack.plot.plot_field(axes[0], h)
    ctr_u = icepack.plot.plot_field(axes[1], u)
    fig.colorbar(ctr_h, ax=axes[0], fraction=0.046, pad=0.04)
    fig.colorbar(ctr_u, ax=axes[1], fraction=0.046, pad=0.04)
    fig.tight_layout()
    plt.show(fig)

