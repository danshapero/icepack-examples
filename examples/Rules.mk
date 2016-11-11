
.PHONY: clean
.SECONDARY:

SOURCE=$(PROGRAM).cpp

$(PROGRAM): $(SOURCE) $(HEADERS)
	mkdir -p build
	cd build && cmake -DCMAKE_BUILD_TYPE=Release .. && make
	mv build/$(PROGRAM) ./

run: $(PROGRAM) $(ARGS)
	./$(PROGRAM) $(ARGS)

doc: $(SOURCE)
	pyccoon -d doc -s ./

clean::
	rm -rf build doc *.ucd $(PROGRAM)
