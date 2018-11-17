'''
------------------------------------------------------------------------------
BCDR += ***** eurocode (en) (155)28 *****
==============================================================================

------------------------------------------------------------------------------
Copyright (C) 2018 <bacadra@gmail.com> <https://github.com/bacadra/bacadra>
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
    #$$ def --init--
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
    def plot(self, name=None):
        mpl.style.use('default')

        # style settings
        plt.figure(figsize=(7, 3))
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
            plt.savefig(name, dpi = 300)

    #$$ def sofi
    def sofi(self, var='PHI_15528', cdb=None, name='x_impact-factor-15528.dat', active=True, make=True):
        se = sofix.trade(cdb=cdb, name=name, active=active)
        se.sto(name=var, val=self.φ_dyn, comment='bcdr:auto-created')

        se.push()
        if make:
            se.make()


#$ class en155
class en155:
    #$$ --init--
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