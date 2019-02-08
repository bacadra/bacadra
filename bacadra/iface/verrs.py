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

from ..tools.verre import BCDR_ERRS,BCDR_WARN,BCDR_INFO

#$ ____ errors _____________________________________________________________ #

class BCDR_project_ERROR(BCDR_ERRS):
    pass

#$ ____ warnings ___________________________________________________________ #

class BCDR_project_WARN(BCDR_WARN):
    pass

#$ ____ infos ______________________________________________________________ #

class BCDR_project_INFO(BCDR_INFO):
    pass

def BCDR_project_INFO_Scope(id):
    BCDR_project_INFO('i0011',
        f'The scope selector change to new id <{id}>.'
    )