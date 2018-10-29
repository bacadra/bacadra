from .umate import umate
from .conce import conce
from .soils import soils

#$ class index
class index:
    #$$ --init--
    def __init__(self, core):
        self.umate = umate.umate(core=core)
        self.conce = conce.conce(core=core)
        self.soils = soils.soils(core=core)

    #$$ def --enter--
    def __enter__(self):
        return self

    #$$ def --exit--
    def __exit__(self, type, value, traceback):
        pass