
#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import icepack, icepack.plot

# This function pulls in the mesh and observational data that we'll use.
import preprocess
preprocess.main()

# Read in the observational data.
vx_obs = icepack.read_arc_ascii_grid(open("ross-vx.txt", "r"))
vy_obs = icepack.read_arc_ascii_grid(open("ross-vy.txt", "r"))
h_obs = icepack.read_arc_ascii_grid(open("ross-h.txt", "r"))

mesh = icepack.read_msh("ross.msh")
fig, ax = plt.subplots()
ax.set_aspect('equal')
icepack.plot.plot_mesh(ax, mesh)
plt.show(fig)

discretization = icepack.make_discretization(mesh, 1)

v = icepack.interpolate(discretization, vx_obs, vy_obs)
h = icepack.interpolate(discretization, h_obs)

# Make a dumb guess for the ice temperature. In "real life", you would want to
# use an inverse method that would tune the temperature to fit observations.
theta = icepack.interpolate(discretization, lambda x: 263.0)

# Solve for the ice velocity, assuming this guess for the temperature.
dirichlet_boundary_ids = {2, 3, 4, 5}
ice_shelf = icepack.IceShelf(dirichlet_boundary_ids)
u = ice_shelf.solve(h, theta, v)

print("Misfit between computed and observed velocities: {}"
      .format(icepack.dist(u, v) / icepack.norm(v)))

fig, axes = plt.subplots(ncols=2, sharey=True)
for ax in axes:
    ax.set_aspect('equal')
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)
ctr_u = icepack.plot.plot_field(axes[0], u)
ctr_v = icepack.plot.plot_field(axes[1], v)
fig.colorbar(ctr_v, ax=axes[1], fraction=0.046, pad=0.04)
fig.tight_layout()
plt.show(fig)

