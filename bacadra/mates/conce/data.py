
import math
from ...cunit.system.ce import MPa

class en1992:
    def __init__(self):
        self._mates = {
            'C12': self.new_C(12*MPa),
            'C16': self.new_C(16*MPa),
            'C20': self.new_C(20*MPa),
            'C25': self.new_C(25*MPa),
            'C30': self.new_C(30*MPa),
            'C35': self.new_C(35*MPa),
            'C40': self.new_C(40*MPa),
            'C45': self.new_C(45*MPa),
            'C50': self.new_C(50*MPa),
            'C55': self.new_C(55*MPa),
            'C60': self.new_C(60*MPa),
            'C70': self.new_C(70*MPa),
            'C80': self.new_C(80*MPa),
            'C90': self.new_C(90*MPa),
        }

    @staticmethod
    def new_C(f_ck=None, f_ck_cube=None):
        if f_ck:
            f_ck_cube = 1.25 * f_ck
        elif f_ck_cube:
            f_ck = f_ck_cube / 1.25

        f_cm = f_ck + 8*MPa

        E_cm = (22*(0.1*f_cm.drop('MPa'))**0.3)*MPa

        ε_c1 = min(0.7*(f_cm.drop('MPa'))**0.31, 2.8)/1000

        if 90*MPa >= f_ck >= 50*MPa:
            f_ctm = (2.12*math.log(1+0.1*f_cm.drop('MPa'),math.e))*MPa
            ε_cu1 = (2.8+27*(0.01*(98-f_cm.drop('MPa')))**4)/1000
            ε_c2  = (2.0+0.085*(f_ck.drop('MPa') - 50)**0.53)/1000
            ε_cu2 = (2.6+35*(0.01*(90 - f_ck.drop('MPa')))**4)/1000
            n     = 1.4+23.4*(0.01*(90-f_ck.drop('MPa')))**4
            ε_c3  = (1.75 + 0.01375*(f_ck.drop('MPa') - 50))/1000
            ε_cu3 = (2.60 + 35*(0.01*(90-f_ck.drop('MPa')))**4)/1000

        elif 50*MPa > f_ck > 0*MPa:
            f_ctm = (0.30*f_ck.drop('MPa')**(2/3))*MPa
            ε_cu1 = 3.50/1000
            ε_c2  = 2.00/1000
            ε_cu2 = 3.50/1000
            n     = 2.00
            ε_c3  = 1.75/1000
            ε_cu3 = 3.50/1000

        f_ctk_005 = 0.7*f_ctm
        f_ctk_095 = 1.3*f_ctm


        return {
            'f_ck'      : f_ck,
            'f_ck_cube' : f_ck_cube,
            'f_cm'      : f_cm,
            'f_ctm'     : f_ctm,
            'f_ctk_005' : f_ctk_005,
            'f_ctk_095' : f_ctk_095,
            'E_cm'      : E_cm,
            'ε_c1'      : ε_c1,
            'ε_cu1'     : ε_cu1,
            'ε_c2'      : ε_c2,
            'ε_cu2'     : ε_cu2,
            'n'         : n,
            'ε_c3'      : ε_c3,
            'ε_cu3'     : ε_cu3,
        }

