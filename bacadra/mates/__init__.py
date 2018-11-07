from ..tools.rootx import rootx

#$ class index
class index(rootx):
    #$$ --init--
    def __init__(self, core):
        from .umate import umate
        from .conce import conce
        from .steea import steea
        from .soile import soile

        self.umate = umate.umate(core=core)
        self.conce = conce.conce(core=core)
        self.steea = steea.steea(core=core)
        self.soile = soile.soile(core=core)