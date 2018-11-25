'''
------------------------------------------------------------------------------
BCDR += ***** (c)oncrete (memb)ers *****
==============================================================================

------------------------------------------------------------------------------
Copyright (C) 2018 <bacadra@gmail.com> <https://github.com/bacadra/bacadra>
Team members developing this package:
    - Sebastian Balcerowiak <asiloisad> <asiloisad.93@gmail.com>
------------------------------------------------------------------------------
'''

from ..cunit import cunit
from ..cunit.system.math import sqrt

class cmemb:
    def __init__(self, h, b, a_1, M_y_Ed, f_cd, f_sd):
        self.b = b
        self.h = h
        self.a_1 = a_1
        self.M_y_Ed = M_y_Ed
        self.f_sd = f_sd
        self.f_cd = f_cd

    def b1_shape_rect_mlaw_rect(self):

        d = self.h - self.a_1
        ξ_eff = 1 - sqrt(1- (2*self.M_y_Ed) / (self.f_cd*self.b * d**2) )

        ρ_1 = self.f_cd / self.f_sd * ξ_eff

        A_s1 = ρ_1 * self.b * d

        return {
            'ξ_eff': ξ_eff,
            'ρ_1'  : ρ_1,
            'A_s1' : A_s1.s('cm**2'),
        }

