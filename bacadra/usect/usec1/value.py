



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
    def add(self, id=None, mate=None, A=None, A_y=None, A_z=None, I_t=None, I_ω=None, I_y=None, I_z=None, u=None, m_g=None, ttl=None, _subcl=None):

        # overwrite last defined unit section 1d
        self.core.mdata.setts.set({'_usec1_ldef':id})

        # if mate is not defined then use last one material
        if mate is None:
            mate = self.core.mdata.setts.get('_mates_ldef')

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
            u     = u,
            m_g   = m_g,
            ttl   = ttl,
            subcl = _subcl,
        )

        # add universal unit section 1d data
        self.core.dbase.add(
            table = '[021:usec1:value]',
            cols  = cols,
            data  = data,
        )

