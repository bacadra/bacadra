from . import value


#$ ____ class tsect ________________________________________________________ #

class tsect:
    #$$ def --init--
    def __init__(self, core):
        self.core = core
        self._value = value.value(core=core)

    #$$ def --enter--
    def __enter__(self):
        return self

    #$$ def --exit--
    def __exit__(self, type, value, traceback):
        pass

    #$$ def add
    def add(self, id=None, mate=None, h_w=None, t_w=None, t_f_1=None, b_f_1=None, t_f_2=None, b_f_2=None, ttl=None):

        # TODO: double def, again in value...
        # if mate is not defined then use last one material
        if mate is None:
            mate = self.core.mdata.setts.get('_mates_ldef')

        A,A_y,A_z,I_t,I_ω,I_y,I_z,u,m_g = self._calc(mate,h_w,t_w,t_f_1,b_f_1,t_f_2,b_f_2)

        # parse universal units section 1d data
        self._value.add(
            id     = id,
            mate   = mate,
            A      = A,
            A_y    = A_y,
            A_z    = A_z,
            I_t    = I_t,
            I_ω    = I_ω,
            I_y    = I_y,
            I_z    = I_z,
            u      = u,
            m_g    = m_g,
            ttl    = ttl,
            _subcl = 'tsect',
        )

        self._spt(id,mate,h_w,t_w,t_f_1,b_f_1,t_f_2,b_f_2)


    def _calc(self, mate, h_w=None, t_w=None, t_f_1=None, b_f_1=None, t_f_2=None, b_f_2=None):
        '''
        Calculate geometric characteristic and few other section parameters.
        '''

        if not h_w  : h_w   = 0
        if not t_w  : t_w   = 0
        if not t_f_1: t_f_1 = 0
        if not b_f_1: b_f_1 = 0
        if not t_f_2: t_f_2 = 0
        if not b_f_2: b_f_2 = 0

        A = h_w * t_w + t_f_1 * b_f_1 + t_f_2 * b_f_2

        S_y = (
            (h_w * t_w) * (t_f_2 + 0.5*h_w) +
            (t_f_1 * b_f_1) * (t_f_2 + h_w + 0.5*t_f_1) +
            (t_f_2 * b_f_2) * (0.5*t_f_2)
        )

        z_0 = S_y/A

        I_y = (
            (  h_w**3*t_w  /12)+(  h_w*t_w  )*(t_f_2+0.5*h_w-z_0)**2 +
            (t_f_1**3*b_f_1/12)+(t_f_1*b_f_1)*(t_f_2+h_w+ 0.5*t_f_1-z_0)**2 +
            (t_f_2**3*b_f_2/12)+(t_f_2*b_f_2)*(0.5*t_f_2-z_0)**2
        )

        I_z = (
            t_w**3 * h_w / 12 +
            b_f_1**3 * t_f_1 / 12 +
            b_f_2**3 * t_f_2 / 12
        )

        u = (
            b_f_1 * 2 - t_w + 2* t_f_1 +
            b_f_2 * 2 - t_w + 2* t_f_2 +
            h_w * 2
        )

        ρ_o = self.core.dbase.get(f'SELECT [ρ_o] FROM [011:mates:umate] WHERE [id]={mate}')[0][0]

        m_g = A * ρ_o

        A_y, A_z, I_t, I_ω = None, None, None, None

        return A,A_y,A_z,I_t,I_ω,I_y,I_z,u,m_g


    def _spt(self, sect=None, mate=None, h_w=None, t_w=None, t_f_1=None, b_f_1=None, t_f_2=None, b_f_2=None):
        '''
        Create stress points.
        '''

        data = [] # id, y, z, ttl

        if h_w and t_w:
            data.append(['ax' , 0,     0,  'stress in gravity center'])
            data.append(['zh+', 0,  h_w/2, 'clear bending My in z+'])
            data.append(['zh-', 0, -h_w/2, 'clear bending My in z-'])

        summary = []
        for row in data:
            cols,data = self.core.dbase.parse(
                sect  = sect,
                id    = row[0],
                mate  = mate,
                y     = row[1],
                z     = row[2],
                ttl   = row[3],
            )
            summary.append(data)

        # add
        self.core.dbase.addm(
            table = '[023:usec1:point]',
            cols  = cols,
            data  = summary,
        )
