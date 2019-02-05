'''
------------------------------------------------------------------------------
***** (value)s 1d unit-sections *****
==============================================================================

------------------------------------------------------------------------------
Copyright (C) 2018 <bacadra@gmail.com> <https://github.com/bacadra>
Team members developing this package:
Sebastian Balcerowiak <asiloisad> <asiloisad.93@gmail.com>
------------------------------------------------------------------------------
'''

from ...dbase import parse
from ...tools.setts import settsmeta

#$ ____ class setts ________________________________________________________ #

class setts(settsmeta):
    _ldef_id = None


#$ ____ class value ________________________________________________________ #

class value:

    # class setts
    setts = setts('setts', (setts,), {})

    #$$ def __init__
    def __init__(self, core):

        # project object
        self.core = core

        # local setts
        self.setts = self.setts('setts',(),{})


    def add(self, id=None, mate=None, A=None, A_y=None, A_z=None, A_1=None, A_2=None, I_y=None, I_z=None, I_t=None, y_c=None, z_c=None, y_sc=None, z_sc=None, I_1=None, I_2=None, y_min=None, y_max=None, z_min=None, z_max=None, C_m=None, C_ms=None, α=None, u=None, m_g=None, ttl=None, subcl=None):

        # drop units to si
        id    = parse.chdr('setts.id'         , id   )
        A     = parse.chdr('usect.usecp.A'    , A    )
        A_y   = parse.chdr('usect.usecp.A_y'  , A_y  )
        A_z   = parse.chdr('usect.usecp.A_z'  , A_z  )
        A_1   = parse.chdr('usect.usecp.A_1'  , A_1  )
        A_2   = parse.chdr('usect.usecp.A_2'  , A_2  )
        I_y   = parse.chdr('usect.usecp.Ι_y'  , I_y  )
        I_z   = parse.chdr('usect.usecp.I_z'  , I_z  )
        I_t   = parse.chdr('usect.usecp.I_t'  , I_t  )
        y_c   = parse.chdr('usect.usecp.y_c'  , y_c  )
        z_c   = parse.chdr('usect.usecp.z_c'  , z_c  )
        z_sc  = parse.chdr('usect.usecp.z_sc' , z_sc )
        y_sc  = parse.chdr('usect.usecp.y_sc' , y_sc )
        I_1   = parse.chdr('usect.usecp.I_1'  , I_1  )
        I_2   = parse.chdr('usect.usecp.I_2'  , I_2  )
        y_min = parse.chdr('usect.usecp.y_min', y_min)
        y_max = parse.chdr('usect.usecp.y_max', y_max)
        z_min = parse.chdr('usect.usecp.z_min', z_min)
        z_max = parse.chdr('usect.usecp.z_max', z_max)
        C_m   = parse.chdr('usect.usecp.C_m'  , C_m  )
        C_ms  = parse.chdr('usect.usecp.C_ms' , C_ms )
        α     = parse.chdr('usect.usecp.α'    , α    )
        u     = parse.chdr('usect.usecp.u'    , u    )
        m_g   = parse.chdr('usect.usecp.m_g'  , m_g  )

        # overwrite last defined unit section 1d
        self.setts._ldef_id = id

        # if mate is not defined then use last one material
        mate = self.core.mates.umate.setts.check_loc('_ldef_id', mate)

        m_g = self._fill(m_g=m_g, A=A, mate=mate)

        self.core.dbase.add(
            mode  = 'r',
            table = '[021:usecp:value]',
            cols  = ['id','mate','A','A_y','A_z','A_1','A_2','I_y','I_z','I_t','y_c','z_c','z_sc','y_sc','I_1','I_2','y_min','y_max','z_min','z_max','C_m','C_ms','α','u','m_g','subcl', 'ttl'],
            data = (id,mate,A,A_y,A_z,A_1,A_2,I_y,I_z,I_t,y_c,z_c,z_sc,y_sc,I_1,I_2,y_min,y_max,z_min,z_max,C_m,C_ms,α,u,m_g,subcl,ttl)
        )


    def _fill(self, **data):
        '''
        Fill properties of cross-section.
        '''

        # if weight is not defined and mates is def
        if data['m_g'] is None and data['mate'] is not None:

            # get material prop from database
            ρ_o = self.core.dbase.get('s','[011:mates:umate]','ρ_o',
                f'id={data["mate"]}')

            # ciezar jednostkowy przekroju
            m_g = data['A'] * ρ_o

        return m_g


    def echo(self, mode='a+', where=None):

        if 'a' in mode:
            data = self.core.dbase.get(
                mode  = 'm',
                table = '[021:usecp:value]',
                cols  ='id,mate,A,A_y,A_z,A_1,A_2,I_y,I_z,I_t,y_c,z_c,z_sc,y_sc,I_1,I_2,y_min,y_max,z_min,z_max,C_m,C_ms,α,u,m_g,ttl,subcl',
                where = where,
            )

            if not data: return

            self.core.pinky.rstme.table(
                caption= 'Cross-sections one dimmensional',
                wrap   = [True,False,False,False,False,False,False],
                width  = [True,8,8,8,9,9,8],
                halign = ['l','c','c','c','r','r','c'],
                valign = ['m','u','u','u','u','u','u'],
                dtype  = ['t','e','e','e','e','e','e'],
                header = [
                    ['id'   ,'subcl','mate' ,'ttl'    ],
                    ['A'    ,'I_t'  ,'C_m'  ,'C_ms'   ],
                    ['A_y'  ,'A_z'  ,'A_1'  ,'A_2'    ],
                    ['I_y'  ,'I_z'  ,'I_1'  ,'I_2'    ],
                    ['y_c'  ,'z_c'  ,'y_sc' ,'z_sc'   ],
                    ['y_min','y_max','z_min','z_max'  ],
                    ['α'    ,'u'    ,'m_g'            ],
                ],
                data   = [[

                    [row['id']   ,row['subcl'],row['mate'] ,row['ttl']  ],
                    [row['A']    ,row['I_t']  ,row['C_m']  ,row['C_ms'] ],
                    [row['A_y']  ,row['A_z']  ,row['A_1']  ,row['A_2']  ],
                    [row['I_y']  ,row['I_z']  ,row['I_1']  ,row['I_2']  ],
                    [row['y_c']  ,row['z_c']  ,row['y_sc'] ,row['z_sc'] ],
                    [row['y_min'],row['y_max'],row['z_min'],row['z_max']],
                    [row['α']    ,row['u']    ,row['m_g']               ],

                ] for row in data],
                precision = 2,
            )

            if not '+' in mode: return

            self.core.pinky.rstme.table(
                wrap   = [False, False, False, True],
                width  = [23, 6, 2,True],
                halign = ['r','l','c','l'],
                valign = ['u','u','u','u'],
                dtype  = ['t','t','t','t'],
                data   = [
                    ['id'   ,''      ,'-','identificator'],
                    ['subcl',''      ,'-',''],
                    ['mate' ,''      ,'-',''],
                    ['ttl'  ,''      ,'-','title'],
                    ['A'    ,'[m2]'  ,'-','section area'],
                    ['I_t'  ,'[m4]'  ,'-','torsional moment of inertia'],
                    ['C_m'  ,'[m6]'  ,'-','warping resistance'],
                    ['C_ms' ,'[m4]'  ,'-','warping shear resistance'],
                    ['A_y,A_z'  ,'[m2]'  ,'-',
                        'transferse shear deformation area along y axis'],
                    ['A_1,A_2'  ,'[m2]'  ,'-',
                        'transferse shear deformation area along principle axis'],
                    ['I_y,I_z'  ,'[m4]'  ,'-',
                        'bending moment of inertia via center local axis'],
                    ['I_1,I_2'  ,'[m4]'  ,'-',
                        'bending moment of inertia via principal axis'],
                    ['y_c,z_c','[m]'   ,'-','ordinate of elastic centroid'],
                    ['y_sc,z_sc' ,'[m]'   ,'-','ordinate of shear centre'],
                    ['y_min,y_max,z_min,z_max','[m]'   ,'-','extreme coordinates relative to centroid'],
                    ['α'    ,'[1]'   ,'-',''],
                    ['u'    ,'[m]'   ,'-',''],
                    ['m_g'  ,'[kg/m]','-',''],
                ],
                border = False,
            )








    #$$ def add
    # def add(self, id=None, mate=None, A=None, A_y=None, A_z=None, I_t=None, I_ω=None, I_y=None, I_z=None, I_ξ=None, I_η=None, I_p=None, u=None, m_g=None, y_gc=None, z_gc=None, y_sc=None, z_sc=None, α=None, ttl=None, _subcl=None):
    #
    #     self.core.mdata.setts.set({'_usec1_ldef':id})
    #     # overwrite last defined unit section 1d
