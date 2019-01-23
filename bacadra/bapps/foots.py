'''
------------------------------------------------------------------------------
BCDR += ***** (f)ounding f(oots) *****
==============================================================================

------------------------------------------------------------------------------
Copyright (C) 2018 <bacadra@gmail.com> <https://github.com/bacadra>
Team members developing this package:
    - Sebastian Balcerowiak <asiloisad> <asiloisad.93@gmail.com>
------------------------------------------------------------------------------
'''


import numpy
import pandas as pd

from ..pinky.pinky import pinky
from ..cunit.ce import *
from ..cunit.cmath import *

class foot_rect:
    γ_Mc = 1.40
    E_cm = 32*GPa
    f_ck = 20*MPa
    H    = 2*m
    B    = 1*m
    γ_Ms = 1.15
    E_s  = 210*GPa
    f_sk = 500*MPa
    γ_z  = 20*kN/m**3
    ϕ_z  = 33.0*deg
    c_z  = 0*kPa
    α_z  = 0*deg
    k_z  = 0.66

    γʾ   = 22*kN/m**3
    ϕʾ   = 16.4*deg
    cʾ   = 28*kPa
    α    = 0*deg
    k    = 0.66

    B    = 2.2*m
    L    = 4.5*m
    h    = 50*cm
    e_ib = 0.25*m
    e_il = 0.10*m

    q    = 0.75*m * γ_z
    q_k  = 5*kPa

    def __init__(self, **kwargs):
        self.tex = pinky(scope=locals())
        for key, val in kwargs.items():
            self.__dict__[key] = val

    def uls_geo(self):
        δ_z  = k_z * ϕ_z
        δ    = k * ϕʾ

    def make(self):
        self.tex.h(0, 'bcdr.foot_rect') #$#
        self.tex.display = False

        self.tex.h(1, 'Dane') #$#


        self.tex.h(2, 'Materiały') #$$#


        self.tex.h(3, 'Beton') #$$$#

        self.tex.i('współczynnik bezpieczeństwa',
            'γ_Mc = @self.γ_Mc@')

        self.tex.i('moduł odksztacalności podłużnej (sieczny, 28 dni)',
            'E_cm = @self.E_cm._GPa@')

        self.tex.i('charakterystyczna wytrzymałość na ściskanie próbki walcowej (28 dni)',
            'f_ck = @self.f_ck._MPa@')


        self.tex.h(3, 'Stal zbrojeniowa') #$$$#


        self.tex.h(3, 'Zasypka gruntowe') #$$$#


        self.tex.h(3, 'Podłoże gruntowe') #$$$#


        self.tex.h(2, 'Wymiary kosntrukcji') #$$#


        self.tex.h(1, 'Obciążenia') #$#





