'''
------------------------------------------------------------------------------
BCDR += ***** (m)odel (data) *****
==============================================================================

------------------------------------------------------------------------------
Copyright (C) 2018 <bacadra@gmail.com> <https://github.com/bacadra>
Team members developing this package:
    - Sebastian Balcerowiak <asiloisad> <asiloisad.93@gmail.com>
------------------------------------------------------------------------------
'''

from ..tools.rootx import rootx

#$ class index
class index(rootx):
    def __init__(self, dbase):
        from . import setts
        self.setts = setts.setts(dbase)

        from . import annex
        self.annex = annex.annex(dbase)