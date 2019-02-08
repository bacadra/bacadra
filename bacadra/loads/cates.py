'''
------------------------------------------------------------------------------
***** loads (cate)gorie(s) *****
==============================================================================

------------------------------------------------------------------------------
Copyright (C) 2018 <bacadra@gmail.com> <https://github.com/bacadra>
Team members developing this package:
+ Sebastian Balcerowiak <asiloisad> <asiloisad.93@gmail.com>
------------------------------------------------------------------------------
'''

from ..dbase import parse
from ..tools.setts import settsmeta

#$ ____ class setts ________________________________________________________ #

class setts(settsmeta):
    _ldef_cates_id = None

#$ ____ class cates ________________________________________________________ #

class cates:

    # class setts
    setts = setts('setts', (setts,), {})

#$$ ________ def __init__ __________________________________________________ #

    def __init__(self, core):

        # project object
        self.core = core

        # local setts
        self.setts = self.setts('setts',(),{})

#$$ ________ def add _______________________________________________________ #

    def add(self, id=None, γ_u=None, γ_f=None, γ_a=None, ψ_0=None, ψ_1=None, ψ_1s=None, ψ_2=None, ttl=None):

        id   = parse.chdr('setts.id'  , id  )
        γ_u  = parse.chdr('loads.cates.γ_u' , γ_u )
        γ_f  = parse.chdr('loads.cates.γ_f' , γ_f )
        γ_a  = parse.chdr('loads.cates.γ_a' , γ_a )
        ψ_0  = parse.chdr('loads.cates.ψ_0' , ψ_0 )
        ψ_1  = parse.chdr('loads.cates.ψ_1' , ψ_1 )
        ψ_1s = parse.chdr('loads.cates.ψ_1s', ψ_1s)
        ψ_2  = parse.chdr('loads.cates.ψ_2' , ψ_2 )
        ttl  = parse.chdr('loads.cates.ttl' , ttl )

        # overwrite last defined category
        self.setts._ldef_cates_id = id

        # add nodes data
        self.core.dbase.add(
            mode  = 'r',
            table = '[051:loads:cates]',
            cols  = ['id','γ_u','γ_f','γ_a','ψ_0','ψ_1','ψ_1s','ψ_2','ttl'],
            data  = [ id , γ_u , γ_f , γ_a , ψ_0 , ψ_1 , ψ_1s , ψ_2 , ttl ],
        )

#$$ ________ def echo ______________________________________________________ #

    def echo(self, mode='a+', where=None):

        if 'a' in mode:
            data = self.core.dbase.get(
                mode  = 'm',
                table = '[051:loads:cates]',
                cols  = ['id','γ_u','γ_f','γ_a','ψ_0','ψ_1','ψ_1s','ψ_2','ttl'],
                where = where,
            )

            if not data: return

            self.core.pinky.rstme.table(
                caption= 'Load categories',
                wrap   = [False, False, False, False, False, False, False, False, True],
                width  = [True,4,4,4,4,4,4,4,True],
                halign = ['l','c','c','c','c','c','c','c','l'],
                valign = ['u','u','u','u','u','u','u','u','u'],
                dtype  = ['t','f','f','f','t','t','t','t','t'],
                header = ['id' ,'γ_u' ,'γ_f','γ_a','ψ_0',
                          'ψ_1','ψ_1s','ψ_2','ttl'],
                data   = data,
                precision = 2,
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
                    ['γ_u'   , ''  , '-', ''       ],
                    ['γ_f'   , ''  , '-', ''       ],
                    ['γ_a'   , ''  , '-', ''       ],
                    ['ψ_0'   , ''  , '-', ''       ],
                    ['ψ_1'   , ''  , '-', ''       ],
                    ['ψ_1s'   , ''  , '-', ''       ],
                    ['ψ_2'   , ''  , '-', ''       ],
                    ['ψ_2'   , ''  , '-', ''       ],
                    ['ttl'   , ''  , '-', ''       ],

                ],
                border = False,
            )
