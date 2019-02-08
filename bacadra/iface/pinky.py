'''
------------------------------------------------------------------------------
***** bacadra (pinky) interface *****
==============================================================================

------------------------------------------------------------------------------
Copyright (C) 2018 <bacadra@gmail.com> <https://github.com/bacadra>
Team members developing this package:
+ Sebastian Balcerowiak <asiloisad> <asiloisad.93@gmail.com>
------------------------------------------------------------------------------
'''

#$ ____ class pinky ________________________________________________________ #

class pinky:

    from ..pinky.texme.texme import texme

    from ..pinky.texme.texpm import texpm

    from ..pinky.rstme.rstme import rstme

    from ..pinky.cator.cator import cator

    def __init__(self, core=None):

        self.texme = self.texme(core=core)

        self.texpm = self.texpm(core=core, tex=self.texme)

        self.rstme = self.rstme(core=core)

        self.cator = self.cator(core=core)


