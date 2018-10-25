



#$ ____ class unics ________________________________________________________ #

class unics:
    #$$ def --init--
    def __init__(self, dbase, pinky, pvars):
        self.dbase = dbase
        self.pinky = pinky
        self.pvars = pvars

    #$$ def --enter--
    def __enter__(self):
        return self

    #$$ def --exit--
    def __exit__(self, type, value, traceback):
        pass

    #$$ def add
    def add(self, id=None, mate=None, A=None, A_y=None, A_z=None, I_t=None, I_ω=None, I_y=None, I_z=None, u=None, m_g=None, ttl=None, _subcl=None):

        # overwrite last defined unit section 1d
        self.pvars.set({'_usec1_ldef':id})

        # if mate is not defined then use cat last one material
        if mate is None:
            mate = self.pvars.get('_mates_ldef')

        # parse universal units section 1d data
        cols,data = self.dbase.parse(
            id    = id,
            mate  = mate,
            A     = A,
            A_y   = A_y,
            A_z   = A_z,
            I_t   = I_t,
            I_w   = I_ω,
            I_y   = I_y,
            I_z   = I_z,
            u     = u,
            m_g   = m_g,
            ttl   = ttl,
            subcl = _subcl,
        )

        # add universal unit section 1d data
        self.dbase.add(
            table = '[021:usec1:unics]',
            cols  = cols,
            data  = data,
        )

