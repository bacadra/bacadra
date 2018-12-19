'''
------------------------------------------------------------------------------
BCDR += ***** (cate)gorie(s) *****
==============================================================================

------------------------------------------------------------------------------
Copyright (C) 2018 <bacadra@gmail.com> <https://github.com/bacadra/bacadra>
Team members developing this package:
    - Sebastian Balcerowiak <asiloisad> <asiloisad.93@gmail.com>
------------------------------------------------------------------------------
'''

# import setts

#$ ____ class cates ________________________________________________________ #

class cates:
    #$$ def __init__
    def __init__(self, core):
        self.core = core

    #$$ def --enter--
    def __enter__(self):
        return self

    #$$ def --exit--
    def __exit__(self, type, value, traceback):
        pass

    def add(self, id=None, γ_u=None, γ_f=None, γ_a=None, γ_1=None, γ_2=None, γ_3=None, ψ_0=None, ψ_1=None, ψ_1s=None, ψ_2=None, ttl=None):

        # overwrite last defined category
        self.core.mdata.setts.set({'_cates_ldef':id})

        # parse data
        cols,data = self.core.dbase.parse(
            id    = id,
            γ_u  = γ_u,
            γ_f  = γ_f,
            γ_a  = γ_a,
            γ_1  = γ_1,
            γ_2  = γ_2,
            γ_3  = γ_3,
            ψ_0  = ψ_0,
            ψ_1  = ψ_1,
            ψ_1s = ψ_1s,
            ψ_2  = ψ_2,
            ttl   = ttl,
        )

        # add data
        self.core.dbase.add(
            table = '[051:loads:cates]',
            cols  = cols,
            data  = data,
        )