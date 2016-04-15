
import numpy as np
import matplotlib.pyplot as plt
import shapefile
from gis import arcinfo, interpolate as itp


def make_streamline(x, y, u, v, missing, x0, y0, d):
    X = [x0]
    Y = [y0]

    while True:
        xt = X[-1]
        yt = Y[-1]

        U = itp.bilinear_interp(x, y, u, missing, xt, yt)
        V = itp.bilinear_interp(x, y, v, missing, xt, yt)

        if U == missing:
            break

        dt = d / np.sqrt(U**2 + V**2)

        X.append(xt + dt * U)
        Y.append(yt + dt * V)

    return X, Y


if __name__ == "__main__":
    xh, yh, h, h_missing = arcinfo.read("thickness/antarctica/ross-h.txt")
    x, y, u, missing = arcinfo.read("velocity/antarctica_measures/ross-vx.txt")
    x, y, v, _ = arcinfo.read("velocity/antarctica_measures/ross-vy.txt")

    h = itp.regrid(xh, yh, h, h_missing, x, y)

    shapes = shapefile.Reader("ross-start-pts").shapes()
    xs = np.array([s.points[0] for s in shapes])

    fig = plt.figure()

    ax1 = plt.subplot(211)
    ax2 = plt.subplot(212)

    M, _ = np.shape(xs)
    for m in range(M):
        X, Y = make_streamline(x, y, u, v, missing, xs[m][0], xs[m][1], 2000.0)
        n = len(X) - 4

        H = np.zeros(n, dtype = np.float64)
        U = np.zeros(n, dtype = np.float64)

        for k in range(n):
            H[k] = max(itp.bilinear_interp(x, y, h, h_missing, X[k], Y[k]), 0)
            vx = itp.bilinear_interp(x, y, u, missing, X[k], Y[k])
            vy = itp.bilinear_interp(x, y, v, missing, X[k], Y[k])
            if vx != missing:
                U[k] = np.sqrt(vx**2 + vy**2)

        L = np.zeros(n, dtype = np.float64)
        for k in range(n-1):
            L[k+1] = L[k] + np.sqrt((X[k+1] - X[k])**2 + (Y[k+1] - Y[k])**2)
        L = np.array(L)
        L /= L[-1]

        ax1.plot(L, H, color = (1.0 - m / M, 0.0, m / M))
        ax2.plot(L, U, color = (1.0 - m / M, 0.0, m / M))

    fig.savefig("ross-transects.png", dpi=100)
