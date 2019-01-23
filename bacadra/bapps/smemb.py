'''
------------------------------------------------------------------------------
BCDR += ***** (s)teel (memb)ers *****
==============================================================================

------------------------------------------------------------------------------
Copyright (C) 2018 <bacadra@gmail.com> <https://github.com/bacadra>
Team members developing this package:
    - Sebastian Balcerowiak <asiloisad> <asiloisad.93@gmail.com>
------------------------------------------------------------------------------
'''

import numpy as np
from ..cunit import cunit
from ..cunit.system.math import sqrt




class smemb:
    def __init__(self):
        pass

    @staticmethod
    def slederness(α_cr=None, val_Rk=None, val_Ek=None, val_cr=None):

        if α_cr and val_Rk and val_Ek:

            # plastic factor
            α_ult_k = (val_Rk)/(val_Ek)

            # slederness
            λ_op = sqrt((α_ult_k)/(α_cr))

        elif val_Rk and val_cr:
            λ_op = sqrt((val_Rk)/(val_cr))

        else:
            raise ValueError()

        return λ_op


    @staticmethod
    def stability_datas(α_imp, γ_M1, val_Rk, val_Ek=1, σ_x_Rk=None, val_cr=None, α_cr=None):

        if   α_imp=='a0': α_imp = 0.13
        elif α_imp=='a' : α_imp = 0.21
        elif α_imp=='b' : α_imp = 0.34
        elif α_imp=='c' : α_imp = 0.49
        elif α_imp=='d' : α_imp = 0.76

        λ_op = smemb.slederness(
            α_cr   = α_cr,
            val_Rk = val_Rk,
            val_Ek = val_Ek,
            val_cr = val_cr,
        )

        # coefficient
        φ_op = 0.5*(1 + α_imp*(λ_op - 0.2) + λ_op**2)
        χ_op = min((1)/(φ_op + sqrt(φ_op**2 - λ_op**2)), 1.0)

        σ_Rd = σ_x_Rk * χ_op / γ_M1

        # returned dictonary
        return {
            'val_cr': val_cr,
            'α_imp': α_imp,
            'α_ult': val_Rk/val_Ek,
            'λ_op' : λ_op,
            'χ_op' : χ_op,
            'σ_Rd' : σ_Rd,
        }




    @staticmethod
    def stability_uniaxial(σ_nmy_Ed, σ_mz_Ed, σ_x_Rk, α_imp=0.76, γ_M1=1.1, λ_op=True, α_cr=None, val_Rk=None, val_Ek=None, val_cr=None):

        if λ_op==True:
            λ_op = smemb.slederness(
                α_cr   = α_cr,
                val_Rk = val_Rk,
                val_Ek = val_Ek,
                val_cr = val_cr
            )

        # coefficient
        φ_op = 0.5*(1 + α_imp*(λ_op - 0.2) + λ_op**2)
        χ_op = min((1)/(φ_op + sqrt(φ_op**2 - λ_op**2)), 1.0)

        # utilization
        util = (
            (σ_nmy_Ed)/(σ_x_Rk / γ_M1 * χ_op) +
            (σ_mz_Ed )/(σ_x_Rk / γ_M1)
        )

        # returned dictonary
        return {
            'λ_op': λ_op,
            'χ_op': χ_op,
            'util': util.s('%'),
        }


    @staticmethod
    def tension(A, A_net, f_yk, f_uk, γ_M0, γ_M2):
        N_pl_Rd  = A     * f_yk       / γ_M0
        N_u_Rd   = 0.9   * A_net*f_uk / γ_M2
        N_net_Rd = A_net * f_yk       / γ_M0

        return {
            'N_pl_Rd': N_pl_Rd,
            'N_u_Rd':N_u_Rd,
            'N_net_Rd':N_net_Rd,
        }



