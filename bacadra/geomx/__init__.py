from ..tools.rootx import rootx

#$ class index
class index(rootx):
    def __init__(self, core):
        from . import geomf
        from . import geoms
        from . import geome

        self.geomf = geomf.index(core=core)
        self.geoms = geoms.index(core=core)
        self.geome = geome.index(core=core)