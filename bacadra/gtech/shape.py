import numpy
import pandas as pd

from ..pinky.pinky import pinky
from ..cunit.ce import *
from ..cunit.cmath import *


class soildb:
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

    def __init__(self, soil=None, **kwargs):
        # try:
            # self.__dict__.update(self._data[soil])
        # except:
            # pass
        self.__dict__.update({'soil':soil})
        self.__dict__.update(kwargs)

    def __repr__(self):
        return str(self.__dict__)

    # @classmethod
    # def set(self, name, **kwargs):
    #     self._data.update({name:kwargs})
    #
    # @classmethod
    # def get(self, name):
    #     return self._data[name]

class layer:
    def __init__(self, no=None, soil=None, h=None, I_D=None, I_L=None, w_n=None, γ=None, ϕ_u=None, C_u=None, E_0=None, M_0=None, β=None):
        self.no  = no
        self.soil= soil
        self.h   = h
        self.I_D = I_D
        self.I_L = I_L
        self.w_n = w_n
        self.γ   = γ
        self.ϕ_u = ϕ_u
        self.C_u = C_u
        self.E_0 = E_0
        self.M_0 = M_0
        self.β   = β

    def __repr__(self):
        return str(self.__dict__)



class bore:
    def __init__(self, no=0):
        self._lay_no = 0
        self._data = []

    def create(self, soil=None, h=None, I_D=None, I_L=None, w_n=None, γ=None, ϕ_u=None, C_u=None, E_0=None, M_0=None, β=None):

        if h == True:
            h = 1*km

        self._lay_no += 1

        if type(soil) is soildb:
            nsoil = soil.__dict__.copy()
            nsoil.update({'no':self._lay_no})
            if h:     nsoil.update({'h'  :h})
            if I_D:   nsoil.update({'I_D':I_D})
            if I_L:   nsoil.update({'I_L':I_L})
            if w_n:   nsoil.update({'w_n':w_n})
            if γ:     nsoil.update({'γ'  :γ})
            if ϕ_u:   nsoil.update({'ϕ_u':ϕ_u})
            if C_u:   nsoil.update({'C_u':C_u})
            if E_0:   nsoil.update({'E_0':E_0})
            if M_0:   nsoil.update({'M_0':M_0})
            if β:     nsoil.update({'β'  :β})

            self._data.append(layer(**nsoil))

        else:
            self._data.append(layer(
                no   = self._lay_no,
                soil = soil,
                I_D  = I_D,
                I_L  = I_L,
                h    = h,
                γ    = γ,
                ϕ_u  = ϕ_u,
                C_u  = C_u
            ))

    def get(self, height):
        sumH = 0
        for lay in self:
            sumH += lay.h
            if sumH >= height:
                return lay

    def abs_hz(self, layer):
        firsabs = 0
        for i in range(layer.no):
            firsabs += self._data[i].h
        return firsabs

    def range(self, hmin, hmax=1*km):
        firs = self.get(hmin)
        firsabs = self.abs_hz(firs)

        last = self.get(hmax)
        lastabs = self.abs_hz(last)

        new_data = []
        for i in range(last.no - firs.no + 1):
            if i == 0:
                if firsabs - hmin == 0 :
                    pass
                else:
                    new_data.append(self.copylay(firs.no))
                    if last.no - firs.no + 1 == 1:
                        new_data[-1].h = hmax - hmin
                    else:
                        new_data[-1].h = firsabs - hmin

            elif i == last.no - firs.no:
                new_data.append(self.copylay(last.no))
                new_data[-1].h = hmax - lastabs + last.h

            else:
                new_data.append(self._data[firs.no-1+i])
            nbore = bore(no=self._lay_no)
            nbore._data = data=new_data

        return nbore
        # last = self.get(hmax)


    def copylay(self, no):
        return layer(**self._data[no-1].__dict__)

    def __repr__(self):
        text = ''
        for lay in self:
            text += str(lay) + '\n'
        return text

    def __iter__(self):
        self._count = 0
        return self

    def __next__(self):
        if self._count == len(self._data):
            raise StopIteration
        self._count += 1
        return self._data[self._count-1]
