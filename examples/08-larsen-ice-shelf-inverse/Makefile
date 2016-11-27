
PROGRAM=larsen_ice_shelf_inverse
HEADERS=data.hpp
ARGS=larsen.msh larsen-h.txt larsen-vx.txt larsen-vy.txt larsen-err.txt
include ../Rules.mk

larsen.msh: ../../data/meshes/larsen/larsen.msh
	cp $< ./

larsen-vx.txt larsen-vy.txt larsen-err.txt: ../../data/measures_antarctica/$@ larsen.msh
	python preprocess.py larsen.msh ../../data/measures_antarctica/$@ $@

larsen-h.txt: ../../data/bedmap2/larsen-h.txt larsen.msh
	python preprocess.py larsen.msh $< $@

clean::
	rm -rf $(ARGS)
