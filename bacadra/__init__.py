"""
bacadra software
================
![Alt](bdata/logo.jpg "Logo")
Main goal
----------------
Provide FEM and design packages, adapted to Civil Engineering, including nonlinear methods in geometrical, materials and design systems, strongly cooperated with dynamic report editor.

Start work with bacadra:
  > `import bacadra as bcdr`
  > `from bacadara.cunit.civil import *`
"""

#$ ____ interface __________________________________________________________ #

from .dbase import dbase
from .cunit import cunit
from .pinky import pinky
from .pvars import pvars
from . import gtech
from . import loads
from . import usect
from . import mates
from . import tools
from . import sofix
from . import geomx
from . import procx
# from . import bapps


class project:
    def __init__(self):
        self.dbase = dbase()

        self.pinky = pinky(
            dbase  = self.dbase)

        self.pvars = pvars(
            dbase  = self.dbase,
            pinky  = self.pinky)

        self.mates = mates.navix(
            dbase  = self.dbase,
            pinky  = self.pinky,
            pvars  = self.pvars)

        self.usect = usect.navix(
            dbase  = self.dbase,
            pinky  = self.pinky,
            pvars  = self.pvars)

        self.geomx = geomx.navix(
            dbase  = self.dbase,
            pinky  = self.pinky,
            pvars  = self.pvars)

        self.loads = loads.navix(
            dbase  = self.dbase,
            pinky  = self.pinky,
            pvars  = self.pvars)

        self.procx = procx.navix(
            dbase  = self.dbase,
            pinky  = self.pinky,
            pvars  = self.pvars)

        self.gtech = gtech.navix(
            dbase  = self.dbase,
            pinky  = self.pinky,
            pvars  = self.pvars)

    #$$ def --enter--
    def __enter__(self):
        return self

    #$$ def --exit--
    def __exit__(self, type, value, traceback):
        pass