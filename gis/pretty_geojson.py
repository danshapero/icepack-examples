import sys
import geojson

def prettify(filename, output_filename):
    with open(filename, "r") as input_file:
        d = geojson.loads(input_file.read())

    with open(output_filename, "w") as output_file:
        output_file.write(geojson.dumps(d, indent = 2))


if __name__ == "__main__":
    prettify(sys.argv[1], sys.argv[1])
