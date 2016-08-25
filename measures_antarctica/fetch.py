
import icepack.util

url = "ftp://n5eil01u.ecs.nsidc.org/SAN/MEASURES/NSIDC-0484.001/1996.01.01/"
big_file   = "antarctica_ice_velocity_450m.nc"
small_file = "antarctica_ice_velocity_900m.nc"

if __name__ == "__main__":
    icepack.util.fetch(url + big_file, big_file)
    icepack.util.fetch(url + small_file, small_file)
