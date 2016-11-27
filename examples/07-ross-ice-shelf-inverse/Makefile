
PROGRAM=ross_ice_shelf_inverse
HEADERS=data.hpp
ARGS=ross.msh ross-h.txt ross-vx.txt ross-vy.txt ross-err.txt
include ../Rules.mk

ross.msh: ../../data/meshes/ross3/ross.msh
	cp $< ./

ross-vx.txt ross-vy.txt ross-err.txt: ../../data/measures_antarctica/$@ ross.msh
	python preprocess.py ross.msh ../../data/measures_antarctica/$@ $@

ross-h.txt: ../../data/bedmap2/ross-h.txt ross.msh
	python preprocess.py ross.msh $< $@

clean::
	rm -rf $(ARGS)
