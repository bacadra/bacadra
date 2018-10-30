# unpack class from module
from .pinky import pinky

#$ class index
class index:
    def __init__(self, dbase, mdata):
        self.pinky = pinky(dbase=dbase, mdata=mdata)

    #$$ def --enter--
    def __enter__(self):
        return self

    #$$ def --exit--
    def __exit__(self, type, value, traceback):
        pass