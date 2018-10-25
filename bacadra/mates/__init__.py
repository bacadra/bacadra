from . import umate
from . import conce
from . import soils

#$ class navix
class navix:
    #$$ --init--
    def __init__(self, dbase, pinky, pvars):

        self.umate = umate.umate(dbase, pinky, pvars)

        self.conce = conce.conce(dbase, pinky, pvars)

        self.soils = soils.soils(dbase, pinky, pvars)
        self.borep = soils.borep(dbase, pinky, pvars)

    #$$ def --enter--
    def __enter__(self):
        return self

    #$$ def --exit--
    def __exit__(self, type, value, traceback):
        pass