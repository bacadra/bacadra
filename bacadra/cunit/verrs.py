'''
------------------------------------------------------------------------------
***** (v)arious (err)or(s) *****
==============================================================================

------------------------------------------------------------------------------
Copyright (C) 2018 <bacadra@gmail.com> <https://github.com/bacadra>
Team members developing this package:
+ Sebastian Balcerowiak <asiloisad> <asiloisad.93@gmail.com>
------------------------------------------------------------------------------
'''

from ..tools.verre  import BCDR_ERRS,BCDR_WARN,BCDR_INFO


#$ ____ errors _____________________________________________________________ #

class BCDR_cunit_ERROR(BCDR_ERRS):
    pass


def BCDR_cunit_ERROR_General(code, text):
    '''
    General warning, can print any text message.
    '''
    BCDR_cunit_ERROR(code, text)


def BCDR_cunit_ERROR_Incompatible(val1, val2, name=None):
    '''
    Value sended to function should be after primary methods. In example val1="m" and val2="mm" will return ERROR!
    '''
    if val1._units != val2._units:
        BCDR_cunit_ERROR('e0511',
            f'Execution "{name}" failed: {val1._units} and {val2._units} can\'t be treat together.'
        )


def BCDR_cunit_ERROR_Undefined_Operator(name, val1, val2):
    '''
    User can try use method with two different types, but name doing can be not defined for this types! Then raise exception.
    '''
    BCDR_cunit_ERROR('e0512',
        f'Operations "{name}" between types {type(val1)} and {type(val2)} is 7not defined.'
    )


def BCDR_cunit_ERROR_System_Exists(system):
    '''
    Return info that system does not exists.
    '''
    BCDR_cunit_ERROR('e0513',
        f'System <{system}> does not exists.\n'
        'Tip: consider to add new one system: bcdr.cunit.create_system(...)'
    )


def BCDR_cunit_ERROR_Units_in_System(system, units):
    '''
    Function return CunitSystemERROR with with info, that units does not exist in current database.
    '''
    BCDR_cunit_ERROR('e0514',
        f'Unit <{units}> does not exists in <{system}> system.\n'
        'Tip: You can add it by .add method'
    )


def BCDR_cunit_ERROR_Already_Exists(system, units):
    '''
    Function return CunitSystemERROR with with info, that units already exist in current database.
    '''
    BCDR_cunit_ERROR('e0515',
        f'Unit <{units}> does already exists in <{system}> system.\n'
        'Tip: You can overwrite it by overwrite=True argument'
    )


def BCDR_cunit_ERROR_Cover(old, new, diff):
    '''
    '''
    BCDR_cunit_ERROR('e0516',
        'Unit is not full cover by new one!\n'
        f'Tip: Old unit: {old}\n'
        f'Tip: New unit: {new}\n'
        f'Tip: You need multiply new unit by: {diff}.\n'
        'Tip: You can perform non-full cover by set .d(.. fcover=False)'
    )


#$ ____ warnings ___________________________________________________________ #

class BCDR_cunit_WARN(BCDR_WARN):
    pass


#$ ____ infos ______________________________________________________________ #

class BCDR_cunit_INFO(BCDR_INFO):
    pass
















