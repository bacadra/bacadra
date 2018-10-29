import numpy  as np
import pandas as pd

from ..pinky.pinky import pinky
from ..cunit.ce import *
from ..cunit.cmath import *
from  .            import shape

class spile:
    '''
    PN-B-02482 1983
    '''

    # bore profile
    bore  = None

    # pile tehcnology
    ptech = '2'

    # pile head's level in bore ucs
    z_0   = 0

    # total length of pile
    L     = 10*m

    # uniform diamater of pile
    D     = 0.4*m

    '''
    1a - Pale prefabrykowane żelbetowe wbijane
    1b - Pale prefabrykowane żelbetowe wpłukiwane (ostatni 1 m wbijany)
    2  - Franki
    '''




    def __init__(self, bore=None, z_0=None, ptech=None, L=None, D=None):
        self.tex  = pinky(scope=locals())
        self.tex.display=False
        self.bore  = bore  if bore  is not None else spile.bore
        self.z_0   = z_0   if z_0   is not None else spile.z_0
        self.ptech = ptech if ptech is not None else spile.ptech
        self.L     = L     if L     is not None else spile.L
        self.D     = D     if D     is not None else spile.D


    def techfact(self, lay):
        I_D = lay.I_D
        I_L = lay.I_L
        # wybor technologii pali i jego zestawu wspolczynnikow
        if self.ptech in ('1a'):
            if I_D:
                if I_D >= 0.67:          S_p, S_s, S_w = 1.0, 1.0, 0.6
                elif 0.67 > I_D >= 0.20: S_p, S_s, S_w = 1.1, 1.1, 0.6
                else:                    S_p, S_s, S_w = 0,     0,   0
            if I_L:
                if I_L <= 0:             S_p, S_s, S_w = 1.0, 1.0, 0.6
                elif 0 < I_L <= 0.75:    S_p, S_s, S_w = 1.1, 1.1, 0.6
                else:                    S_p, S_s, S_w = 0,     0,   0

        elif self.ptech in ('1b'):
            if I_D:
                if I_D >= 0.67:          S_p, S_s, S_w = 1.0, 0.8, 0.4
                elif 0.67 > I_D >= 0.20: S_p, S_s, S_w = 1.0, 0.8, 0.4
                else:                    S_p, S_s, S_w =   0,   0,   0
            if I_L:
                if I_L <= 0:             S_p, S_s, S_w = 1.0, 1.0, 0.7
                elif 0 < I_L <= 0.75:    S_p, S_s, S_w = 1.0, 0.9, 0.6
                else:                    S_p, S_s, S_w =   0,   0,   0

        elif self.ptech in ('1c'):
            if I_D:
                if I_D >= 0.67:          S_p, S_s, S_w =   0,   0,   0
                elif 0.67 > I_D >= 0.20: S_p, S_s, S_w = 1.0, 0.8, 0.5
                else:                    S_p, S_s, S_w =   0,   0,   0
            if I_L:
                if I_L <= 0:             S_p, S_s, S_w =   0,   0,   0
                elif 0 < I_L <= 0.75:    S_p, S_s, S_w =   0,   0,   0
                else:                    S_p, S_s, S_w =   0,   0,   0

        elif self.ptech in ('2'):
            if I_D:
                if I_D >= 0.67:          S_p, S_s, S_w = 1.3, 1.1, 1.0
                elif 0.67 > I_D >= 0.20: S_p, S_s, S_w = 1.8, 1.6, 1.0
                else:                    S_p, S_s, S_w = 0, 0,0
            if I_L:
                if I_L <= 0:             S_p, S_s, S_w = 1.2, 1.1, 0.8
                elif 0 < I_L <= 0.75:    S_p, S_s, S_w = 1.1, 1.0, 0.7
                else:                    S_p, S_s, S_w = 0,0,0

        elif self.ptech in ('3'):
            if I_D:
                if I_D >= 0.67:          S_p, S_s, S_w = 1.1, 1.0, 0.6
                elif 0.67 > I_D >= 0.20: S_p, S_s, S_w = 1.4, 1.1, 0.6
                else:                    S_p, S_s, S_w = 0,0,0
            if I_L:
                if I_L <= 0:             S_p, S_s, S_w = 1.0, 1.0, 0.6
                elif 0 < I_L <= 0.75:    S_p, S_s, S_w = 1.0, 0.9, 0.6
                else:                    S_p, S_s, S_w = 0,0,0

        elif self.ptech in ('4a'):
            if I_D:
                if I_D >= 0.67:          S_p, S_s, S_w = 1.0, 0.8, 0.7
                elif 0.67 > I_D >= 0.20: S_p, S_s, S_w = 1.0, 0.9, 0.7
                else:                    S_p, S_s, S_w = 0,0,0
            if I_L:
                if I_L <= 0:             S_p, S_s, S_w = 1.0, 0.9, 0.6
                elif 0 < I_L <= 0.75:    S_p, S_s, S_w = 1.0, 0.9, 0.6
                else:                    S_p, S_s, S_w = 0,0,0

        elif self.ptech in ('4b'):
            if I_D:
                if I_D >= 0.67:          S_p, S_s, S_w = 1.0, 0.8, 0.6
                elif 0.67 > I_D >= 0.20: S_p, S_s, S_w = 1.0, 0.8, 0.6
                else:                    S_p, S_s, S_w = 0,0,0
            if I_L:
                if I_L <= 0:             S_p, S_s, S_w = 1.0, 0.8, 0.6
                elif 0 < I_L <= 0.75:    S_p, S_s, S_w = 1.0, 0.8, 0.5
                else:                    S_p, S_s, S_w = 0,0,0

        elif self.ptech in ('4c'):
            if I_D:
                if I_D >= 0.67:          S_p, S_s, S_w = 1.0, 1.0, 0.7
                elif 0.67 > I_D >= 0.20: S_p, S_s, S_w = 1.0, 1.1, 0.7
                else:                    S_p, S_s, S_w = 0,0,0
            if I_L:
                if I_L <= 0:             S_p, S_s, S_w = 1.0, 1.0, 0.7
                elif 0 < I_L <= 0.75:    S_p, S_s, S_w = 1.0, 1.0, 0.6
                else:                    S_p, S_s, S_w = 0,0,0

        elif self.ptech in ('4d'):
            if I_D:
                if I_D >= 0.67:          S_p, S_s, S_w = 1.0, 1.0, 0.7
                elif 0.67 > I_D >= 0.20: S_p, S_s, S_w = 1.0, 1.0, 0.7
                else:                    S_p, S_s, S_w = 0,0,0
            if I_L:
                if I_L <= 0:             S_p, S_s, S_w = 0,0,0
                elif 0 < I_L <= 0.75:    S_p, S_s, S_w = 1.0, 0.9,0.5
                else:                    S_p, S_s, S_w = 0,0,0

        elif self.ptech in ('4e'):
            if I_D:
                if I_D >= 0.67:          S_p, S_s, S_w = 1.0, 1.0, 0.7
                elif 0.67 > I_D >= 0.20: S_p, S_s, S_w = 1.0, 1.0, 0.7
                else:                    S_p, S_s, S_w = 0,0,0
            if I_L:
                if I_L <= 0:             S_p, S_s, S_w = 0,0,0
                elif 0 < I_L <= 0.75:    S_p, S_s, S_w = 0,0,0
                else:                    S_p, S_s, S_w = 0,0,0

        elif self.ptech in ('4f'):
            if I_D:
                if I_D >= 0.67:          S_p, S_s, S_w = 1.0, 0.8, 0.6
                elif 0.67 > I_D >= 0.20: S_p, S_s, S_w = 1.0, 0.9, 0.6
                else:                    S_p, S_s, S_w = 0,0,0
            if I_L:
                if I_L <= 0:             S_p, S_s, S_w = 1.0, 0.9, 0.6
                elif 0 < I_L <= 0.75:    S_p, S_s, S_w = 1.0, 0.8, 0.5
                else:                    S_p, S_s, S_w = 0,0,0

        elif self.ptech in ('5a'):
            if I_D:
                if I_D >= 0.67:          S_p, S_s, S_w = 0.8,0.6,0.4
                elif 0.67 > I_D >= 0.20: S_p, S_s, S_w = 0.9,0.7,0.5
                else:                    S_p, S_s, S_w = 0,0,0
            if I_L:
                if I_L <= 0:             S_p, S_s, S_w = 0,0,0
                elif 0 < I_L <= 0.75:    S_p, S_s, S_w = 0,0,0
                else:                    S_p, S_s, S_w = 0,0,0

        elif self.ptech in ('5b'):
            if I_D:
                if I_D >= 0.67:          S_p, S_s, S_w = 0.8,0.6,0.4
                elif 0.67 > I_D >= 0.20: S_p, S_s, S_w = 0.9,0.7,0.5
                else:                    S_p, S_s, S_w = 0,0,0
            if I_L:
                if I_L <= 0:             S_p, S_s, S_w = 0,0,0
                elif 0 < I_L <= 0.75:    S_p, S_s, S_w = 0,0,0
                else:                    S_p, S_s, S_w = 0,0,0

        elif self.ptech in ('5c'):
            if I_D:
                if I_D >= 0.67:          S_p, S_s, S_w = 0.8,0.7,0.5
                elif 0.67 > I_D >= 0.20: S_p, S_s, S_w = 0.9,0.8,0.5
                else:                    S_p, S_s, S_w = 0,0,0
            if I_L:
                if I_L <= 0:             S_p, S_s, S_w = 0,0,0
                elif 0 < I_L <= 0.75:    S_p, S_s, S_w = 0,0,0
                else:                    S_p, S_s, S_w = 0,0,0

        elif self.ptech in ('5d'):
            if I_D:
                if I_D >= 0.67:          S_p, S_s, S_w = 1.0, 1.0, 0.7
                elif 0.67 > I_D >= 0.20: S_p, S_s, S_w = 1.0, 1.0, 0.7
                else:                    S_p, S_s, S_w = 0,0,0
            if I_L:
                if I_L <= 0:             S_p, S_s, S_w = 0,0,0
                elif 0 < I_L <= 0.75:    S_p, S_s, S_w = 0,0,0
                else:                    S_p, S_s, S_w = 0,0,0

        elif self.ptech in ('5e'):
            if I_D:
                if I_D >= 0.67:          S_p, S_s, S_w = 1.0, 1.0, 0.7
                elif 0.67 > I_D >= 0.20: S_p, S_s, S_w = 1.0, 1.0, 0.7
                else:                    S_p, S_s, S_w = 0,0,0
            if I_L:
                if I_L <= 0:             S_p, S_s, S_w = 0,0,0
                elif 0 < I_L <= 0.75:    S_p, S_s, S_w = 0,0,0
                else:                    S_p, S_s, S_w = 0,0,0

        elif self.ptech in ('5f'):
            if I_D:
                if I_D >= 0.67:          S_p, S_s, S_w = 0.8,0.6,0.5
                elif 0.67 > I_D >= 0.20: S_p, S_s, S_w = 0.9,0.7,0.5
                else:                    S_p, S_s, S_w = 0,0,0
            if I_L:
                if I_L <= 0:             S_p, S_s, S_w = 0,0,0
                elif 0 < I_L <= 0.75:    S_p, S_s, S_w = 0,0,0
                else:                    S_p, S_s, S_w = 0,0,0

        elif self.ptech in ('6a'):
            if I_D:
                if I_D >= 0.67:          S_p, S_s, S_w = 0,0,0
                elif 0.67 > I_D >= 0.20: S_p, S_s, S_w = 1.1,1.0,0.5
                else:                    S_p, S_s, S_w = 0,0,0
            if I_L:
                if I_L <= 0:             S_p, S_s, S_w = 1.0,1.1,0.5
                elif 0 < I_L <= 0.75:    S_p, S_s, S_w = 1.0,0.9,0.5
                else:                    S_p, S_s, S_w = 0,0,0

        elif self.ptech in ('6b'):
            if I_D:
                if I_D >= 0.67:          S_p, S_s, S_w = 1.0,0.7,0.4
                elif 0.67 > I_D >= 0.20: S_p, S_s, S_w = 1.0,0.6,0.4
                else:                    S_p, S_s, S_w = 0,0,0
            if I_L:
                if I_L <= 0:             S_p, S_s, S_w = 0,0,0
                elif 0 < I_L <= 0.75:    S_p, S_s, S_w = 0,0,0
                else:                    S_p, S_s, S_w = 0,0,0

        elif self.ptech in ('6c'):
            if I_D:
                if I_D >= 0.67:          S_p, S_s, S_w = 0,0,0
                elif 0.67 > I_D >= 0.20: S_p, S_s, S_w = 1.0,0.8,0.5
                else:                    S_p, S_s, S_w = 0,0,0
            if I_L:
                if I_L <= 0:             S_p, S_s, S_w = 0,0,0
                elif 0 < I_L <= 0.75:    S_p, S_s, S_w = 0,0,0
                else:                    S_p, S_s, S_w = 0,0,0

        elif self.ptech in ('7a'):
            if I_D:
                if I_D >= 0.67:          S_p, S_s, S_w = 1.0,0.8,0.5
                elif 0.67 > I_D >= 0.20: S_p, S_s, S_w = 1.0,0.9,0.5
                else:                    S_p, S_s, S_w = 0,0,0
            if I_L:
                if I_L <= 0:             S_p, S_s, S_w = 1.0,1.0,0.5
                elif 0 < I_L <= 0.75:    S_p, S_s, S_w = 1.0,0.9,0.5
                else:                    S_p, S_s, S_w = 0,0,0

        elif self.ptech in ('7b'):
            if I_D:
                if I_D >= 0.67:          S_p, S_s, S_w = 1.0,0.5,0.3
                elif 0.67 > I_D >= 0.20: S_p, S_s, S_w = 1.0,0.6,0.3
                else:                    S_p, S_s, S_w = 0,0,0
            if I_L:
                if I_L <= 0:             S_p, S_s, S_w = 0,0,0
                elif 0 < I_L <= 0.75:    S_p, S_s, S_w = 0,0,0
                else:                    S_p, S_s, S_w = 0,0,0

        elif self.ptech in ('7c'):
            if I_D:
                if I_D >= 0.67:          S_p, S_s, S_w = 0,0,0
                elif 0.67 > I_D >= 0.20: S_p, S_s, S_w = 1.0,0.7,0.4
                else:                    S_p, S_s, S_w = 0,0,0
            if I_L:
                if I_L <= 0:             S_p, S_s, S_w = 0,0,0
                elif 0 < I_L <= 0.75:    S_p, S_s, S_w = 0,0,0
                else:                    S_p, S_s, S_w = 0,0,0



        return S_p, S_s, S_w


    # funkcja nosnosci podstawy pala w zaleznosci od gruntu
    def N_p(self):
        lay = self.bore.get(self.z_0 + self.L)
        self.tex.i('warstwa gruntu, na której opiera się podstawa pala',
            'lay = @_1@', scope={'_1':lay.soil}, inherit='q_base.lay')

        h_0 = 10*m
        self.tex.item('glebokość porównawcza',
            'h_0 = @_1@', scope={'_1':h_0}, inherit='q_base.h_0')

        D_0 = 0.4*m
        self.tex.item('średnica porównawcza',
            'D_0 = @_1@', scope={'_1':D_0}, inherit='q_base.D_0')

        # modyfikacja nosnosci podloza ze wzgledu na srednice pala
        q_p = self.q_p_data(lay) * sqrt(D_0 / self.D)

        # modyfikacja glebokosci efektywnej ze wzgledu na srednice pala
        h_c = h_0 * sqrt(self.D / D_0)

        # nosnosc podloza z uwzglednieniem srednicy apala
        q_p = np.interp((self.z_0 + self.L).drop(),
                      [0, h_c     , h_c*2],
                      [0, q_p.drop(), q_p.drop()])*kPa

        return q_p


    def q_p_data(self, lay):
        soil = lay.soil
        I_D = lay.I_D
        I_L = lay.I_L

        if I_D: # jezeli jest to grunt spoisty
            I_D_range = [0.20, 0.33, 0.67, 1.00]
            if   soil in ('Ż', 'Po'):
                q_p = [1950, 3000, 5100, 7750]
            elif soil in ('Pr', 'Ps'):
                q_p = [1450, 2150, 3600, 5850]
            elif soil == 'Pd':
                q_p = [1050, 1650, 2700, 4100]
            elif soil == 'Pπ':
                q_p = [ 700, 1150, 2100, 3350]
            return np.interp(I_D, I_D_range, q_p)

        elif I_L: # jezeli jest to grunt niespoisty
            I_L_range = [-0.01, 0, 0.50, 0.75]
            if   soil in ('Żg', 'Pog'):
                q_p = [4150, 2750, 1650, 850]
            elif soil in ('Pg', 'Gp', 'G', 'Gπ'):
                q_p = [2750, 1950, 850, 450]
            elif soil in ('Gpz', 'Gz', 'Gπz', 'Ip', 'I', 'Iπ'):
                q_p = [2800, 1950, 800, 400]
            elif soil in ('πp', 'π'):
                v = [1850, 1250, 500, 250]
            return np.interp(I_L, I_L_range, q_p)


    def t_s_data(self, h_z, lay):
        if lay.I_D: # jezeli jest to grunt spoisty
            I_D_range = [0.20, 0.33, 0.67, 1.00]
            if   lay.soil in ('Ż', 'Po'):
                t_s = [59,74,110,165]
            elif lay.soil in ('Pr', 'Ps'):
                t_s = [34,47,74,132]
            elif lay.soil == 'Pd':
                t_s = [22,31,62,100]
            elif lay.soil == 'Pπ':
                t_s = [16,25,45,75]
            else:
                t_s = [0, 0, 0, 0]
            t_s = np.interp(I_D, I_D_range, t_s)
            return np.interp(h_z.drop('m'),[0, 5, 6], [0, t_s, t_s])*kPa

        elif lay.I_L: # jezeli jest to grunt niespoisty
            I_L_range = [-0.01, 0, 0.50, 0.75]
            if   lay.soil in ('Żg', 'Pog'):
                t_s = [134,95,67,44]
            elif lay.soil in ('Pg', 'Gp', 'G', 'Gπ'):
                t_s = [95,50,31,14]
            elif lay.soil in ('Gpz', 'Gz', 'Gπz', 'Ip', 'I', 'Iπ'):
                t_s = [95,50,25,11]
            elif lay.soil in ('πp', 'π'):
                t_s = [65,30,16,7]
            elif lay.soil in ('NM'):
                t_s = [48,18,0,0]
            else:
                t_s = [0, 0, 0, 0]
            t_s = np.interp(I_L, I_L_range, t_s)
            t_s = np.interp(h_z.drop('m'),[0,5, 6], [0, t_s, t_s])*kPa
            return t_s


    def N_s(self):
        N_s_sum = 0
        for lay in self.bore.range(self.z_0, self.z_0 + self.L):
            S_p, S_s, S_w = self.techfact(lay.I_D, lat.I_L)
            t_s = self.t_s_data(z=self.bore.abs_hz(lay), lay)
            N_s_sum += S_s*t_s*(π*self.D)
        return N_s_sum


    def N_t(self):
        S_p, S_s, S_w = self.techfact()
        q_r = self.q_base()
        t_s = self.t_s()
        A_p = π * (self.D)**2 * 0.25
        A_s = self.L * π * self.D
        N_p = S_p * q_r * A_p
        N_s = S_s * t_s * A_s
        N_t = N_p + N_s
        return N_t


    def N_w(self):
        N_w_sum = 0
        for lay in self.bore.range(self.z_0, self.z_0 + self.L):
            S_p, S_s, S_w = self.techfact(lay.I_D, lat.I_L)
            t_s = self.t_s_data(z=self.bore.abs_hz(lay), lay)
            N_w_sum += S_w*t_s*(π*self.D)
        return N_w_sum

    def Q_r(self, force=1*kN):
        m_f = 0.90
        if force>0:
            N_axial = self.N_t()
        else:
            N_axial = self.N_w()
        Q_r = m_f * N_axial
        return Q_r




    def make(self):
        self.tex.display = False

        self.Q_r()

        self.tex.h(1, 'Analiza nośności') #$#

        self.tex.h(2, 'Nośność podłoża gruntowego') #$$#

        self.tex.h(3, 'Nośność podstawy pala') #$$$#

        self.tex.item('obliczeniowa nośność gruntu',
            'γ_M_u = γ_M_u')

        self.tex.get('q_base.lay')
        self.tex.get('q_base.h_0')
        self.tex.get('q_base.D_0')


        self.tex.h(3, 'Nośność pobocznicy pala') #$$$#


        self.tex.h(3, 'Obliczeniowa nośność pala') #$$$#

        self.tex.item('obliczeniowa nośność pala wciskanego',
            'N_t_d = N_p + N_s = S_p * q_pd * A_p + ∑{i} S_s_i * t_d_i A_s_i')

        self.tex.item('obliczeniowa nośnoć pala wyciąganego',
            'N_w_d = ∑{i} S_w_i * t_d_i * A_s_i')

        self.tex.i('współczynnik korekcyjny nośności osiowej pala',
            'm_f = m_f')

        self.tex.i('nośność osiowa obliczeniowa pala',
            'Q_r <= m_f * N')


    #     self.tex.h(1, 'Dane') #$#
    #
    #
    #     self.tex.h(2, 'Materiały') #$$#
    #
    #
    #     self.tex.h(3, 'Beton') #$$$#
    #
    #     self.tex.i('współczynnik bezpieczeństwa',
    #         'γ_Mc = @self.γ_Mc@')
    #
    #     self.tex.i('moduł odksztacalności podłużnej (sieczny, 28 dni)',
    #         'E_cm = @self.E_cm._GPa@')
    #
    #     self.tex.i('charakterystyczna wytrzymałość na ściskanie próbki walcowej (28 dni)',
    #         'f_ck = @self.f_ck._MPa@')
    #
    #
    #     self.tex.h(3, 'Stal zbrojeniowa') #$$$#
    #
    #
    #     self.tex.h(3, 'Zasypka gruntowe') #$$$#
    #
    #
    #     self.tex.h(3, 'Podłoże gruntowe') #$$$#
    #
    #
    #     self.tex.h(2, 'Wymiary kosntrukcji') #$$#
    #
    #
    #     self.tex.h(1, 'Obciążenia') #$#

#$$ test
