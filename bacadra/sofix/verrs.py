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

class BCDRsofixError(Exception):
    pass

def envcheckBCDRsofixError(path):
    raise BCDRsofixError('enviroment does not exists! path: ' + path)

def cdbcheckBCDRsofixError(path):
    raise BCDRsofixError('.cdb does not exists! path: ' + path)

def gracheckBCDRsofixError(path):
    raise BCDRsofixError('.gra does not exists! path: ' + path)