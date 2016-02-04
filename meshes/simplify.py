
import numpy as np
from numpy.linalg import det


def dist(p1, p2, p3):
    return np.sqrt(0.5 * np.abs(det(np.array([p2 - p1, p3 - p1]))))


# --------------------------------------
def ramer_douglas_peucker(x, y, epsilon):
    """
    Given an input curve, simplify it using the Ramer-Douglas-Peucker algorithm
    and return a mask of boolean values indicating which points to keep
    """
    n = len(x)

    mask = np.zeros(n, dtype = bool)
    mask[0] = True
    mask[-1] = True
    stack = [(0, n-1)]
    while stack:
        k1, k2 = stack.pop()

        p1 = np.array([x[k1], y[k1]])
        p2 = np.array([x[k2], y[k2]])

        k = np.argmax([dist(p1, p2, np.array([x[i], y[i]]))
                       for i in range(k1, k2)]) + k1

        if dist(p1, p2, np.array([x[k], y[k]])) > epsilon:
            mask[k] = True
            stack.append((k1, k))
            stack.append((k, k2))

    return mask
