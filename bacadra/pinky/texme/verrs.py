'''
------------------------------------------------------------------------------
BCDR += ***** (v)arious (err)ors *****
==============================================================================

------------------------------------------------------------------------------
Copyright (C) 2018 <bacadra@gmail.com> <https://github.com/bacadra/bacadra>
Team members developing this package:
    - Sebastian Balcerowiak <asiloisad> <asiloisad.93@gmail.com>
------------------------------------------------------------------------------
'''

class BCDR_rstme_Error(Exception):
    pass

class BCDR_rstme_path_Error(Exception):
    pass

def pathError(path):
    raise BCDR_rstme_path_Error(f'Path <{path}> does not exists.')