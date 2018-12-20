import numpy as np

from .pbase  import pbase

from ...cunit import cunit
from ...cunit.system.math import sqrt,ln,exp
from ...cunit.system.ce   import MPa

class steea:
    #$$ def __init__
    def __init__(self, core):
        self.core = core

        from ..umate import umate
        self._umate = umate.umate(core=core)


    #$$ def add
    def add(self,
    # parametry ogolne
    id=None, ρ_o=cunit(7850, {'kg':1, 'm':-3}), E_1=None, v_1=0.30, G_1=None, t_e=cunit(12*10**-6, {'°C':-1}), ttl=None, orm=False,

    grade=None, t_max=None,
    f_yk=None, f_uk =None, E_a=None, ε_yk=None, ε_uk=None, γ_M0=None, γ_M1=None, γ_M2=None, γ_M3=None, γ_M4=None, γ_M5=None, γ_M6=None):

        if grade:
            pbase.set(grade=grade, t_max=t_max, f_yk=f_yk)

            f_yk      = pbase.get(f_yk      , 'f_yk'      )
            f_uk      = pbase.get(f_uk      , 'f_uk'      )
            E_a       = pbase.get(E_a       , 'E_a'       )
            ε_yk      = pbase.get(ε_yk      , 'ε_yk'      )
            ε_uk      = pbase.get(ε_uk      , 'ε_uk'      )
            γ_M0      = pbase.get(γ_M0      , 'γ_M0'      )
            γ_M1      = pbase.get(γ_M1      , 'γ_M1'      )
            γ_M2      = pbase.get(γ_M2      , 'γ_M2'      )
            γ_M3      = pbase.get(γ_M3      , 'γ_M3'      )
            γ_M4      = pbase.get(γ_M4      , 'γ_M4'      )
            γ_M5      = pbase.get(γ_M5      , 'γ_M5'      )
            γ_M6      = pbase.get(γ_M6      , 'γ_M6'      )

        if not E_1: E_1 = E_a

        # add universal material
        self._umate.add(
            id     = id,
            ρ_o    = ρ_o,
            E_1    = E_1,
            v_1    = v_1,
            G_1    = G_1,
            t_e    = t_e,
            ttl    = ttl,
            _subcl = 'A',
        )

        # parse data for steel material
        cols,data  = self.core.dbase.parse(
            id     = id,
            grade = grade,
            t_max  = t_max,
            f_yk   = f_yk,
            f_uk   = f_uk,
            E_a    = E_a,
            ε_yk   = ε_yk,
            ε_uk   = ε_uk,
            γ_M0   = γ_M0,
            γ_M1   = γ_M1,
            γ_M2   = γ_M2,
            γ_M3   = γ_M3,
            γ_M4   = γ_M4,
            γ_M5   = γ_M5,
            γ_M6   = γ_M6,
        )

        # add data for steel material
        self.core.dbase.add(
            table = '[013:mates:steea]',
            cols  = cols,
            data  = data,
        )

        if orm:
            return self.orm(where=f'id="{id}"')

    #$$ def orm
    def orm(self, id=None, where=None):
        from ...dbase.bxorm import bxorm_mates_steea

        if id and not where:
            where = f'id="{id}"'

        return bxorm_mates_steea(
            dbase = self.core.dbase,
            where = where,
        )


    #$$ def estimate
    def estimate(self, data, V_x_Q=True, V_x_min=0.1):
        # macierz -j zmiennych losowych
        # x = np.array([310,353,270,310]*MPa)
        x = data

        # liczba wyników badań lub symulacji numerycznych
        n = len(x)

        # wartość obliczeniowa współczynnika konwersji
        # jeśli nie jest on zawarty w współczynniku częściowym γ_M
        η_d = 1 # TODO

        # wspolczynnik rozkladu nieznany
        if V_x_Q is False:
            k_n = np.interp(
                n,
                [3   ,4   ,5   ,6   ,8,10  ,20  ,30  ,1000],
                [3.37,2.36,2.33,2.18,2,1.92,1.76,1.73,1.64],
            )

            k_d_n = np.interp(
                n,
                [4   ,5   ,6   ,8   ,10  ,20  ,30  ,1000],
                [11.4,7.85,6.36,5.07,4.51,3.64,3.44,3.04],
            )

        # wspolczynnik rozkladu znany
        elif V_x_Q is True:
            k_n = np.interp(
                n,
                [1   ,2   ,3   ,4   ,5   ,6   ,8   ,10  ,20  ,30  ,1000],
                [2.31,2.01,1.89,1.83,1.80,1.77,1.47,1.72,1.68,1.67,1.64],
            )

            k_d_n = np.interp(
                n,
                [1   ,2   ,3   ,4   ,5   ,6   ,8   ,10  ,20  ,30  ,1000],
                [4.36,3.77,3.56,3.44,3.37,3.33,3.27,3.23,3.16,3.13,3.04],
            )

        # średnia z próby n wyników
        m_y = (sum(ln(x_i.d('MPa')) for x_i in x))*MPa / n

        # współczynnik obliczeniowy przypisany kwantylowi wartości charakterystycznej
        s_y = max(0.1*MPa, sqrt(1/(n-1) * sum([(ln(x_i.d('MPa'))*MPa - m_y)**2 for x_i in x])))


        # D7.2 Oszacowanie wartości charakterystycznych
        f_k = η_d * exp((m_y - k_n*s_y).d('MPa'))*MPa

        # D7.3 Bezpośrednie oszacowanie wartości obliczeniowych do sprawdzania stanów granicznych nośności ULS
        f_d = η_d * exp((m_y - k_d_n * s_y).d('MPa'))*MPa

        return {
            'k_n'     : k_n,
            'k_d'     : k_d_n,
            'm_y'     : m_y.s('MPa'),
            's_y'     : s_y.s('MPa'),
            'f_k'     : f_k.s('MPa'),
            'f_d'     : f_d.s('MPa'),
            'γ_m'     : f_k / f_d,
        }
