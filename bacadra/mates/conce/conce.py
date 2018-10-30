from .  import mdata
from .. import umate

from ...cunit import cunit

class conce:
    #$$ def --init--
    def __init__(self, core):
        self.core = core
        self._umate = umate.umate(core=core)

    #$$ def --enter--
    def __enter__(self):
        return self

    #$$ def --exit--
    def __exit__(self, type, value, traceback):
        pass

    #$$ def add
    def add(self,
    # parametry ogolne
    id=None, ρ_o=25*cunit('kN')/(cunit('m'))**3, E_1=None, v_1=0.20, G_1=None, t_e=10**-5, ttl=None,

    # parametry betonu
    cclass=None,
    f_ck=None, f_ck_cube=None, f_cm=None, f_ctm=None, f_ctk_005=None, f_ctk_095=None, E_cm=None, ε_c1=None, ε_cu1=None, ε_c2=None, ε_cu2=None, n_c=None, ε_c3=None, ε_cu3=None, γ_M=None):

        if cclass:
            cdata = mdata.mdata().get(cclass)
            if not f_ck     : f_ck      = cdata['f_ck']
            if not f_ck_cube: f_ck_cube = cdata['f_ck_cube']
            if not f_cm     : f_cm      = cdata['f_cm']
            if not f_ctm    : f_ctm     = cdata['f_ctm']
            if not f_ctk_005: f_ctk_005 = cdata['f_ctk_005']
            if not f_ctk_095: f_ctk_095 = cdata['f_ctk_095']
            if not E_cm     : E_cm      = cdata['E_cm']
            if not ε_c1     : ε_c1      = cdata['ε_c1']
            if not ε_cu1    : ε_cu1     = cdata['ε_cu1']
            if not ε_c2     : ε_c2      = cdata['ε_c2']
            if not ε_cu2    : ε_cu2     = cdata['ε_cu2']
            if not n_c      : n_c       = cdata['n_c']
            if not ε_c3     : ε_c3      = cdata['ε_c3']
            if not ε_cu3    : ε_cu3     = cdata['ε_cu3']

        if not E_1: E_1 = E_cm

        # add universal material
        self._umate.add(
            id     = id,
            ρ_o    = ρ_o,
            E_1    = E_1,
            v_1    = v_1,
            G_1    = G_1,
            t_e    = t_e,
            ttl    = ttl,
            _subcl = 'C',
        )

        # parse data for concrete material
        cols,data = self.core.dbase.parse(
            id        = id,
            cclass    = cclass,
            f_ck      = f_ck,
            f_ck_cube = f_ck_cube,
            f_cm      = f_cm,
            f_ctm     = f_ctm,
            f_ctk_005 = f_ctk_005,
            f_ctk_095 = f_ctk_095,
            E_cm      = E_cm,
            ε_c1      = ε_c1,
            ε_cu1     = ε_cu1,
            ε_c2      = ε_c2,
            ε_cu2     = ε_cu2,
            n_c       = n_c,
            ε_c3      = ε_c3,
            ε_cu3     = ε_cu3,
        )

        # add data for concrete material
        self.core.dbase.add(
            table = '[012:mates:conce]',
            cols  = cols,
            data  = data,
        )