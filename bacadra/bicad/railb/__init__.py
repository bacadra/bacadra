'''
------------------------------------------------------------------------------
BCDR += ***** (rail)way (b)ridges *****
==============================================================================

------------------------------------------------------------------------------
Copyright (C) 2018 <bacadra@gmail.com> <https://github.com/bacadra>
Team members developing this package:
    - Sebastian Balcerowiak <asiloisad> <asiloisad.93@gmail.com>
------------------------------------------------------------------------------
'''

from .en155 import en155
from .ecode import ecode

from ...tools.rootx import rootx

#$ class index
class index(rootx):
    def __init__(self, core=None):

        self.en155 = en155(core=core)
        self.ecode = ecode(core=core)