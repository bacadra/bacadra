'''
------------------------------------------------------------------------------
BCDR += ***** load (patte)rn *****
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
    def __init__(self, core=None):
        from .windl import windl
        from .therl import therl

        self.windl = windl(core=core)
        self.therl = therl(core=core)        