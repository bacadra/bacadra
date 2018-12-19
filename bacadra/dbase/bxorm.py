'''
------------------------------------------------------------------------------
BCDR += ***** (b)acadra   (x)    (o)riented (r)elational (m)apped *****
==============================================================================

------------------------------------------------------------------------------
Copyright (C) 2018 <bacadra@gmail.com> <https://github.com/bacadra/bacadra>
Team members developing this package:
    - Sebastian Balcerowiak <asiloisad> <asiloisad.93@gmail.com>
------------------------------------------------------------------------------
'''

from ..cunit import cunit

c_unitle = cunit(1,{})
c_length = cunit(1,{'m':1}).primary()
c_pressu = cunit(1,{'kg':1, 'm':-1, 's':-2}).primary()
c_temper = cunit(1,{'K':1}).primary()
c_densin = cunit(1,{'kg':1,'m':-3}).primary()


class bcdr:
    '''
    bacadra orm
    '''
    def __repr__(self):
        out = ''
        for key,val in self.__dict__.items():
            out += str(key) + ' = ' + str(val) +'\n'
        return out[:-1]
        return str(self.__dict__).replace(', ',',\n')


#$$$ ____________ [010:mates] ______________________________________________ #

class bcdr_mates(bcdr):
    pass


#$$$$ ________________ [013:mates:steea] ___________________________________ #

class bcdr_mates_steea(bcdr_mates):
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


