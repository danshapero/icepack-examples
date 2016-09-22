
# icepack-examples

This directory contains the example code for icepack.
The core icepack library and the icepack python library must be installed on your path somewhere.
Some examples use purely synthetic data; others use real data sets, which can be fetched and processed using the scripts in `../data/`.
Each example folder contains a Makefile which wraps most of the build process (invoking CMake with the right flags, building, etc.) in a single command.

Every example program should be commented to explain all of the major steps.
Rather than read the source code directly, you can invoke

    make doc

in any of the example directories to build an HTML page with a nicer view of the source code.
This will show any explanatory notes and mathematics alongside the source code itself.

If any of documentation doesn't make sense or explain the code enough, please raise an issue on the icepack-examples github repository.
These examples are to show you how to use icepack, so if they don't make sense then I haven't done my job!


### Makefile targets

Every makefile has 3 targets:

* `run`: execute the example program, possibly building the program if it hasn't already
* `doc`: generate the HTML documentation into the folder `doc`; to view it, open `doc/index.html` in your browser
* `clean`: delete any generated files; the compiled program, the program output, the documentation, etc.

TODO: a `plot` target


### Dependencies

* [pyccoon](https://github.com/ckald/pyccoon) for making documentation
* TODO: matplotlib for postprocessing

