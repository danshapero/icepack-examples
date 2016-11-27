
import numpy as np

# -------------------------------
def interpolate(x, y, x0, y0, q):
    """
    Interpolate the value of the field `q` defined on the grid `x`, `y`
    to the point `x0`, `y0`
    """
    dx = x[1]-x[0]
    dy = y[1]-y[0]

    i = int( (y0-y[0])/dy )
    j = int( (x0-x[0])/dx )

    alpha_x = (x0 - x[j]) / dx
    alpha_y = (y0 - y[i]) / dy

    p = (q[i,j]
            + alpha_x * (q[i, j + 1] - q[i, j])
            + alpha_y * (q[i + 1, j] - q[i, j])
            + alpha_x * alpha_y * (q[i + 1, j + 1] + q[i, j]
                                     - q[i + 1, j] - q[i, j + 1]))

    return p


# ------------------------------------------------------------------
def streamline(x, y, vx, vy, x0, y0, sign = 1, dx = 150.0):
    """
    Given the x/y velocity fields `vx`, `vy`, defined at the grid points
    `x`, `y`, generate a streamline originating at the point `x0`, `y0`.
    The streamline will go backwards if the optional argument `sign` = -1.

    Precondition: all missing data have been masked to 0.0.

    The algorithm we use is an adaptive forward Euler method. It's not very
    good. Willie hears ye; Willie don't care.

    Parameters:
    ==========
    x, y: coordinates at which the fields are defined
    vx, vy: velocities in the x, y directions
    x0, y0: starting coordinate of the streamline
    sign: optional; =1 if the streamline is forward, -1 if backward
    dx: optional; desired distance for each step

    Returns:
    =======
    X, Y: coordinates of the resultant streamline
    """

    # Find the initial velocity
    u = interpolate(x, y, x0, y0, vx)
    v = interpolate(x, y, x0, y0, vy)
    speed = np.sqrt(u**2 + v**2)

    # Initialize the streamline from the start points
    X = [(x0, y0)]

    # Keep going until we have too many points or the ice speed has dropped to 0
    k = 0
    while (speed > 5.0 and k < 10000 and
           x[0] + dx < x0 < x[-1] - dx and
           y[0] + dx < y0 < y[-1] - dx):
        k += 1
        dt = sign * dx / speed

        x0 = x0 + dt * u
        y0 = y0 + dt * v

        X.append((x0, y0))

        u = interpolate(x, y, x0, y0, vx)
        v = interpolate(x, y, x0, y0, vy)
        speed = np.sqrt(u**2 + v**2)

    return X


# --------------------------------
def coarsen_streamline(X, res):
    """
    Parameters:
    ==========
    X: coordinates of a path
    res:  resolution of the coarsening

    Returns:
    =======
    Xc: coordinates of the coarsened path
    """
    Xc = []

    Xc.append(X[0])

    for i in range(1, len(X)):
        dist = np.sqrt((X[i][0] - Xc[-1][0])**2 + (X[i][1] - Xc[-1][1])**2)
        if dist > res:
            Xc.append(X[i])

    return Xc

