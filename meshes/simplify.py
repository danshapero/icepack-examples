
import numpy as np
from numpy.linalg import eig

# -------------------------------------------------
def extract_segment(k1, k2, component, index, x, y):
    if k1 < k2:
        return x[index[component[k1:k2]]], y[index[component[k1:k2]]]

    X1, Y1 = x[index[component[k1:]]], y[index[component[k1:]]]
    X2, Y2 = x[index[component[:k2]]], y[index[component[:k2]]]

    return np.concatenate([X1, X2]), np.concatenate([Y1, Y2])


# -------------------------------------
def straightness(k1, k2, component, index, x, y):
    X, Y = extract_segment(k1, k2, component, index, x, y)
    L, _ = eig(np.cov(X, Y))
    return L[1] / L[0]


# --------------------------------------------------------
def longest_linear_segment(K, component, index, x, y, tol):
    """
    Given a component of a PSLG and a starting index, return the indices of the
    longest segment of the input comonent which is close to linear
    """
    n = len(component)

    k1 = K
    k2 = (k1 + 2) % n

    while True:
        if straightness(k1, (k2 + 1) % n, component, index, x, y) > tol:
            break
        k2 = (k2 + 1) % n

    while True:
        if straightness((k1 - 1) % n, k2, component, index, x, y) > tol:
            break
        k1 = (k1 - 1) % n

    return k1, k2
