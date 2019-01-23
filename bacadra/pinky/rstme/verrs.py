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

class rstmeError(Exception):
    pass

def lvlrstmeError(lvl):
    raise rstmeError(f'The typped level <{lvl}> outside domain. The header level be defined as integer between <0,5>')