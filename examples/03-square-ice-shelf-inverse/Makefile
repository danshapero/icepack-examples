
.PHONY: clean
.SECONDARY:

ice_shelf_inverse: ice_shelf_inverse.cpp data.cpp
	mkdir -p build
	cd build && cmake -DCMAKE_BUILD_TYPE=Release .. && make
	mv build/ice_shelf_inverse ./

run: ice_shelf_inverse
	./ice_shelf_inverse

clean:
	rm -rf build ice_shelf_inverse *.ucd

