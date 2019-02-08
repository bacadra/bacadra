from bacadra_dev.cunit.system.ce import MPa


class joint:

    def __init__(self,**kwargs):
        self.d  = kwargs['d']
        self.d0 = kwargs['d0']

        self.cl = kwargs['cl']
        self.f_ub = int(self.cl)*100*MPa
        self.f_yb = self.f_ub*(self.cl-int(self.cl))



class sconn:
    γ_M2 = 1.25

    def F_t_Rd(self, jt):
        return 0.9*jt.f_ub*jt.A_s/self.γ_M2

    def F_v_Rd(self, jt):
        return jt.α_v*jt.f_ub*jt.A_v/self.γ_M2


