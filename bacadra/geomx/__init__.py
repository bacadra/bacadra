from . import geomf
from . import geomd

#$ class navix
class navix:
    def __init__(self, dbase, pinky, pvars):
        self.geomf = geomf.navix(dbase, pinky, pvars)
        self.geomd = geomd.navix(dbase, pinky, pvars)

    #$$ def --enter--
    def __enter__(self):
        return self

    #$$ def --exit--
    def __exit__(self, type, value, traceback):
        pass