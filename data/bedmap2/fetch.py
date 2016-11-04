
import os
import icepack.util

url = "https://secure.antarctica.ac.uk/data/bedmap2/"
zipfile_name = "bedmap2_bin.zip"

if __name__ == "__main__":
    icepack.util.fetch(url + zipfile_name, zipfile_name)

    if not os.path.exists("bedmap2_bin"):
        os.system("unzip " + zipfile_name)
