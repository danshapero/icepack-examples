
import numpy as np


# ---------------------------------
def write(filename, x, y, components):
    with open(filename, "w") as geo_file:
        geo_file.write("cl = 1.0e+22;\n")

        # Write out the PSLG nodes
        count = 1
        num_nodes = len(x)
        for i in range(num_nodes):
            geo_file.write("Point({0}) = {{{1}, {2}, 0.0, cl}};\n"
                           .format(count + i, x[i], y[i]))

        count += num_nodes
        geo_file.write("\n")

        # Write out the PSLG edges
        line_loops = []
        for component in components:
            n = len(component)
            current_loop = []
            for k in range(n):
                geo_file.write("Line({0}) = {{{1}, {2}}};\n"
                               .format(count + k,
                                       component[k] + 1,
                                       component[(k + 1) % n] + 1))
                current_loop.append(count + k)

            line_loops.append(current_loop)
            count += n

        geo_file.write("\n")

        # Write out line loops for each component of the boundary
        plane_surface = []
        for loop in line_loops:
            # First write the line loop
            geo_file.write("Line Loop({0}) = {{{1}"
                           .format(count, loop[0]))

            for k in range(1, len(loop)):
                geo_file.write(", {0}".format(loop[k]))

            geo_file.write("};\n")

            # Then make a compound line for mesh simplification
            geo_file.write("Compound Line({0}) = {{{1}"
                           .format(count + 1, loop[0]))

            for k in range(1, len(loop)):
                geo_file.write(", {0}".format(loop[k]))

            geo_file.write("};\n")

            plane_surface.append(count)
            count += 2
        geo_file.write("\n")

        # Write out a plane surface containing all of the line loops
        geo_file.write("Plane Surface({0}) = {{{1}"
                       .format(count, plane_surface[0]))
        for k in range(1, len(plane_surface)):
            geo_file.write(", {0}".format(plane_surface[k]))
        geo_file.write("};\n\n")

        geo_file.write("Mesh.RecombineAll=1;\n")
        geo_file.write("Mesh.Algorithm=8;\n")
