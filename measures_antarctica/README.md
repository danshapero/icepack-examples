
[Original source.](http://nsidc.org/data/docs/measures/nsidc0484_rignot/)

The original 450 m-resolution velocity data file is too large for my purposes.
The `munge` script reads in the original data and writes several ArcInfo ASCII Grid files of the regions that are most interesting to me, namely the Ross, Filchner-Ronne, and Amery ice shelves and the Amundsen Sea Embayment.
The coordinates for these regions are stored in a Python dictionary `antarctica` in the module `regions`, which I came up with myself from eyeballing a plot I made (see `plot.py`).
