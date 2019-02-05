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

from .verre  import BCDR_ERRS,BCDR_WARN,BCDR_INFO


#$ ____ errors _____________________________________________________________ #

class BCDR_tools_ERROR(BCDR_ERRS):
    pass

def BCDR_tools_ERROR_General(code, text):
    BCDR_tools_ERROR(code, text)

#$ ____ warnings ___________________________________________________________ #

class BCDR_tools_WARN(BCDR_WARN):
    pass

def BCDR_tools_WARN_General(code, text):
    BCDR_tools_WARN(code, text)

#$ ____ infos ______________________________________________________________ #

class BCDR_tools_INFO(BCDR_INFO):
    pass

def BCDR_tools_INFO_General(code, text):
    BCDR_tools_INFO(code, text)
