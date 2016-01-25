
import scipy.io
import numpy as np
from scipy.sparse import lil_matrix
from matplotlib.path import Path

import meshes.triangle
import meshes.gmsh

# ===========================================================================
# The following routines are used to turn the original triangular mesh of the
# Ross Ice Shelf into a planar straight-line graph (PSLG) of its boundary.
#
# This is a somewhat complicated operation. We only have the node coordinates,
# indices of the nodes in each triangle, and boundary markers of the original
# triangulation. To get extract the PSLG of the boundary, we need to extract
# the boundary from the triangulation with a consistent numbering. Then we
# need to find the connected components of the boundary; for example, there is
# one component corresponding to the whole inflow and front of RIS, and one
# component corresponding to Roosevelt Island. Then we need to determine which
# components are in the interior so that we can find points inside them; these
# hole points are necessary for writing a PSLG in Triangle's format.
# ===========================================================================


# ------------------------------------
def get_boundary_graph(triangles, bnd):
    """
    Return a sparse graph representing the boundary of a triangulation
    """

    num_nodes = len(bnd)
    num_bnd_points = sum(bnd != 0)
    index = np.zeros(num_bnd_points, dtype = np.int32)
    index_inverse = np.zeros(num_nodes, dtype = np.int32)
    count = 0
    for i in range(num_nodes):
        if bnd[i] != 0:
            index[count] = i
            count += 1

    for i in range(num_bnd_points):
        index_inverse[index[i]] = i

    g = lil_matrix((num_bnd_points, num_bnd_points), dtype = np.int32)
    num_triangles, _ = np.shape(triangles)
    for n in range(num_triangles):
        triangle = triangles[n, :]
        for k in range(3):
            i, j = triangle[k], triangle[(k + 1) % 3]
            if bnd[i] != 0 and bnd[j] != 0:
                I, J = index_inverse[[i, j]]
                # Assign a weight to the edge if it's on the boundary. However,
                # just because both vertices of the edge are on the boundary
                # doesn't mean that the edge is! If the current triangle is on
                # a corner, we could have an internal edge, both of whose
                # vertices are on the triangulation boundary. If it is internal
                # then we'll see it twice at some point though, so we can
                # subtract off the current weight and get rid of the erroneous
                # edge eventually.
                weight = max(bnd[i], bnd[j]) - g[I, J]
                g[I, J] = weight
                g[J, I] = weight

    return g, index


# -------------------------
def connected_components(g):
    """
    Given a graph, stored as a scipy sparse matrix, return a list of its
    components
    """
    num_nodes, _ = np.shape(g)

    components = []
    visited = np.zeros(num_nodes, dtype = bool)

    # TODO: make this not so stupid and inefficient
    while not all(visited):
        # TODO: make this also not so stupid and inefficient
        i = np.argmin(visited)
        visited[i] = True
        stack = [i]
        current_component = []

        while stack:
            i = stack.pop()
            current_component.append(i)
            _, neighbors = g[i, :].nonzero()

            for j in neighbors:
                if not visited[j]:
                    visited[j] = True
                    stack.append(j)

        components.append(current_component)

    return components


# ------------------------
class GoofyPSLG(Exception):
    pass


# -----------------------------------------
def outermost_path(components, index, x, y):
    """
    Given a set of connected components of the boundary, find which component
    contains all the others
    """

    # Make a list of lists of the Path object corresponding to each component
    # of the boundary
    gammas = [Path(list(zip(x[index[component]],
                            y[index[component]])),
                   closed = True)
              for component in components]

    # Find which component contains all others
    num_components = len(gammas)
    for i in range(num_components):
        gamma_i = gammas[i]
        for j in range(i + 1, num_components):
            gamma_j = gammas[j]
            if gamma_i.contains_path(gamma_j):
                return i

    # I have no idea how this could happen but I'd sure like to know if it does
    raise GoofyPSLG()


# ---------------------------------------------------------
def get_holes(components, outermost_component, index, x, y):
    """
    To generate a PSLG that Triangle can read, we need to find a point within
    each hole of the triangulation
    """
    xh, yh = [], []
    for n in range(len(components)):
        if n != outermost_component:
            component = components[n]
            gamma = Path(list(zip(x[index[component]],
                                  y[index[component]])),
                         closed = True)

            X, Y = 0.0, 0.0
            i, j = 0, len(gamma)/2 - 1

            while not gamma.contains_point((X, Y)):
                j += 1
                X, Y = 0.5 * (gamma.vertices[i,:] + gamma.vertices[j,:])

            xh.append(X)
            yh.append(Y)

    return np.array(xh), np.array(yh)


if __name__ == "__main__":
    ross = scipy.io.loadmat("Mesh_RIS.mat")
    num_elements = ross['nel'][0][0]
    num_nodes = ross['nods'][0][0]

    def fetch(key):
        return np.asarray([dat[0] for dat in ross[key]])

    x, y = fetch('x'), fetch('y')

    boundary, ice_front = fetch('bdynode'), fetch('icefntnode')
    bnd = boundary + ice_front

    triangles = np.asarray([[k-1 for k in t] for t in ross['index']])

    meshes.triangle.write("ross_original.1", x, y, bnd, triangles)
    meshes.gmsh.write("ross_original.msh", x, y, bnd, triangles)

    g, index = get_boundary_graph(triangles, bnd)
    components = connected_components(g)
    outermost = outermost_path(components, index, x, y)
    xh, yh = get_holes(components, outermost, index, x, y)

    bnd_edges = []
    for component in components:
        n = len(component)
        for i in range(n):
            bnd_edges.append([component[i], component[(i + 1) % n]])
    bnd_edges = np.asarray(bnd_edges)

    meshes.triangle.write_poly("ross.poly",
                               x[index], y[index], bnd[index],
                               bnd_edges, xh, yh)
