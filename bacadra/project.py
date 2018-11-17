'''
------------------------------------------------------------------------------
BCDR += ***** bacadra FEM (project) *****
==============================================================================

------------------------------------------------------------------------------
Copyright (C) 2018 <bacadra@gmail.com> <https://github.com/bacadra/bacadra>
Team members developing this package:
    - Sebastian Balcerowiak <asiloisad> <asiloisad.93@gmail.com>
------------------------------------------------------------------------------
'''

from .tools.rootx import rootx

class project(rootx):
    def __init__(self):

        from . import dbase as dbase
        self.dbase = dbase.dbase()

        from . import mdata as mdata
        self.mdata = mdata.index(dbase=self.dbase)

        from . import pinky as pinky
        self.pinky = pinky.index(dbase=self.dbase,
                                 mdata=self.mdata)

        class core:
            dbase = self.dbase
            mdata = self.mdata
            pinky = self.pinky

        from . import tools
        self.tools = tools.index(core=core)

        from . import mates
        self.mates = mates.index(core=core)

        from . import usect
        self.usec1 = usect.index(core=core).usec1
        self.usec2 = usect.index(core=core).usec2
        self.usec3 = usect.index(core=core).usec3

        from . import geomx
        self.geomf = geomx.index(core=core).geomf
        self.geoms = geomx.index(core=core).geoms
        self.geome = geomx.index(core=core).geome

        from . import loads
        self.loads = loads.index(core=core)

        from . import mosas
        self.mosas = mosas.index(core=core)

        from . import solve
        self.solve = solve.index(core=core)

        from . import cadob
        self.cadob = cadob.index(core=core)