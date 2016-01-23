
import urllib.request
import gzip

url = "http://websrv.cs.umt.edu/isis/images/4/4d/Mesh_RIS.mat.gz"
filename = "Mesh_RIS.mat"

if __name__ == "__main__":
    urllib.request.urlretrieve(url, filename + ".gz")
    with gzip.open(filename + ".gz", "rb") as zipfile:
        contents = zipfile.read()
        with open(filename, "wb") as matfile:
            matfile.write(contents)
