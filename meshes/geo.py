
import numpy as np


# ---------------------------------
def write(filename, x, y, components):
    with open(filename, "w") as geo_file:
        geo_file.write("cl = 1.0e+22;\n")

        # Write out the PSLG nodes
        count = 1
        num_nodes = len(x)
        for i in range(len(x)):
            geo_file.write("Point({0}) = {{{1}, {2}, 0.0, cl}};\n"
                           .format(count + i, x[i], y[i]))

        count += num_nodes

        # Write out the PSLG edges
        for component in components:
            n = len(component)
            for k in range(n):
                geo_file.write("Line({0}) = {{{1}, {2}}};\n"
                               .format(count + k,
                                       component[k] + 1,
                                       component[(k + 1) % n] + 1))
            count += n
