'''
------------------------------------------------------------------------------
BCDR += ***** (nodes) finite elements *****
==============================================================================

------------------------------------------------------------------------------
Copyright (C) 2018 <bacadra@gmail.com> <https://github.com/bacadra>
Team members developing this package:
    - Sebastian Balcerowiak <asiloisad> <asiloisad.93@gmail.com>
------------------------------------------------------------------------------
'''

# from ...cunit import cunit

#$ ____ class nodes ________________________________________________________ #

class nodes:
    #$$ def __init__
    def __init__(self, core):
        self.core = core
        self._id_auto_last = 0

    #$$ def --enter--
    def __enter__(self):
        return self

    #$$ def --exit--
    def __exit__(self, type, value, traceback):
        pass

    def add(self, id=None, x=0, y=0, z=0, ucst=None, ucid=None, fix=None, id_auto=False, ttl=None):
        '''
        Add node into FEM system.abs

        :ucst: name of reference element, e.g. "node".
        "ucid: id of reference element.
        '''

        # if fix is none, then use default setting
        if fix is None:
            fix = self.core.mdata.setts.get('nodes_fix')

        if id_auto and not id:
            id = self._id_auto(True)

        # reference type if-block
        x,y,z = self._reference(ucst=ucst, ucid=ucid, x=x, y=y, z=z)

        # parse data do nodes data
        cols,data = self.core.dbase.parse(
            id    = id,
            x     = x,
            y     = y,
            z     = z,
            ucst  = ucst,
            ucid  = ucid,
            fix   = fix,
            ttl   = ttl,
        )

        # add nodes data
        self.core.dbase.add(
            table = '[111:nodes:topos]',
            cols  = cols,
            data  = data,
        )


    def addm(self, cols, data, defs={}):
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
        cols,data = self.core.dbase.parse(parse_mode='addm',
            cols  = cols,
            data  = data,
            defs  = defs,
        )

        # loop over list with kwargs and apply it to defualt add method
        for row in data:

            # unpack cols data
            self.add(**row)



    def edit(self, where, id=None, x=None, y=None, z=None, ucst=None, ucid=None, fix=None, ttl=None):

        # parse data do nodes data
        cols,data = self.core.dbase.parse( parse_mode='update',
            id    = id,
            x     = x,
            y     = y,
            z     = z,
            ucst  = ucst,
            ucid  = ucid,
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


    def _reference(self, ucst, ucid, x, y, z):
        '''
        Method return new nodal coordinate due to reference object.
        '''

        if ucst == 'node':
            # if reference object is node, then add ref node coor to user input
            Δnode = self.core.dbase.get(f'''
            SELECT [x],[y],[z] FROM [111:nodes:topos] WHERE [id] = {ucid}
            ''')[0]

            return x+Δnode[0], y+Δnode[1], z+Δnode[2]

        elif ucst==None:
            return x,y,z

        else:
            raise ValueError('Undefined reference type')

