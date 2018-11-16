
from ..cunit.system.math import sqrt

class smemb:
    def __init__(self):
        pass

    def slederness(self, α_cr=None, val_Rk=None, val_Ek=None, val_cr=None):

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


    def stability_uniaxial(self, σ_nmy_Ed, σ_mz_Ed, σ_x_Rk, α_imp=0.76, γ_a_M1=1.1, λ_op=True,
    α_cr=None, val_Rk=None, val_Ek=None, val_cr=None):

        if λ_op==True:
            λ_op = self.slederness(
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
            (σ_nmy_Ed)/(σ_x_Rk / γ_a_M1 * χ_op) +
            (σ_mz_Ed )/(σ_x_Rk / γ_a_M1)
        )

        # returned dictonary
        return {
            'λ_op': λ_op,
            'χ_op': χ_op,
            'util': util.s('%'),
        }


