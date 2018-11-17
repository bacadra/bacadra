'''
------------------------------------------------------------------------------
BCDR += ***** general and special (mate)rial(s) *****
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
    #$$ --init--
    def __init__(self, core):
        from .umate import umate
        from .conce import conce
        from .steea import steea
        from .soile import soile

        self.umate = umate.umate(core=core)
        self.conce = conce.conce(core=core)
        self.steea = steea.steea(core=core)
        self.soile = soile.soile(core=core)