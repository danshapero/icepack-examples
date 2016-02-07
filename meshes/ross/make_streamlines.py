
from gis import arcinfo
from meshes import streamlines as sl
import numpy as np
import geojson

if __name__ == "__main__":
    with open("ross_front.geojson", "r") as inflow:
        text = inflow.read()

    raw_json = geojson.loads(text)
    X0 = np.array(raw_json['features'][0]['geometry']['coordinates'])

    x0, y0 = X0[:,0], X0[:,1]

    x, y, vx, missing = arcinfo.read("../../velocity/antarctica/ross-vx.txt")
    x, y, vy, missing = arcinfo.read("../../velocity/antarctica/ross-vy.txt")

    Vx, Vy = (vx != missing) * vx, (vy != missing) * vy

    S = [sl.streamline(x, y, Vx, Vy, X0, Y0, -1) for (X0, Y0) in zip(x0, y0)]

    features = [geojson.Feature(geometry = geojson.LineString(s)) for s in S]
    feature_collection = geojson.FeatureCollection(features,
                                                   crs = raw_json['crs'])

    with open("ross_streamlines.geojson", "w") as streamlines_file:
        streamlines_file.write(geojson.dumps(feature_collection, indent = 2))
