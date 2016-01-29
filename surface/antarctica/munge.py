
from osgeo import gdal

if __name__ == "__main__":
    dem = gdal.Open("krigged_dem_nsidc.bin")

    gt = dem.GetGeoTransform()
    xmin, ymax = gt[0], gt[3]
    dx, dy = gt[1], gt[5]

    nx, ny = dem.RasterXSize, dem.RasterYSize
    s = dem.GetRasterBand(1).ReadAsArray()
