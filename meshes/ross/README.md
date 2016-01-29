
[Original source.](http://websrv.cs.umt.edu/isis/index.php/Ice_shelves)

This directory contains scripts for fetching and unpacking a mesh of the Ross ice shelf used for demos during the 2009 Portland, OR Summer Modeling School.
Near as I can tell, the mesh was made in COMSOL by Todd Dupont and Olga Sergienko.

The Python script `fetch` retrieves the mesh from the interwebs and unpacks it from the original format, a Matlab `.mat` archive.
The `munge` script does various manipulations to turn the mesh into a format I can use.
In particular, I'd like to take the original domain and remesh it at a coarser resolution using a quad mesh, so that I can do computations with [deal.II](http://www.dealii.org).
This involves extracting the boundary from the original mesh, which is more complicated than it sounds.
