'''
------------------------------------------------------------------------------
bxorm += ***** (b)acadra   (x)    (o)riented (r)elational (m)apped *****
==============================================================================

------------------------------------------------------------------------------
Copyright (C) 2018 <bacadra@gmail.com> <https://github.com/bacadra/bacadra>
Team members developing this package:
    - Sebastian Balcerowiak <asiloisad> <asiloisad.93@gmail.com>
------------------------------------------------------------------------------
'''

import inspect
from ..cunit import cunit


c_unitle = cunit(1,{})
c_length = cunit(1,{'m':1})
c_pressu = cunit(1,{'kg':1, 'm':-1, 's':-2})
c_temper = cunit(1,{'K':1})
c_densin = cunit(1,{'kg':1,'m':-3})


class bxorm:
    '''
    bacadra orm
    '''

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    #$$ def --repr--
    def __repr__(self):
        '''
        Print only overwritten parameters and only not "private" atributes and methods.
        '''

        data = []
        for key in dir(self):
            if (key[0] != '_'):
                val = eval('self.' + key)
                if type(val) is str: val = '"' + str(val) + '"'
                data.append('> {:14s} : {}'.format(key, val))

        return '\n'.join(data) if len(data) > 0 else 'There are no overwritten atributes :-)'

#$$$ ____________ [010:mates] ______________________________________________ #

class bxorm_mates(bxorm):
    pass


#$$$$ ________________ [012:mates:conce] ___________________________________ #

class bxorm_mates_conce(bxorm_mates):
    def __init__(self, dbase, where):

        data = dbase.get(f'''
        SELECT

            [T1].[id],
            [T1].[grade],
            [T1].[f_ck],
            [T1].[f_ck_cube],
            [T1].[f_cm],
            [T1].[f_ctm],
            [T1].[f_ctk_005],
            [T1].[f_ctk_095],
            [T1].[E_cm],
            [T1].[ε_c1],
            [T1].[ε_cu1],
            [T1].[ε_c2],
            [T1].[ε_cu2],
            [T1].[n_c],
            [T1].[ε_c3],
            [T1].[ε_cu3],
            [T1].[γ_M],

            [T2].[ρ_o],
            [T2].[E_1],
            [T2].[v_1],
            [T2].[G_1],
            [T2].[t_e],
            [T2].[ttl]

        FROM  [012:mates:conce] as [T1]
        JOIN  [011:mates:umate] as [T2] on [T2].id = [T1].[id]
        WHERE [T1].{where}
        ''')[0]

        i =0; self.id        = data[i]
        i+=1; self.grade     = data[i]
        i+=1; self.f_ck      = data[i] * c_pressu
        i+=1; self.f_ck_cube = data[i] * c_pressu
        i+=1; self.f_cm      = data[i] * c_pressu
        i+=1; self.f_ctm     = data[i] * c_pressu
        i+=1; self.f_ctk_005 = data[i] * c_pressu
        i+=1; self.f_ctk_095 = data[i] * c_pressu
        i+=1; self.E_cm      = data[i] * c_pressu
        i+=1; self.ε_c1      = data[i] * c_unitle
        i+=1; self.ε_cu1     = data[i] * c_unitle
        i+=1; self.ε_c2      = data[i] * c_unitle
        i+=1; self.ε_cu2     = data[i] * c_unitle
        i+=1; self.n_c       = data[i] * c_unitle
        i+=1; self.ε_c3      = data[i] * c_unitle
        i+=1; self.ε_cu3     = data[i] * c_unitle
        i+=1; self.γ_M       = data[i] * c_unitle

        i+=1; self.ρ_o   = data[i] * c_densin
        i+=1; self.E_1   = data[i] * c_pressu
        i+=1; self.v_1   = data[i] * c_unitle
        i+=1; self.G_1   = data[i] * c_pressu
        i+=1; self.t_e   = data[i] * c_temper**-1
        i+=1; self.ttl   = data[i]



#$$$$ ________________ [013:mates:steea] ___________________________________ #

class bxorm_mates_steea(bxorm_mates):
    def __init__(self, dbase, where):

        data = dbase.get(f'''
        SELECT

            [T1].[id],
            [T1].[grade],
            [T1].[t_max],
            [T1].[f_yk],
            [T1].[f_uk],
            [T1].[E_a],
            [T1].[γ_M0],
            [T1].[γ_M1],
            [T1].[γ_M2],
            [T1].[γ_M3],
            [T1].[γ_M4],
            [T1].[γ_M5],
            [T1].[γ_M6],

            [T2].[ρ_o],
            [T2].[E_1],
            [T2].[v_1],
            [T2].[G_1],
            [T2].[t_e],
            [T2].[ttl]

        FROM  [013:mates:steea] as [T1]
        JOIN  [011:mates:umate] as [T2] on [T2].id = [T1].[id]
        WHERE [T1].{where}
        ''')[0]

        i =0; self.id    = data[i]
        i+=1; self.grade = data[i]
        i+=1; self.t_max = data[i] * c_length
        i+=1; self.f_yk  = data[i] * c_pressu
        i+=1; self.f_uk  = data[i] * c_pressu
        i+=1; self.E_a   = data[i] * c_pressu
        i+=1; self.γ_M0  = data[i] * c_unitle
        i+=1; self.γ_M1  = data[i] * c_unitle
        i+=1; self.γ_M2  = data[i] * c_unitle
        i+=1; self.γ_M3  = data[i] * c_unitle
        i+=1; self.γ_M4  = data[i] * c_unitle
        i+=1; self.γ_M5  = data[i] * c_unitle
        i+=1; self.γ_M6  = data[i] * c_unitle

        i+=1; self.ρ_o   = data[i] * c_densin
        i+=1; self.E_1   = data[i] * c_pressu
        i+=1; self.v_1   = data[i] * c_unitle
        i+=1; self.G_1   = data[i] * c_pressu
        i+=1; self.t_e   = data[i] * c_temper**-1
        i+=1; self.ttl   = data[i]