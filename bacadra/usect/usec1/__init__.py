'''
------------------------------------------------------------------------------
BCDR += ***** (u)nit (sec)tions (1)d *****
==============================================================================

------------------------------------------------------------------------------
Copyright (C) 2018 <bacadra@gmail.com> <https://github.com/bacadra/bacadra>
Team members developing this package:
    - Sebastian Balcerowiak <asiloisad> <asiloisad.93@gmail.com>
------------------------------------------------------------------------------
'''


from ...tools.rootx import rootx

#$ class index
class index(rootx):
    #$$ --init--
    def __init__(self, core):
        from . import value
        from . import tsect
        from . import thinw
        from .sprof import sprof

        self.value = value.value(core=core)
        self.tsect = tsect.tsect(core=core)
        self.thinw = thinw.thinw(core=core)
        self.sprof = sprof.sprof(core=core)