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

from ...tools.verre  import BCDR_ERRS,BCDR_WARN,BCDR_INFO


#$ ____ errors _____________________________________________________________ #

class BCDR_pinky_rstme_ERROR(BCDR_ERRS):
    pass

def BCDR_pinky_rstme_ERROR_General(code, text):
    BCDR_pinky_rstme_ERROR(code, text)

def BCDR_pinky_rstme_ERROR_Header_Level(lvl):
    BCDR_pinky_rstme_ERROR('e0711',
        f'Typped level <{lvl}> outside domain <0,5>.'
    )

def BCDR_pinky_rstme_ERROR_Type_Check(sent, correct):
    BCDR_pinky_rstme_ERROR('e0721',
        f'The type sent <{sent}> does not match the requirements of the attribute <{correct}>.'
    )

def BCDR_pinky_rstme_ERROR_String_Selector(sent, correct):
    BCDR_pinky_rstme_ERROR('e0722',
        f'Unknown parameter <{sent}>, you can use a single or mix of available parameters <{correct}>.'
    )

#$ ____ warnings ___________________________________________________________ #

class BCDR_pinky_rstme_WARN(BCDR_WARN):
    pass

def BCDR_pinky_rstme_WARN_General(code, text):
    BCDR_pinky_rstme_WARN(code, text)

#$ ____ infos ______________________________________________________________ #

class BCDR_pinky_rstme_INFO(BCDR_INFO):
    pass

def BCDR_pinky_rstme_INFO_General(code, text):
    BCDR_pinky_rstme_INFO(code, text)


