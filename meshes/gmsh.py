
import numpy as np

# ---------------------------------------
def write(filename, x, y, bnd, triangles):
    num_nodes = len(x)
    num_triangles, _ = np.shape(triangles)

    with open(filename, "w") as msh_file:
        msh_file.write("$MeshFormat\n")
        msh_file.write("2.0 0 8\n")
        msh_file.write("$EndMeshformat\n")

        msh_file.write("$Nodes\n")
        msh_file.write("{0}\n".format(num_nodes))
        for i in range(num_nodes):
            msh_file.write("{0} {1} {2} 0.0\n".format(i+1, x[i], y[i]))
        msh_file.write("$EndNodes\n")

        msh_file.write("$Elements\n")
        msh_file.write("{0}\n".format(num_triangles))
        for n in range(num_triangles):
            t = [k + 1 for k in triangles[n, :]]
            msh_file.write("{0} 2 0 {1} {2} {3}\n".format(n+1, t[0], t[1], t[2]))
        msh_file.write("$Endelements\n")
