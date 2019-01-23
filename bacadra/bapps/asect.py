'''
------------------------------------------------------------------------------
BCDR += ***** (s)teel (sect)ions design *****
==============================================================================

------------------------------------------------------------------------------
Copyright (C) 2018 <bacadra@gmail.com> <https://github.com/bacadra>
Team members developing this package:
    - Sebastian Balcerowiak <asiloisad> <asiloisad.93@gmail.com>
------------------------------------------------------------------------------
'''

from ..tools import setts
from ..cunit.system.math import sqrt

#$ ____ def __init__   ____________________________________________________ #

class asect:
    #$$ def __init__
    def __init__(self, core, **kwargs):
        self.core = core
        self.setts = self.setts('setts',(),{})
        self.setts.othe = self
        self.setts.__run_init__(**kwargs)


    class setts(setts.settsmeta):
        othe = None

        def __run_init__(self, **kwargs):
            # loop over items send from texme class
            for key,val in kwargs.items():
                exec(f'self.{key}={val}')

#$$ ________ materials _____________________________________________________ #

#$$$ ____________ atribute f_yk ____________________________________________ #

        _f_yk   = None


        @property
        def f_yk(self):
            return self._f_yk

        @staticmethod
        def _f_yk_(value):
            return value

        @f_yk.setter
        def f_yk(self, value):
            self._f_yk = self._f_yk_(value)

#$$$ ____________ atribute γ_M0 ____________________________________________ #

        _γ_M0   = None

        @property
        def γ_M0(self):
            return self._γ_M0

        @staticmethod
        def _γ_M0_(value):
            return value

        @γ_M0.setter
        def γ_M0(self, value):
            self._γ_M0 = self._γ_M0_(value)

#$$$ ____________ atribute γ_M1 ____________________________________________ #

        _γ_M1   = None

        @property
        def γ_M1(self):
            return self._γ_M1

        @staticmethod
        def _γ_M1_(value):
            return value

        @γ_M1.setter
        def γ_M1(self, value):
            self._γ_M1 = self._γ_M1_(value)

#$$$ ____________ atribute γ_M2 ____________________________________________ #

        _γ_M2   = None

        @property
        def γ_M2(self):
            return self._γ_M2

        @staticmethod
        def _γ_M2_(value):
            return value

        @γ_M2.setter
        def γ_M2(self, value):
            self._γ_M2 = self._γ_M2_(value)


#$$ ________ unit-section-1d _______________________________________________ #

#$$$ ____________ atribute sect_id _________________________________________ #

        _sect_id    = None

        @property
        def sect_id(self):
            return self._sect_id

        @staticmethod
        def _sect_id_(value):
            return value

        @sect_id.setter
        def sect_id(self, value):

            cs = self.othe.core.dbase.get(f'''
            SELECT
                [CS].[A],
                [CS].[A_y],
                [CS].[A_z],
                [CS].[I_t],
                [CS].[I_y],
                [CS].[I_z],
                [MT].[G_1],
                [SA].[E_a],
                [SA].[f_yk],
                [SA].[f_uk],
                [SA].[γ_M0],
                [SA].[γ_M1],
                [SA].[γ_M2]
            FROM [021:usec1:value]      AS [CS]
            LEFT JOIN [011:mates:umate] AS [MT] ON [CS].[mate] = [MT].[id]
            LEFT JOIN [013:mates:steea] AS [SA] ON [CS].[mate] = [SA].[id]
            WHERE [CS].[id]="{value}"
            ''')[0]

            self._sect_id = self._sect_id_(value)
            self._A   = cs[0]
            self._A_y = cs[1]
            self._A_z = cs[2]








#$$$ ____________ atribute scl _____________________________________________ #

        _scl    = None

        @property
        def scl(self):
            return self._scl

        @staticmethod
        def _scl_(value):
            return value

        @scl.setter
        def scl(self, value):
            self._scl = self._scl_(value)

#$$$ ____________ atribute stp _____________________________________________ #

        _stp    = 'I-rollled'

        # 'I-rollled'
        # 'I-welded'
        # 'I-welded'

        @property
        def stp(self):
            return self._stp

        @staticmethod
        def _stp_(value):
            return value

        @stp.setter
        def stp(self, value):
            self._stp = self._stp_(value)



