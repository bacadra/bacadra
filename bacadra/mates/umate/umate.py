'''
------------------------------------------------------------------------------
BCDR += ***** univerial (mate)rials *****
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
    _ldef_id = None


#$ ____ class umate ________________________________________________________ #

class umate:

    # class setts
    setts = setts('setts', (setts,), {})


#$$ ________ def __init__ __________________________________________________ #

    def __init__(self, core):

        # project object
        self.core = core

        # local setts
        self.setts = self.setts('setts',(),{})

#$$ ________ def add _______________________________________________________ #

    def add(self, id=None, ρ_o=None, E_1=None, v_1=None, G_1=None, t_e=None, ttl=None, subcl=None):

        # drop units to si
        id  = parse.chdr('setts.id' , id )
        ρ_o = parse.chdr('mates.umate.ρ_o', ρ_o)
        E_1 = parse.chdr('mates.umate.E_1', E_1)
        G_1 = parse.chdr('mates.umate.G_1', G_1)
        t_e = parse.chdr('mates.umate.t_e', t_e)

        # overwrite last defined material
        self.setts._ldef_id = id

        # resolve coparamaters
        E_1,v_1,G_1 = self._linear_EvG(E_1, v_1, G_1)

        # add universal material
        self.core.dbase.add(
            mode  = 'r',
            table = '[011:mates:umate]',
            cols  = '[id],[ρ_o],[E_1],[v_1],[G_1],[t_e],[ttl],[subcl]',
            data  = (id,ρ_o,E_1,v_1,G_1,t_e,ttl,subcl),
        )


#$$ ________ def obj _______________________________________________________ #

    def obj(self, where=None, sn='1', unit=None, mode=None):
        if where==None:
            where='id='+str(self.setts._ldef_id)

        return self.core.dbase.obj(
            name  = 'mates.umate-'+sn,
            where = where,
            unit  = unit,
            mode  = mode
        )

#$$ ________ def echo ______________________________________________________ #

    def echo(self, mode='a+', where=None, label=None):

        if 'a' in mode:
            data = self.core.dbase.get(
                mode  = 'm',
                table = '[011:mates:umate]',
                cols  = '[id],[ρ_o],[E_1],[v_1],[G_1],[t_e],[subcl],[ttl]',
                where = where,
            )

            if not data: return

            caption = 'General properties of materials'

            out = self.core.pinky.rstme.table(
                caption = None if 'x' in mode else caption,
                wrap    = [False,False,False,False,False,False,False,True],
                width   = [True,8,8,4,8,8,5,True],
                halign  = ['l','c','c','c','c','c','c','l'],
                valign  = ['u','u','u','u','u','u','u','u'],
                dtype   = ['t','e','e','e','e','e','t','t'],
                header  = ['id','ρ_o','E_1','v_1','G_1','t_e','subcl','ttl'],
                data    = data,
                precision = 2,
                inherit = True if 'x' in mode else False,
            )

            if 'x' in mode:
                self.core.pinky.texme.code(
                    caption=caption, code=out, rst=True, label=None,strip=False)


        if 'b' in mode:
            data = self.core.dbase.get(
                mode  = 'm',
                table = '[011:mates:umate]',
                cols  = '[id],[ρ_o],[E_1],[v_1],[G_1],[t_e],[subcl],[ttl]',
                where = where,
            )

            if not data: return

            caption = 'General properties of materials'

            out = self.core.pinky.rstme.table(
                caption = None if 'x' in mode else caption,
                wrap    = [False,False,False,False,False,False,False,True],
                width   = [True,8,8,4,8,8,5,True],
                halign  = ['l','c','c','c','c','c','c','l'],
                valign  = ['u','u','u','u','u','u','u','u'],
                dtype   = ['t','e','e','e','e','e','t','t'],
                header  = [
                    'id',
                    ['ρ_o','[kg/m3]'],['E_1','[N/m2]'],['v_1','[1]'],['G_1','[N/m2]'],['t_e','[1/°C]'],'subcl','ttl'],
                data    = data,
                precision = 2,
                inherit = True if 'x' in mode else False,
            )

            if 'x' in mode:
                self.core.pinky.texme.code(
                    caption=caption, code=out, rst=True, label=None,strip=False)



        if '+' in mode:

            out = self.core.pinky.rstme.table(
                wrap   = [False, False, False, True],
                width  = [8, 8, 2,True],
                halign = ['r','l','c','l'],
                valign = ['u','u','u','u'],
                dtype  = ['t','t','t','t'],
                data   = [
                    ['id' , ''       , '-', 'identificator'   ],
                    ['ρ_o', '[kg/m3]', '-', 'densinity'       ],
                    ['E_1', '[N/m2]' , '-', 'Young\'s modulus'],
                    ['G_1', '[N/m2]' , '-', 'Kirchoff modulus'],
                    ['v_1', '[1]'    , '-', 'poisson ratio'   ],
                    ['t_e', '[1/°C]' , '-', 'Kirchoff modulus'],
                    ['ttl', ''       , '-', 'title'           ],
                ],
                border = False,
                inherit = True if 'x' in mode else False,
            )

            if 'x' in mode:
                self.core.pinky.texme.code(
                    code=out, rst=True, label=None,strip=False)




    def _linear_EvG(self, E, v, G):
        '''
        Calc third value of material constant
        '''

        if E and v and not G:
            G = (E) / (2 * (1 + v))

        elif E and not v and G:
            v = E/G * 0.5 - 1

        elif not E and v and G:
            E = G * (2 * (1 + v))

        return E,v,G


