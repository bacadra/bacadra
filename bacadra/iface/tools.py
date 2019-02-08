'''
------------------------------------------------------------------------------
***** bacadra (tools) interface *****
==============================================================================

------------------------------------------------------------------------------
Copyright (C) 2018 <bacadra@gmail.com> <https://github.com/bacadra>
Team members developing this package:
+ Sebastian Balcerowiak <asiloisad> <asiloisad.93@gmail.com>
------------------------------------------------------------------------------
'''

import copy

#$ ____ class tools ________________________________________________________ #

class tools:

    from ..tools.clang import clang

    from ..tools.verre import verrs

    from ..tools import fpack

    from ..tools import vpatt

    def __init__(self, core=None):

        self.clang = self.clang(core=core)