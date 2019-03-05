'''
------------------------------------------------------------------------------
***** univerial (mate)rials *****
==============================================================================

------------------------------------------------------------------------------
Copyright (C) 2018 <bacadra@gmail.com> <https://github.com/bacadra>
Team members developing this package:
+ Sebastian Balcerowiak <asiloisad> <asiloisad.93@gmail.com>
------------------------------------------------------------------------------
'''

#$ ######################################################################### #

from ...dbase import parse
from ...tools.setts import setts_init

#$ ____ class setts ________________________________________________________ #

class setts(setts_init):

    _ldef_id = None


#$ ____ class umate ________________________________________________________ #

class umate:

    setts = setts()


#$$ ________ def __init__ __________________________________________________ #

    def __init__(self, core):

        self.core = core

        self.setts = setts(self.setts, self)


#$$ ________ def add _______________________________________________________ #

    def add(self, id=None, ρ_o=None, E_1=None, v_1=None, G_1=None, t_e=None, ttl=None, subcl=None):

        table = '011:mates:umate'
        id    = parse.chdr(table , 'id'    , id    )
        ρ_o   = parse.chdr(table , 'ρ_o'   , ρ_o   )
        E_1   = parse.chdr(table , 'E_1'   , E_1   )
        v_1   = parse.chdr(table , 'v_1'   , v_1   )
        G_1   = parse.chdr(table , 'G_1'   , G_1   )
        t_e   = parse.chdr(table , 't_e'   , t_e   )
        ttl   = parse.chdr(table , 'ttl'   , ttl   )
        subcl = parse.chdr(table , 'subcl' , subcl )

        # overwrite last defined material
        self.setts._ldef_id = id

        # resolve coparamaters
        E_1,v_1,G_1 = self._linear_EvG(E_1, v_1, G_1)

        # add universal material
        self.core.dbase.add(
            mode  = 'r',
            table = ['011:mates:umate'],
            cols  = ['id','ρ_o','E_1','v_1','G_1','t_e','ttl','subcl'],
            data  = [id,ρ_o,E_1,v_1,G_1,t_e,ttl,subcl],
        )




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


#$ ######################################################################### #
