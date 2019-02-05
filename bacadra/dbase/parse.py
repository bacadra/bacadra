'''
------------------------------------------------------------------------------
***** (parse) data *****
==============================================================================

------------------------------------------------------------------------------
Copyright (C) 2018 <bacadra@gmail.com> <https://github.com/bacadra>
Team members developing this package:
Sebastian Balcerowiak <asiloisad> <asiloisad.93@gmail.com>
------------------------------------------------------------------------------
'''

from ..cunit.cunit import cunit
from . import verrs


data = {
    'setts.id'         : {'t':[int,str,float]},
    'setts.ttl'        : {'t':[str]},

    'mates.umate.ρ_o'  : {'u':'kg m**-3'},
    'mates.umate.E_1'  : {'u':'Pa'},
    'mates.umate.G_1'  : {'u':'Pa'},
    'mates.umate.t_e'  : {'u':'°C**-1'},

    'usect.usecp.A'    : {'u':'m**2'},
    'usect.usecp.A_y'  : {'u':'m**2'},
    'usect.usecp.A_z'  : {'u':'m**2'},
    'usect.usecp.A_1'  : {'u':'m**2'},
    'usect.usecp.A_2'  : {'u':'m**2'},
    'usect.usecp.Ι_y'  : {'u':'m**4'},
    'usect.usecp.I_z'  : {'u':'m**4'},
    'usect.usecp.I_t'  : {'u':'m**4'},
    'usect.usecp.y_c'  : {'u':'m'},
    'usect.usecp.z_c'  : {'u':'m'},
    'usect.usecp.z_sc' : {'u':'m'},
    'usect.usecp.y_sc' : {'u':'m'},
    'usect.usecp.I_1'  : {'u':'m**4'},
    'usect.usecp.I_2'  : {'u':'m**4'},
    'usect.usecp.y_min': {'u':'m'},
    'usect.usecp.y_max': {'u':'m'},
    'usect.usecp.z_min': {'u':'m'},
    'usect.usecp.z_max': {'u':'m'},
    'usect.usecp.C_m'  : {'u':'m**6'},
    'usect.usecp.C_ms' : {'u':'m**4'},
    'usect.usecp.α'    : {'u':{}},
    'usect.usecp.u'    : {'u':'m'},
    'usect.usecp.m_g'  : {'u':'kg m**-1'},

    'usect.point.y'    : {'u':'m'},
    'usect.point.z'    : {'u':'m'},

    'usect.tsect.h'    : {'u':'m'},
    'usect.tsect.h_w'  : {'u':'m'},
    'usect.tsect.t_w'  : {'u':'m'},
    'usect.tsect.t_f_u': {'u':'m'},
    'usect.tsect.b_f_u': {'u':'m'},
    'usect.tsect.t_f_l': {'u':'m'},
    'usect.tsect.b_f_l': {'u':'m'},

    'geomf.nodes.x'    : {'u':'m'},
    'geomf.nodes.y'    : {'u':'m'},
    'geomf.nodes.z'    : {'u':'m'},

    'loads.cates.γ_u'  : {'u':'m'},
    'loads.cates.γ_f'  : {'u':'m'},
    'loads.cates.γ_a'  : {'u':'m'},
    'loads.cates.ψ_0'  : {'u':'m'},
    'loads.cates.ψ_1'  : {'u':'m'},
    'loads.cates.ψ_1s' : {'u':'m'},
    'loads.cates.ψ_2'  : {'u':'m'},
    'loads.cates.ttl'  : {'t':[str]},
}



def chdr(name, value):
    '''
    Check and drop. Validate value according to principles in data.
    '''

    # check type
    if 't' in data[name] and value!=None:
        if type(value) == cunit:
            type_value = type(cunit._value)
        else:
            type_value = type(value)

        if type_value not in data[name]['t']:
            verrs.BCDR_dbase_ERROR_Parse_Type(data[name]['t'])


    # checks for cunit
    if 'u' in data[name]:
        if type(value)==cunit and data[name]['u']!=None:
            value = value.drop(
                units  = data[name]['u'],
                fcover = True,
                system = 'si',
            )

    return value



#$ def get
def get(name, value):
    '''
    Return cunit object with given value and unit according to data.
    '''

    if type(value)!=cunit and data[name]['u']!=None:
        value = cunit.cc(value, data[name]['u'])
    return value




#$ def adm
def adm(cols, data, defs={}):
    '''
    Prepare data to multiadd command.
    '''

    ldict = []

    #save length of cols header
    cols_len = len(cols)

    # loop over data row in data argument
    for i in range(len(data)):

        # at first check consist of data, like length
        # TODO: implement it
        if len(data[i]) > cols_len:
            verrs.f1ParseMultiError(len(data[i]), cols_len, data[i])
        elif len(data[i]) < cols_len:
            data[i] = [data[i][j] if j<len(data[i]) else None for j in range(cols_len)]

        if type(data[i])==tuple:
            data[i] = list(data[i])

        idict = {}
        # loop over data in row
        for j in range(cols_len):

            # if factor of col is defined
            if cols[j]+'+f' in defs:
                # check that value is valid form to multiply
                if type(data[i][j]) in [float,int,cunit]:
                    data[i][j] *= defs[cols[j]+'+f']

            # if default value of col is defined then replace None value
            if cols[j]+'+d' in defs:
                # then check that val is undefined (None)
                if data[i][j] in [None]:
                    # if it is, then replace it with default value
                    data[i][j] = defs[cols[j]+'+d']

            idict.update({cols[j]:data[i][j]})

        ldict.append(idict)

    return ldict
    # return tuple(cols),ldict

