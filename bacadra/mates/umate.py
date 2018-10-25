#$ **** module concs **** __________________________________________________ #

#$$ ________ import ________________________________________________________ #

# from ..cunit.ce import *
# from ..cunit.cmath import *

# import numpy  as np
# import pandas as pd

#$ ____ class umate ________________________________________________________ #

class umate:
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

    #$$ def add
    def add(self,
    # parametry ogolne
    id=None, ρ=None, E_1=None, v_1=None, G_1=None, texp=None, ttl=None, _subcl=None):

        # calc third value of material constant
        if E_1 and v_1 and not G_1:
            G_1 = (E_1) / (2 * (1 + v_1))

        elif E_1 and not v_1 and G_1:
            v_1 = E_1/G_1 * 0.5 - 1

        elif not E_1 and v_1 and G_1:
            E_1 = G_1 * (2 * (1 + v_1))

        # overwrite last defined material
        self.pvars.set({'_mates_ldef':id})

        # parse data do univeral material
        cols,data = self.dbase.parse(
            id    = id,
            rho   = ρ,
            E_1   = E_1,
            v_1   = v_1,
            G_1   = G_1,
            texp  = texp,
            ttl   = ttl,
            subcl = _subcl,
        )

        # add universal material
        self.dbase.add(
            table = '[011:mates:umate]',
            cols  = cols,
            data  = data,
        )
