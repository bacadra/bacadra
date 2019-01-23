'''
------------------------------------------------------------------------------
BCDR += ***** eurocode (en) (155)28 *****
==============================================================================

------------------------------------------------------------------------------
Copyright (C) 2018 <bacadra@gmail.com> <https://github.com/bacadra>
Team members developing this package:
    - Sebastian Balcerowiak <asiloisad> <asiloisad.93@gmail.com>
------------------------------------------------------------------------------
'''


import math
import matplotlib as mpl
import matplotlib.pyplot as plt

from ...cunit import cunit
from ...cunit.system.math import exp

from ... import sofix


#$ class dfact
class dfact:
    #$$ def __init__
    def __init__(self):
        self.data = None

    #$$ def --enter--
    def __enter__(self):
        return self

    #$$ def --exit--
    def __exit__(self, type, value, traceback):
        pass

    #$$ def calc
    def calc(self, n_0, L_φ, v=None, mode='stan', plot=False, name=None):
        '''
        '''
        if v is None:
            v = cunit.range('km*hr**-1',0,201)

        def φ_dyn(n_0, L_φ, v, mode):

            # drop units inserted by user, full cover flag True
            if type(n_0) is cunit: n_0 = n_0.d('Hz')
            if type(L_φ) is cunit: L_φ = L_φ.d('m')
            if type(v)   is cunit: v   =   v.d('m s**-1')


            # first factor function
            K = (v)/(2*L_φ*n_0)

            # first dyn factor part
            if K < 0.76:
                φʾ = K/(1-K+K**4)
            else:
                φʾ = 1.325

            if v <= 22:
                α = v/22
            elif v > 22:
                α = 1

            φʾʾ = max(
                (α)/(100) *
                    (56*exp(-L_φ**2/100) +
                    50*(L_φ*n_0/80-1)*exp(-L_φ**2/400)),
                0)

            if   mode=='stan':
                φ_dyn = 1 + φʾ + φʾʾ
            elif mode=='clea':
                φ_dyn = 1 + φʾ + 0.50*φʾʾ

            return φ_dyn

        if type(v)==range or type(v)==cunit.crange:
            self.speed = [v_1.d('km hr**-1') for v_1 in v]
            self.φ_dyn = [φ_dyn(n_0, L_φ, v_1, mode) for v_1 in v]
            if plot:
                self.plot(name=name)
        else:
            self.speed = v
            self.φ_dyn = φ_dyn(n_0, L_φ, v, mode)
            return {'speed':self.speed.s('km hr**-1') , 'φ_dyn':self.φ_dyn}

    #$$ def plot
    def plot(self, name=None, echo=False):
        mpl.style.use('default')

        # style settings
        plt.figure(figsize=(7, 4))
        upper = max([math.ceil(max(self.φ_dyn)*2)/2, 2])
        plt.axis([0,200,1,upper])
        plt.grid(True, axis='both') #axis=['x','y','both']
        plt.locator_params(nbins=20, axis='x')
        plt.locator_params(nbins=10, axis='y')
        plt.minorticks_on()
        # plt.title('Wykres wartości')
        plt.xlabel('Prędkość pojazdu [km/h]')
        plt.ylabel('Współczynnik dynamiczny [1]')
        plt.rcParams['font.family'] = 'Times New Roman'
        plt.rcParams['font.size'] = 10
        plt.axhline(y=0, linewidth=1, color='0', linestyle='-')
        plt.axvline(x=0, linewidth=1, color='0', linestyle='-')

        # print settings
        plt.tight_layout()

        plt.plot(self.speed, self.φ_dyn, linewidth=3.0, label='linia')

        if name:
            plt.savefig(name, dpi = 320)

        if not echo in [True, 'p']:
            plt.close()

    #$$ def sofi
    def sofi(self, var='PHI_15528', cdb=None, name='x_impact-factor-15528.dat', active=True, make=True, sofix=None):
        if sofix is None:
            se = sofix.trade(cdb=cdb, name=name, active=active)
            se.sto(name=var, val=self.φ_dyn, comment='bcdr:auto-created')

            se.push()
            if make:
                se.make()
        else:
            sofix.sto(name=var, val=self.φ_dyn, comment='bcdr:auto-created')

