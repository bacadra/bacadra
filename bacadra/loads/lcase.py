'''
------------------------------------------------------------------------------
***** (l)oads (case)s *****
==============================================================================

------------------------------------------------------------------------------
Copyright (C) 2018 <bacadra@gmail.com> <https://github.com/bacadra>
Team members developing this package:
Sebastian Balcerowiak <asiloisad> <asiloisad.93@gmail.com>
------------------------------------------------------------------------------
'''

from ..dbase import parse
from ..tools.setts import settsmeta


#$ ____ class setts ________________________________________________________ #

class setts(settsmeta):
    _ldef_lcase_id = None


#$ ____ class lcase ________________________________________________________ #

class lcase:

    # class setts
    setts = setts('setts', (setts,), {})


#$$ ________ def __init__ __________________________________________________ #

    def __init__(self, core):
        self.core = core

        # local setts
        self.setts = self.setts('setts',(),{})

#$$ ________ def add _______________________________________________________ #

    def add(self, id=None, cates=None, fact=None, γ_u=None, γ_f=None, γ_a=None, ψ_0=None, ψ_1=None, ψ_1s=None, ψ_2=None, ttl=None):

        id    = parse.chdr('setts.id'        , id    )
        cates = parse.chdr('setts.id'        , cates )
        ttl   = parse.chdr('setts.ttl'       , ttl   )
        γ_u   = parse.chdr('loads.cates.γ_u' , γ_u   )
        γ_f   = parse.chdr('loads.cates.γ_f' , γ_f   )
        γ_a   = parse.chdr('loads.cates.γ_a' , γ_a   )
        ψ_0   = parse.chdr('loads.cates.ψ_0' , ψ_0   )
        ψ_1   = parse.chdr('loads.cates.ψ_1' , ψ_1   )
        ψ_1s  = parse.chdr('loads.cates.ψ_1s', ψ_1s  )
        ψ_2   = parse.chdr('loads.cates.ψ_2' , ψ_2   )

        # get last defined cates
        cates = self.core.loads.cates.setts.check_loc(
            '_ldef_cates_id',cates)

        # overwrite last one defined lcase
        self.setts._ldef_lcase_id = id

        # add nodes data
        self.core.dbase.add(
            mode  = 'r',
            table = '[052:loads:lcase]',
            cols  = ['id','cates','ttl','γ_u','γ_f',
                'γ_a','ψ_0','ψ_1','ψ_1s','ψ_2'],
            data  = [id,cates,ttl,γ_u,γ_f,γ_a,ψ_0,ψ_1,ψ_1s,ψ_2],
        )

#$$ ________ def echo ______________________________________________________ #

    def echo(self, mode='a+', where=None):

        if 'a' in mode:
            data = self.core.dbase.get(
                mode  = 'm',
                table = '[052:loads:lcase]',
                cols  = ['id','cates','γ_u','γ_f',
                    'γ_a','ψ_0','ψ_1','ψ_1s','ψ_2','ttl'],
                where = where,
            )

            if not data: return

            self.core.pinky.rstme.table(
                caption= 'Load cases',
                wrap   = [False, False, False, False, False, False, False, False, False, True],
                width  = [True,True,4,4,4,4,4,4,4,True],
                halign = ['l','l','c','c','c','c','c','c','c','l'],
                valign = ['u','u','u','u','u','u','u','u','u','u'],
                dtype  = ['t','t','f','f','f','t','t','t','t','t'],
                header = ['id','cates','γ_u' ,'γ_f','γ_a','ψ_0',
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


