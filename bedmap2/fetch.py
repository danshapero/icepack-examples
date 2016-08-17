
import os
import sys
import json
import numpy as np
import urllib.request


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


url = "https://secure.antarctica.ac.uk/data/bedmap2/"
zipfile_name = "bedmap2_bin.zip"

if __name__ == "__main__":
    if not os.path.exists(zipfile_name):
        urllib.request.urlretrieve(url + zipfile_name,
                                   zipfile_name,
                                   progress_bar_hook)

    if not os.path.exists("bedmap2_bin"):
        os.system("unzip " + zipfile_name)
