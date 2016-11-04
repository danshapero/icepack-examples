
import math
import numpy as np
import geojson
import netCDF4
from icepack.grid import arcinfo, GridData

filename = "Antarctica_5km_dev1.0.nc"

if __name__ == "__main__":
    dataset = netCDF4.Dataset(filename, "r")
    x = dataset['x1'][:]
    y = dataset['y1'][:]
    T = dataset['temp'][:][0,:,:]
    dataset.close()

    dx, dy = x[1] - x[0], y[1] - y[0]

    with open("../regions/antarctica.geojson", "r") as geojson_file:
        regions = geojson.loads(geojson_file.read())

    for obj in regions['features']:
        name = obj['properties']['name']
        bounding_box = obj['geometry']['coordinates']

        xmin, ymin = bounding_box[0]
        xmax, ymax = bounding_box[1]

        imin = int(math.ceil(ymin - y[0])/dy)
        imax = int(math.floor(ymax - y[0])/dy)

        jmin = int(math.ceil(xmin - x[0])/dx)
        jmax = int(math.floor(xmax - x[0])/dx)

        T_region = T[imin:imax, jmin:jmax]

        arcinfo.write(name.lower() + "-temp.txt",
                      GridData(x[jmin:jmax], y[imin:imax], T_region, -9999.0))
