'''
------------------------------------------------------------------------------
***** (v)arious (err)or(s) *****
==============================================================================

------------------------------------------------------------------------------
Copyright (C) 2018 <bacadra@gmail.com> <https://github.com/bacadra>
Team members developing this package:
Sebastian Balcerowiak <asiloisad> <asiloisad.93@gmail.com>
------------------------------------------------------------------------------
'''

from ..tools.verre  import BCDR_Error,BCDR_WARN,BCDR_Info


#$ ____ errors _____________________________________________________________ #

class BCDR_cunit_Error(BCDR_Error):
    pass


def BCDR_cunit_Error_General(text):
    '''
    General warning, can print any text message.
    '''
    raise BCDR_cunit_Error(text)


def BCDR_cunit_Error_Incompatible(val1, val2, name=None):
    '''
    Value sended to function should be after primary methods. In example val1="m" and val2="mm" will return error!
    '''
    if val1._units != val2._units:
        raise BCDR_cunit_Error(
            f'Execution "{name}" failed: {val1._units} and {val2._units} can\'t be treat together.'
        )


def BCDR_cunit_Error_Undefined_Operator(name, val1, val2):
    '''
    User can try use method with two different types, but name doing can be not defined for this types! Then raise exception.
    '''
    raise BCDR_cunit_Error(
        f'Operations "{name}" between types {type(val1)} and {type(val2)} is not defined.'
    )


def BCDR_cunit_Error_System_Exists(system):
    '''
    Return info that system does not exists.
    '''
    raise BCDR_cunit_Error(
        f'System <{system}> does not exists.\n'
        'Tip: consider to add new one system: bcdr.cunit.create_system(...)'
    )


def BCDR_cunit_Error_Units_in_System(system, units):
    '''
    Function return CunitSystemError with with info, that units does not exist in current database.
    '''
    raise BCDR_cunit_Error(
        f'Unit <{units}> does not exists in <{system}> system.\n'
        'Tip: You can add it by .add method'
    )


def BCDR_cunit_Error_Already_Exists(system, units):
    '''
    Function return CunitSystemError with with info, that units already exist in current database.
    '''
    raise BCDR_cunit_Error(
        f'Unit <{units}> does already exists in <{system}> system.\n'
        'Tip: You can overwrite it by overwrite=True argument'
    )


def BCDR_cunit_Error_Cover(val):
    '''
    '''
    raise BCDR_cunit_Error(
        f'Unit is not full covere by new one! You need multiply new unit by: {val}.\n'
        'Tip: You can perform non-full cover by fcover=False'
    )


#$ ____ warnings ___________________________________________________________ #

class BCDR_cunit_WARN(BCDR_WARN):
    pass


#$ ____ infos ______________________________________________________________ #

class BCDR_cunit_Info(BCDR_Info):
    pass
















