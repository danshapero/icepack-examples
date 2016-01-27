
import numpy as np
import netCDF4
import json
import math

from gis import arcinfo


if __name__ == "__main__":
    # Read in a JSON file describing some interesting regions on the ice sheet
    regions = json.loads(open("regions.json", 'r').read())

    velocity_data = netCDF4.Dataset("antarctica_ice_velocity_900m.nc", "r")

    Xmin, Ymax = float(velocity_data.xmin[:-1]), float(velocity_data.ymax[:-1])
    dx = float(velocity_data.spacing[:-1])

    for name, region in regions.items():
        xmin, xmax = region['x']
        ymin, ymax = region['y']

        # The data in the netCDF file are stored upside-down in the `y`-
        # direction, making everything very confusing
        imax = int(math.floor((Ymax - ymax) / dx))
        imin = int(math.ceil((Ymax - ymin) / dx))

        jmax = int(math.ceil((xmax - Xmin) / dx))
        jmin = int(math.floor((xmin - Xmin) / dx))

        vx = (velocity_data['vx'][imax:imin, jmin:jmax])[::-1,:]
        vy = (velocity_data['vy'][imax:imin, jmin:jmax])[::-1,:]
        err = (velocity_data['err'][imax:imin, jmin:jmax])[::-1,:]

        x = np.linspace(Xmin + jmin * dx, Xmin + jmax * dx, jmax - jmin, False)
        y = np.linspace(Ymax - imin * dx, Ymax - imax * dx, imin - imax, False)

        arcinfo.write(name + "-vx.txt", x, y, vx, -2.0e+9)
        arcinfo.write(name + "-vy.txt", x, y, vy, -2.0e+9)
        arcinfo.write(name + "-err.txt", x, y, err, -2.0e+9)

    velocity_data.close()
