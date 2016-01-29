
This repository contains scripts I've used for processing various glaciological data and computational meshes as part of my research.
Here's hoping I can save you the aggravation of doing this yourself.


## DEMs, velocity maps

Most of these come from the [National Snow and Ice Data Center (NSIDC)](http://www.nsidc.org) or the [Center for Remote Sensing of Ice Sheets (CReSIS)](https://www.cresis.ku.edu/).
For each data source, I include a script `fetch.py` for retrieving it from wherever it originated and another script `munge.py` for extracting what I need from it or other processing.
For example, the MeASUREs data set is rather large, so the data munging script extracts a few interesting regions (Amundsen Sea Embayment, Ross Ice Shelf, etc.) and writes them to ArcInfo ASCII Grid format.
I usually convert everything to this format because it's human- and QGIS-readable and I can write a parser for it in a few minutes in any programming language whether or not it has GDAL bindings.


### Computational meshes

The meshes are all stored either in either or both of two formats:

* the format used in the program [Triangle](http://www.cs.cmu.edu/~quake/triangle.html), i.e. a `.poly` file for a PSLG or a `.node`, `.ele`, `.edge`, `.neigh` etc. file for a complete Triangular mesh
* the `.geo` and `.msh` formats used by [gmsh](http://gmsh.info/).

I drew some of the mesh outlines by hand in QGIS from a combination Landsat 8 imagery and whichever data sets I was using; some of them come from around the internet.
If someone else made the mesh and it's somewhere on the internet, I include scripts for fetching the original mesh and whatever I used to convert that mesh from its original format.


### Dependencies

* Python 3
* numpy/scipy
* osgeo
* GDAL
* netCDF
* zlib

Other programs that are useful:

* [gmsh](http://gmsh.info/) and [Triangle](https://www.cs.cmu.edu/~quake/triangle.html/), 2D unstructured mesh generators
* [tethex](https://github.com/martemyev/tethex) converts triangular meshes into quad meshes, such as would be used in [deal.II](http://github.com/dealii/dealii)


### Rationale

I regularly work from 3 different computers with butt in chair, and 2/3 others over SSH, so putting all data and mesh munging into one version-controlled repository that I can easily sync between them is time saved.
Also, I believe as a matter of principle that all workflows should be reproducible and the provenance of all data should be easily trackable.
