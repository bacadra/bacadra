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

class BCDR_sofix_ERROR(BCDR_ERRS):
    pass

def BCDR_sofix_ERROR_General(code, text):
    BCDR_sofix_ERROR(code, text)

#$ ____ warnings ___________________________________________________________ #

class BCDR_sofix_WARN(BCDR_WARN):
    pass

def BCDR_sofix_WARN_General(code, text):
    BCDR_sofix_WARN(code, text)


#$ ____ infos ______________________________________________________________ #

class BCDR_sofix_INFO(BCDR_INFO):
    pass

def BCDR_sofix_INFO_General(code, text):
    BCDR_sofix_INFO(code, text)


def BCDR_sofix_INFO_Rum():
    BCDR_sofix_INFO('i0915',
        'Mass conversion started! Please be patient.\n'
        'Tip: if you call one wingraf several times then remember to close pdf windows after every one conversion... will be fixed in future\n'
    )