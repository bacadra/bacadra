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

from ...cunit import cunit


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
