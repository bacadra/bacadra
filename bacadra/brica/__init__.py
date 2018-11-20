'''
------------------------------------------------------------------------------
BCDR += ***** (bri)dge (c)omputer (a)ided design *****
==============================================================================

------------------------------------------------------------------------------
Copyright (C) 2018 <bacadra@gmail.com> <https://github.com/bacadra/bacadra>
Team members developing this package:
    - Sebastian Balcerowiak <asiloisad> <asiloisad.93@gmail.com>
------------------------------------------------------------------------------
'''

from ..tools.rootx import rootx

from . import railb
from . import roadb
from . import footb

#$ class index
class index(rootx):
    def __init__(self, core):

        self.railb = railb.index(core=core)
        self.roadb = roadb.index(core=core)
        self.footb = footb.index(core=core)