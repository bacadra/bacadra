'''
------------------------------------------------------------------------------
***** Structural (stee)l *****
==============================================================================

------------------------------------------------------------------------------
Copyright (C) 2018 <bacadra@gmail.com> <https://github.com/bacadra>
Team members developing this package:
+ Sebastian Balcerowiak <asiloisad> <asiloisad.93@gmail.com>
------------------------------------------------------------------------------
'''

import numpy as np

from ...dbase import parse
from ...tools.setts import settsmeta
from ...tools.mdata import mdata
from ...cunit.cunit import cunit

from ...cunit.si    import kN
from ...cunit.cmath import ln,sqrt,exp


#$ ____ class setts ________________________________________________________ #

class setts(settsmeta):
    _ldef_id = None

#$ ____ class steea ________________________________________________________ #

class steea:
    a = kN+15*kN

    # class setts
    setts = setts('setts', (setts,), {})

#$$ ________ def __init__ __________________________________________________ #

    def __init__(self, core):

        # project object
        self.core = core

        # local setts
        self.setts = self.setts('setts',(),{})

#$$ ________ def add _______________________________________________________ #

    def add(self,
    id     = None  , ρ_o   = 7850 , E_1 = 210e9  , v_1  = 0.30 , G_1  = None ,
    t_e    = 1.2e-5, ttl   = None ,
    family = None  , grade = None , t_max = None , f_yk = None , f_uk = None ,
    E_a    = None  , ε_yk  = None , ε_uk  = None , γ_M0 = None , γ_M1 = None ,
    γ_M2   = None  , γ_M3  = None , γ_M4  = None , γ_M5 = None , γ_M6 = None ,
    ):

        table  = '011:mates:umate'
        id     = parse.chdr(table , 'id'     , id     )
        ρ_o    = parse.chdr(table , 'ρ_o'    , ρ_o    )
        E_1    = parse.chdr(table , 'E_1'    , E_1    )
        v_1    = parse.chdr(table , 'v_1'    , v_1    )
        G_1    = parse.chdr(table , 'G_1'    , G_1    )
        t_e    = parse.chdr(table , 't_e'    , t_e    )
        ttl    = parse.chdr(table , 'ttl'    , ttl    )

        table  = '013:mates:steea'
        id     = parse.chdr(table , 'id'     , id     )
        family = parse.chdr(table , 'family' , family )
        grade  = parse.chdr(table , 'grade'  , grade  )
        t_max  = parse.chdr(table , 't_max'  , t_max  )
        f_yk   = parse.chdr(table , 'f_yk'   , f_yk   )
        f_uk   = parse.chdr(table , 'f_uk'   , f_uk   )
        E_a    = parse.chdr(table , 'E_a'    , E_a    )
        ε_yk   = parse.chdr(table , 'ε_yk'   , ε_yk   )
        ε_uk   = parse.chdr(table , 'ε_uk'   , ε_uk   )
        γ_M0   = parse.chdr(table , 'γ_M0'   , γ_M0   )
        γ_M1   = parse.chdr(table , 'γ_M1'   , γ_M1   )
        γ_M2   = parse.chdr(table , 'γ_M2'   , γ_M2   )
        γ_M3   = parse.chdr(table , 'γ_M3'   , γ_M3   )
        γ_M4   = parse.chdr(table , 'γ_M4'   , γ_M4   )
        γ_M5   = parse.chdr(table , 'γ_M5'   , γ_M5   )
        γ_M6   = parse.chdr(table , 'γ_M6'   , γ_M6   )

        # resolve Young module
        if   not E_1 and E_a: E_1 = E_a
        elif not E_a and E_1: E_a = E_1

        # overwrite last defined material
        self.setts._ldef_id = id

        # add universal material
        self.core.mates.umate.add(id=id, ρ_o=ρ_o, E_1=E_1, v_1=v_1, G_1=G_1, t_e=t_e, ttl=ttl, subcl='steea')

        # add steea material
        self.core.dbase.add(
            mode  = 'r',
            table = ['013:mates:steea'],
            cols  = ['id','family','grade','t_max','f_yk','f_uk','E_a','ε_yk',
                     'ε_uk','γ_M0','γ_M1','γ_M2','γ_M3','γ_M4','γ_M5','γ_M6'],
            data  =
                [id,family,grade,t_max,f_yk,f_uk,E_a,ε_yk,
                ε_uk,γ_M0,γ_M1,γ_M2,γ_M3,γ_M4,γ_M5,γ_M6],
        )


    # def sample(self, family, grade):





