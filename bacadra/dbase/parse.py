'''
------------------------------------------------------------------------------
***** (parse) data *****
==============================================================================

------------------------------------------------------------------------------
Copyright (C) 2018 <bacadra@gmail.com> <https://github.com/bacadra>
Team members developing this package:
+ Sebastian Balcerowiak <asiloisad> <asiloisad.93@gmail.com>
------------------------------------------------------------------------------
'''

from ..cunit.cunit import cunit
from .dlist import chk
from . import verrs

#$ ____ def chdr ____________________________________________________________ #

def chdr(t, n, v):
    '''
    Check and drop. Validate value according to principles in chk.
    t -- table name
    n -- columns name
    v -- value
    '''

    # check type
    if v==None: return

    # first resolve cunit
    if type(v)==cunit:
        type_value = type(v._value)
    else:
        type_value = type(v)

    if chk[t][n]['c']!=None and type_value not in chk[t][n]['c']:
        verrs.BCDR_dbase_ERROR_Parse_Type(chk[t][n]['c'])


    # checks for cunit
    if type(v)==cunit and chk[t][n]['u']!=None:
        v = v.drop(
            units  = chk[t][n]['u'],
            fcover = True,
            system = 'si',
        )

    return v

#$ ____ def get _____________________________________________________________ #

def get(t, n, v=None):
    '''
    Return cunit object with given value and unit according to chk.
    '''

    if v==None: return v

    u = chk[t][n]['u']

    return cunit(v, u) if u!=None else v






#$ ____ def adm _____________________________________________________________ #

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

