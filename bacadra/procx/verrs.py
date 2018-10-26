
# from .units import Procx


class ProcxError(Exception):
    '''
    General Procx exception.
    '''
    pass



class ProcxIncompatibleErorr(Exception):
    pass

def fProcxIncompatibleErorr(val1, val2, name=None):
    '''
    Value sended to function should be after primary methods. In example val1="m" and val2="mm" will return error!
    '''
    if val1._units != val2._units:
        raise ProcxIncompatibleErorr(f'Execution "{name}" failed: {val1._units} and {val2._units} can\'t be treat together')



class ProcxUndefinedOperationError(Exception):
    pass

def fProcxUndefinedOperationError(name, val1, val2):
    '''
    User can try use method with two different types, but name doing can be not defined for this types! Then raise exception.
    '''
    raise ProcxUndefinedOperationError(f'Operations "{name}" between types {type(val1)} and {type(val2)} is not defined')




class ProcxSystemError(Exception):
    pass

def f0ProcxSystemError(text):
    raise ProcxSystemError(text)

def f1ProcxSystemError(system, units):
    '''
    Function return ProcxSystemError with with info, that units does not exist in current database.
    '''
    raise ProcxSystemError(f'Unit <{units}> does not exists in <{system}> system \nTip: You can add it by .add method')

def f2ProcxSystemError(system):
    '''
    '''
    raise ProcxSystemError(f'system was typed as <{system}> type. Procx.primary provide interface only for None, str and dict types')

def f3ProcxSystemError(system, units):
    '''
    Function return ProcxSystemError with with info, that units already exist in current database.
    '''
    raise ProcxSystemError(f'Unit <{units}> does already exists in <{system}> system \nTip: You can overwrite it by overwrite=True argument')


class ProcxCoverError(Exception):
    pass

def f1ProcxCoverError(val):
    '''
    '''
    raise ProcxCoverError(f'Unit is not full covere by new one! You need multiply new unit by: {val} \n Tip: You can perform non-full cover by fcover=False')