#$$ ________ def estimate __________________________________________________ #

    def estimate(self, f_y=None, f_u=None, V_x_Q=True, V_x_min=0.1):

        def est1(data):
            # macierz -j zmiennych losowych
            # x = np.array([310,353,270,310]*MPa)
            x = data

            # liczba wyników badań lub symulacji numerycznych
            n = len(x)

            # wartość obliczeniowa współczynnika konwersji
            # jeśli nie jest on zawarty w współczynniku częściowym γ_M
            η_d = 1

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
            m_y = (sum(ln(x_i.d('MPa')) for x_i in x))*cunit(1,'MPa') / n

            # współczynnik obliczeniowy przypisany kwantylowi wartości charakterystycznej
            s_y = max(
                V_x_min*cunit(1,'MPa'),

                sqrt(1/(n-1)*sum([(ln(x_i.d('MPa'))*cunit(1,'MPa')-m_y)**2
                    for x_i in x]))
                )

            # D7.2 Oszacowanie wartości charakterystycznych
            f_k = η_d * exp((m_y - k_n*s_y).d('MPa'))*cunit(1,'MPa')

            # D7.3 Bezpośrednie oszacowanie wartości obliczeniowych do sprawdzania stanów granicznych nośności ULS
            f_d = η_d * exp((m_y - k_d_n * s_y).d('MPa'))*cunit(1,'MPa')



            return mdata({
                'data'    : data,
                'len'     : len(data),
                'η_d'     : η_d,
                'k_n'     : k_n,
                'k_d'     : k_d_n,
                'm_y'     : m_y.s('MPa'),
                's_y'     : s_y.s('MPa'),
                'f_k'     : f_k.s('MPa'),
                'f_d'     : f_d.s('MPa'),
                'γ_m'     : f_k / f_d,
                'V_x_min' : V_x_min,
            })

        obj = mdata({
            'f_y':  est1(f_y),
            'f_u':  est1(f_u),
        })

        obj.max = mdata({
            'γ_m': max(obj.f_y.γ_m, obj.f_y.γ_m)
        })

        return obj


#$$ ________ def echo ______________________________________________________ #

    def echo(self, mode='a+', where=None, label=None):

        if 'a' in mode:
            data = self.core.dbase.get(
                mode  = 'm',
                table = '[013:mates:steea]',
                cols  = '[id],[grade],[t_max],[f_yk],[f_uk],[E_a],[ε_yk],[ε_uk],[γ_M0],[γ_M1],[γ_M2],[γ_M3],[γ_M4],[γ_M5],[γ_M6]',
                where = where,
            )

            caption = self.core.tools.clang(
                en = 'Structural steel properties',
                pl = 'Parametry stali konstrukcyjnej',
            )

            out = self.core.pinky.rstme.table(
                caption = None if 'x' in mode else caption,
                wrap    = [False,False,False,False,False],
                width   = [True,True,True,True,True],
                halign  = ['l','c','c','c','c'],
                valign  = ['u','u','u','u','u'],
                dtype   = ['t','e','e','e','e'],
                header  = [
                    ['id','grade','t_max'],
                    ['f_yk','f_uk','E_a'],
                    ['ε_yk','ε_uk','γ_M0'],
                    ['γ_M1','γ_M2','γ_M3'],
                    ['γ_M4','γ_M5','γ_M6']
                ],
                data    = [[
                    [row['id'],row['grade'],row['t_max']],
                    [row['f_yk'],row['f_uk'],row['E_a']],
                    [row['ε_yk'],row['ε_uk'],row['γ_M0']],
                    [row['γ_M1'],row['γ_M2'],row['γ_M3']],
                    [row['γ_M4'],row['γ_M5'],row['γ_M6']],
                ] for row in data],
                precision = 2,
                inherit = True if 'x' in mode else False,
            )

            if 'x' in mode:
                self.core.pinky.texme.code(
                    caption=caption, code=out, rst=True, label=None,strip=False)