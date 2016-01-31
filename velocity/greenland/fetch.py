
import json
import urllib.request

def fetch(url):
    return urllib.request.urlopen(url).read().decode('utf-8').split()

nsidc = "ftp://sidads.colorado.edu/pub/DATASETS/nsidc0481_MEASURES_greenland_V01/"

if __name__ == "__main__":
    directories = [s for s in fetch(nsidc) if "coast" in s]

    regions = json.loads(open("regions.json", 'r').read())

    for name, region in regions.items():
        r = region[0] + "coast-" + region[1:] + "/"
        dates = [s for s in fetch(nsidc + r) if "TSX" in s]

        for date in dates:
            filenames = [s for s in fetch(nsidc + r + date) if "TSX" in s]

            for f in filenames:
                print(f, flush = True)
                urllib.request.urlretrieve(nsidc + r + date + "/" + f, f)
