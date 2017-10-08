
import os.path
import subprocess

text = """
cl = 50000.0;
Point(1) = {{0.0, 0.0, 0.0, cl}};
Point(2) = {{{length}, 0.0, 0.0, cl}};
Point(3) = {{{length}, {width}, 0.0, cl}};
Point(4) = {{0.0, {width}, 0.0, cl}};

Line(5) = {{1, 2}};
Line(6) = {{2, 3}};
Line(7) = {{3, 4}};
Line(8) = {{4, 1}};

Physical Line(1) = {{7, 5}};
Physical Line(2) = {{8}};
Physical Line(3) = {{6}};

Line Loop(9) = {{5, 6, 7, 8}};

Plane Surface(10) = {{9}};
Physical Surface(4) = {{10}};

Recombine Surface{{10}};
Mesh.SubdivisionAlgorithm=1;
Mesh.Algorithm=8;
"""

def main(length, width, filename):
    if not os.path.isfile(filename + ".geo"):
        with open(filename + ".geo", "w") as mesh_file:
            mesh_file.write(text.format(length = length, width = width))

        subprocess.call(["gmsh", "-2", filename + ".geo"])


if __name__ == "__main__":
    main(1000.0, 1000.0, "rectangle")

