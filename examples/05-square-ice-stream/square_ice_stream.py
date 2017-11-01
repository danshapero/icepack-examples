
import numpy as np, matplotlib.pyplot as plt
import icepack, icepack.plot
from icepack import rho_ice, rho_water, gravity

# All of this is similar to example 1.
import make_mesh
length, width = 20.0e3, 20.0e3
make_mesh.main(length, width, "rectangle")

mesh = icepack.read_msh("rectangle.msh")
mesh.refine_global(3)
discretization = icepack.make_discretization(mesh, 1)

h0, dh = 500.0, 250.0
def thickness(x):
    return h0 - dh * x[0] / length

h = icepack.interpolate(discretization, thickness)
u0, du = 200.0, 200.0
v = icepack.interpolate(discretization,
                        lambda x: u0 + du * x[0] / length, lambda x: 0.0)
theta = icepack.interpolate(discretization, lambda x: 254.15)


# For a grounded ice stream, we also need to pick the surface elevation (or
# equivalently the bed elevation). Make the surface elevation at 50m above
# flotation.
def surface(x):
    return (1 - rho_ice / rho_water) * thickness(x) + 20
s = icepack.interpolate(discretization, surface)

# We also need to set the friction coefficient, which we'll choose to be a low
# value throughout but with a jump in the center of the domain.
def friction(x):
    bump = (length/4 < x[0] < 3*length/4) and (width/4 < x[1] < 3*width/4)
    return 5.0e-4 + 1.0e-3 * bump
beta = icepack.interpolate(discretization, friction)

# Finally, make a model object and solve for the ice velocity.
ice_stream = icepack.IceStream({1})
u = ice_stream.solve(h, s, theta, beta, v)

fig, ax = plt.subplots()
ax.set_aspect('equal')
ctr = icepack.plot.plot_field(ax, u)
fig.colorbar(ctr, ax=ax)
plt.show(fig)

