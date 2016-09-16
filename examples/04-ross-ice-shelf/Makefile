
.PHONY: clean
.SECONDARY:

ross_ice_shelf: ross_ice_shelf.cpp
	mkdir -p build
	cd build && cmake -DCMAKE_BUILD_TYPE=Release .. && make
	mv build/ross_ice_shelf ./

ross.msh: ../../data/meshes/ross/ross.msh
	cp $< ./

ross-vx.txt ross-vy.txt: ../../data/measures_antarctica/$@ ross.msh
	python preprocess.py ross.msh ../../data/measures_antarctica/$@ $@

ross-h.txt: ../../data/bedmap2/ross-h.txt ross.msh
	python preprocess.py ross.msh $< $@

run: ross_ice_shelf ross.msh ross-h.txt ross-vx.txt ross-vy.txt
	./ross_ice_shelf ross.msh ross-h.txt ross-vx.txt ross-vy.txt

doc: ross_ice_shelf.cpp
	pyccoon -d doc -s ./

clean:
	rm -rf build doc ross_ice_shelf ross.msh ross-h.txt ross-vx.txt ross-vy.txt *.ucd
