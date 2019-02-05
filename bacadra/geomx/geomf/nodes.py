'''
------------------------------------------------------------------------------
***** (nodes) finite elements *****
==============================================================================

------------------------------------------------------------------------------
Copyright (C) 2018 <bacadra@gmail.com> <https://github.com/bacadra>
Team members developing this package:
Sebastian Balcerowiak <asiloisad> <asiloisad.93@gmail.com>
------------------------------------------------------------------------------
'''

from ...dbase import parse
from ...tools.setts import settsmeta

#$ ____ class setts ________________________________________________________ #

class setts(settsmeta):
    _id_auto = 0

#$ ____ class nodes ________________________________________________________ #

class nodes:

    # class setts
    setts = setts('setts', (setts,), {})


#$$ ________ def __init__ __________________________________________________ #

    def __init__(self, core):

        # project object
        self.core = core

        # local setts
        self.setts = self.setts('setts',(),{})


#$$ ________ def add _______________________________________________________ #

    def add(self, id=None, x=0, y=0, z=0, ucst=None, ucid=None, fix=None, id_auto=False, ttl=None):

        id  = parse.chdr('setts.id' , id )
        x   = parse.chdr('geomf.nodes.x'  , x  )
        y   = parse.chdr('geomf.nodes.y'  , y  )
        z   = parse.chdr('geomf.nodes.z'  , z  )

        # if fix is none, then use default setting
        fix = self.core.setts.check_loc('nodes_fix', fix)

        if id_auto and not id:
            id = self._id_auto(True)

        # reference type if-block
        if ucst:
            x,y,z = self._reference(ucst=ucst, ucid=ucid, x=x, y=y, z=z)

        # add nodes data
        self.core.dbase.add(
            mode  = 'r',
            table = '[111:nodes:topos]',
            cols  = 'id,x,y,z,ucst,ucid,fix,ttl',
            data  = (id,x,y,z,ucst,ucid,fix,ttl),
        )


#$$ ________ def adm _______________________________________________________ #

    def adm(self, cols, data, defs={}):
        '''
        Data are parsed due to multi parser. All specific of multiparser are avaiable, like defs

        e.g. defs={"x+f":mm, "z+d"=100} set factor for x column - please note that factor is applied only to non True,False and None and only if value is valid; second command set default value for z column, it will be apply if value in row occur as None - please note that factor is not applied to default value.

        Tip: if some value will form in non-perfomed way (user want somethink other), but the tools addm is very consistet to problem, then single rows in db can be edited by edit method.
        '''

        # TODO: consider redef method
        # it can in more clever way call to add method (like inherit in pinky)
        # and use multiadd data do database (much faster)

        # parse data by multiparser
        # it return list of dictonary which can be used as **kwargs
        data = parse.adm(
            cols  = cols,
            data  = data,
            defs  = defs,
        )

        # loop over list with kwargs and apply it to defualt add method
        for row in data:

            # unpack cols data
            self.add(**row)

    #
    #
    # def edit(self, where, id=None, x=None, y=None, z=None, ucst=None, ucid=None, fix=None, ttl=None):
    #
    #     # parse data do nodes data
    #     cols,data = self.core.dbase.parse( parse_mode='update',
    #         id    = id,
    #         x     = x,
    #         y     = y,
    #         z     = z,
    #         ucst  = ucst,
    #         ucid  = ucid,
    #         fix   = fix,
    #         ttl   = ttl,
    #     )
    #
    #     # edit nodes data
    #     self.core.dbase.edit(
    #         table = '[111:nodes:topos]',
    #         cols  = cols,
    #         data  = data,
    #         where = where,
    #     )


#$$ ________ def _id_auto __________________________________________________ #

    def _id_auto(self, add=False):
        if add:
            self.setts._id_auto += 1
        return 'a:' + str(self.setts._id_auto)


#$$ ________ def _reference ________________________________________________ #

    def _reference(self, ucst, ucid, x, y, z):
        '''
        Method return new nodal coordinate due to reference object.
        '''

        if ucst == 'node':
            # if reference object is node, then add ref node coor to user input
            Δnode = self.core.dbase.get(
                mode  = 'r',
                table = '[111:nodes:topos]',
                cols  = '[x],[y],[z]',
                where = f'[id]={ucid}',
            )

            return x+Δnode[0], y+Δnode[1], z+Δnode[2]


#$$ ________ def auto ______________________________________________________ #

    def echo(self, mode='a+', where=None):

        if 'a' in mode:
            data = self.core.dbase.get(
                mode  = 'm',
                table = '[111:nodes:topos]',
                cols  = 'id,x,y,z,ucst,ucid,fix,ttl',
                where = where,
            )

            if not data: return

            self.core.pinky.rstme.table(
                caption= 'Nodes properties',
                wrap   = [False, False, False, False, False, False, False, True],
                width  = [True,True,True,True,True,True,True, True],
                halign = ['l','c','c','c','c','c','c','l'],
                valign = ['u','u','u','u','u','u','u','u'],
                dtype  = ['t','f','f','f','t','t','t','t'],
                header = ['id','x','y','z','ucst','ucid','fix','ttl'],
                data   = data,
                precision = [2,4,4,4,2,2,2,2],
            )

            if not '+' in mode: return

            self.core.pinky.rstme.table(
                wrap   = [False, False, False, True],
                width  = [8, 8, 2,True],
                halign = ['r','l','c','l'],
                valign = ['u','u','u','u'],
                dtype  = ['t','t','t','t'],
                data   = [
                    ['id'   , ''  , '-', 'identificator'       ],
                    ['x',   '[m]' , '-', 'global x coordinate' ],
                    ['y',   '[m]' , '-', 'global y coordinate' ],
                    ['z',   '[m]' , '-', 'global z coordinate' ],
                    ['ucst' , ''  , '-', 'reference type   '   ],
                    ['ucid' , ''  , '-', 'reference id'        ],
                    ['fix'  , ''  , '-', 'stiff fix'           ],
                    ['ttl'  , ''  , '-', 'title'               ],
                ],
                border = False,
            )
