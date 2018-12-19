'''
------------------------------------------------------------------------------
BCDR += ***** (m)echanics (o)f (s)olids and (s)tructures *****
==============================================================================

------------------------------------------------------------------------------
Copyright (C) 2018 <bacadra@gmail.com> <https://github.com/bacadra/bacadra>
Team members developing this package:
    - Sebastian Balcerowiak <asiloisad> <asiloisad.93@gmail.com>
------------------------------------------------------------------------------
'''

from ..tools.rootx import rootx

#$ class index
class index(rootx):
    #$$ __init__
    def __init__(self, core):
        from .linex import linex

        self.linex  = linex.linex(core=core)