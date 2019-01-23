'''
------------------------------------------------------------------------------
BCDR += ***** (u)nit (sect)ions *****
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
    #$$ __init__
    def __init__(self, core):
        from . import usec1
        from . import usec2
        from . import usec3

        self.usec1 = usec1.index(core=core)
        self.usec2 = usec2.index(core=core)
        self.usec3 = usec3.index(core=core)
