from .tools.rootx import rootx

class project(rootx):
    def __init__(self):
        from . import pinky as pinky
        from . import dbase as dbase
        from . import mdata as mdata
        from . import gtech as gtech
        from . import loads as loads
        from . import usect as usect
        from . import mates as mates
        from . import geomx as geomx
        from . import mosas as mosas

        self.dbase = dbase.dbase()
        self.mdata = mdata.index(dbase=self.dbase)
        self.pinky = pinky.index(dbase=self.dbase,
                                 mdata=self.mdata)

        class core:
            dbase = self.dbase
            mdata = self.mdata
            pinky = self.pinky

        self.mates = mates.index(core=core)

        self.usec1 = usect.index(core=core).usec1
        self.usec2 = usect.index(core=core).usec2
        self.usec3 = usect.index(core=core).usec3

        self.geomf = geomx.index(core=core).geomf
        self.geoms = geomx.index(core=core).geoms
        self.geome = geomx.index(core=core).geome

        self.loads = loads.index(core=core)
        self.mosas = mosas.index(core=core)
        self.gtech = gtech.index(core=core)