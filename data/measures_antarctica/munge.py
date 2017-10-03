
import numpy as np
import netCDF4
import geojson
import math

from icepack.grid import arcinfo, GridData


def get_feature_name(geojson_obj):
    return geojson_obj['properties']['name']

def get_feature_bounding_box(geojson_obj):
    return geojson_obj['geometry']['coordinates']


if __name__ == "__main__":
    velocity_data = netCDF4.Dataset("antarctica_ice_velocity_900m.nc", "r")

    Xmin, Ymax = float(velocity_data.xmin[:-1]), float(velocity_data.ymax[:-1])
    dx = float(velocity_data.spacing[:-1])

    with open("../regions/antarctica.geojson", "r") as geojson_file:
        regions = geojson.loads(geojson_file.read())

    for obj in regions['features']:
        name = get_feature_name(obj).lower()
        bounding_box = get_feature_bounding_box(obj)

        xmin, ymin = bounding_box[0]
        xmax, ymax = bounding_box[1]

        # The data in the netCDF file are stored upside-down in the `y`-
        # direction, making everything very confusing
        imax = int(math.floor((Ymax - ymax) / dx))
        imin = int(math.ceil((Ymax - ymin) / dx))

        jmax = int(math.ceil((xmax - Xmin) / dx))
        jmin = int(math.floor((xmin - Xmin) / dx))

        ny, nx = imin - imax, jmax - jmin

        vx = (velocity_data['vx'][imax:imin, jmin:jmax])[::-1,:]
        vy = (velocity_data['vy'][imax:imin, jmin:jmax])[::-1,:]

        err = np.zeros((ny, nx), dtype = np.float64)
        err[:,:] = (velocity_data['err'][imax:imin, jmin:jmax])[::-1,:]

        # Anything where the error is 0.0 is really missing data, so fill this
        # in with a tag value
        for i in range(ny):
            for j in range(nx):
                if err[i, j] == 0.0:
                    err[i, j] = -2.0e+9
                    vx[i, j] = -2.0e+9
                    vy[i, j] = -2.0e+9

        x = np.linspace(Xmin + jmin * dx, Xmin + jmax * dx, nx, False)
        y = np.linspace(Ymax - imin * dx, Ymax - imax * dx, ny, False)

        arcinfo.write(open(name + "-vx.txt", "w"), GridData(x, y, vx, -2.0e+9))
        arcinfo.write(open(name + "-vy.txt", "w"), GridData(x, y, vy, -2.0e+9))
        arcinfo.write(open(name + "-err.txt", "w"), GridData(x, y, err, -2.0e+9))

    velocity_data.close()

