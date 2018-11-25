from .pbase  import pbase
from ...cunit import cunit

class steea:
    #$$ def --init--
    def __init__(self, core):
        self.core = core

        from ..umate import umate
        self._umate = umate.umate(core=core)


    #$$ def add
    def add(self,
    # parametry ogolne
    id=None, ρ_o=cunit(7850, {'kg':1, 'm':-3}), E_1=None, v_1=0.30, G_1=None, t_e=cunit(12*10**-6, {'°C':-1}), ttl=None, orm=False,

    grade=None, max_t=None,
    f_yk=None, f_uk =None, E_a=None, ε_yk=None, ε_uk=None, γ_M0=None, γ_M1=None, γ_M2=None, γ_M3=None, γ_M4=None, γ_M5=None, γ_M6=None):

        if grade:
            pbase.set(grade=grade, max_t=max_t, f_yk=f_yk)

            f_yk      = pbase.get(f_yk      , 'f_yk'      )
            f_uk      = pbase.get(f_uk      , 'f_uk'      )
            E_a       = pbase.get(E_a       , 'E_a'       )
            ε_yk      = pbase.get(ε_yk      , 'ε_yk'      )
            ε_uk      = pbase.get(ε_uk      , 'ε_uk'      )
            γ_M0      = pbase.get(γ_M0      , 'γ_M0'      )
            γ_M1      = pbase.get(γ_M1      , 'γ_M1'      )
            γ_M2      = pbase.get(γ_M2      , 'γ_M2'      )
            γ_M3      = pbase.get(γ_M3      , 'γ_M3'      )
            γ_M4      = pbase.get(γ_M4      , 'γ_M4'      )
            γ_M5      = pbase.get(γ_M5      , 'γ_M5'      )
            γ_M6      = pbase.get(γ_M6      , 'γ_M6'      )

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
            grade = grade,
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

        if orm:
            return self.orm(where=f'id={id}')

    #$$ def orm
    def orm(self, where):
        from ...dbase.bxorm import bcdr_mates_steea

        return bcdr_mates_steea(
            dbase = self.core.dbase,
            where = where,
        )



    # def estimate(self, data):
