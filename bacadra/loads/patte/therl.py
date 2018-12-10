'''
------------------------------------------------------------------------------
BCDR += ***** (ther)mal (l)oads *****
==============================================================================

------------------------------------------------------------------------------
Copyright (C) 2018 <bacadra@gmail.com> <https://github.com/bacadra/bacadra>
Team members developing this package:
    - Sebastian Balcerowiak <asiloisad> <asiloisad.93@gmail.com>
------------------------------------------------------------------------------
'''


import numpy as np

from ...cunit import cunit

m   = cunit(1, 'm')
cu  = cunit(1, '')
kPa = cunit(1, 'kPa')
C   = cunit(1, '°C')

class therl:
    def __init__(self, core=None):
        self.core = core

    class ecode:
        def T_e(mode, T):
            # pomosty stalowe
            if mode=='1':
                return np.interp(
                    T.d('°C'),
                    np.array([-50, 0,30,50]),
                    np.array([-55,-3,46,66]),
                ) * C

            # pomosty zespolone
            elif mode=='2':
                return np.interp(
                    T.d('°C'),
                    np.array([-50, 0,30,50]),
                    np.array([-45, 5,35,55]),
                ) * C

            # pomosty betonowe
            elif mode=='3':
                return np.interp(
                    T.d('°C'),
                    np.array([-50, 0,30,50]),
                    np.array([-42, 9,32,52]),
                ) * C 

            else:
                raise ValueError('Undefined type, try: "1", "2" or "3"')