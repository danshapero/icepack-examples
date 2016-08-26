
import icepack.util

url = "https://nsidc.org/data/velmap/ross_shelf/riggs/"
filename = "riggs_data.txt"

if __name__ == "__main__":
    icepack.util.fetch(url + filename, filename)
