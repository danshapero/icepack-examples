
This repository contains computational meshes of various prominent outlet glaciers and assorted tools for the munging thereof.
Here's hoping I can save you the aggravation of doing this yourself.
The meshes are all stored either in either or both of two formats:

* the format used in the program [Triangle](http://www.cs.cmu.edu/~quake/triangle.html), i.e. a `.poly` file for a PSLG or a `.node`, `.ele`, `.edge`, `.neigh` etc. file for a complete Triangular mesh
* the `.geo` and `.msh` formats used by [gmsh](http://gmsh.info/).

I drew some of the mesh outlines by hand in QGIS from a combination Landsat 8 imagery and whichever data sets I was using; some of them come from around the internet.
If someone else made the mesh and it's somewhere on the internet, I include scripts for fetching the original mesh and whatever I used to convert that mesh from its original format.


### Dependencies

* Python 3
* numpy/scipy
* zlib

Other programs that are useful:

* [gmsh](http://gmsh.info/) and [Triangle](https://www.cs.cmu.edu/~quake/triangle.html/), 2D unstructured mesh generators
* [tethex](https://github.com/martemyev/tethex) converts triangular meshes into quad meshes, such as would be used in [deal.II](http://github.com/dealii/dealii)
