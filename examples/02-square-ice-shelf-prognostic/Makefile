
.PHONY: clean
.SECONDARY:

ice_shelf_prognostic: ice_shelf_prognostic.cpp data.cpp
	mkdir -p build
	cd build && cmake -DCMAKE_BUILD_TYPE=Release .. && make
	mv build/ice_shelf_prognostic ./

run: ice_shelf_prognostic
	./ice_shelf_prognostic

doc: ice_shelf_prognostic.cpp
	pyccoon -s ./ -d doc

clean:
	rm -rf build doc ice_shelf_prognostic *.ucd

