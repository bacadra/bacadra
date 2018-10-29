from . import setts
from . import annex

#$ class index
class index:
    def __init__(self, dbase):
        self.setts = setts.setts(dbase)
        self.annex = annex.annex(dbase)

    #$$ def --enter--
    def __enter__(self):
        return self

    #$$ def --exit--
    def __exit__(self, type, value, traceback):
        pass