#$$$ ____________ atribute η_s _____________________________________________ #

        _η_s = None

        @property
        def η_s(self):
            return self._η_s

        @staticmethod
        def _η_s_(value):
            return value

        @η_s.setter
        def η_s(self, value):
            self._η_s = self._η_s_(value)


#$$$ ____________ atribute h _______________________________________________ #

        _h= None

        @property
        def h(self):
            return self._h

        @staticmethod
        def _h_(value):
            return value

        @h.setter
        def h(self, value):
            self._h = self._h_(value)


#$$$ ____________ atribute t_w _____________________________________________ #

        _t_w = None

        @property
        def t_w (self):
            return self._t_w

        @staticmethod
        def _t_w_(value):
            return value

        @t_w.setter
        def t_w(self, value):
            self._t_w = self._t_w_(value)

#$$$ ____________ atribute b_f _____________________________________________ #

        _b_f = None

        @property
        def b_f(self):
            return self._b_f

        @staticmethod
        def _b_f_(value):
            return value

        @b_f.setter
        def b_f(self, value):
            self._b_f = self._b_f_(value)


#$$$ ____________ atribute t_f _____________________________________________ #

        _t_f = None

        @property
        def t_f(self):
            return self._t_f

        @staticmethod
        def _t_f_(value):
            return value

        @t_f.setter
        def t_f(self, value):
            self._t_f = self._t_f_(value)



#$$$ ____________ atribute r _______________________________________________ #

        _r = None

        @property
        def r(self):
            return self._r

        @staticmethod
        def _r_(value):
            return value

        @r.setter
        def r(self, value):
            self._ρ = self._r_(value)

#$$$ ____________ atribute A _______________________________________________ #

        _A      = None

        @property
        def A(self):
            return self._A

        @staticmethod
        def _A_(value):
            return value

        @A.setter
        def A(self, value):
            self._A = self._A_(value)


#$$$ ____________ atribute A_y _____________________________________________ #

        _A_y = None

        @property
        def A_y(self):
            return self._A_y

        @staticmethod
        def _A_y_(value):
            return value

        @A_y.setter
        def A_y(self, value):
            self._A_y = self._A_y_(value)


#$$$ ____________ atribute A_z _____________________________________________ #

        _A_z = None

        @property
        def A_z(self):
            return self._A_z

        @staticmethod
        def _A_z_(value):
            return value

        @A_z.setter
        def A_z(self, value):
            self._A_z = self._A_z_(value)


#$$$ ____________ atribute W_y_el __________________________________________ #

        _W_y_el = None

        @property
        def W_y_el(self):
            return self._W_y_el

        @staticmethod
        def _W_y_el_(value):
            return value

        @W_y_el.setter
        def W_y_el(self, value):
            self._W_y_el = self._W_y_el_(value)


#$$$ ____________ atribute W_z_el __________________________________________ #

        _W_z_el = None

        @property
        def W_z_el(self):
            return self._W_z_el

        @staticmethod
        def _W_z_el_(value):
            return value

        @W_z_el.setter
        def W_z_el(self, value):
            self._W_z_el = self._W_z_el_(value)

#$$$ ____________ atribute W_y_pl __________________________________________ #

        _W_y_pl = None

        @property
        def W_y_pl(self):
            return self._W_y_pl

        @staticmethod
        def _W_y_pl_(value):
            return value

        @W_y_pl.setter
        def W_y_pl(self, value):
            self._W_y_pl = self._W_y_pl_(value)

#$$$ ____________ atribute W_z_pl __________________________________________ #

        _W_z_pl = None

        @property
        def W_z_pl(self):
            return self._W_z_pl

        @staticmethod
        def _W_z_pl_(value):
            return value

        @W_z_pl.setter
        def W_z_pl(self, value):
            self._W_z_pl = self._W_z_pl_(value)






#$$$ ____________ atribute W_y_ef __________________________________________ #

        _W_y_ef = None

        @property
        def W_y_ef(self):
            return self._W_y_ef

        @staticmethod
        def _W_y_ef_(value):
            return value

        @W_y_ef.setter
        def W_y_ef(self, value):
            self._W_y_ef = self._W_y_ef_(value)


