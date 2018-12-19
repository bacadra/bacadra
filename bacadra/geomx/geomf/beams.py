'''
------------------------------------------------------------------------------
BCDR += ***** (beams) finite elements *****
==============================================================================

------------------------------------------------------------------------------
Copyright (C) 2018 <bacadra@gmail.com> <https://github.com/bacadra/bacadra>
Team members developing this package:
    - Sebastian Balcerowiak <asiloisad> <asiloisad.93@gmail.com>
------------------------------------------------------------------------------
'''


import math
from . import nodes
from ...cunit import cunit

#$$ ________ class beams ___________________________________________________ #

class beams:
    #$$ def __init__
    def __init__(self, core):
        self.core = core
        self._nodes = nodes.nodes(core=core)
        self._id_auto = 1

    #$$ def --enter--
    def __enter__(self):
        return self

    #$$ def --exit--
    def __exit__(self, type, value, traceback):
        pass

    def add(self, id=None, n1=None, n2=None, sect=None, div=None, id_auto=False, ttl=None):

        if div:
            return self._mesh_manual(div, id, n1, n2, sect, ttl)

        if id_auto and not id:
            id = 'a-' + str(self._id_auto)
            self._id_auto += 1

        # if sect is not defined then use cat last one define unit section 1d
        if sect is None:
            sect = self.setts.get('_usec1_ldef')

        # warning: node1 and node2 right side should return only one row
        # TODO: add checking of length data vector
        # the same as in truss elements

        # get nodal coordinate of start node
        node1 = self.core.dbase.get(f'''
        SELECT [x],[y],[z] FROM [111:nodes:topos] WHERE [id]="{n1}"
        ''')[0]

        # get nodal coordinate of end node
        node2 = self.core.dbase.get(f'''
        SELECT [x],[y],[z] FROM [111:nodes:topos] WHERE [id]="{n2}"
        ''')[0]

        # calculate projected and main legnth of elemenet
        Δx = node2[0]-node1[0]
        Δy = node2[1]-node1[1]
        Δz = node2[2]-node1[2]
        L = (Δx**2 + Δy**2 + Δz**2)**0.5

        # parse data
        cols,data = self.core.dbase.parse(
            id    = id,
            n1    = n1,
            n2    = n2,
            sect  = sect,
            ttl   = ttl,
            L     = L,
            ΔX    = Δx,
            ΔY    = Δy,
            ΔZ    = Δz,
        )

        # add data
        self.core.dbase.add(
            table = '[131:beams:topos]',
            cols  = cols,
            data  = data,
        )

    def _mesh_manual(self, div, id, n1, n2, sect, ttl):
        # get nodal coordinate of start node
        node1 = self.core.dbase.get(f'''
        SELECT [x],[y],[z] FROM [111:nodes:topos] WHERE [id]="{n1}"
        ''')[0]

        # get nodal coordinate of end node
        node2 = self.core.dbase.get(f'''
        SELECT [x],[y],[z] FROM [111:nodes:topos] WHERE [id]="{n2}"
        ''')[0]

        # calculate projected and main legnth of elemenet
        Δx = node2[0]-node1[0]
        Δy = node2[1]-node1[1]
        Δz = node2[2]-node1[2]
        L = (Δx**2 + Δy**2 + Δz**2)**0.5

        if type(div) == cunit:
            div = int(math.ceil(L/div.drop('m', fcover=True)))

        for i in range(div):

            if i != 0:
                n1id = self._nodes._id_auto()
            else:
                n1id = n1

            if i != div-1:
                x = node1[0] + Δx/div*(i+1)
                y = node1[1] + Δy/div*(i+1)
                z = node1[2] + Δz/div*(i+1)
                self._nodes.add(x=x, y=y, z=z, id_auto=True)
                n2id = self._nodes._id_auto()
            else:
                n2id = n2

            self.add(n1=n1id, n2=n2id, sect=sect, ttl=ttl, id_auto=True)
