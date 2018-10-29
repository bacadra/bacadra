from .. import umate
from . import data

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
    id=None, ρ=None, E_1=None, v_1=None, G_1=None, texp=None, ttl=None,

    # parametry betonu
    cclass=None,
    f_ck=None, f_ck_cube=None, f_cm=None, f_ctm=None, f_ctk_005=None, f_ctm_095=None, E_cm=None, ε_c1=None, ε_cu1=None, ε_c2=None, ε_cu2=None, n_c=None, ε_c3=None, ε_cu3=None):

        # if cclass:

        # parse data for concrete material
        cols,data = self.core.dbase.parse(
            id        = id,
            cclass    = cclass,
            f_ck      = f_ck,
            f_ck_cube = f_ck_cube,
            f_cm      = f_cm,
            f_ctm     = f_ctm,
            f_ctk_005 = f_ctk_005,
            f_ctm_095 = f_ctm_095,
            E_cm      = E_cm,
            ε_c1      = ε_c1,
            ε_cu1     = ε_cu1,
            ε_c2      = ε_c2,
            ε_cu2     = ε_cu2,
            n_c       = n_c,
            ε_c3      = ε_c3,
            ε_cu3     = ε_cu3,
        )


        # add universal material
        self._umate.add(
            id     = id,
            ρ      = ρ,
            E_1    = E_1,
            v_1    = v_1,
            G_1    = G_1,
            texp   = texp,
            ttl    = ttl,
            _subcl = 'C',
        )

        # # parse data for concrete material
        # cols,data = self.core.dbase.parse(
        #     id    = id,
        #     cclass= cclass,
        #     f_ck  = f_ck,
        # )

        # add data for concrete material
        self.core.dbase.add(
            table = '[012:mates:conce]',
            cols  = cols,
            data  = data,
        )

    # def create_code_material(self, f_ck):
    #     return data.en1992.create(f_ck)