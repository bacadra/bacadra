class project:
    def __init__(self):
        from . import pinky as _pinky
        from . import dbase as _dbase
        from . import mdata as _mdata
        from . import gtech as _gtech
        from . import loads as _loads
        from . import usect as _usect
        from . import mates as _mates
        from . import geomx as _geomx
        from . import mosas as _mosas

        self.dbase = _dbase.dbase()
        self.mdata = _mdata.index(dbase=self.dbase)
        self.pinky = _pinky.index(dbase=self.dbase, mdata=self.mdata)

        class core:
            dbase = self.dbase
            pinky = self.pinky
            mdata = self.mdata

        self.mates = _mates.index(core=core)
        self.usec1 = _usect.index(core=core).usec1
        self.usec2 = _usect.index(core=core).usec2
        self.usec3 = _usect.index(core=core).usec3

        self.geomf = _geomx.index(core=core).geomf
        self.geome = _geomx.index(core=core).geome


        self.loads = _loads.index(core=core)
        self.mosas = _mosas.index(core=core)
        self.gtech = _gtech.index(core=core)

    #$$ def --enter--
    def __enter__(self):
        return self

    #$$ def --exit--
    def __exit__(self, type, value, traceback):
        pass

