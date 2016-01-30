
from osgeo import gdal
import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":
    dem = gdal.Open("krigged_dem_nsidc.bin")

    gt = dem.GetGeoTransform()
    xmin, ymax = gt[0], gt[3]
    dx, dy = gt[1], gt[5]

    nx, ny = dem.RasterXSize, dem.RasterYSize
    s = dem.GetRasterBand(1).ReadAsArray()
    for i in range(ny):
        for j in range(nx):
            s[i, j] = max(s[i, j], 0.0)

    x = np.asarray([xmin + i*dx for i in range(nx)])
    y = np.asarray([ymax - i*dx for i in range(ny)])

    plt.figure()
    plt.gca().set_aspect('equal')
    plt.contourf(x/1000.0, y/1000.0, s, 36, shading='faceted', cmap = 'Greys')
    plt.colorbar()
    plt.xlabel('x (km)')
    plt.ylabel('y (km)')
    plt.title('Antarctica surface elevation')
    plt.savefig("antarctica_dem.png", dpi=300)

