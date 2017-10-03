
from icepack.util import fetch_nsidc

url = "https://n5eil01u.ecs.nsidc.org/MEASURES/NSIDC-0484.001/1996.01.01/"
big_file_name = "antarctica_ice_velocity_450m.nc"
small_file_name = "antarctica_ice_velocity_900m.nc"

fetch_nsidc([url + small_file_name, url + big_file_name],
            [open(small_file_name, 'wb'), open(big_file_name, 'wb')])

