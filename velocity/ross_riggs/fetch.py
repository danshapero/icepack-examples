
import os
import urllib.request

url = "https://nsidc.org/data/velmap/ross_shelf/riggs/"
filename = "riggs_data.txt"

if __name__ == "__main__":
    if not os.path.exists(filename):
        urllib.request.urlretrieve(url + filename, filename)
