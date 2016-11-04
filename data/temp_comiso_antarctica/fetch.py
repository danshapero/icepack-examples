
import icepack.util

filename = "Antarctica_5km_dev1.0.nc"
url = "http://websrv.cs.umt.edu/isis/images/4/4d/Antarctica_5km_dev1.0.nc"

if __name__ == "__main__":
    icepack.util.fetch(url, filename)
