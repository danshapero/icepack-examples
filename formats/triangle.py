
import numpy as np

# -----------------
def read(file_stem):
    """
    Read in a mesh in Triangle's format.

    Parameters
    ==========
    file_stem: the stem of the filename for the mesh, so if the mesh is stored
      in the files <meshname>.X.node, <meshname>.X.ele, etc. then the argument
      should be the string "<meshname>.X"

    Returns:
    =======
    x, y: coordinates of the mesh points
    ele: (num_triangles, 3)-array of nodes in each triangle
    edge: (num_edges, 2)-array of nodes on each edge
    neigh: (num_triangles, 3)-array of neighboring triangles of each triangle
    bnd: boundary marker of each node
    edge_bnd: boundary marker of each edge
    """

    x, y, bnd = _read_node(file_stem)
    triangles = _read_ele(file_stem)

    return x, y, triangles, bnd


# -----------------------
def _read_node(file_stem):
    with open(file_stem + ".node", "r") as node_file:
        num_nodes = int(node_file.readline().split()[0])
        x = np.zeros(num_nodes, dtype = np.float64)
        y = np.zeros(num_nodes, dtype = np.float64)
        bnd = np.zeros(num_nodes, dtype = np.int32)

        for i in range(num_nodes):
            line = node_file.readline().split()
            x[i], y[i] = float(line[1]), float(line[2])
            bnd[i] = int(line[3])

    return x, y, bnd


# ----------------------
def _read_ele(file_stem):
    with open(file_stem + ".ele", "r") as ele_file:
        num_triangles = int(ele_file.readline().split()[0])
        triangles = np.zeros((num_triangles, 3), dtype = np.int32)

        for i in range(num_triangles):
            triangles[i, :] = [k - 1 for k in
                               map(int, ele_file.readline().split()[1:])]

    return triangles
