'''
------------------------------------------------------------------------------
BCDR += ***** (v)arious (err)or(s) *****
==============================================================================

------------------------------------------------------------------------------
Copyright (C) 2018 <bacadra@gmail.com> <https://github.com/bacadra>
Team members developing this package:
    - Sebastian Balcerowiak <asiloisad> <asiloisad.93@gmail.com>
------------------------------------------------------------------------------
'''

class CunitError(Exception):
    '''
    General cunit exception.
    '''
    pass



class CunitIncompatibleErorr(Exception):
    pass

def fCunitIncompatibleErorr(val1, val2, name=None):
    '''
    Value sended to function should be after primary methods. In example val1="m" and val2="mm" will return error!
    '''
    if val1._units != val2._units:
        raise CunitIncompatibleErorr(f'Execution "{name}" failed: {val1._units} and {val2._units} can\'t be treat together')


def f2CunitIncompatibleErorr(val1, name=None):
    '''
    A function can take input data only without units.
    '''
    if val1._units != {}:
        raise CunitIncompatibleErorr(f'The function "{name}" failed, because they can\'t take value with units!')






class CunitUndefinedOperationError(Exception):
    pass

def fCunitUndefinedOperationError(name, val1, val2):
    '''
    User can try use method with two different types, but name doing can be not defined for this types! Then raise exception.
    '''
    raise CunitUndefinedOperationError(f'Operations "{name}" between types {type(val1)} and {type(val2)} is not defined')




class CunitSystemError(Exception):
    pass

def f0CunitSystemError(text):
    raise CunitSystemError(text)

def f1CunitSystemError(system, units):
    '''
    Function return CunitSystemError with with info, that units does not exist in current database.
    '''
    raise CunitSystemError(f'Unit <{units}> does not exists in <{system}> system \nTip: You can add it by .add method')

def f2CunitSystemError(system):
    '''
    '''
    raise CunitSystemError(f'system was typed as <{system}> type. cunit.primary provide interface only for None, str and dict types')

def f3CunitSystemError(system, units):
    '''
    Function return CunitSystemError with with info, that units already exist in current database.
    '''
    raise CunitSystemError(f'Unit <{units}> does already exists in <{system}> system \nTip: You can overwrite it by overwrite=True argument')


class CunitCoverError(Exception):
    pass

def f1CunitCoverError(val):
    '''
    '''
    raise CunitCoverError(f'Unit is not full covere by new one! You need multiply new unit by: {val} \n Tip: You can perform non-full cover by fcover=False')


