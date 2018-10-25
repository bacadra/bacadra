#$ **** module concs **** __________________________________________________ #

#$$ ________ import ________________________________________________________ #

# from ..cunit.ce import *
# from ..cunit.cmath import *

# import numpy  as np
# import pandas as pd

from . import umate

#$ ____ class conce ________________________________________________________ #

class conce:
    #$$ def --init--
    def __init__(self, dbase, pinky, pvars):
        self.dbase = dbase
        self.pinky = pinky
        self.pvars = pvars

        self._umate = umate.umate(self.dbase, self.pinky, self.pvars)

    #$$ def --enter--
    def __enter__(self):
        return self

    #$$ def --exit--
    def __exit__(self, type, value, traceback):
        pass

    #$$ def add
    def add(self,
    # parametry ogolne
    id=None, ρ=None, E_1=None, v_1=None, G_1=None, texp=None, ttl=None,

    # parametry betonu
    cclass=None, f_ck=None):

        # add universal material
        self._umate.add(
            id     = id,
            ρ      = ρ,
            E_1    = E_1,
            v_1    = v_1,
            G_1    = G_1,
            texp   = texp,
            ttl    = ttl,
            _subcl = 'C',
        )

        # parse data for concrete material
        cols,data = self.dbase.parse(
            id    = id,
            cclass= cclass,
            f_ck  = f_ck,
        )

        # add data for concrete material
        self.dbase.add(
            table = '[012:mates:conce]',
            cols  = cols,
            data  = data,
        )