#$$$ ____________ atribute W_z_ef __________________________________________ #

        _W_z_ef = None

        @property
        def W_z_ef(self):
            return self._W_z_ef

        @staticmethod
        def _W_z_ef_(value):
            return value

        @W_z_ef.setter
        def W_z_ef(self, value):
            self._W_z_ef = self._W_z_ef_(value)




#$$$ ____________ atribute N_pl_Rk _________________________________________ #

        _N_pl_Rk = None

        @property
        def N_pl_Rk(self):
            return self._N_pl_Rk

        @staticmethod
        def _N_pl_Rk_(value):
            return value

        @N_pl_Rk.setter
        def N_pl_Rk(self, value):
            self._N_pl_Rk = self._N_pl_Rk_(value)



#$$$ ____________ atribute M_y_pl_Rk _______________________________________ #

        _M_y_pl_Rk = None

        @property
        def M_y_pl_Rk(self):
            return self._M_y_pl_Rk

        @staticmethod
        def _M_y_pl_Rk_(value):
            return value

        @M_y_pl_Rk.setter
        def M_y_pl_Rk(self, value):
            self._M_y_pl_Rk = self._M_y_pl_Rk_(value)



#$$$ ____________ atribute M_z_pl_Rk _______________________________________ #

        _M_z_pl_Rk = None

        @property
        def M_z_pl_Rk(self):
            return self._M_z_pl_Rk

        @staticmethod
        def _M_z_pl_Rk_(value):
            return value

        @M_z_pl_Rk.setter
        def M_z_pl_Rk(self, value):
            self._M_z_pl_Rk = self._M_z_pl_Rk_(value)



#$$$ ____________ atribute V_y_pl_Rk _______________________________________ #

        _V_y_pl_Rk = None

        @property
        def V_y_pl_Rk(self):
            return self._V_y_pl_Rk

        @staticmethod
        def _V_y_pl_Rk_(value):
            return value

        @V_y_pl_Rk.setter
        def V_y_pl_Rk(self, value):
            self._V_y_pl_Rk = self._V_y_pl_Rk_(value)


#$$$ ____________ atribute V_z_pl_Rk _______________________________________ #

        _V_z_pl_Rk = None

        @property
        def V_z_pl_Rk(self):
            return self._V_z_pl_Rk

        @staticmethod
        def _V_z_pl_Rk_(value):
            return value

        @V_z_pl_Rk.setter
        def V_z_pl_Rk(self, value):
            self._V_z_pl_Rk = self._V_z_pl_Rk_(value)










#$$ ________ forces ________________________________________________________ #

#$$$ ____________ atribute N-Ed ____________________________________________ #

        _N_Ed   = None

        @property
        def N_Ed(self):
            return self._N_Ed

        @staticmethod
        def _N_Ed_(value):
            return value

        @N_Ed.setter
        def N_Ed(self, value):
            self._N_Ed = self._N_Ed_(value)

#$$$ ____________ atribute V-y-Ed __________________________________________ #

        _V_y_Ed = None

        @property
        def V_y_Ed(self):
            return self._V_y_Ed

        @staticmethod
        def _V_y_Ed_(value):
            return value

        @V_y_Ed.setter
        def V_y_Ed(self, value):
            self._V_y_Ed = self._V_y_Ed_(value)

#$$$ ____________ atribute V-z-Ed __________________________________________ #

        _V_z_Ed = None

        @property
        def V_z_Ed(self):
            return self._V_z_Ed

        @staticmethod
        def _V_z_Ed_(value):
            return value

        @V_z_Ed.setter
        def V_z_Ed(self, value):
            self._V_z_Ed = self._V_z_Ed_(value)

#$$$ ____________ atribute M-x-Ed __________________________________________ #

        _M_x_Ed = None

        @property
        def M_x_Ed(self):
            return self._A

        @staticmethod
        def _M_x_Ed_(value):
            return value

        @M_x_Ed.setter
        def M_x_Ed(self, value):
            self._M_x_Ed = self._M_x_Ed_(value)

#$$$ ____________ atribute M-y-Ed __________________________________________ #

        _M_y_Ed = None

        @property
        def M_y_Ed(self):
            return self._M_y_Ed

        @staticmethod
        def _M_y_Ed_(value):
            return value

        @M_y_Ed.setter
        def M_y_Ed(self, value):
            self._M_y_Ed = self._M_y_Ed_(value)

