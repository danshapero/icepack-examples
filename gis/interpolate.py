
import numpy as np

def index_of_point(x, y, X, Y):
    i = int((Y - y[0]) / (y[1] - y[0]))
    j = int((X - x[0]) / (x[1] - x[0]))

    if (0 <= i < len(y) - 1 and 0 <= j < len(x) - 1):
        return i, j

    return -1, -1


def is_missing(m, q, i, j):
    return m in [q[i, j], q[i+1, j], q[i, j+1], q[i+1, j+1]]


def regrid(x, y, q, missing, X, Y):
    """
    Interpolate a gridded data set `x, y, q` to a new grid `X, Y`
    """

    nX, nY = len(X), len(Y)
    dx, dy = x[1] - x[0], y[1] - y[0]

    Q = missing * np.ones((nY, nX), dtype = np.float64)

    for I in range(nY):
        for J in range(nX):
            i, j = index_of_point(x, y, X[J], Y[I])
            if not is_missing(missing, q, i, j):
                ax = (X[J] - x[j]) / dx
                ay = (Y[I] - y[i]) / dy
                dx_q = q[i, j+1] - q[i, j]
                dy_q = q[i+1, j] - q[i, j]
                dx_dy_q = q[i, j] + q[i+1, j+1] - q[i+1, j] - q[i, j+1]
                Q[I, J] = q[i, j] + ax * dx_q + ay * dy_q + ax * ax * dx_dy_q

    return Q
