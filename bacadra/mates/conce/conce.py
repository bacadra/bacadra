from .pbase  import pbase
from ...cunit import cunit

class conce:
    #$$ def __init__
    def __init__(self, core):
        self.core = core

        from ..umate import umate
        self._umate = umate.umate(core=core)


    #$$ def add
    def add(self,
    # parametry ogolne
    id=None, ρ_o=cunit(2500, 'kg m**-3'), E_1=None, v_1=0.20, G_1=None, t_e=10**-5, ttl=None, orm=False,

    # parametry betonu
    grade=None,
    f_ck=None, f_ck_cube=None, f_cm=None, f_ctm=None, f_ctk_005=None, f_ctk_095=None, E_cm=None, ε_c1=None, ε_cu1=None, ε_c2=None, ε_cu2=None, n_c=None, ε_c3=None, ε_cu3=None, γ_M=None):

        if grade:
            pbase.set(grade=grade, f_ck=f_ck, f_ck_cube=f_ck_cube)

            f_ck      = pbase.get(f_ck      , 'f_ck'      )
            f_ck_cube = pbase.get(f_ck_cube , 'f_ck_cube' )
            f_cm      = pbase.get(f_cm      , 'f_cm'      )
            f_ctm     = pbase.get(f_ctm     , 'f_ctm'     )
            f_ctk_005 = pbase.get(f_ctk_005 , 'f_ctk_005' )
            f_ctk_095 = pbase.get(f_ctk_095 , 'f_ctk_095' )
            E_cm      = pbase.get(E_cm      , 'E_cm'      )
            ε_c1      = pbase.get(ε_c1      , 'ε_c1'      )
            ε_cu1     = pbase.get(ε_cu1     , 'ε_cu1'     )
            ε_c2      = pbase.get(ε_c2      , 'ε_c2'      )
            ε_cu2     = pbase.get(ε_cu2     , 'ε_cu2'     )
            n_c       = pbase.get(n_c       , 'n_c'       )
            ε_c3      = pbase.get(ε_c3      , 'ε_c3'      )
            ε_cu3     = pbase.get(ε_cu3     , 'ε_cu3'     )


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
            grade     = grade,
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
            γ_M       = γ_M,
        )

        # add data for concrete material
        self.core.dbase.add(
            table = '[012:mates:conce]',
            cols  = cols,
            data  = data,
        )

        if orm:
            return self.orm(where=f'id="{id}"')

    def get(self, id):
        cols = '[id],[grade],[f_ck],[f_ck_cube],[f_cm],[f_ctm],[f_ctk_005],[f_ctk_095],[E_cm],[ε_c1],[ε_cu1],[ε_c2],[ε_cu2],[n_c],[ε_c3],[ε_cu3]'

        data = self.core.dbase.get(f'''
        SELECT {cols} FROM [012:mates:conce] WHERE [id]="{id}"
        ''')[0]

        output = {}
        for key,val in zip(cols.split(','),data):
            output.update({key[1:-1]:val})

        return output

    #$$ def orm
    def orm(self, id=None, where=None):
        from ...dbase.bxorm import bxorm_mates_conce

        if id and not where:
            where = f'id="{id}"'

        return bxorm_mates_conce(
            dbase = self.core.dbase,
            where = where,
        )