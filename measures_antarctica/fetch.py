
import os
import sys
import urllib.request

url = "ftp://n5eil01u.ecs.nsidc.org/SAN/MEASURES/NSIDC-0484.001/1996.01.01/"
big_file   = "antarctica_ice_velocity_450m.nc"
small_file = "antarctica_ice_velocity_900m.nc"

def progress_bar_hook(block_num, block_size, total_size):
    read_so_far = block_num * block_size
    if total_size > 0:
        percent = read_so_far * 100 / total_size
        s = "\r%5.1f%% %*d / %d" % (
        percent, len(str(total_size)), read_so_far, total_size)
        sys.stderr.write(s)
        if read_so_far >= total_size:
            sys.stderr.write("\n")

    else:
        sys.stderr.write("read %d\n" % (read_so_far,))

if __name__ == "__main__":
    if not os.path.exists(big_file):
        urllib.request.urlretrieve(url + big_file, big_file, progress_bar_hook)

    if not os.path.exists(small_file):
        urllib.request.urlretrieve(url + small_file, small_file, progress_bar_hook)

