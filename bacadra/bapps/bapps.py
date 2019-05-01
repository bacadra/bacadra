'''
------------------------------------------------------------------------------
***** (b)acadra (app)lication(s) *****
==============================================================================

------------------------------------------------------------------------------
Copyright (C) 2018 <bacadra@gmail.com> <https://github.com/bacadra>
Team members developing this package:
+ Sebastian Balcerowiak <asiloisad> <asiloisad.93@gmail.com>
------------------------------------------------------------------------------
'''


class bapps:

    from .steea import steea

    def __init__(self, core=None):

        self.steea = self.steea(core=core)