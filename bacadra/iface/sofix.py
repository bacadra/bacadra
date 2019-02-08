'''
------------------------------------------------------------------------------
***** bacadra (sofix) interface *****
==============================================================================

------------------------------------------------------------------------------
Copyright (C) 2018 <bacadra@gmail.com> <https://github.com/bacadra>
Team members developing this package:
+ Sebastian Balcerowiak <asiloisad> <asiloisad.93@gmail.com>
------------------------------------------------------------------------------
'''

#$ ____ class sofix ________________________________________________________ #

class sofix:

    from ..sofix.sbase import sbase

    from ..sofix.trade import trade

    from ..sofix.wgraf import wgraf

    def __init__(self, core=None):

        self.sbase = sofix.sbase(core=core)

        self.trade = sofix.trade(core=core)

        self.wgraf = sofix.wgraf(core=core)