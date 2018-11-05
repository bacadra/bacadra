class umate:
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
    def add(self,
    # parametry ogolne
    id=None, ρ_o=None, E_1=None, v_1=None, G_1=None, t_e=None, ttl=None, _subcl=None):

        # overwrite last defined material
        self.core.mdata.setts.set({'_mates_ldef':id})

        # resolve coparamaters
        E_1,v_1,G_1 = self._linear_EvG(E_1, v_1, G_1)

        # parse data do univeral material
        cols,data = self.core.dbase.parse(
            id    = id,
            ρ_o   = ρ_o,
            E_1   = E_1,
            v_1   = v_1,
            G_1   = G_1,
            t_e   = t_e,
            ttl   = ttl,
            subcl = _subcl,
        )

        # add universal material
        self.core.dbase.add(
            table = '[011:mates:umate]',
            cols  = cols,
            data  = data,
        )


    def _linear_EvG(self, E, v, G):
        '''
        Calc third value of material constant
        '''

        if E and v and not G:
            G = (E) / (2 * (1 + v))

        elif E and not v and G:
            v = E/G * 0.5 - 1

        elif not E and v and G:
            E = G * (2 * (1 + v))

        return E,v,G

    def echo(self, mode='1', save=False, inherit=False):
        data = self.core.dbase.get('''
            SELECT
                [id],
                [ρ_o],
                [E_1],
                [v_1],
                [G_1],
                [t_e],
                [ttl]
            FROM [011:mates:umate]
        ''')

        self.core.pinky.rstme.table(
            caption= 'General material properties',
            wrap   = [False, False, False, False, False, False, True],
            width  = [True,True,True,True,True,True,True],
            halign = ['l','c','c','c','c','c','l'],
            valign = ['u','u','u','u','u','u','u'],
            dtype  = ['t','e','e','e','e','e','t'],
            header = ['id','ρ_o','E_1','v_1','G_1','t_e','ttl'],
            data   = data,
            precision = 2,
            inherit = inherit,
        )

        self.core.pinky.rstme.table(
            wrap   = [False, False, False, True],
            width  = [8, 8, 2,True],
            halign = ['r','l','c','l'],
            valign = ['u','u','u','u'],
            dtype  = ['t','t','t','t'],
            data   = [
                ['id' , ''       , '-', 'identificator'   ],
                ['ρ_o', '[kg/m3]', '-', 'densinity'       ],
                ['E_1', '[N/m2]' , '-', 'Young\'s modulus'],
                ['v_1', '[1]'    , '-', 'poisson ratio'   ],
                ['G_1', '[1]'    , '-', 'Kirchoff modulus'],
                ['t_e', '[1/°C]' , '-', 'Kirchoff modulus'],
                ['ttl', ''       , '-', 'title'           ],
            ],
            border = False,
        )

