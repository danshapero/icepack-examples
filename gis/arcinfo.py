
import numpy as np

# --------------------------------------
def write(filename, x, y, data, missing):
    """
    Write a gridded data set to an ArcInfo ASCII format file, which can be read
    by GIS software such as ArcGIS or QGIS.

    Parameters:
    ==========
    filename: the destination file
    x, y: coordinates of the grid nodes
    data: the gridded data set values at x, y
    missing: value to indicate no data at a given point
    """
    nx = len(x)
    ny = len(y)

    if (ny, nx) != np.shape(data):
        raise Exception()

    with open(filename, "w") as fid:
        fid.write("ncols           {0}\n".format(nx))
        fid.write("nrows           {0}\n".format(ny))
        fid.write("xllcorner       {0}\n".format(x[0]))
        fid.write("yllcorner       {0}\n".format(y[0]))
        fid.write("cellsize        {0}\n".format(x[1] - x[0]))
        fid.write("NODATA_value    {0}\n".format(missing))

        for i in range(ny-1, -1, -1):
            for j in range(nx):
                fid.write("{0} ".format(data[i, j]))
            fid.write("\n")


# ----------------
def read(filename):
    """
    Read an ArcInfo ASCII file into a gridded data set.

    Returns:
    =======
    x, y: coordinates of the grid points
    data: data values at the grid points
    missing: value to indicate missing data at a grid point
    """
    with open(filename, "r") as fid:
        def rd():
            return fid.readline().split()[1]

        nx = int(rd())
        ny = int(rd())
        xo = float(rd())
        yo = float(rd())
        dx = float(rd())
        missing = float(rd())

        x = np.array([xo + dx * i for i in range(nx)], dtype = np.float64)
        y = np.array([yo + dx * i for i in range(ny)], dtype = np.float64)
        data = np.zeros((ny, nx), dtype = np.float64)

        for i in range(ny-1, -1, -1):
            data[i, :] = map(float, fid.readline().split())

        return x, y, data, missing
