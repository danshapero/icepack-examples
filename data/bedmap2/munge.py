
import math
from osgeo import gdal
import numpy as np
import geojson

from icepack.grid import arcinfo, GridData


def get_feature_name(geojson_obj):
    return geojson_obj['properties']['name']

def get_feature_bounding_box(geojson_obj):
    return geojson_obj['geometry']['coordinates']


if __name__ == "__main__":
    dem = gdal.Open("bedmap2_bin/bedmap2_thickness.flt")
    icemask = gdal.Open("bedmap2_bin/bedmap2_icemask_grounded_and_shelves.flt")

    gt = dem.GetGeoTransform()
    Xmin, Ymax = gt[0], gt[3]
    dx, dy = gt[1], gt[5]

    raster_band = dem.GetRasterBand(1)
    no_data = raster_band.GetNoDataValue()
    h = raster_band.ReadAsArray()

    mask = icemask.GetRasterBand(1).ReadAsArray()

    with open("../regions/antarctica.geojson", "r") as geojson_file:
        regions = geojson.loads(geojson_file.read())

    for obj in regions['features']:
        name = get_feature_name(obj).lower()
        bounding_box = get_feature_bounding_box(obj)

        xmin, ymin = bounding_box[0]
        xmax, ymax = bounding_box[1]

        imax = int(math.floor((Ymax - ymax) / dx))
        imin = int(math.ceil((Ymax - ymin) / dx))

        jmax = int(math.ceil((xmax - Xmin) / dx))
        jmin = int(math.floor((xmin - Xmin) / dx))

        h_region = (h[imax:imin, jmin:jmax])[::-1,:]
        mask_region = (mask[imax:imin, jmin:jmax])[::-1,:]

        x = np.linspace(Xmin + jmin*dx, Xmin + jmax*dx, jmax - jmin, False)
        y = np.linspace(Ymax - imin*dx, Ymax - imax*dx, imin - imax, False)

        arcinfo.write(open(name + "-h.txt", "w"),
                      GridData(x, y, h_region, no_data))
        arcinfo.write(open(name + "-mask.txt", "w"),
                      GridData(x, y, mask_region, no_data))
