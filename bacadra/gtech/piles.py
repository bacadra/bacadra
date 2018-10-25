# from ..pinky.pinky import pinky
from ..cunit.ce import *
from ..cunit.cmath import *

# import numpy  as np
# import pandas as pd


#$ ____ class main _________________________________________________________ #

class main:
    #$$ def --init--
    def __init__(self, dbase, pinky, pvars):
        self.dbase = dbase
        self.pinky = pinky
        self.pvars = pvars
        self.pnb83 = pnb83(self.dbase, self.pinky, self.pvars)


#$ ____ class pnb83 ________________________________________________________ #

class pnb83:
    '''
    PN-B-02482 1983
    '''
    #$$ def --init--
    def __init__(self, dbase, pinky, pvars):
        self.dbase = dbase
        self.pinky = pinky
        self.pvars = pvars


    def techfact(self, lay):
        I_D = lay.I_D
        I_L = lay.I_L
        # wybor technologii pali i jego zestawu wspolczynnikow
        if self.ptech in ('1a'):
            if I_D:
                if I_D >= 0.67:          S_p, S_s, S_w = 1.0, 1.0, 0.6
                elif 0.67 > I_D >= 0.20: S_p, S_s, S_w = 1.1, 1.1, 0.6
                else:                    S_p, S_s, S_w = 0,     0,   0
            if I_L:
                if I_L <= 0:             S_p, S_s, S_w = 1.0, 1.0, 0.6
                elif 0 < I_L <= 0.75:    S_p, S_s, S_w = 1.1, 1.1, 0.6
                else:                    S_p, S_s, S_w = 0,     0,   0

        elif self.ptech in ('1b'):
            if I_D:
                if I_D >= 0.67:          S_p, S_s, S_w = 1.0, 0.8, 0.4
                elif 0.67 > I_D >= 0.20: S_p, S_s, S_w = 1.0, 0.8, 0.4
                else:                    S_p, S_s, S_w =   0,   0,   0
            if I_L:
                if I_L <= 0:             S_p, S_s, S_w = 1.0, 1.0, 0.7
                elif 0 < I_L <= 0.75:    S_p, S_s, S_w = 1.0, 0.9, 0.6
                else:                    S_p, S_s, S_w =   0,   0,   0

        elif self.ptech in ('1c'):
            if I_D:
                if I_D >= 0.67:          S_p, S_s, S_w =   0,   0,   0
                elif 0.67 > I_D >= 0.20: S_p, S_s, S_w = 1.0, 0.8, 0.5
                else:                    S_p, S_s, S_w =   0,   0,   0
            if I_L:
                if I_L <= 0:             S_p, S_s, S_w =   0,   0,   0
                elif 0 < I_L <= 0.75:    S_p, S_s, S_w =   0,   0,   0
                else:                    S_p, S_s, S_w =   0,   0,   0

        elif self.ptech in ('2'):
            if I_D:
                if I_D >= 0.67:          S_p, S_s, S_w = 1.3, 1.1, 1.0
                elif 0.67 > I_D >= 0.20: S_p, S_s, S_w = 1.8, 1.6, 1.0
                else:                    S_p, S_s, S_w = 0, 0,0
            if I_L:
                if I_L <= 0:             S_p, S_s, S_w = 1.2, 1.1, 0.8
                elif 0 < I_L <= 0.75:    S_p, S_s, S_w = 1.1, 1.0, 0.7
                else:                    S_p, S_s, S_w = 0,0,0

        elif self.ptech in ('3'):
            if I_D:
                if I_D >= 0.67:          S_p, S_s, S_w = 1.1, 1.0, 0.6
                elif 0.67 > I_D >= 0.20: S_p, S_s, S_w = 1.4, 1.1, 0.6
                else:                    S_p, S_s, S_w = 0,0,0
            if I_L:
                if I_L <= 0:             S_p, S_s, S_w = 1.0, 1.0, 0.6
                elif 0 < I_L <= 0.75:    S_p, S_s, S_w = 1.0, 0.9, 0.6
                else:                    S_p, S_s, S_w = 0,0,0

        elif self.ptech in ('4a'):
            if I_D:
                if I_D >= 0.67:          S_p, S_s, S_w = 1.0, 0.8, 0.7
                elif 0.67 > I_D >= 0.20: S_p, S_s, S_w = 1.0, 0.9, 0.7
                else:                    S_p, S_s, S_w = 0,0,0
            if I_L:
                if I_L <= 0:             S_p, S_s, S_w = 1.0, 0.9, 0.6
                elif 0 < I_L <= 0.75:    S_p, S_s, S_w = 1.0, 0.9, 0.6
                else:                    S_p, S_s, S_w = 0,0,0

        elif self.ptech in ('4b'):
            if I_D:
                if I_D >= 0.67:          S_p, S_s, S_w = 1.0, 0.8, 0.6
                elif 0.67 > I_D >= 0.20: S_p, S_s, S_w = 1.0, 0.8, 0.6
                else:                    S_p, S_s, S_w = 0,0,0
            if I_L:
                if I_L <= 0:             S_p, S_s, S_w = 1.0, 0.8, 0.6
                elif 0 < I_L <= 0.75:    S_p, S_s, S_w = 1.0, 0.8, 0.5
                else:                    S_p, S_s, S_w = 0,0,0

        elif self.ptech in ('4c'):
            if I_D:
                if I_D >= 0.67:          S_p, S_s, S_w = 1.0, 1.0, 0.7
                elif 0.67 > I_D >= 0.20: S_p, S_s, S_w = 1.0, 1.1, 0.7
                else:                    S_p, S_s, S_w = 0,0,0
            if I_L:
                if I_L <= 0:             S_p, S_s, S_w = 1.0, 1.0, 0.7
                elif 0 < I_L <= 0.75:    S_p, S_s, S_w = 1.0, 1.0, 0.6
                else:                    S_p, S_s, S_w = 0,0,0

        elif self.ptech in ('4d'):
            if I_D:
                if I_D >= 0.67:          S_p, S_s, S_w = 1.0, 1.0, 0.7
                elif 0.67 > I_D >= 0.20: S_p, S_s, S_w = 1.0, 1.0, 0.7
                else:                    S_p, S_s, S_w = 0,0,0
            if I_L:
                if I_L <= 0:             S_p, S_s, S_w = 0,0,0
                elif 0 < I_L <= 0.75:    S_p, S_s, S_w = 1.0, 0.9,0.5
                else:                    S_p, S_s, S_w = 0,0,0

        elif self.ptech in ('4e'):
            if I_D:
                if I_D >= 0.67:          S_p, S_s, S_w = 1.0, 1.0, 0.7
                elif 0.67 > I_D >= 0.20: S_p, S_s, S_w = 1.0, 1.0, 0.7
                else:                    S_p, S_s, S_w = 0,0,0
            if I_L:
                if I_L <= 0:             S_p, S_s, S_w = 0,0,0
                elif 0 < I_L <= 0.75:    S_p, S_s, S_w = 0,0,0
                else:                    S_p, S_s, S_w = 0,0,0

        elif self.ptech in ('4f'):
            if I_D:
                if I_D >= 0.67:          S_p, S_s, S_w = 1.0, 0.8, 0.6
                elif 0.67 > I_D >= 0.20: S_p, S_s, S_w = 1.0, 0.9, 0.6
                else:                    S_p, S_s, S_w = 0,0,0
            if I_L:
                if I_L <= 0:             S_p, S_s, S_w = 1.0, 0.9, 0.6
                elif 0 < I_L <= 0.75:    S_p, S_s, S_w = 1.0, 0.8, 0.5
                else:                    S_p, S_s, S_w = 0,0,0

        elif self.ptech in ('5a'):
            if I_D:
                if I_D >= 0.67:          S_p, S_s, S_w = 0.8,0.6,0.4
                elif 0.67 > I_D >= 0.20: S_p, S_s, S_w = 0.9,0.7,0.5
                else:                    S_p, S_s, S_w = 0,0,0
            if I_L:
                if I_L <= 0:             S_p, S_s, S_w = 0,0,0
                elif 0 < I_L <= 0.75:    S_p, S_s, S_w = 0,0,0
                else:                    S_p, S_s, S_w = 0,0,0

        elif self.ptech in ('5b'):
            if I_D:
                if I_D >= 0.67:          S_p, S_s, S_w = 0.8,0.6,0.4
                elif 0.67 > I_D >= 0.20: S_p, S_s, S_w = 0.9,0.7,0.5
                else:                    S_p, S_s, S_w = 0,0,0
            if I_L:
                if I_L <= 0:             S_p, S_s, S_w = 0,0,0
                elif 0 < I_L <= 0.75:    S_p, S_s, S_w = 0,0,0
                else:                    S_p, S_s, S_w = 0,0,0

        elif self.ptech in ('5c'):
            if I_D:
                if I_D >= 0.67:          S_p, S_s, S_w = 0.8,0.7,0.5
                elif 0.67 > I_D >= 0.20: S_p, S_s, S_w = 0.9,0.8,0.5
                else:                    S_p, S_s, S_w = 0,0,0
            if I_L:
                if I_L <= 0:             S_p, S_s, S_w = 0,0,0
                elif 0 < I_L <= 0.75:    S_p, S_s, S_w = 0,0,0
                else:                    S_p, S_s, S_w = 0,0,0

        elif self.ptech in ('5d'):
            if I_D:
                if I_D >= 0.67:          S_p, S_s, S_w = 1.0, 1.0, 0.7
                elif 0.67 > I_D >= 0.20: S_p, S_s, S_w = 1.0, 1.0, 0.7
                else:                    S_p, S_s, S_w = 0,0,0
            if I_L:
                if I_L <= 0:             S_p, S_s, S_w = 0,0,0
                elif 0 < I_L <= 0.75:    S_p, S_s, S_w = 0,0,0
                else:                    S_p, S_s, S_w = 0,0,0

        elif self.ptech in ('5e'):
            if I_D:
                if I_D >= 0.67:          S_p, S_s, S_w = 1.0, 1.0, 0.7
                elif 0.67 > I_D >= 0.20: S_p, S_s, S_w = 1.0, 1.0, 0.7
                else:                    S_p, S_s, S_w = 0,0,0
            if I_L:
                if I_L <= 0:             S_p, S_s, S_w = 0,0,0
                elif 0 < I_L <= 0.75:    S_p, S_s, S_w = 0,0,0
                else:                    S_p, S_s, S_w = 0,0,0

        elif self.ptech in ('5f'):
            if I_D:
                if I_D >= 0.67:          S_p, S_s, S_w = 0.8,0.6,0.5
                elif 0.67 > I_D >= 0.20: S_p, S_s, S_w = 0.9,0.7,0.5
                else:                    S_p, S_s, S_w = 0,0,0
            if I_L:
                if I_L <= 0:             S_p, S_s, S_w = 0,0,0
                elif 0 < I_L <= 0.75:    S_p, S_s, S_w = 0,0,0
                else:                    S_p, S_s, S_w = 0,0,0

        elif self.ptech in ('6a'):
            if I_D:
                if I_D >= 0.67:          S_p, S_s, S_w = 0,0,0
                elif 0.67 > I_D >= 0.20: S_p, S_s, S_w = 1.1,1.0,0.5
                else:                    S_p, S_s, S_w = 0,0,0
            if I_L:
                if I_L <= 0:             S_p, S_s, S_w = 1.0,1.1,0.5
                elif 0 < I_L <= 0.75:    S_p, S_s, S_w = 1.0,0.9,0.5
                else:                    S_p, S_s, S_w = 0,0,0

        elif self.ptech in ('6b'):
            if I_D:
                if I_D >= 0.67:          S_p, S_s, S_w = 1.0,0.7,0.4
                elif 0.67 > I_D >= 0.20: S_p, S_s, S_w = 1.0,0.6,0.4
                else:                    S_p, S_s, S_w = 0,0,0
            if I_L:
                if I_L <= 0:             S_p, S_s, S_w = 0,0,0
                elif 0 < I_L <= 0.75:    S_p, S_s, S_w = 0,0,0
                else:                    S_p, S_s, S_w = 0,0,0

        elif self.ptech in ('6c'):
            if I_D:
                if I_D >= 0.67:          S_p, S_s, S_w = 0,0,0
                elif 0.67 > I_D >= 0.20: S_p, S_s, S_w = 1.0,0.8,0.5
                else:                    S_p, S_s, S_w = 0,0,0
            if I_L:
                if I_L <= 0:             S_p, S_s, S_w = 0,0,0
                elif 0 < I_L <= 0.75:    S_p, S_s, S_w = 0,0,0
                else:                    S_p, S_s, S_w = 0,0,0

        elif self.ptech in ('7a'):
            if I_D:
                if I_D >= 0.67:          S_p, S_s, S_w = 1.0,0.8,0.5
                elif 0.67 > I_D >= 0.20: S_p, S_s, S_w = 1.0,0.9,0.5
                else:                    S_p, S_s, S_w = 0,0,0
            if I_L:
                if I_L <= 0:             S_p, S_s, S_w = 1.0,1.0,0.5
                elif 0 < I_L <= 0.75:    S_p, S_s, S_w = 1.0,0.9,0.5
                else:                    S_p, S_s, S_w = 0,0,0

        elif self.ptech in ('7b'):
            if I_D:
                if I_D >= 0.67:          S_p, S_s, S_w = 1.0,0.5,0.3
                elif 0.67 > I_D >= 0.20: S_p, S_s, S_w = 1.0,0.6,0.3
                else:                    S_p, S_s, S_w = 0,0,0
            if I_L:
                if I_L <= 0:             S_p, S_s, S_w = 0,0,0
                elif 0 < I_L <= 0.75:    S_p, S_s, S_w = 0,0,0
                else:                    S_p, S_s, S_w = 0,0,0

        elif self.ptech in ('7c'):
            if I_D:
                if I_D >= 0.67:          S_p, S_s, S_w = 0,0,0
                elif 0.67 > I_D >= 0.20: S_p, S_s, S_w = 1.0,0.7,0.4
                else:                    S_p, S_s, S_w = 0,0,0
            if I_L:
                if I_L <= 0:             S_p, S_s, S_w = 0,0,0
                elif 0 < I_L <= 0.75:    S_p, S_s, S_w = 0,0,0
                else:                    S_p, S_s, S_w = 0,0,0

        return S_p, S_s, S_w


    def add(self, id=None, name=None, tech=None, bore=None, z_0=None, L_t=None, usect=None, x=None, y=None, ttl=None):

        if type(x) is list:
            i = 0
            for x1,y1 in x,y:
                i += 1
                A,B,C = self.dbase.parse(x=x1, y=y1, id=id, name=name, tech=tech, bore=bore, z_0=z_0, L_t=L_t, usect=usect, ttl=ttl, i=i)

            self.dbase.exe("INSERT INTO [312:gtech:piles]" + A + " VALUES" + B ,C)

        else:
            A,B,C = self.dbase.parse(x=x, y=y, id=id, name=name, tech=tech, bore=bore, z_0=z_0, L_t=L_t, usect=usect, ttl=ttl, i=1)

            self.dbase.exe("INSERT INTO [312:gtech:piles]" + A + " VALUES" + B ,C)
