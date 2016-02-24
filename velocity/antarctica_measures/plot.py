
import numpy as np
import netCDF4
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

if __name__ == "__main__":
    velocity_data = netCDF4.Dataset("antarctica_ice_velocity_900m.nc", "r")

    vx = velocity_data.variables['vx'][:]
    vy = velocity_data.variables['vy'][:]
    v = np.sqrt(vx**2 + vy**2)

    nx = velocity_data.nx
    ny = velocity_data.ny

    # These are stored as strings in the original netCDF file, so we have to
    # convert them to numbers
    xmin, ymax = float(velocity_data.xmin[:-1]), float(velocity_data.ymax[:-1])
    dx = float(velocity_data.spacing[:-1])

    x = np.asarray([xmin + i * dx for i in range(nx)])
    y = np.asarray([ymax - i * dx for i in range(ny)])

    plt.figure()
    plt.gca().set_aspect('equal')
    plt.contourf(x/1000.0, y/1000.0, v,
                 levels=[1.0e-2, 5.0e-2, 1.0e-1, 5.0e-1,
                         1.0e0, 5.0e0, 1.0e1, 5.0e1,
                         1.0e2, 5.0e2, 1.0e3],
                 shading='faceted', cmap = 'Greys', norm = LogNorm())
    plt.colorbar()
    plt.xlabel('x (km)')
    plt.ylabel('y (km)')
    plt.title("Antarctica ice velocity")
    plt.savefig("antarctica_900m.png", dpi=300)

    velocity_data.close()
