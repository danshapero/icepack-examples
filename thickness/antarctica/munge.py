
import math
from osgeo import gdal
import numpy as np

import regions
from gis import arcinfo

if __name__ == "__main__":
    dem = gdal.Open("bedmap2_bin/bedmap2_thickness.flt")

    gt = dem.GetGeoTransform()
    Xmin, Ymax = gt[0], gt[3]
    dx, dy = gt[1], gt[5]

    nx, ny = dem.RasterXSize, dem.RasterYSize
    raster_band = dem.GetRasterBand(1)
    no_data = raster_band.GetNoDataValue()

    h = raster_band.ReadAsArray()

    for name, region in regions.antarctica.items():
        xmin, xmax = region['x']
        ymin, ymax = region['y']

        imax = int(math.floor((Ymax - ymax) / dx))
        imin = int(math.ceil((Ymax - ymin) / dx))

        jmax = int(math.ceil((xmax - Xmin) / dx))
        jmin = int(math.floor((xmin - Xmin) / dx))

        h_region = (h[imax:imin, jmin:jmax])[::-1,:]

        x = np.linspace(Xmin + jmin*dx, Xmin + jmax*dx, jmax - jmin, False)
        y = np.linspace(Ymax - imin*dx, Ymax - imax*dx, imin - imax, False)

        arcinfo.write(name.lower() + "-h.txt", x, y, h_region, no_data)