#$$$ ____________ atribute M-z-Ed __________________________________________ #

        _M_z_Ed = None

        @property
        def M_z_Ed(self):
            return self._M_z_Ed

        @staticmethod
        def _M_z_Ed_(value):
            return value

        @M_z_Ed.setter
        def M_z_Ed(self, value):
            self._M_z_Ed = self._M_z_Ed_(value)


    class setts(setts, metaclass=setts):
        pass


    def N_pl_Rd(self, f_yk=None, γ_M0=None, A=None, _check=True):
        '''
        Tension: the design plastic resistance of the gross cross-section
        '''

        if _check:
            f_yk  = self.setts.test('f_yk', f_yk)
            γ_M0  = self.setts.test('γ_M0', γ_M0)
            A     = self.setts.test('A', A)

        return A * f_yk / γ_M0



    def N_u_Rd(self, A_net=None, f_uk=None, γ_M2=None, _check=True):
        '''
        Tension:  the design ultimate resistance of the net cross-section at holes for fasteners
        '''

        if _check:
            A_net = self.setts.test('A_net', A_net)
            f_uk  = self.setts.test('f_uk' , f_uk)
            γ_M2  = self.setts.test('γ_M2' , γ_M2)

        return 0.9 * A_net * f_uk / γ_M2



    def N_t_Rd(self, f_yk=None, γ_M0=None, A=None, A_net=None, f_uk=None, γ_M2=None, _check=True):
        '''
        For sections with holes the design tension resistance N t,Rd  should be taken as the smaller of:
        '''

        if _check:
            f_yk  = self.setts.test('f_yk', f_yk)
            γ_M0  = self.setts.test('γ_M0', γ_M0)
            A     = self.setts.test('A', A)
            A_net = self.setts.test('A_net', A_net)
            f_uk  = self.setts.test('f_uk' , f_uk)
            γ_M2  = self.setts.test('γ_M2' , γ_M2)

        return min([
            self.N_pl_Rd(f_yk, γ_M0, A),
            self.N_u_Rd(A_net, f_uk, γ_M2),
        ])


    def η_T(self, N_Ed=None, f_yk=None, γ_M0=None, A=None, A_net=None, f_uk=None, γ_M2=None, _check=True):

        if _check:
            N_Ed  = self.setts.test('N_Ed', N_Ed)
            f_yk  = self.setts.test('f_yk', f_yk)
            γ_M0  = self.setts.test('γ_M0', γ_M0)
            A     = self.setts.test('A', A)
            A_net = self.setts.test('A_net', A_net)
            f_uk  = self.setts.test('f_uk' , f_uk)
            γ_M2  = self.setts.test('γ_M2' , γ_M2)

        N_t_Rd = self.N_t_Rd(f_yk=f_yk, γ_M0=γ_M0, A=A, A_net=A_net, f_uk=f_uk, γ_M2=γ_M2, _check=False)

        return N_Ed / N_t_Rd


    def N_ef_Rd(self, A_ef=None, f_yk=None, γ_M0=None, _check=True):
        '''
        Compression efective
        '''

        if _check:
            f_yk  = self.setts.test('f_yk', f_yk)
            γ_M0  = self.setts.test('γ_M0', γ_M0)
            A_ef = self.setts.test('A_ef', A_ef)

        return A_ef * f_yk / γ_M0


    def N_c_Rd(self, scl=None, A=None, A_ef=None, f_yk=None, γ_M0=None, _check=True):
        '''
        The design resistance of the cross-section for uniform compression N   should be determined as follows.
        '''

        if _check:
            scl   = self.setts.test('scl', scl)
            f_yk  = self.setts.test('f_yk', f_yk)
            γ_M0  = self.setts.test('γ_M0', γ_M0)
            A_ef = self.setts.test('A_ef', A_ef)
            A     = self.setts.test('A', A)

        if self.scl in [1,2,3]:
            return self.N_pl_Rd(A, f_yk, γ_M0)
        else:
            return self.N_ef_Rd(A_ef, f_yk, γ_M0)

    def η_C(self, N_Ed=None, scl=None, A=None, A_ef=None, f_yk=None, γ_M0=None, _check=True):

        if _check:
            N_Ed  = self.setts.test('N_Ed', N_Ed)
            scl   = self.setts.test('scl', scl)
            A     = self.setts.test('A', A)
            A_ef = self.setts.test('A_ef', A_ef)
            f_yk  = self.setts.test('f_yk', f_yk)
            γ_M0  = self.setts.test('γ_M0', γ_M0)

        N_c_Rd = self.N_c_Rd(N_Ed=N_Ed, scl=scl, A=A, A_ef=A_ef, f_yk=f_yk, γ_M0=γ_M0, _check=False)

        return N_Ed / N_c_Rd


    def M_y_el_Rd(self, W_y_el=None, f_yk=None, γ_M0=None, _check=True):
        '''
        Bending elastic
        '''

        if _check:
            f_yk  = self.setts.test('f_yk', f_yk)
            γ_M0  = self.setts.test('γ_M0', γ_M0)
            W_y_el= self.setts.test('W_y_el', W_y_el)

        return W_y_el * f_yk / γ_M0


    def M_y_pl_Rd(self, W_y_pl=None, f_yk=None, γ_M0=None, _check=True):
        '''
        Bending plastic
        '''

        if _check:
            f_yk  = self.setts.test('f_yk', f_yk)
            γ_M0  = self.setts.test('γ_M0', γ_M0)
            W_y_pl= self.setts.test('W_y_el', W_y_pl)

        return W_y_pl * f_yk / γ_M0



    def M_y_ef_Rd(self, W_y_ef=None, f_yk=None, γ_M0=None, _check=True):
        '''
        Bending efective
        '''

        if _check:
            f_yk  = self.setts.test('f_yk', f_yk)
            γ_M0  = self.setts.test('γ_M0', γ_M0)
            W_y_ef= self.setts.test('W_y_el', W_y_ef)

        return W_y_ef * f_yk / γ_M0


    def M_y_c_Rd(self, W_y_el=None, W_y_pl=None, W_y_ef=None, f_yk=None, γ_M0=None):
        '''
        Bending efective
        '''

        if self.scl in [1,2]:
            return self.M_z_pl_Rd(W_y_pl, f_yk, γ_M0)
        elif self.scl in [3]:
            return self.M_z_el_Rd(W_y_el, f_yk, γ_M0)
        else:
            return self.M_z_ef_Rd(W_y_ef, f_yk, γ_M0)



    def M_z_pl_Rd(self, W_z_pl=None, f_yk=None, γ_M0=None, _check=True):
        '''
        Bending plastic
        '''

        if _check:
            f_yk  = self.setts.test('f_yk', f_yk)
            γ_M0  = self.setts.test('γ_M0', γ_M0)
            W_z_pl= self.setts.test('W_y_el', W_z_pl)

        return W_z_pl * f_yk / γ_M0

    def M_z_el_Rd(self, W_z_el=None, f_yk=None, γ_M0=None, _check=True):
        '''
        Bending elastic
        '''

        if _check:
            f_yk  = self.setts.test('f_yk', f_yk)
            γ_M0  = self.setts.test('γ_M0', γ_M0)
            W_z_el= self.setts.test('W_y_el', W_z_el)

        return W_z_el * f_yk / γ_M0


    def M_z_ef_Rd(self, W_z_ef=None, f_yk=None, γ_M0=None, _check=True):
        '''
        Bending efective
        '''

        if _check:
            f_yk  = self.setts.test('f_yk', f_yk)
            γ_M0  = self.setts.test('γ_M0', γ_M0)
            W_z_ef= self.setts.test('W_y_el', W_z_ef)

        return W_z_ef * f_yk / γ_M0


    def M_z_c_Rd(self, W_z_el=None, W_z_pl=None, W_z_ef=None, f_yk=None, γ_M0=None):
        '''
        Bending efective
        '''

        if self.scl in [1,2]:
            return self.M_z_pl_Rd(W_z_pl, f_yk, γ_M0)
        elif self.scl in [3]:
            return self.M_z_el_Rd(W_z_el, f_yk, γ_M0)
        else:
            return self.M_z_ef_Rd(W_z_ef, f_yk, γ_M0)


    def V_z_pl_Rd(self, A=None, A_z=None, f_yk=None, γ_M0=None, b_f=None, t_f=None, t_w=None, h=None, η_s=None, stp=None, r=None, _check=True):

        if _check:
            f_yk  = self.setts.test('f_yk', f_yk)
            A_z   = self.setts.test('A_z' , A_z )
            γ_M0  = self.setts.test('γ_M0', γ_M0)
            γ_M0  = self.setts.test('γ_M0', γ_M0)

        if A_z is None:
            if stp == 'I-rolled':
                A_z = max(A - 2*b_f*t_f + (t_w+2*r)*t_f, t_w*(h-2*t_f)*η_s)
            elif stp == 'I-welded':
                A_z = η_s*(h-2*t_f)*t_w

        return A_z * f_yk / sqrt(3) / γ_M0


    def V_y_pl_Rd(self, A=None, A_y=None, f_yk=None, γ_M0=None, b_f=None, t_f=None, t_w=None, h=None, η_s=None, stp=None, r=None, _check=True):

        if _check:
            f_yk  = self.setts.test('f_yk', f_yk)
            A_y   = self.setts.test('A_y' , A_y )
            γ_M0  = self.setts.test('γ_M0', γ_M0)
            γ_M0  = self.setts.test('γ_M0', γ_M0)

        if A_y is None:
            if stp in ['I-rolled']:
                A_y = A - (h-2*t_f)*t_w

        return A_y * f_yk / sqrt(3) / γ_M0



    def NVVMM(self,

    N_Ed=None, M_y_Ed=None, M_z_Ed=None, V_y_Ed=None, V_z_Ed=None,

    A=None, A_z=None, A_y=None, r=None, b_f=None, t_f=None, stp=None, t_w=None, h=None, η_s=None, W_y_pl=None, W_z_pl=None,

    N_pl_Rk=None, M_y_pl_Rk=None, M_z_pl_Rk=None, V_z_pl_Rk=None, V_y_pl_Rk=None,

    f_yk=None, γ_M0=None,

    _check=True):

        if _check:
            N_Ed      = self.setts.test('N_Ed'     , N_Ed        )
            M_y_Ed    = self.setts.test('M_y_Ed'   , M_y_Ed      )
            M_z_Ed    = self.setts.test('M_z_Ed'   , M_z_Ed      )
            V_y_Ed    = self.setts.test('V_y_Ed'   , V_y_Ed      )
            V_z_Ed    = self.setts.test('V_z_Ed'   , V_z_Ed      )
            A         = self.setts.test('A'        , A           )
            A_z       = self.setts.test('A_z'      , A_z         )
            A_y       = self.setts.test('A_y'      , A_y         )
            b_f       = self.setts.test('b_f'      , b_f         )
            t_f       = self.setts.test('t_f'      , t_f         )
            r         = self.setts.test('r'        , r           )
            stp       = self.setts.test('stp'      , stp         )
            t_w       = self.setts.test('t_w'      , t_w         )
            h         = self.setts.test('h'        , h           )
            η_s       = self.setts.test('η_s'      , η_s         )
            W_y_pl    = self.setts.test('W_y_pl'   , W_y_pl      )
            W_z_pl    = self.setts.test('W_z_pl'   , W_z_pl      )
            N_pl_Rk   = self.setts.test('N_pl_Rk'  , N_pl_Rk     )
            M_y_pl_Rk = self.setts.test('M_y_pl_Rk', M_y_pl_Rk   )
            M_z_pl_Rk = self.setts.test('M_z_pl_Rk', M_z_pl_Rk   )
            V_z_pl_Rk = self.setts.test('V_z_pl_Rk', V_z_pl_Rk   )
            V_y_pl_Rk = self.setts.test('V_y_pl_Rk', V_y_pl_Rk   )
            f_yk      = self.setts.test('f_yk'     , f_yk        )
            γ_M0      = self.setts.test('γ_M0'     , γ_M0        )


        if stp in ['I-rolled', 'I-welded-bi']:

            # axial plastic resistance
            N_pl_Rd = self.N_pl_Rd(
                f_yk=f_yk, γ_M0=γ_M0, A=A,
                _check=False,
            )

            # shear plastic resistance
            V_z_pl_Rd = self.V_z_pl_Rd(
                A=A, A_z=A_z, f_yk=f_yk, γ_M0=γ_M0, b_f=b_f, t_f=t_f, t_w=t_w, h=h, η_s=η_s, stp=stp, r=r,
                _check=False,
            )

            V_y_pl_Rd = self.V_y_pl_Rd(
                A=A, A_y=A_z, f_yk=f_yk, γ_M0=γ_M0, b_f=b_f, t_f=t_f, t_w=t_w, h=h, η_s=η_s, stp=stp, r=r,
                _check=False,
            )

            # reduction factors

            ρ_z = (min(1, max(0, (2 * V_z_Ed) / (V_z_pl_Rd) - 1)))**2

            ρ_y = (min(1, max(0, (2 * V_y_Ed) / (V_y_pl_Rd) - 1)))**2

            # axial utilization
            n = N_Ed / N_pl_Rd
            print('n',n)

            # web area properties
            a = min((A - 2 * b_f * t_f) / A, 0.5)

            # bending resistance due to shear and axial forces
            M_y_pl_Rd = self.M_y_pl_Rd(
                W_y_pl=W_y_pl, f_yk=f_yk*(1-ρ_z), γ_M0=γ_M0,
                _check=False,
            )

            M_N_y_Rd = min(M_y_pl_Rd * (1-n)/(1-0.5*a), M_y_pl_Rd)

            M_z_pl_Rd = self.M_z_pl_Rd(
                W_z_pl=W_z_pl, f_yk=f_yk*(1-ρ_y), γ_M0=γ_M0,
                _check=False,
            )

            if n <= a:
                M_N_z_Rd = M_z_pl_Rd
            else:
                M_N_z_Rd = M_z_pl_Rd * (1 - ((n-a) / (1-a))**2)


            # interaction My & Mz factors
            α = 2

            β = max(1, 5*n)

            # utilization
            η = (M_y_Ed/M_N_y_Rd)**α + (M_z_Ed/M_N_z_Rd)**β

            print('N_pl_Rd', N_pl_Rd)
            print('V_z_pl_Rd',V_z_pl_Rd)
            print('V_y_pl_Rd', V_y_pl_Rd)
            print('ρ_z',ρ_z)
            print('ρ_y',ρ_y)
            print('a', a)
            print('M_y_pl_Rd',M_y_pl_Rd)
            print('M_N_y_Rd',M_N_y_Rd)
            print('M_z_pl_Rd',M_z_pl_Rd)
            print('M_N_z_Rd',M_N_z_Rd)
            print('α',α,'β',β)
            print('η',η.s('%'))

            return η



    def csr(self, N_Ed=None, V_y_Ed=None, V_z_Ed=None, M_x_Ed=None, M_y_Ed=None, M_z_Ed=None):
        '''
        Cross-section resistance.
        '''

        result = {}

        # (η_T) Axial force tensin
        if N_Ed > 0:
            result.update({'η_T': self.η_T(N_Ed)})

        # (η_C) Axial force compression
        if N_Ed < 0:
            result.update({'η_T': self.η_T(N_Ed)})

        # (My) Bending moment My

        # (Mz) Bending moment Mz

        # (Vy) Shear force Vy

        # (Vz) Shear force Vz

        # (Tt) Torsion

        # (VyMy) Bending My with shear force Vy

        # (VyTtMy) Bending My with shear force Vy and torsion

        # (VzMz) Bending My with shear force Vz

        # (VzTtMz) Bending My with shear force Vz and torsion

        # (AxMyMz)

        # (AxVyVzMtMyMz)




    def linsum(self, N_Ed=None, V_y_Ed=None, V_z_Ed=None, M_x_Ed=None, M_y_Ed=None, M_z_Ed=None):
        '''
        EN-1993-1-1 6.2.1(7) eq 6.2. Additional utilization with shear forces is calculated too,
        '''

        η_σ = [
            N_Ed   / self.N_c_Rd(),
            M_y_Ed / self.M_y_c_Rd(),
            M_z_Ed / self.M_z_c_Rd(),
        ]

        η_τ = [
            V_y_Ed / self.V_y_c_Rd(),
            V_z_Ed / self.V_z_c_Rd(),
            M_x_Ed / self.M_x_c_Rd(),
        ]

        return {
            'η_σ' : η_σ,
            'η_τ' : η_τ,
            'η'   : η_σ + η_τ,
        }

