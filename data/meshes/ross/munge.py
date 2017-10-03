
import geojson
from icepack.mesh import stitch, geo


# ----------------------------
class GeometryError(Exception):
    def __init__(self, geometry_type):
        self.geometry_type = geometry_type

    def __str__(self):
        return geometry_type


# -----------------------
if __name__ == "__main__":
    input_filenames = ["ross_front.geojson", "roosevelt_island.geojson",
                       "ross_inflow.geojson", "ross_sides.geojson"]

    Xs = []
    for input_filename in input_filenames:
        with open(input_filename, "r") as input_file:
            dataset = geojson.loads(input_file.read())
            for feature in dataset['features']:
                if feature['geometry']['type'] != 'LineString':
                    raise GeometryError(feature['geometry']['type'])

                X = feature['geometry']['coordinates']
                Xs.append(X)

    Xs, successors = stitch.segment_successors(Xs)
    geo.write(open("ross.geo", "w"), Xs, successors, dx = 5.0e4, quad = True)
