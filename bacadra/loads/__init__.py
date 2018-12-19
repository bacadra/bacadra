'''
------------------------------------------------------------------------------
BCDR += ***** general finite and free (loads) *****
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
        from .ltree import cates
        from .ltree import lcase
        from .assig import nodes
        from .assig import handy
        from . import patte

        self.cates = cates.cates(core=core)
        self.lcase = lcase.lcase(core=core)
        self.nodes = nodes.nodes(core=core)
        self.handy = handy.handy(core=core)
        self.patte = patte.index(core=core)