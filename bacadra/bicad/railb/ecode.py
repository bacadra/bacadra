'''
------------------------------------------------------------------------------
BCDR += ***** (e)uro(code) EN 1990+A2 & EN 1991-2 *****
==============================================================================

------------------------------------------------------------------------------
Copyright (C) 2018 <bacadra@gmail.com> <https://github.com/bacadra/bacadra>
Team members developing this package:
    - Sebastian Balcerowiak <asiloisad> <asiloisad.93@gmail.com>
------------------------------------------------------------------------------
'''

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

from ...cunit import cunit

m  = cunit(1, 'm')
Hz = cunit(1, 'Hz')
t  = cunit(1, 't' )
yr = cunit(1, 'yr')


#$ class ecode
class ecode:
    #$$ def --init--
    def __init__(self, core=None):
        self.core = core

    @staticmethod
    def dz_limit(L):
        '''
        Pionowe przemieszczenie przęsła należy sprawdzać dla obciążenia sklasyfikowanego LM71 bez uwzględnienia współczynnika dynamicznego.
        '''
        return L / 600


    @staticmethod
    def dz_comfort(L, v, span, comfort='very_good'):
        '''
        Limitation of deflection due to passenger comfort
        ------------------------------------------------------------------------
        References: Eurocode (EN)  EN1990/A1:2006 A2.4.4.3.2
        ------------------------------------------------------------------------
        - At each design cross-section, for each rail track, the following criterion is checked.

        Symbols:
        - dz_comfort - Deflection of the bridge at the track centreline,
        - L          - Length of the span in which the cross-section is located
        - v          - Considered speed.
        - span       - construction type.
        - comfort    - passenger comfort level.

        ------------------------------------------------------------------------
        PL:
        Ugięcia pionowe δ powinny być określone na podstawie modelu obciążenia 71 mnożonego przez Współczynnik φ oraz z wartością α=1. W przypadku mostów dwu- lub więcej torowych powinien być obciążany tylko jeden tor.
        '''

        # drop cunit
        if type(L) is cunit: L = L.d('m')
        if type(v) is cunit: v = v.d('km hr**-1')

        # catch exception
        if L >= 120:
            raise ValueError('(6) Wartości L/δ podane na rysunku A2.3 są miarodajne w przypadku długości przęseł do 120 m. W przypadku dłuższych przęseł niezbędna jest specjalna analiza.')


        # if-block comfort level
        if   comfort == 'very_good'    : comfort = 1.0
        elif comfort == 'good'         : comfort = 1.3
        elif comfort == 'acceptable'   : comfort = 2.0


        # pojedyncze przęsła lub układ dwóch belek swobodnie podpartych lub dwa przęsła w układzie ciągłym
        if   1 <= span <= 2:
            span = 0.7

        # trzy lub więcej przęseł w układzie ciągłym
        elif 3 <= span:
            span = 0.7

        # szereg belek swobodnie podpartych z co najmniej 3 przęsłami
        elif span ==0:
            span = 1.0

        # 1st interpolation datas
        v_100 = np.array([[600 ,0],[600 ,120]])
        v_120 = np.array([[800 ,0],[800 ,10 ],[900 ,22],[600,35 ],[600,120]])
        v_160 = np.array([[900 ,0],[900 ,12 ],[1200,29],[600,63 ],[600,120]])
        v_200 = np.array([[1000,0],[1000,14 ],[1550,37],[600,90 ],[600,120]])
        v_220 = np.array([[1200,0],[1200,17 ],[170 ,40],[600,102],[600,120]])

        # 2st interpolated data
        P = np.array([
            [  0, np.interp(L, v_100[:,1], v_100[:,0])],
            [100, np.interp(L, v_100[:,1], v_100[:,0])],
            [120, np.interp(L, v_120[:,1], v_120[:,0])],
            [160, np.interp(L, v_160[:,1], v_160[:,0])],
            [200, np.interp(L, v_200[:,1], v_200[:,0])],
            [220, np.interp(L, v_220[:,1], v_220[:,0])],
        ])

        # base limit value
        Lpδ = np.interp(v, P[:,0], P[:,1])

        # deflection limit
        dz_Rd = L / max(600, Lpδ * span / comfort) * cunit('m')

        return dz_Rd

    @staticmethod
    def ttorb(v):
        '''
        Track twist on railway bridges
        ------------------------------------------------------------------------
        References:  Eurocode  EN1990/A1:2006 A2.4.4.2.2
        ------------------------------------------------------------------------
        - At each design cross-section of railways bridges, for each rail track, the following criterion is checked.

        '''

        pass


    @staticmethod
    def vibration_limit(n_0, L_T, name):

        def n_0_up(L_T):
            return 94.76*(L_T/m)**(-0.748) * Hz

        def n_0_low(L_T):
            if 1*m <= L_T <= 20*m:
                return 80/(L_T/m) * Hz
            elif 20*m < L_T <= 100*m:
                return 23.58 * (L_T/m)**(-0.592) * Hz

        def fig_sett(name):
            mpl.style.use('default')

            plt.axis([1,100,1,100])
            plt.grid(True, which='both') #axis=['x','y','both']
            plt.xscale('log')
            plt.yscale('log')

            # plt.locator_params(nbins=20, axis='x')
            # plt.locator_params(nbins=10, axis='y')
            plt.minorticks_on()
            # plt.title('Wykres wartości')
            plt.xlabel('Rozpiętość teoretyczna obiektu [m]')
            plt.ylabel('Częstość drgań własnych [Hz]')
            plt.rcParams['font.family'] = 'Times New Roman'
            plt.rcParams['font.size'] = 10
            plt.axhline(y=0, linewidth=1, color='0', linestyle='-')
            plt.axvline(x=0, linewidth=1, color='0', linestyle='-')
            # plt.legend(loc='lower right', frameon=True, shadow=True, facecolor='1')

            # print settings
            plt.tight_layout()
            plt.savefig(name, dpi = 300)

        def fig(n_0, name):
            # data settings
            L = np.arange(1*m,100*m,1*m)
            fn_0_up = np.array([n_0_up(L_T=L0) for L0 in L])
            fn_0_low = np.array([n_0_low(L_T=L0) for L0 in L])

            # style settings
            plt.figure(figsize=(7, 3))
            plt.plot(L, fn_0_up, linewidth=3.0, label='linia')
            plt.plot(L, fn_0_low, linewidth=3.0, label='linia')
            plt.plot([L_T], [n_0], 'ro')
            fig_sett(name)


        fig(n_0, name)


    @staticmethod
    def φ_dyn(mode, L_φ):
        if mode.lower() == 'clea':
            φ = 1.44/((L_φ/m)**0.5-0.2)+0.85
            return min(max(φ,1.0),1.67)

        elif mode.lower() == 'stan':
            φ = 2.16/((L_φ/m)**0.5-0.2)+0.73
            return min(max(φ,1.0),2.00)


    @staticmethod
    def fatigue(L_φ, L_w, σ_p_max, Δσ_c, σ_p_min=0):
        '''
        Przy określaniu Å, krytyczną długość linii Wpłyvvu przyjmuje się jak następuje:
        dla momentów:
        - dla przęseł swobodnie podpartych, rozpiętość przęsła L,;
        dla przęseł ciągłych W przekroju środkowym, patrz Rysunek 9.7, rozpiętość rozważanego przęsła L,;
        dla przęseł ciągłych W przekrojach podporowych, patrz Rysunek 9.7, średnia z dwóch rozpiętości L, IL,-
        przyiegłych do podpory;
        - dla dżwigarów poprzecznych, podpierających podkłady szynowe (lub belki podłużne), suma rozpiętości
        dwóch przyległych przęseł bezpośrednio przylegających do dżwigara poprzecznego;
        - dla płyty pomostu opartej tylko na dżwigarach poprzecznych lub żebrach poprzecznych (bez elementów
        podłużnych) i dla tych poprzecznych elementów podparcia, długość linii Wpływowej do ugięć (z pominię-
        ciem jakiejkolwiek części ugięcia ku górze), uwzględniając przy rozdziale obciążeń sztywność szyn. Dla
        elementów poprzecznych o rozstawie większym niż 750 mm, można przyjąć 2 krotną rozpiętość elementu
        poprzecznego + 3 m.

        dla ścinania W przęsłach swobodnie podpartych i ciągłych:
        W przekroju podporowym, patrz Rysunek 9.7, rozważana rozpiętość L,;
        W przekroju środkowym, patrz Rysunek 9.7, 0,4 × rozważana rozpiętość L,.
        '''

        γ_Ff = 1.0

        # +współczynnik zniszczenia elementu duży
        # +metoda tolerowanych uszkodzeń
        γ_Mf = 1.15

        # współczynnik dynamiczny równoważny uszkodzenia na skutek uderzenia.
        φ_2 = min(max(1.44/((L_φ/m)**0.5-0.2)+0.85,1.0),1.67)


        # Współczynnik, wyrażający efekt uszkodzenia od ruchu, zależny od długości linii wpływu;
        λ_1_type = 'EC_MIX'
        if λ_1_type == 'EC_MIX':
            λ_1 = np.interp(
                L_w.d('m'),
                np.array([0.5,1.0,1.5,2.0,2.5,3.0,3.5,4.0,4.5,5.0,6,7,8,9,10,12.5,15,17.5,20,25,30,35,40,45,50,60,70,80,90,100]),
                np.array([1.60,1.60,1.60,1.46,1.38,1.35,1.17,1.07,1.02,1.03,1.03,0.97,0.92,0.88,0.85,0.82,0.76,0.70,0.67,0.66,0.65,0.64,0.64,0.64,0.63,0.63,0.62,0.61,0.61,0.60]),
            )

        q_w = 25*10**6*t/yr

        # Współczynnik wyrażający wpływ natężenia ruchu;
        λ_2 = np.interp(
            q_w.drop('t yr**-1'),
            [5,10,15,20,25,30,35,40,50],
            [0.72,0.83,0.90,0.96,1,1.04,1.07,1.10,1.15],
        )

        t_life = 100*yr

        # Współczynnik wyrażający wpływ okresu użytkowania mostu;
        λ_3 = np.interp(
            t_life.d('yr'),
            [50,60,70,80,90,100,120],
            [0.87,0.90,0.93,0.96,0.98,1.00,1.04],
        )

        σ1pσ12 = 1.00

        # współczynnik stosowany W elementach konstrukcyjnych obciążonych na więcej niż jednym torze;
        λ_4 = np.interp(
            σ1pσ12,
            [0.50,0.60,0.70,0.80,0.90,1.00],
            [0.71,0.72,0.77,0.84,0.91,1.00],
        )

        # maksymalna Wartość /I uwzględniająca granicę zmęczenia, patrz (9).
        λ_max = 1.40

        # współczynnik równoważności uszkodzenia określony W 9.5
        λ = min(λ_1 * λ_2 * λ_3 * λ_4 , λ_max)

        # Zakres naprężenia odniesienia A0,, do określania spektrum (widma) efektów uszkodzeń na skutek naprężeń oblicza się z wzoru
        Δσ_p = abs(σ_p_max - σ_p_min)

        # Efekty uszkodzeń na skutek spektrum zakresu naprężenia można przedstawić za pomocą równoważnego zakresu naprężenia odniesionego do 2 ×1O6 cykli
        Δσ_E2=λ*φ_2*Δσ_p

        # Ocenę zmęczenia należy przeprowadzić jak następuje
        γ_Ff * Δσ_E2 <= Δσ_c/γ_Mf

        util = (γ_Ff * Δσ_E2)/(Δσ_c/γ_Mf)

        return {
            'φ_2':φ_2,
            'λ':λ,
            'Δσ_E2':Δσ_E2,
            'Δσ_c':Δσ_c,
            'util':util.s('%')
        }