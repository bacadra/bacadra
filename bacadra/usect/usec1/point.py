'''
------------------------------------------------------------------------------
BCDR += ***** stress (point)s in 1d unit-sections *****
==============================================================================

------------------------------------------------------------------------------
Copyright (C) 2018 <bacadra@gmail.com> <https://github.com/bacadra>
Team members developing this package:
    - Sebastian Balcerowiak <asiloisad> <asiloisad.93@gmail.com>
------------------------------------------------------------------------------
'''

#$ class point
class point:
    #$$ def __init__
    def __init__(self, core):
        self.core = core

    #$$ def --enter--
    def __enter__(self):
        return self

    #$$ def --exit--
    def __exit__(self, type, value, traceback):
        pass

    #$$ def add
    def add(self, id=None, sect=None, mate=None, y=None, z=None, ttl=None):

        # parse data
        cols,data = self.core.dbase.parse(
            id   = id,
            sect = sect,
            mate = mate,
            y    = y,
            z    = z,
            ttl  = ttl,
        )

        # add stress points
        self.core.dbase.add(
            table = '[023:usec1:point]',
            cols  = cols,
            data  = data,
        )
