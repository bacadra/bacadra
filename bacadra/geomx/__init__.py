from . import geomf
from . import geome

#$ class index
class index:
    def __init__(self, core):
        self.geomf = geomf.index(core=core)
        self.geome = geome.index(core=core)

    #$$ def --enter--
    def __enter__(self):
        return self

    #$$ def --exit--
    def __exit__(self, type, value, traceback):
        pass