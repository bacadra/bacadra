
# from ..cunit.ce import *
# from ..cunit.cmath import *

# import numpy  as np
# import pandas as pd
# import math

#$$ ________ class beams ___________________________________________________ #

class beams:
    #$$ def --init--
    def __init__(self, dbase, pinky, pvars):
        self.dbase = dbase
        self.pinky = pinky
        self.pvars = pvars

    #$$ def --enter--
    def __enter__(self):
        return self

    #$$ def --exit--
    def __exit__(self, type, value, traceback):
        pass

    def add(self, id=None, n1=None, n2=None, sect=None, ttl=None):

        # if sect is not defined then use cat last one define unit section 1d
        if sect is None:
            sect = self.pvars.get('_usec1_ldef')

        # warning: node1 and node2 right side should return only one row
        # TODO: add checking of length data vector
        # the same as in truss elements

        # get nodal coordinate of start node
        node1 = self.dbase.get(f'''
        SELECT [x],[y],[z] FROM [111:nodes:topos] WHERE [id]="{n1}"
        ''')[0]

        # get nodal coordinate of end node
        node2 = self.dbase.get(f'''
        SELECT [x],[y],[z] FROM [111:nodes:topos] WHERE [id]="{n2}"
        ''')[0]

        # calculate projected and main legnth of elemenet
        Δx = node2[0]-node1[0]
        Δy = node2[1]-node1[1]
        Δz = node2[2]-node1[2]
        L = (Δx**2 + Δy**2 + Δz**2)**0.5

        # parse data
        cols,data = self.dbase.parse(
            id      = id,
            n1      = n1,
            n2      = n2,
            sect    = sect,
            ttl     = ttl,
            L       = L,
            delta_X = Δx,
            delta_Y = Δy,
            delta_Z = Δz,
        )

        # add data
        self.dbase.add(
            table = '[131:beams:topos]',
            cols  = cols,
            data  = data,
        )

