



#$ ____ class value ________________________________________________________ #

class value:
    #$$ def --init--
    def __init__(self, core):
        self.core = core

    #$$ def --enter--
    def __enter__(self):
        return self

    #$$ def --exit--
    def __exit__(self, type, value, traceback):
        pass

    #$$ def add
    def add(self, id=None, mate=None, A=None, A_y=None, A_z=None, I_t=None, I_ω=None, I_y=None, I_z=None, I_ξ=None, I_η=None, I_p=None, u=None, m_g=None, y_gc=None, z_gc=None, y_sc=None, z_sc=None, α=None, ttl=None, _subcl=None):

        # overwrite last defined unit section 1d
        self.core.mdata.setts.set({'_usec1_ldef':id})

        # if mate is not defined then use last one material
        if mate is None:
            mate = self.core.mdata.setts.get('_mates_ldef')

        m_g = self._fill_prop(m_g=m_g,A=A,mate=mate)

        # parse universal units section 1d data
        cols,data = self.core.dbase.parse(
            id    = id,
            mate  = mate,
            A     = A,
            A_y   = A_y,
            A_z   = A_z,
            I_t   = I_t,
            I_ω   = I_ω,
            I_y   = I_y,
            I_z   = I_z,
            I_ξ   = I_ξ,
            I_η   = I_η,
            I_p   = I_p,
            u     = u,
            m_g   = m_g,
            ttl   = ttl,
            y_gc  = y_gc,
            z_gc  = z_gc,
            y_sc  = y_sc,
            z_sc  = z_sc,
            α     = α,
            subcl = _subcl,
        )

        # add universal unit section 1d data
        self.core.dbase.add(
            table = '[021:usec1:value]',
            cols  = cols,
            data  = data,
        )


    def _fill_prop(self, **kwargs):
        m_g  = kwargs['m_g']
        A    = kwargs['A']
        mate = kwargs['mate']

        if m_g is None and mate is not None:
            # get material prop from database
            ρ_o = self.core.dbase.get(f'SELECT [ρ_o] FROM [011:mates:umate] WHERE [id]={mate}')[0][0]
            # ciezar jednostkowy przekroju
            m_g = A * ρ_o

        return m_g