#
#
# tex.h(1, 'Analiza statyczna układu') #$#
#
# data_path = r'reaction.dat'
# df = pd.read_csv(data_path, sep='\s+',header=None)
#
# F_Ek = df[df[0] < 20000][[2,3,4,5,6,7]]
# F_Ed = df[df[0] > 20000][[2,3,4,5,6,7]]
#
# tex.h(1, 'Analiza nośności') #$#
#
# tex.h(2, 'Podłoże gruntowe') #$$#
#
# tex.h(3, 'Wypór gruntu spod fundamentu') #$$$#
#
#
#
# def uls_geo(B,L,h,γʾ,ϕʾ,cʾ,α,F_Ek,F_Ed,q):
#     PX_Ek = abs(F_Ek[0])*kN
#     PY_Ek = abs(F_Ek[1])*kN
#     PZ_Ek = abs(F_Ek[2])*kN
#     MX_Ek = abs(F_Ek[3])*kNm
#     MY_Ek = abs(F_Ek[4])*kNm
#     MZ_Ek = abs(F_Ek[5])*kNm
#
#     PX_Ed = abs(F_Ed[0])*kN
#     PY_Ed = abs(F_Ed[1])*kN
#     PZ_Ed = abs(F_Ed[2])*kN
#     MX_Ed = abs(F_Ed[3])*kNm
#     MY_Ed = abs(F_Ed[4])*kNm
#     MZ_Ed = abs(F_Ed[5])*kNm
#
#     H  = (PX_Ek**2 + PY_Ek**2)**0.5
#
#     e_b = MY_Ek/PZ_Ek
#     e_L = MX_Ek/PZ_Ek
#     Bʾ = B - 2 * (e_b - e_ib)
#     Lʾ = L - 2 * (e_L - e_il)
#     Aʾ = Bʾ * Lʾ
#
#     N_q = e**(π * tan(ϕʾ))*(tan(45 * deg + ϕʾ / 2))**2
#     N_c = (N_q - 1) * cot(ϕʾ)
#     N_γ = 2 * (N_q - 1) * tan(ϕʾ)
#
#     b_γ = (1-α * tan(ϕʾ))**2
#     b_q = b_γ
#     b_c = b_q - (1 - b_q)/(N_c * tan(ϕʾ))
#
#     s_q = 1 + (Bʾ/Lʾ) * sin(ϕʾ)
#     s_γ = 1 - 0.3 * Bʾ/Lʾ
#     s_c = (s_q * N_q - 1)/(N_q - 1)
#
#     m_b = (2 + Bʾ/Lʾ)/(1 + Bʾ/Lʾ)
#     m_l = (2 + Lʾ/Bʾ)/(1 + Lʾ/Bʾ)
#
#     θ  = atan(PY_Ek/PX_Ek)
#     m_s  = m_l * (cos(θ))**2 + m_b * (sin(θ))**2
#
#
#     m_b
#     m_l
#     m_l
#
#     H/(PZ_Ek + Aʾ * cʾ * cot(ϕʾ))
#
#     i_q = (1 - H/(PZ_Ek + Aʾ * cʾ * cot(ϕʾ)))**(m_s)
#     i_c = i_q - (1 - i_q)/(N_c * tan(ϕʾ))
#     i_γ = (1- H/(PZ_Ek + Aʾ * cʾ * cot(ϕʾ)))**(m_s+1)
#
#     i_q
#     i_c
#     i_γ
#
#     # warunki z odplywem # nośność obliczeniowa
#     Rk = Aʾ * (cʾ * N_c * b_c * s_c * i_c + q * N_q * b_q * s_q * i_q
#         + 0.5 * γʾ * Bʾ * N_γ * b_γ * s_γ * i_γ)
#     Rk
#
#
#     γ_m = 1.4
#
#     Rd = Rk / γ_m
#
#     util = PZ_Ed / Rd
#     print('Bʾ/B=',Bʾ/B, 'Lʾ/L=',Lʾ/L, Rd.prt(1.7),PZ_Ed.prt(1.7),util.prt(2.7))
#     return util
#
#
#
# for i in range(len(F_Ed)):
#     uls_geo(B,L,h,γʾ,ϕʾ,cʾ,α,
#         F_Ek.values[i],F_Ed.values[i],q)
#
#
# tex.h(3, 'Ścięcie gruntu') #$$$#
#
# PZ_Ek = 100*kN
# PX_Ed = 20*kN
# H_d = 10*kN
#
# γ_Rh = 1.1
# R_dh = PZ_Ek * tan(δ_z) / γ_Rh * 1*m
# H_d  = PX_Ed * 1*m
#
# UTIL = H_d/R_dh
# UTIL
#
#
# tex.h(2, 'Fundament prostokątny') #$$#
#
# def uls_conc_as1_calc(B,L,h,F_Ed):
#     PZ_Ed = abs(F_Ed[2])*kN
#     MY_Ed = abs(F_Ed[4])*kNm
#     A  = B*L
#     IY = B**3*L/12
#     q_max = PZ_Ed/A + MY_Ed/IY * B/2
#     Mmax = (0.5*B * (q_max) * 0.5*B)
#     df = h - 5*cm * 2 - 20*mm
#     ξ_eff = 1 - (1 - 2*Mmax/(f_ck/1.4 * df**2))**0.5
#     ρ1=(f_ck/1.4)/(f_sk/1.15)*ξ_eff
#     A_s1 = ρ1 * df
#     print('ξ_eff=', ξ_eff, 'As1=',A_s1.convert('cm**2 m**-1'))
#
#
# for i in range(len(F_Ed)):
#     uls_conc_as1_calc(B,L,h,F_Ed.values[i])
#
# cm**2
# (0.003 * cm**2 / m * 10000).convert('cm**2')
