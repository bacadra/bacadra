'''
------------------------------------------------------------------------------
BCDR += ***** (wind) (l)oads *****
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


class windl:
    def __init__(self, core=None):
        self.core = core

    class ecode:
        def z_min(CT):
            if   CT=='0'  : return 1*m
            elif CT=='I'  : return 1*m
            elif CT=='II' : return 2*m
            elif CT=='III': return 5*m
            elif CT=='IV' : return 10*m

        def z_max(CT):
            if   CT=='0'  : return 200*m
            elif CT=='I'  : return 200*m
            elif CT=='II' : return 300*m
            elif CT=='III': return 400*m
            elif CT=='IV' : return 500*m

        def c_e(CT, z):
            z = z.drop('m')*cu
            if   CT=='0'  : return 3.0 * ((z)/(10))**0.17
            elif CT=='I'  : return 2.8 * ((z)/(10))**0.19
            elif CT=='II' : return 2.3 * ((z)/(10))**0.24
            elif CT=='III': return 1.9 * ((z)/(10))**0.26
            elif CT=='IV' : return 1.5 * ((z)/(10))**0.29

        def q_b_0(WZ, A_sea):
            A_sea = A_sea.d('m')
            if WZ=='1':
                if A_sea <= 300:
                    return 0.30*kPa
                else:
                    return 0.30*(1+0.0006*(A_sea-300))**2 *kPa
            elif WZ=='2':
                return 0.42*kPa
            elif WZ=='3':
                if A_sea <= 300:
                    return 0.30*kPa
                else:
                    return 0.30*(1+0.0006*(A_sea-300))**2 * (20000-A_sea)/(20000+A_sea) *kPa

        def c_f_y(bpd):
            # bpd = b/d
            bpd = bpd.d()
            return np.interp(
                bpd,
                np.array([0  ,0.2,5  ,12]),
                np.array([2.4,2.4,1.0,1.0]),
            )
