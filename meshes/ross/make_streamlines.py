
from icepack.grid import arcinfo
import streamlines as sl
import numpy as np
import geojson

if __name__ == "__main__":
    raw_json = geojson.loads(open("ross_front.geojson", "r").read())
    X0 = np.array(raw_json['features'][0]['geometry']['coordinates'])

    x0, y0 = X0[:,0], X0[:,1]

    vx = arcinfo.read("../../measures_antarctica/ross-vx.txt")
    vy = arcinfo.read("../../measures_antarctica/ross-vy.txt")

    mask = vx.data != vx.missing
    Vx, Vy = mask * vx.data, mask * vy.data

    S = [sl.streamline(vx.x, vx.y, Vx, Vy, X0, Y0, -1) for (X0, Y0) in zip(x0, y0)]

    features = [geojson.Feature(geometry = geojson.LineString(s)) for s in S]
    feature_collection = geojson.FeatureCollection(features,
                                                   crs = raw_json['crs'])

    with open("ross_streamlines.geojson", "w") as streamlines_file:
        streamlines_file.write(geojson.dumps(feature_collection, indent = 2))