#$ class en155
class en155:
    #$$ __init__
    def __init__(self, core=None):
        self.core = core

    #$$ def --enter--
    def __enter__(self):
        return self

    #$$ def --exit--
    def __exit__(self, type, value, traceback):
        pass

    #$$ obj dfact
    dfact = dfact()

    def speed_summary(self, A=True, B1=True, B2=True, C2=True, C3=True, C4=True, D2=True, D3=True, D4=-1, inherit=False, mode='1t', label=None, caption=None):
        '''
        Generate texme table with speed summary of 15528 trains.
        '''

        if mode=='1t':

            # drop units
            if type(A)  is cunit:
                    A  = int( A.d('km hr**-1')*1.00001)
            elif A is True:
                    A  = -1
            if type(B1) is cunit:
                    B1 = int(B1.d('km hr**-1')*1.00001)
            elif B1 is True:
                    B1 = -1
            if type(B2) is cunit:
                    B2 = int(B2.d('km hr**-1')*1.00001)
            elif B2 is True:
                    B2 = -1
            if type(C2) is cunit:
                    C2 = int(C2.d('km hr**-1')*1.00001)
            elif C2 is True:
                    C2 = -1
            if type(C3) is cunit:
                    C3 = int(C3.d('km hr**-1')*1.00001)
            elif C3 is True:
                    C3 = -1
            if type(C4) is cunit:
                    C4 = int(C4.d('km hr**-1')*1.00001)
            elif C4 is True:
                    C4 = -1
            if type(D2) is cunit:
                    D2 = int(D2.d('km hr**-1')*1.00001)
            elif D2 is True:
                    D2 = -1
            if type(D3) is cunit:
                    D3 = int(D3.d('km hr**-1')*1.00001)
            elif D3 is True:
                    D3 = -1
            if type(D4) is cunit:
                    D4 = int(D4.d('km hr**-1')*1.00001)
            elif D4 is True:
                    D4 = -1


            # try get value
            if   A  ==-1:  A  = max(B1,B2,C2,C3,C4,D2,D3,D4)
            if   A  <  0:  A  = '--'

            if   B1 ==-1:  B1 = max(   B2,C2,C3,C4,D2,D3,D4)
            if   B1 <  0:  B1 = '--'

            if   B2 ==-1:  B2 = max(      C2,C3,C4,D2,D3,D4)
            if   B2 <  0:  B2 = '--'

            if   C2 ==-1:  C2 = max(         C3,C4,D2,D3,D4)
            if   C2 <  0:  C2 = '--'

            if   C3 ==-1:  C3 = max(            C4,   D3,D4)
            if   C3 <  0:  C3 = '--'

            if   C4 ==-1:  C4 =                          D4
            if   C4 <  0:  C4 = '--'

            if   D2 ==-1:  D2 = max(                  D3,D4)
            if   D2 <  0:  D2 = '--'

            if   D3 ==-1:  D3 =                          D4
            if   D3 <  0:  D3 = '--'

            if   D4 <  0:  D4 = '--'


            if caption is None:
                caption = 'Prędkości dopuszczalne dla modeli ruchu kolejowego \\cite{pnen15528}'

            return self.core.pinky.texme.t(
                    cols     = r'|e{4cm}|C|C|C|C|C|C|C|C|C|',
                    stretchV = 1.3,
                    label    = label,
                    caption  = caption,
                    inherit  = True,
                    data     = fr'''
                \hline
                Model obciążenia &
                A & B1 & B2 & C2 & C3 & C4 & D2 & D3 & D4
                \\ \hline
                Dopuszczalna prędkość [km/h] &
                {A} & {B1} & {B2} & {C2} & {C3} & {C4} & {D2} & {D3} & {D4}
                \\ \hline
                ''')
        else:
            raise ValueError(f'Method not prepared for this mode <{mode}>')