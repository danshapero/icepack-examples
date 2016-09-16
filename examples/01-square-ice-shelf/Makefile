
.PHONY: clean
.SECONDARY:

square_ice_shelf: square_ice_shelf.cpp
	mkdir -p build
	cd build && cmake -DCMAKE_BUILD_TYPE=Release .. && make
	mv build/square_ice_shelf ./

run: square_ice_shelf
	./square_ice_shelf

clean:
	rm -rf build square_ice_shelf *.ucd

