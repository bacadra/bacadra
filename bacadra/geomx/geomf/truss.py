'''
------------------------------------------------------------------------------
***** (truss) finite elements *****
==============================================================================

------------------------------------------------------------------------------
Copyright (C) 2018 <bacadra@gmail.com> <https://github.com/bacadra>
Team members developing this package:
+ Sebastian Balcerowiak <asiloisad> <asiloisad.93@gmail.com>
------------------------------------------------------------------------------
'''

from ...tools.setts import settsmeta


#$ ____ class setts ________________________________________________________ #

class setts(settsmeta):
    pass


#$ ____ class truss ________________________________________________________ #

class truss:

    setts = setts('setts', (setts,), {})


#$$ ________ def __init__ __________________________________________________ #

    def __init__(self, core):

        # project object
        self.core = core

        # local setts
        self.setts = self.setts('setts',(),{})


#$$ ________ def add _______________________________________________________ #

    def add(self, id=None, n1=None, n2=None, sect=None, grp=None, ttl=None):

        # if sect is not defined then use cat last one define unit section 1d
        sect = self.core.usecp.value.setts.check_loc('_ldef_id', sect)

        # get nodal coordinate of start node
        node1 = self.core.dbase.get(
            mode  = 'r',
            table = '[111:nodes:topos]',
            cols  = '[x],[y],[z]',
            where = f'[id]="{n1}"'
        )

        # get nodal coordinate of start node
        node2 = self.core.dbase.get(
            mode  = 'r',
            table = '[111:nodes:topos]',
            cols  = '[x],[y],[z]',
            where = f'[id]="{n2}"'
        )

        # calculate projected and main legnth of elemenet
        Δx = node2['x']-node1['x']
        Δy = node2['y']-node1['y']
        Δz = node2['z']-node1['z']
        L = (Δx**2 + Δy**2 + Δz**2)**0.5

        # add data
        self.core.dbase.add(
            mode  = 'r',
            table = '[121:truss:topos]',
            cols  = 'id,n1,n2,sect,ttl,grp,L,Δx,Δy,Δz',
            data  = (id,n1,n2,sect,ttl,grp,L,Δx,Δy,Δz),
        )

#$$ ________ def echo ______________________________________________________ #

    def echo(self, mode='a+', where=None):

        if 'a' in mode:
            data = self.core.dbase.get(
                mode  = 'm',
                table = '[121:truss:topos]',
                cols  = 'id,n1,n2,sect,grp,L,ttl',
                where = where,
            )

            if not data: return

            self.core.pinky.rstme.table(
                caption= 'Truss elements properties',
                wrap   = [False, False, False, False, False, False, True],
                width  = [True , True , True , True , True , 6    , True],
                halign = ['l','c','c','c','c','c','l'],
                valign = ['u','u','u','u','u','u','u'],
                dtype  = ['t','t','t','t','t','f','t'],
                header = ['id','n1','n2','sect','grp','L','ttl'],
                data   = data,
                precision = 4,
            )

            if not '+' in mode: return

            self.core.pinky.rstme.table(
                wrap   = [False, False, False, True],
                width  = [8, 8, 2,True],
                halign = ['r','l','c','l'],
                valign = ['u','u','u','u'],
                dtype  = ['t','t','t','t'],
                data   = [
                    ['id'   , ''  , '-', 'identificator'          ],
                    ['n1'   , ''  , '-', 'id of first node'       ],
                    ['n2'   , ''  , '-', 'id of second node'      ],
                    ['sect' , ''  , '-', 'id of cross-section 1d' ],
                    ['grp'  , ''  , '-', 'structural groups'],
                    ['L' , '[m]'  , '-', 'total length of element'],
                    ['ttl'  , ''  , '-', 'title'                  ],
                ],
                border = False,
            )
