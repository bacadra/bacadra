'''
------------------------------------------------------------------------------
***** stress (point)s in one dim section *****
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
    pass


#$ ____ class point ________________________________________________________ #

class point:

    # class setts
    setts = setts('setts', (setts,), {})

#$$ ________ def __init__ __________________________________________________ #

    def __init__(self, core):

        # project object
        self.core = core

        # local setts
        self.setts = self.setts('setts',(),{})

#$$ ________ def add _______________________________________________________ #

    def add(self, sect=None, id=None, mate=None, y=None, z=None, ttl=None):

        y = parse.chdr('usect.point.y', y)
        z = parse.chdr('usect.point.z', z)

        # if sect is not defined then use last one section
        sect = self.core.usecp.value.setts.check_loc('_ldef_id', sect)

        self.core.dbase.add(
            mode  = 'r',
            table = '[023:usecp:point]',
            cols  = ['sect','id','mate','y','z','ttl'],
            data  = (sect,id,mate,y,z,ttl)
        )

#$$ ________ def adm _______________________________________________________ #

    def adm(self, cols, data, defs={}):
        '''
        Data are parsed due to multi parser. All specific of multiparser are avaiable, like defs

        e.g. defs={"x+f":mm, "z+d"=100} set factor for x column - please note that factor is applied only to non True,False and None and only if value is valid; second command set default value for z column, it will be apply if value in row occur as None - please note that factor is not applied to default value.

        Tip: if some value will form in non-perfomed way (user want somethink other), but the tools addm is very consistet to problem, then single rows in db can be edited by edit method.
        '''

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

#$$ ________ def echo ______________________________________________________ #

    def echo(self, mode='a+', where=None):
        if 'a' in mode:
            data = self.core.dbase.get(
                mode  = 'm',
                table = '[023:usecp:point]',
                cols  = ['sect','id','mate','y','z','ttl'],
                where = where,
            )

            if data:

                self.core.pinky.rstme.table(
                    caption= 'Stress points in one dimmensional unit-section',
                    wrap   = [True,False,False,False,False,True],
                    width  = [7,7,7,6,6,True],
                    halign = ['l','c','c','r','r','l'],
                    valign = ['m','u','u','u','u','u'],
                    dtype  = ['t','t','t','f','f','t'],
                    header = ['sect','id','mate' ,'y','z','ttl'],
                    data   = data,
                    precision = 4,
                )

        if not '+' in mode:

            self.core.pinky.rstme.table(
                wrap   = [False, False, False, True],
                width  = [23, 6, 2,True],
                halign = ['r','l','c','l'],
                valign = ['u','u','u','u'],
                dtype  = ['t','t','t','t'],
                data   = [
                    ['sect' ,''      ,'-','identificator of usecp'],
                    ['id'   ,''      ,'-','identificator'],
                    ['mate' ,''      ,'-','reference material of point'],
                    ['y,z'  ,'[m]'   ,'-','coordinates in local usecp system'],
                    ['ttl'  ,''      ,'-','title'],
                ],
                border = False,
            )