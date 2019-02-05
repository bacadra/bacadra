'''
------------------------------------------------------------------------------
***** (m)apped (data)base *****
==============================================================================

------------------------------------------------------------------------------
Copyright (C) 2018 <bacadra@gmail.com> <https://github.com/bacadra>
Team members developing this package:
Sebastian Balcerowiak <asiloisad> <asiloisad.93@gmail.com>
------------------------------------------------------------------------------
'''

from ..tools.color import colored
from ..cunit.cunit import cunit
from .parse import data

# mapped object data
class odata:

    def __init__(self, obj, uname={}, mapname=None):
        self.__mapname__ = mapname
        self.__keys__ = obj.keys()
        for key in self.__keys__:
            if key in uname and uname[key] in data and 'u' in data[uname[key]] and type(obj[key]) in [int, float]:
                setattr(self, key, cunit.cc(obj[key], data[uname[key]]['u']))
            else:
                setattr(self, key, obj[key])

    def __repr__(self):
        if self.__mapname__:
            pdata = [colored('---------------------------------------------------------------------------\n''***** bacadra object atributes: "'+self.__mapname__+'" *****', 'magenta')]
        else:
            pdata = [colored('---------------------------------------------------------------------------\n''***** bacadra object atributes *****', 'magenta')]

        for key in self.__keys__:
            val = getattr(self, key)
            if type(val) is str: val = "'" + str(val) + "'"
            pdata.append('> {:14s} : {}'.format(key, val))

        return '\n'.join(pdata)


# mapped dictonary data
def ddata(obj, uname={}):
    ndata = {}
    for key in obj.keys():
        if key in uname and uname[key] in data and 'u' in data[uname[key]] and type(obj[key]) in [int, float]:
            ndata.update({key: cunit.cc(obj[key], data[uname[key]]['u'])})
        else:
            ndata.update({key: obj[key]})
    return ndata


# create object
def obj(self, name, where=None, cols=None, unit=None, mode=None, formula=None, mapto=None):
    if mode    == None : mode    = 'r'
    if unit    == None : unit    = True
    if formula == None : formula = 2
    if mapto   == None : mapto   = 'o'


    if name=='mates.umate-1':
        data = self.get(
            formula = formula,
            where   = where,
            mode    = mode,
            table   = '[011:mates:umate]',
            join    = None,
            cols    = cols,
        )
        uname = {
            'ρ_o':'mates.umate.ρ_o',
            'E_1':'mates.umate.E_1',
            'G_1':'mates.umate.G_1',
            't_e':'mates.umate.t_e',
        } if unit==True else {}


    elif name=='usecp.tsect-1':
        data = self.get(
            formula = formula,
            where   = where,
            mode    = mode,
            table   = '[025:usecp:tsect] as tsect',
            join    = [
                'LEFT JOIN [021:usecp:value] AS value ON value.id=tsect.id',
                'LEFT JOIN [011:mates:umate] AS umate ON umate.id=value.mate'
            ],
            cols    = [
                'tsect.id    as id',
                'tsect.h     as h',
                'tsect.h_w   as h_w',
                'tsect.t_w   as t_w',
                'tsect.t_f_u as t_f_u',
                'tsect.b_f_u as b_f_u',
                'tsect.t_f_l as t_f_l',
                'tsect.b_f_l as b_f_l',

                'value.mate  as mate',
                'value.A     as A',
                'value.A_y   as A_y',
                'value.A_z   as A_z',
                'value.A_1   as A_1',
                'value.A_2   as A_2',
                'value.I_y   as I_y',
                'value.I_z   as I_z',
                'value.I_t   as I_t',
                'value.y_c   as y_c',
                'value.z_c   as z_c',
                'value.y_sc  as y_sc',
                'value.z_sc  as z_sc',
                'value.I_1   as I_1',
                'value.I_2   as I_2',
                'value.y_min as y_min',
                'value.y_max as y_max',
                'value.z_min as z_min',
                'value.z_max as z_max',
                'value.C_m   as C_m',
                'value.C_ms  as C_ms',
                'value.α     as α',
                'value.u     as u',
                'value.m_g   as m_g',

                'umate.ρ_o  as ρ_o',
                'umate.E_1  as E_1',
                'umate.v_1  as v_1',
                'umate.G_1  as G_1',
                'umate.t_e  as t_e',
            ],
        )
        uname = {
            'ρ_o':'mates.umate.ρ_o',
            'E_1':'mates.umate.E_1',
            'G_1':'mates.umate.G_1',
            't_e':'mates.umate.t_e',
        } if unit==True else {}

    else:
        raise ValueError()



    if mapto=='o':

        if mode=='r':
            return odata(data, uname, name)

        elif mode=='m':
            return [odata(obj, uname, name) for obj in data]

        else:
            raise ValueError()

    elif mapto=='d':

        if mode=='r':
            return ddata(data, uname)

        elif mode=='m':
            return [ddata(row, uname) for row in data]

        else:
            raise ValueError()

    else:
        raise ValueError()

