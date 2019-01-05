'''
------------------------------------------------------------------------------
BCDR += ***** composite steel-concrete (f)filler (deck)s *****
==============================================================================

------------------------------------------------------------------------------
Copyright (C) 2018 <bacadra@gmail.com> <https://github.com/bacadra/bacadra>
Team members developing this package:
    - Sebastian Balcerowiak <asiloisad> <asiloisad.93@gmail.com>
------------------------------------------------------------------------------
'''

from sympy.solvers import solve
from sympy import Symbol as symbol

from ..tools.bdata import bdata
from ..cunit import cunit
from ..cunit.system.math import sqrt

kN  = cunit(1, 'kN')
m   = cunit(1, 'm')
kPa = cunit(1, 'kPa')
kNm = cunit(1, 'kN m')
kg  = cunit(1, 'kg')

class fdeck:
    def __init__(self, **kwargs):
        pass

    def prop(self, f_cd, f_yd, b_c, h_c, b_f, t_f, t_w, h, h_s):
        '''
        ***** materials *****
         f_cd --  concrete design compressive strength
         f_yd --  steel design strength

        ***** cross-section dimensions*****
         b_c  --  concrete width
         h_c  --  concrete height
         b_f  --  steel flange width
         t_f  --  steel flange thickness
         t_w  --  steel web thickness
         h    --  steel total height
         h_s  --  wysokosc nadbetonu
        '''

        z = symbol('z')

        # drop units
        b_c  = b_c.d('m')
        h_c  = h_c.d('m')
        b_f  = b_f.d('m')
        t_f  = t_f.d('m')
        t_w  = t_w.d('m')
        h    = h.d('m')
        h_s  = h_s.d('m')
        f_cd = f_cd.d('kPa')
        f_yd = f_yd.d('kPa')


        # web height
        h_w = h - 2*t_f

        # steel area
        A_s = b_f*t_f*2 + h_w*t_w

        # concrete area
        A_c = b_c*h_c - A_s

        A = A_s + A_c

        # concrete strengh factor
        temp = 0.85

        #$ ____ plastic ____________________________________________________________ #

        # axial force of upper side
        N_upp = b_c*h_s*f_cd*temp + b_f*t_f*(f_yd-f_cd*temp) + b_c*z*f_cd*temp + t_w*z*(f_yd-f_cd*temp)

        # axial force of bottom side
        N_low = (b_f*t_f + (h_w - z)*t_w)*f_yd

        # solved height
        z_pl_0 = float(solve(N_upp - N_low, z)[0])

        # plastic moment
        M_pl_Rd = (
            - (b_c*h_s*f_cd*temp) * (h_s*0.5) +
            - (b_f*t_f*(f_yd-f_cd*temp)) * (h_s+0.5*t_f) +
            - (b_c*z_pl_0*f_cd*temp + t_w*z_pl_0*(f_yd-f_cd*temp)) * (h_s+t_f+z_pl_0/2) +
            + (b_f*t_f*f_yd) * (h_s+h-0.5*t_f) +
            + ((h_w - z_pl_0)*t_w*f_yd) * (h_s+h-t_f -(h_w-z_pl_0)/2)
        )

        # check compability
        z_pl = z_pl_0+t_f+h_s

        ε = 0.1
        if not 1-ε <= (N_low.subs({'z':z_pl_0}))/(N_upp.subs({'z':z_pl_0})) <= 1+ε:
            raise ValueError('Non equal axis forces of upper and lower sides')

        if z_pl_0 < 0:
            raise ValueError('Compressive zone over bottom side of upper flange')


        #$ static

        n_0 = 210/31.476

        A_eff = (b_c*(h_s + t_f + z) - t_f*b_f - z*t_w)/n_0 + b_f*t_f*2 + h_w*t_w

        S_y_I  = (0.5*b_c*(h_s + t_f + z)**2)/n_0 + 0.5*t_w*z**2 *(1-1/n_0) + t_f*b_f*(0.5*t_f + z)*(1-1/n_0)

        S_y_II = 0.5*t_w*(h_w-z)**2 + (h_w-z+0.5*t_f)*t_f*b_f

        z_el_0 = float(solve(S_y_II-S_y_I, z)[1])

        # I_y_el = (0.25*b_c*(h_s + t_f + z)**3)/n_0 + 0.25*t_w*z**3 *(1-1/n_0) + t_f*b_f*(0.5*t_f + z)**2 *(1-1/n_0) + 0.25*t_w*(h_w-z)**3 + (h_w-z+0.5*t_f)**2 *t_f*b_f
        # I_y_el = float(I_y_el.subs({'z':z_el_0}))

        z_el = z_el_0 + h_s + t_f

        A_eff = float(A_eff.subs({'z':z_el_0}))

        I_y_el = ((b_c*z_el**3/12 + b_c*z_el*(z_el/2)**2)/n_0
            + (t_f**3*b_f/12 + t_f*b_f*(z_el_0+0.5*t_f)**2) *(1-1/n_0)
            + t_w*z_el_0**3/12 + t_w*z_el_0*(z_el_0/2)**3
            + t_w*(h_w-z_el_0)**3/12 + t_w*(h_w-z_el_0)*((h_w-z_el_0)/2)**2
            + t_f**3*b_f/12 + t_f*b_f*(0.5*t_f+h_w-z_el_0)**2)

        M_el_Rd_c = I_y_el/z_el * n_0 * f_cd
        M_el_Rd_a = I_y_el/(h_s+h-z_el) * f_yd
        M_el_Rd   = min([M_el_Rd_c, M_el_Rd_a])

        V_pl_Rd = h_w*t_w*f_yd/sqrt(3)



        return bdata({
            'A'      : A       * m**2,
            'A_eff'  : A_eff   * m**2,
            'A_s'    : A_s     * m**2,
            'A_c'    : A_c     * m**2,

            'z_pl'   : z_pl    * m,
            'z_el'   : z_el    * m,

            'V_pl_Rd': V_pl_Rd * kN,
            'M_el_Rd': M_el_Rd * kNm,
            'M_pl_Rd': M_pl_Rd * kNm,

            'I_y_el' : I_y_el  * m**4,
            'm_g'    : A_s*m**2 * 7850*kg/m**3 + A_c*m**2 * 2500*kg/m**3,
        })




    def prop_high_hs(self, f_cd, f_yd, b_c, h_c, b_f, t_f, t_w, h, h_s):
        '''
        ***** materials *****
         f_cd --  concrete design compressive strength
         f_yd --  steel design strength

        ***** cross-section dimensions*****
         b_c  --  concrete width
         h_c  --  concrete height
         b_f  --  steel flange width
         t_f  --  steel flange thickness
         t_w  --  steel web thickness
         h    --  steel total height
         h_s  --  wysokosc nadbetonu
        '''

        z = symbol('z')

        # drop units
        b_c  = b_c.d('m')
        h_c  = h_c.d('m')
        b_f  = b_f.d('m')
        t_f  = t_f.d('m')
        t_w  = t_w.d('m')
        h    = h.d('m')
        h_s  = h_s.d('m')
        f_cd = f_cd.d('kPa')
        f_yd = f_yd.d('kPa')


        # web height
        h_w = h - 2*t_f

        # steel area
        A_s = b_f*t_f*2 + h_w*t_w

        # concrete area
        A_c = b_c*h_c - A_s

        A = A_s + A_c

        # concrete strengh factor
        temp = 0.85

        #$ ____ plastic ____________________________________________________________ #

        # axial force of upper side
        N_upp = b_c*z*f_cd*temp

        # axial force of bottom side
        N_low = (b_f*t_f*2 + (h_w)*t_w)*f_yd

        # solved height
        z_pl_0 = float(solve(N_upp - N_low, z)[0])

        # plastic moment
        M_pl_Rd = (
            - (b_c*z_pl_0*f_cd*temp) * (z_pl_0*0.5) +
            + (b_f*t_f*2 + (h_w)*t_w)*f_yd * (h_s-z_pl_0+0.5*h)
        )

        # check compability
        z_pl = z_pl_0

        ε = 0.1
        if not 1-ε <= (N_low)/(N_upp.subs({'z':z_pl_0})) <= 1+ε:
            raise ValueError('Non equal axis forces of upper and lower sides')

        if not 0 <= z_pl < h_s:
            print(z_pl)
            raise ValueError('Compressive zone below upper side of upper flange')

        V_pl_Rd = h_w*t_w*f_yd/sqrt(3)


        return bdata({
            'A'      : A       * m**2,
            'A_s'    : A_s     * m**2,
            'A_c'    : A_c     * m**2,
            'z_pl'   : z_pl    * m,
            'V_pl_Rd': V_pl_Rd * kN,
            'M_pl_Rd': M_pl_Rd * kNm,
            'm_g'    : A_s*m**2 * 7850*kg/m**3 + A_c*m**2 * 2500*kg/m**3,
        })