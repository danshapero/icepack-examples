
import numpy as np
import matplotlib.pyplot as plt
import shapefile
from gis import arcinfo, interpolate


def make_streamline(x, y, u, v, missing, x0, y0, d):
    X = [x0]
    Y = [y0]

    while True:
        xt = X[-1]
        yt = Y[-1]

        U = interpolate.bilinear_interp(x, y, u, missing, xt, yt)
        V = interpolate.bilinear_interp(x, y, v, missing, xt, yt)

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

    h = interpolate.regrid(xh, yh, h, h_missing, x, y)

    shapes = shapefile.Reader("ross-start-pts").shapes()
    xs = np.array([s.points[0] for s in shapes])

    plt.figure()
    plt.gca().set_aspect('equal')
    plt.contourf(x, y, h,
                 np.linspace(0.0, 1000.0, 21), cmap = 'Greys',
                 hold = True)

    for x0, y0 in xs:
        X, Y = make_streamline(x, y, u, v, missing, x0, y0, 2000.0)
        plt.plot(X, Y, color='b', linewidth=0.5, hold = True)

    plt.savefig("ross-transects.png", dpi=100)
