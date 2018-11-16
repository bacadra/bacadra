
from ...cunit import cunit
from ...cunit.system.math import exp

#$ class en155
class en155:
    #$$ --init--
    def __init__(self, core=None):
        self.core = core


    def dfact(self, n_0, L_φ, v=None, mode='stan'):
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
            return [φ_dyn(n_0, L_φ, v_1, mode) for v_1 in v]
        else:
            return φ_dyn(n_0, L_φ, v, mode)
