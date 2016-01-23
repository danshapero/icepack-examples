
import scipy.io
import numpy as np

if __name__ == "__main__":
    ross = scipy.io.loadmat("Mesh_RIS.mat")
    num_elements = ross['nel'][0][0]
    num_nodes = ross['nods'][0][0]

    def fetch(key):
        return np.asarray([dat[0] for dat in ross[key]])

    x, y = fetch('x'), fetch('y')

    boundary, ice_front = fetch('bdynode'), fetch('icefntnode')
    bnd = boundary + ice_front

    triangles = np.asarray(ross['index'])

    with open("ross.1.node", "w") as node:
        node.write("{0} 2 0 1\n".format(num_nodes))
        for i in range(num_nodes):
            node.write("{0} {1} {2} {3}\n".format(i + 1, x[i], y[i], bnd[i]))

    with open("ross.1.ele", "w") as ele:
        ele.write("{0} 3 0\n".format(num_elements))
        for i in range(num_elements):
            t = triangles[i]
            ele.write("{0} {1} {2} {3}\n".format(i+1, t[0], t[1], t[2]))
