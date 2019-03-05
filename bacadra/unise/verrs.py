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

#$ ######################################################################### #

#$ ____ import _____________________________________________________________ #

from ..tools.erwin  import erwin

#$ ____ errors _____________________________________________________________ #

def BCDR_unise_ERROR_Units_Incompatible(s, o, name):
    if s._units != o._units:
        erwin('e0111',
            f'Operation <{name}> failed, because {s._units} and {o._units} can not be treat together.'
        )

def BCDR_unise_ERROR_Undefined_Operator(s, o, name):
    erwin('e0112',
        f'Operations <{name}> failed, because there are undefined types behaviour between self <{type(s).__name__}> and other <{type(o).__name__}>.'
    )

def BCDR_unise_ERROR_Units_in_System(system, units):
    erwin('e0114',
        f'Unit <{units}> does not exists in <{system}> system.\n'
        'Tip: You can add it by .add method'
    )

def BCDR_unise_ERROR_Already_Exists(system, units):
    erwin('e0115',
        f'Unit <{units}> does already exists in <{system}> system.\n'
        'Tip: You can overwrite it by overwrite=True argument'
    )

def BCDR_unise_ERROR_Cover(old, new, diff):
    '''
    '''
    erwin('e0116',
        'Unit is not full cover by new one!\n'
        f'Tip: Old unit: {old}\n'
        f'Tip: New unit: {new}\n'
        f'Tip: You need multiply new unit by: {diff}.\n'
        'Tip: You can perform non-full cover by set .d(.. cover=False)'
    )

def BCDR_unise_ERROR_Power2unise(o):
    erwin('e0117',
        f'Power to unise <{o._units}> is not implemented due to non consistent physics.'
    )

#$ ____ warnings ___________________________________________________________ #

#$ ____ infos ______________________________________________________________ #

#$ ######################################################################### #
