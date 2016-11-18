
from icepack import ucd
import os
import numpy as np
import matplotlib.pyplot as plt


T0 = 263.15
year = 365.25 * 24 * 60 * 60
A0 = 3.985e-13 * year * 1.0e18 # [A] = MPa^(-3) * years^(-1)
Q_cold = 60
Q_warm = 139
R = 8.314e-3

def f(T):
    Q = Q_cold if T < T0 else Q_warm
    df = 0 if T < T0 else (Q_warm - Q_cold) / (R * T0)
    return Q / (R * T) - df

def A(T):
    return A0 * np.exp(-f(T))

def B(T):
    return A(T)**(-1.0/3)


def read_results(name):
    x, y, cells, theta = ucd.read("theta_" + name + ".ucd")
    _, _, _, u, v = ucd.read("v_" + name + ".ucd")

    triangles = ucd.quad_cells_to_triangles(x, y, cells)

    x /= 1000.0
    y /= 1000.0

    return x, y, triangles, theta, u, v


def plot_results(x, y, triangles, theta, u, v, filename):
    fig, (ax1, ax2) = plt.subplots(1, 2)

    Bs = np.array([B(T) for T in theta])
    ctr1 = ax1.tricontourf(x, y, triangles, Bs,
                           np.linspace(0.0, 0.75, 26),
                           extend = "both", cmap = "viridis")
    ax1.set_aspect('equal')
    ax1.set_xlabel("x (km)", fontsize = 16)
    ax1.set_ylabel("y (km)", fontsize = 16)
    ax1.set_title("Rheology", fontsize = 18)
    cbar1 = fig.colorbar(ctr1, ax = ax1, fraction = 0.046, pad = 0.04)
    cbar1.ax.set_title("MPa years${}^{1/3}$", fontsize = 14)

    ctr2 = ax2.tricontourf(x, y, triangles, np.sqrt(u**2 + v**2),
                           36, extend = "both", cmap = "viridis")
    ax2.set_aspect('equal')
    ax2.set_title("Speed", fontsize = 18)
    ax2.set_xticklabels([])
    ax2.set_yticklabels([])
    cbar2 = fig.colorbar(ctr2, ax = ax2, fraction = 0.046, pad = 0.04)
    cbar2.ax.set_title("m/a", fontsize = 14)

    plt.tight_layout()
    plt.savefig(filename + ".png", dpi = 100, bbox_inches = "tight")
    plt.close(fig)


if __name__ == "__main__":
    filenames = [f[6:-4] for f in os.listdir()
                 if f[-4:] == ".ucd" and f[:6] == "theta_"]

    for filename in filenames:
        x, y, triangles, theta, u, v = read_results(filename)
        plot_results(x, y, triangles,
                     theta, u, v,
                     "ross-shelf-" + filename)
