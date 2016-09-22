
This repository contains scripts I've used for processing various glaciological data and computational meshes as part of my research.
Here's hoping I can save you the aggravation of doing this yourself.

The processed data sets are used as inputs for example programs demonstrating the functionality of the glacier flow modelling library [icepack](http://github.com/danshapero/icepack).
The example codes for icepack are contained in the directory `../examples`.


### DEMs, velocity maps

Most of these come from the [National Snow and Ice Data Center (NSIDC)](http://www.nsidc.org) or the [Center for Remote Sensing of Ice Sheets (CReSIS)](https://www.cresis.ku.edu/).
For each data source, I include a script `fetch.py` for retrieving it from wherever it originated and another script `munge.py` for extracting what I need from it or other processing.
For example, the MeASUREs data set is rather large, so the data munging script extracts a few interesting regions (Amundsen Sea Embayment, Ross Ice Shelf, etc.) and writes them to ArcInfo ASCII Grid format.
I usually convert everything to this format because it's human- and QGIS-readable and I can write a parser for it in a few minutes in any programming language whether or not it has GDAL bindings.


### Computational meshes

The meshes are all stored either in either or both of two formats:

* the format used in the program [Triangle](http://www.cs.cmu.edu/~quake/triangle.html), i.e. a `.poly` file for a PSLG or a `.node`, `.ele`, `.edge`, `.neigh` etc. file for a complete Triangular mesh
* the `.geo` and `.msh` formats used by [gmsh](http://gmsh.info/).

I drew some of the mesh outlines by hand in QGIS from a combination Landsat 8 imagery and whichever data sets I was using; some of them come from around the internet.
If I hand-drew the mesh, I include any hand-drawn geometries in GeoJSON format as well as scripts for combining the geometries into the mesh boundary.
If someone else made the mesh and it's somewhere on the internet, I include scripts for fetching the original mesh and whatever I used to convert that mesh from its original format.


### Dependencies

* Python 3
* numpy/scipy
* osgeo
* GDAL
* netCDF
* geojson
* zlib
* gmsh
* [icepack](http://github.com/danshapero/icepack.git)

The python helper scripts included with icepack must be installed somewhere on your `PYTHONPATH`, e.g. in `$HOME/.local` or `/usr/local/`.


### Rationale

I regularly work from 3 different computers with butt in chair, and 2/3 others over SSH, so putting all data and mesh munging into one version-controlled repository that I can easily sync between them is time saved.
Additionally, the processed data sets are used in the example programs for icepack.
Also, I believe as a matter of principle that all workflows should be reproducible and the provenance of all data should be easily trackable.
