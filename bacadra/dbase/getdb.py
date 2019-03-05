'''
------------------------------------------------------------------------------
***** (get) (d)ata(b)ase data *****
==============================================================================

------------------------------------------------------------------------------
Copyright (C) 2018 <bacadra@gmail.com> <https://github.com/bacadra>
Team members developing this package:
+ Sebastian Balcerowiak <asiloisad> <asiloisad.93@gmail.com>
------------------------------------------------------------------------------
'''

#$ ######################################################################### #

from ..tools.fpack import mdata
from . import parse

#$ ____ def obj ____________________________________________________________ #

def obj(self, name, sub='a', where=None, unit=True, out='m', mode='r'):
    '''
    '''

    # cols: table, cols name, alias
    cols,data = eval(name+'_'+sub)(self, where=where, mode=mode)

    # convert sqlite3.row to dict depend on mode
    if mode=='r':
        data = dict(data)
    elif mode=='m':
        data = [dict(row) for row in data]

    # is user want object with units, then create it
    if unit:
        if mode=='r':
            for row in cols:
                data[row[2]] = parse.get(row[0], row[1], data[row[2]])

        elif mode=='m':
            for row in cols:
                for drow in data:
                    drow[row[2]] = parse.get(row[0], row[1], drow[row[2]])

    # return mdata object
    if out=='m':
        if   mode=='r': return mdata(data)
        elif mode=='m': return [mdata(row) for row in data]

    # return dict object
    elif out=='d':
        if   mode=='r': return data
        elif mode=='m': return data

    # there is no more options
    else:               raise ValueError()

#$ ____ def mates_umate_a __________________________________________________ #

def mates_umate_a(self, **kwargs):
    cols = [
        ['011:mates:umate','id' ,'id' ],
        ['011:mates:umate','ρ_o','ρ_o'],
        ['011:mates:umate','E_1','E_1'],
        ['011:mates:umate','v_1','v_1'],
        ['011:mates:umate','G_1','G_1'],
        ['011:mates:umate','t_e','t_e'],
        ['011:mates:umate','ttl','ttl'],
    ]

    data = self.core.dbase.get(
        table   = ['011:mates:umate'],
        formula = 2,
        where   = kwargs['where'],
        mode    = kwargs['mode'],
        cols    = cols,
    )

    return cols,data

#$ ____ def mates_steea_a __________________________________________________ #

def mates_steea_a(self, **kwargs):
    cols = [
        ['011:mates:umate' ,'id'      ,'id'         ] ,
        ['011:mates:umate' ,'ρ_o'     ,'ρ_o'        ] ,
        ['011:mates:umate' ,'E_1'     ,'E_1'        ] ,
        ['011:mates:umate' ,'v_1'     ,'v_1'        ] ,
        ['011:mates:umate' ,'G_1'     ,'G_1'        ] ,
        ['011:mates:umate' ,'t_e'     ,'t_e'        ] ,
        ['011:mates:umate' ,'ttl'     ,'ttl'        ] ,

        ['013:mates:steea' ,'grade'   ,'grade'      ] ,
        ['013:mates:steea' ,'t_max'   ,'t_max'      ] ,
        ['013:mates:steea' ,'f_yk'    ,'f_yk'       ] ,
        ['013:mates:steea' ,'f_uk'    ,'f_uk'       ] ,
        ['013:mates:steea' ,'E_a'     ,'E_a'        ] ,
        ['013:mates:steea' ,'ε_yk'    ,'ε_yk'       ] ,
        ['013:mates:steea' ,'ε_uk'    ,'ε_uk'       ] ,
        ['013:mates:steea' ,'γ_M0'    ,'γ_M0'       ] ,
        ['013:mates:steea' ,'γ_M1'    ,'γ_M1'       ] ,
        ['013:mates:steea' ,'γ_M2'    ,'γ_M2'       ] ,
        ['013:mates:steea' ,'γ_M3'    ,'γ_M3'       ] ,
        ['013:mates:steea' ,'γ_M4'    ,'γ_M4'       ] ,
        ['013:mates:steea' ,'γ_M5'    ,'γ_M5'       ] ,
        ['013:mates:steea' ,'γ_M6'    ,'γ_M6'       ] ,
        ['013:mates:steea' ,'γ_M_ser' ,'γ_M_ser'    ] ,
    ]

    data = self.get(
        table   = ['013:mates:steea'],
        formula = 2,
        where   = kwargs['where'],
        mode    = kwargs['mode'],
        cols    = cols,
        join    = [
            ['LEFT JOIN', '[011:mates:umate]', '[011:mates:umate].[id]=[013:mates:steea].[id]'],
        ],
    )

    return cols,data

#$ ######################################################################### #
