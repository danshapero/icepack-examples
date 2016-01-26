
import sys
import urllib.request

url = "ftp://n5eil01u.ecs.nsidc.org/SAN/MEASURES/NSIDC-0484.001/1996.01.01/antarctica_ice_velocity_450m.nc"
filename = "antarctica_ice_velocity_450m.nc"

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
    urllib.request.urlretrieve(url, filename, progress_bar_hook)

