#$ **** module soils **** __________________________________________________ #

#$$ ________ import ________________________________________________________ #

from ..cunit.ce import *
from ..cunit.cmath import *

import numpy  as np
import pandas as pd


#$ ____ class soils ________________________________________________________ #

class soils:
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

    #$$ def clear
    def clear(self):
        self.dbase.exes(
            "DELETE FROM [011:mate:gene];"
            "DELETE FROM [016:mate:soil];"
        )

    #$$ def add
    def add(self,
    # parametry ogolne
    id=None, name=None, ρ=None, E_1=None, v_1=None, texp=None, ttl=None,

    # parametry soil
    soil=None, I_DL=None, w_n=None, ϕ_u=None, c_u=None, β=None, E_0=None, M_0=None):

        # TODO: E_0 i M_0 sa niewykorzystane
        A,B,C = self.dbase.parse(id=id, name=name, rho=ρ, E_1=E_1, v_1=v_1, texp=texp, ttl=ttl)

        self.dbase.exe("INSERT INTO [011:mates:umate]" + A + " VALUES" + B ,C)

        A,B,C = self.dbase.parse(soil=soil, I_DL=I_DL, w_n=w_n, phi_u=ϕ_u, c_u=c_u, beta=β)

        self.dbase.exe("INSERT INTO [017:mates:soile]" + A + " VALUES" + B ,C)



#$ ____ class borep ________________________________________________________ #

class borep:
    #$$ def --init--
    def __init__(self, dbase, pinky, pvars):
        self.dbase = dbase
        self.pinky = pinky
        self.pvars = pvars

    #$$ def add
    def add(self, id=None, name=None, soil=None, h=None, ttl=None):
        if h == True:
            h = 1*km

        i = 0
        for i in range(len(soil)):
            if type(h[i]) == cunit: h[i] = h[i].drop()

            self.dbase.exe(
            "INSERT INTO [311:gtech:borep]([id],[name],[i],[soil],[h],[ttl]) "
            "VALUES(?,?,?,?,?,?)"
            , (id, name, i+1, soil[i], h[i], ttl))



    # #$$ def get
    # def get(self, id, print=False):
    #     self.dbase.exe(
    #     "SELECT * FROM [311:gtech:borep]"
    #     "LEFT JOIN [016:mate:soil] ON [211:bore:gene].[soil] = [016:mate:soil].[id]"
    #     "WHERE [211:bore:gene].[id]=(?) ORDER BY [211:bore:gene].[i]"
    #     , (id,))
    #     res = self.dbase.db.fetchall()
    #
    #     if print:
    #         for lay in res:
    #             print(lay)
    #     else:
    #         return res

        # self.dbase.exe(
        # "SELECT [id],[name],[i],[soil],[h],[title] FROM [211:bore:gene] WHERE [id]=(?) ORDER BY [i]"
        # , (id,))
        # res = self.dbase.db.fetchall()
        # return res

    #$$ def check_layer
    def check_layer(self, id, h_z):
        if type(h_z) == cunit: h_z = h_z.drop()

        self.dbase.exe(
        "SELECT [id],[name],[i],[soil],[h],[title] FROM [211:bore:gene] WHERE [id]=(?) ORDER BY [i]"
        , (id,))
        res = self.dbase.db.fetchall()

        sumH = 0
        for lay in res:
            sumH += lay[4]
            if sumH >= h_z:
                return lay

    #$$ def abs_floor_hz
    def abs_floor_hz(self, id, i):
        self.dbase.exe(
        "SELECT [h] FROM [211:bore:gene] WHERE [id]=(?) ORDER BY [i]"
        , (id,))
        res = self.dbase.db.fetchall()

        firsabs = 0
        for j in range(i):
            firsabs += res[j][0]
        return firsabs

    #$$ def range_pile
    def range_pile(self, id, h_min, h_max=1*km):
        if type(h_min) == cunit: h_min = h_min.drop()
        if type(h_max)  == cunit: h_max = h_max.drop()

        self.dbase.exe(
        "SELECT [id],[name],[i],[soil],[h],[title] FROM [211:bore:gene] WHERE [id]=(?) ORDER BY [i]"
        , (id,))
        res = self.dbase.db.fetchall()

        # first_layer = self.abs_floor_hz(h_min)
        # last_layer  = self.abs_floor_hz(h_max)

        lay_now = []
        h_now = 0
        for lay in res:
            h_now += lay[4]
            if h_min < h_now < h_max:
                lay_now.append(lay)

        if len(lay_now)==0:
            layer_h_min = self.check_layer(no, h_min)
            layer_h_min = list(layer_h_min)
            layer_h_min[4] = h_max - h_min
            layer_h_min = tuple(layer_h_min)
            return [layer_h_min]

        elif len(lay_now)==1:
            layer_h_min = list(lay_now[0])

            layer_h_min[4] = self.abs_floor_hz(     layer_h_min[0],layer_h_min[2]) - h_min

            layer_h_min = tuple(layer_h_min)

            layer_h_max = list(self.check_layer(no, h_max))
            layer_h_max[4] = h_max - self.abs_floor_hz(     layer_h_min[0],layer_h_min[2])

            return [layer_h_min, layer_h_max]

        else:
            layer_h_min = list(lay_now[0])

            layer_h_min[4] = self.abs_floor_hz(     layer_h_min[0],layer_h_min[2]) - h_min

            layer_h_min = tuple(layer_h_min)

            layer_h_max = list(self.check_layer(no, h_max))
            layer_h_max[4] = layer_h_max[4] - (self.abs_floor_hz(     layer_h_max[0],layer_h_max[2]) - h_max)

            lay_now[0] = layer_h_min
            lay_now.append(layer_h_max)

            return lay_now

#$ ____ class sbank ________________________________________________________ #

class sbank:
    _data = {
        'KW':
            {'name':'KW',
             'fullname':'zwietrzelina'},
        'KWg':
            {'name':'KWg',
            'fullname':'zwietrzelina gliniasta'},
        'KR':
            {'fullname':'rumosz'},
        'KRg':
            {'fullname':'rumosz gliniasty'},
        'KO':
            {'fullname':'otoczaki'},
        'Ż':
            {'fullname':'żwir'},
        'Żg':
            {'fullname':'żwir gliniasty'},
        'Po':
            {'fullname':'posółka'},
        'Pog':
            {'fullname':'pospółka gliniasta'},
        'Pr':
            {'fullname':'Piasek gruby'},
        'Ps':
            {'fullname':'Piasek średni'},
        'Pd':
            {'fullname':'Piasek drobny'},
        'Pπ':
            {'fullname':'Piasek pylasty'},
        'Pg':
            {'fullname':'piasek gliniasty'},
        'πp':
            {'fullname':'pył piaszczysty'},
        'π':
            {'fullname':'pył'},
        'Gp':
            {'fullname':'glina piaszczysta'},
        'G':
            {'fullname':'glina'},
        'Gπ':
            {'fullname':'glina pylasta'},
        'Gpz':
            {'fullname':'glina piaszczysta zwięzła'},
        'Gz':
            {'fullname':'glina zwięzła'},
        'Gπz':
            {'fullname':'glina pylasta zwięzła'},
        'Ip':
            {'fullname':'ił piaszczysty'},
        'I':
            {'fullname':'ił'},
        'Iπ':
            {'fullname':'ił pylasty'},
    }
