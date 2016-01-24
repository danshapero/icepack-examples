
import scipy.io
import numpy as np

import formats.triangle
import formats.gmsh

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

    formats.triangle.write("ross.1", x, y, bnd, triangles)
    formats.gmsh.write("ross.msh", x, y, bnd, triangles)
