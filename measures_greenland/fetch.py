
import json
import urllib.request
import os

import icepack.util


def fetch(url):
    return urllib.request.urlopen(url).read().decode('utf-8').split()


month_numbers = {"Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04",
                 "May": "05", "Jun": "06", "Jul": "07", "Aug": "08",
                 "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12"}


def convert_date(date_string):
    month, day, year = date_string.split("-")
    return year + "-" + month_numbers[month] + "-" + day


nsidc = "ftp://sidads.colorado.edu/pub/DATASETS/nsidc0481_MEASURES_greenland_V01/"

if __name__ == "__main__":
    directories = [s for s in fetch(nsidc) if "coast" in s]

    regions = json.loads(open("regions.json", 'r').read())

    for name, coord in regions.items():
        if not os.path.exists(name):
            os.makedirs(name)

        region = coord[0] + "coast-" + coord[1:] + "/"
        subdirectories = [s for s in fetch(nsidc + region) if "TSX" in s]

        for subdirectory in subdirectories:
            s = subdirectory[len("TSX_"):]
            n = len("MMM-DD-YYYY")
            date1 = convert_date(s[:n])
            date2 = convert_date(s[n + 1: 2*n + 1])

            files = [s for s in fetch(nsidc + region + subdirectory) if "TSX" in s]

            for f in files:
                ext = f[-len(".vx.tif"):]
                url = nsidc + region + subdirectory + "/" + f
                filename = name + "/" + date1 + "_" + date2 + ext
                icepack.util.fetch(url, filename, show_progress = False)
                print(f, flush = True)
