
import numpy as np
import matplotlib.pyplot as plt
import icepack, icepack.plot

import preprocess
preprocess.main()

# All of this is the same as example 3.
vx_obs = icepack.read_arc_ascii_grid(open("ross-vx.txt", "r"))
vy_obs = icepack.read_arc_ascii_grid(open("ross-vy.txt", "r"))
h_obs = icepack.read_arc_ascii_grid(open("ross-h.txt", "r"))

mesh = icepack.read_msh("ross.msh")
discretization = icepack.make_discretization(mesh, 1)

v = icepack.interpolate(discretization, vx_obs, vy_obs)
h0 = icepack.interpolate(discretization, h_obs)
theta = icepack.interpolate(discretization, lambda x: 253.0)

dirichlet_boundary_ids = {2, 3, 4, 5}
ice_shelf = icepack.IceShelf(dirichlet_boundary_ids);
u0 = ice_shelf.solve(h0, theta, v)

# And this should be familiar from example 2.
dt = min(1.0, icepack.compute_timestep(0.5, u0))

# Make a steady-state accumulation rate field.
a0 = icepack.interpolate(discretization, lambda x: 0.0)
a0 = (ice_shelf.solve(dt, h0, a0, u0, h0) - h0) / dt

# Really hacky way to compute the average of a field.
one = icepack.interpolate(discretization, lambda x: 1.0)
a_avg = icepack.inner_product(a0, one) / icepack.norm(one)**2

# Make things even simpler by replacing the accumulation with its average.
a = icepack.interpolate(discretization, lambda x: a_avg)

h, u = h0, u0

# Pick a final time and compute the number of timesteps
T = 50.0
N = int(T / dt)
for k in range(N):
    fig, axes = plt.subplots(ncols=2)
    for ax in axes:
        ax.set_aspect('equal')
    ctr_h = icepack.plot.plot_field(axes[0], h)
    ctr_u = icepack.plot.plot_field(axes[1], u)
    fig.colorbar(ctr_h, ax=axes[0], fraction=0.046, pad=0.04)
    fig.colorbar(ctr_u, ax=axes[1], fraction=0.046, pad=0.04)
    fig.tight_layout()
    plt.show(fig)

    h = ice_shelf.solve(dt, h, a, u, h0)
    u = ice_shelf.solve(h, theta, u0)

