import math
from ...cunit.system.ce import MPa,mm,GPa

class mdata:
    def __init__(self):
        pass

    def get(self, name):
        '''
        User input name pattern, eg. C30, then method return valide dict with parametrs.
        '''

        return self._en_1993_S(name)

    def _en_1993_S(self, name):
        data = {
            'S235-40':{
                'max_t': 40*mm,
                'f_yk' : 235*MPa,
                'f_uk' : 275*MPa,
                'E_a'  : 210*GPa,
                'ε_yk' : (235*MPa) / (210*GPa),
                'ε_uk' : 0.05,
            },
        }

        if name in data:
            return data[name]
        else:
            return
