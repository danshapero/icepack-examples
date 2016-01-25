
import urllib.request
import gzip
import numpy as np
import scipy.io

import meshes.triangle
import meshes.gmsh

url = "http://websrv.cs.umt.edu/isis/images/4/4d/Mesh_RIS.mat.gz"
filename = "Mesh_RIS.mat"

if __name__ == "__main__":
    # Download the archived mesh and extract it
    urllib.request.urlretrieve(url, filename + ".gz")
    with gzip.open(filename + ".gz", "rb") as zipfile:
        contents = zipfile.read()
        with open(filename, "wb") as matfile:
            matfile.write(contents)

    # Read in the matlab archive of the mesh
    ross = scipy.io.loadmat("Mesh_RIS.mat")
    num_elements = ross['nel'][0][0]
    num_nodes = ross['nods'][0][0]

    def fetch(key):
        return np.asarray([dat[0] for dat in ross[key]])

    x, y = fetch('x'), fetch('y')

    boundary, ice_front = fetch('bdynode'), fetch('icefntnode')
    bnd = boundary + ice_front

    triangles = np.asarray([[k-1 for k in t] for t in ross['index']])

    # Write the original mesh to both the Triangle gmsh formats
    meshes.triangle.write("ross_original.1", x, y, bnd, triangles)
    meshes.gmsh.write("ross_original.msh", x, y, bnd, triangles)
