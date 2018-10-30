from .  import mdata
from .. import umate

from ...cunit import cunit

class steea:
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
    id=None, ρ_o=78.5*cunit('kN')/(cunit('m'))**3, E_1=None, v_1=0.30, G_1=None, t_e=12*10**-6, ttl=None,

    # parametry betonu
    cclass=None, max_t=None,
    f_yk=None, f_uk =None, E_a=None, ε_yk=None, ε_uk=None, γ_M0=None, γ_M1=None, γ_M2=None, γ_M3=None, γ_M4=None, γ_M5=None, γ_M6=None):

        if cclass:
            cdata = mdata.mdata().get(cclass)
            if not f_yk     : f_yk      = cdata['f_yk']
            if not f_uk     : f_uk      = cdata['f_uk']
            if not E_a      : E_a       = cdata['E_a']
            if not ε_yk     : ε_yk      = cdata['ε_yk']
            if not ε_uk     : ε_uk      = cdata['ε_uk']
            # if not γ_M0     : γ_M0      = cdata['γ_M0']
            # if not γ_M1     : γ_M1      = cdata['γ_M1']
            # if not γ_M2     : γ_M2      = cdata['γ_M2']
            # if not γ_M3     : γ_M3      = cdata['γ_M3']
            # if not γ_M4     : γ_M4      = cdata['γ_M4']
            # if not γ_M5     : γ_M5      = cdata['γ_M5']
            # if not γ_M6     : γ_M6      = cdata['γ_M6']

        if not E_1: E_1 = E_a

        # add universal material
        self._umate.add(
            id     = id,
            ρ_o    = ρ_o,
            E_1    = E_1,
            v_1    = v_1,
            G_1    = G_1,
            t_e    = t_e,
            ttl    = ttl,
            _subcl = 'A',
        )

        # parse data for steel material
        cols,data  = self.core.dbase.parse(
            id     = id,
            cclass = cclass,
            max_t  = max_t,
            f_yk   = f_yk,
            f_uk   = f_uk,
            E_a    = E_a,
            ε_yk   = ε_yk,
            ε_uk   = ε_uk,
            γ_M0   = γ_M0,
            γ_M1   = γ_M1,
            γ_M2   = γ_M2,
            γ_M3   = γ_M3,
            γ_M4   = γ_M4,
            γ_M5   = γ_M5,
            γ_M6   = γ_M6,
        )

        # add data for steel material
        self.core.dbase.add(
            table = '[013:mates:steea]',
            cols  = cols,
            data  = data,
        )