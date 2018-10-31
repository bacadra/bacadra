
# from ..cunit.ce import m
# from ..cunit.cmath import *

# import numpy  as np
# import pandas as pd


#$ ____ class nodes ________________________________________________________ #

class nodes:
    #$$ def --init--
    def __init__(self, core):
        self.core = core
        self._id_auto_last = 0

    #$$ def --enter--
    def __enter__(self):
        return self

    #$$ def --exit--
    def __exit__(self, type, value, traceback):
        pass

    def add(self, id=None, x=0, y=0, z=0, ucst=None, ucsi=None, fix=None, id_auto=False, ttl=None):

        # if fix is none, then use default setting
        if fix is None:
            fix = self.core.mdata.setts.get('nodes_fix')

        if id_auto and not id:
            id = self._id_auto(True)

        # reference type if-block
        if ucst == 'node':
            # if reference object is node, then add ref node coor to user input
            Δnode = self.core.dbase.get(f'''
            SELECT [x],[y],[z] FROM [111:nodes:topos] WHERE [id] = {ucsi}
            ''')[0]

            x += Δnode[0]
            y += Δnode[1]
            z += Δnode[2]


        # parse data do nodes data
        cols,data = self.core.dbase.parse(
            id    = id,
            x     = x,
            y     = y,
            z     = z,
            ucst  = ucst,
            ucsi  = ucsi,
            fix   = fix,
            ttl   = ttl,
        )

        # add nodes data
        self.core.dbase.add(
            table = '[111:nodes:topos]',
            cols  = cols,
            data  = data,
        )



    def edit(self, where, id=None, x=None, y=None, z=None, ucst=None, ucsi=None, fix=None, ttl=None):

        # parse data do nodes data
        cols,data = self.core.dbase.parse( parse_mode='update',
            id    = id,
            x     = x,
            y     = y,
            z     = z,
            ucst  = ucst,
            ucsi  = ucsi,
            fix   = fix,
            ttl   = ttl,
        )

        # edit nodes data
        self.core.dbase.edit(
            table = '[111:nodes:topos]',
            cols  = cols,
            data  = data,
            where = where,
        )

    def _id_auto(self, add=False):
        if add:
            self._id_auto_last += 1
        return 'a-' + str(self._id_auto_last)