#
#         # if mate is not defined then use last one material
#         if mate is None:
#             mate = self.core.mdata.setts.get('_mates_ldef')
#
#         m_g = self._fill_prop(m_g=m_g,A=A,mate=mate)
#
#         # parse universal units section 1d data
#         cols,data = self.core.dbase.parse(
#             id    = id,
#             mate  = mate,
#             A     = A,
#             A_y   = A_y,
#             A_z   = A_z,
#             I_t   = I_t,
#             I_ω   = I_ω,
#             I_y   = I_y,
#             I_z   = I_z,
#             I_ξ   = I_ξ,
#             I_η   = I_η,
#             I_p   = I_p,
#             u     = u,
#             m_g   = m_g,
#             ttl   = ttl,
#             y_gc  = y_gc,
#             z_gc  = z_gc,
#             y_sc  = y_sc,
#             z_sc  = z_sc,
#             α     = α,
#             subcl = _subcl,
#         )
#
#         # add universal unit section 1d data
#         self.core.dbase.add(
#             table = '[021:usec1:value]',
#             cols  = cols,
#             data  = data,
#         )
#
#     def _fill_prop(self, **kwargs):
#         m_g  = kwargs['m_g']
#         A    = kwargs['A']
#         mate = kwargs['mate']
#
#         if m_g is None and mate is not None:
#             # get material prop from database
#             ρ_o = self.core.dbase.get(f'SELECT [ρ_o] FROM [011:mates:umate] WHERE [id]={mate}')[0][0]
#             # ciezar jednostkowy przekroju
#             m_g = A * ρ_o
#
#         return m_g