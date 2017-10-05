
import subprocess
import os.path

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

Line Loop(9) = {{5, 6, 7, 8}};

Plane Surface(10) = {{9}};

Recombine Surface{{10}};
Mesh.SubdivisionAlgorithm=1;
Mesh.Algorithm=8;
"""

def main(length, width, filename):
    if not os.path.isfile(filename):
        with open(filename, "w") as geo_file:
            geo_file.write(text.format(length=length, width=width))
        subprocess.call(["gmsh", "-2", filename])

if __name__ == "__main__":
    main(20.0e3, 20.0e3, "rectangle.geo")

