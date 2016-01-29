
import os
import urllib.request

filenames = ["krigged_dem_errormap_nsidc.bin",
             "krigged_dem_nsidc.bin"]

url = "ftp://sidads.colorado.edu/pub/DATASETS/DEM/nsidc0422_antarctic_1km_dem/"

if __name__ == "__main__":
    for filename in filenames:
        for ext in ["", ".hdr"]:
            f = filename + ext
            if not os.path.exists(f):
                urllib.request.urlretrieve(url + f, f)
